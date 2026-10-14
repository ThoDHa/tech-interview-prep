# Case Study: Rate Limiter

"Design an API rate limiter" is the deep-dive prompt in miniature: one [building block](../building_blocks.md#rate-limiting), fully unpacked. It is popular with interviewers because the algorithms are simple enough to discuss precisely, while the distributed version has real teeth. A scaffolded workthrough of the [6-step method](../method.md); attempt each collapsed answer first.

## Step 1: Requirements

**Functional:**

- Limit requests per client (API key or user id) against configured rules,
  e.g. "100 requests per minute per user".
- Over-limit requests are rejected with HTTP 429 and enough information to
  behave well (when to retry, what the limit is).
- Rules vary by endpoint and customer tier, and can change without a
  deploy.

**Non-functional:**

- Sits on the hot path of *every* request: the check must add well under
  ~2 ms.
- Scale: protect a service handling 100,000 requests/second at peak, from
  ~10 million active clients.
- Accuracy is negotiable, availability is not: briefly letting a client
  send 105 requests instead of 100 is fine; the limiter taking down the API is the one unforgivable failure.

That last line is the thesis of the whole design. Say it in step 1 and the rest of the interview arranges itself around it.

## Step 2: Estimation

**Prompt A: How much memory does per-client token bucket state need for 10 million active clients?**

??? note "Answer"
    Token bucket state per client: a token count and a last-refill timestamp, ~16 B, plus the key (~40 B with overhead): round to ~60 B.

    10^7 clients × 60 B ≈ 600 MB.

    Conclusion: the *entire* limiter state fits comfortably in one Redis node's memory. Memory is not the hard problem here; throughput and latency are.

**Prompt B: What load does the counter store see, and what does that imply?**

??? note "Answer"
    Every API request performs one check-and-update: 100,000/s at peak, each a small read-modify-write.

    A single Redis node sustains on the order of 100,000 ops/s, so one node is *exactly* at the edge: no headroom. Conclusion: shard the counter store by client id (each client's state lives wholly on one shard, so no cross-shard coordination), or cut the load with local batching (deep dive 2).

    Latency check: one same-datacenter round trip ≈ 0.5 ms, inside the 2 ms budget, but only if the limiter never queues behind slow commands.

**Prompt C: A fixed window allows how much burst? "100/minute", windows reset on the minute, client sends as fast as possible.**

??? note "Answer"
    100 requests at 11:59:59 (end of one window) and 100 more at 12:00:00 (start of the next): 200 requests in ~2 seconds, all accepted.

    Conclusion: a fixed window enforces at most 2x the intended rate across a boundary. That factor-of-two is the entire motivation for sliding windows and token buckets, and being able to produce this example on demand is what "knows the algorithms" sounds like.

## Step 3: API and data model

The limiter's "API" is mostly a contract with the services it protects and with well-behaved clients:

```
check(client_id, rule) -> allow | deny(retry_after)

Response headers on every request:
  X-RateLimit-Limit: 100          the rule
  X-RateLimit-Remaining: 37       budget left
  Retry-After: 12                 on 429 only, seconds

Rule:    {scope: user|ip|global, endpoint, limit, window, tier}
Counter: {client_id+rule -> tokens, last_refill}   (the hot state)
```

Rules are tiny, rarely change, and are read constantly: perfect for caching in each limiter node's memory with a short TTL or a pub/sub refresh. Counters are the opposite: tiny, hot, and mutated on every request. Separating those two lifecycles *is* the data model.

## Step 4: High-level architecture

```
 clients ──▶ ┌───────────────┐     allow      ┌───────────────┐
             │  API gateway  │───────────────▶│  app servers  │
             │  + limiter    │                └───────────────┘
             │  middleware   │──▶ 429 + Retry-After (deny)
             └──────┬────────┘
                    │ check-and-update (one round trip)
                    ▼
          ┌───────────────────┐      ┌──────────────┐
          │ counter store     │      │ rules config │──▶ cached in
          │ (Redis, sharded   │      │ (DB / config │    each gateway
          │  by client id)    │      │  service)    │    node
          └───────────────────┘      └──────────────┘
```

The limiter lives in the gateway/middleware layer, in front of the app servers, so rejected traffic never consumes application capacity: that placement is the point of having a limiter at all.

## Step 5: Deep dives

### 1. Which algorithm, and why?

- **Token bucket** (rate `r`, burst `B`): O(1) memory per client, allows
  controlled bursts, refill is computed lazily from the timestamp on each check, so there is no background work. The industry default; pick it and defend it.
- **Fixed window counter**: simplest possible, but the 2x boundary burst
  from Prompt C. Acceptable for coarse abuse limits, not for billing-grade quotas.
- **Sliding window log** (timestamp per request): exact, but O(requests)
  memory per client: at 100/min per client and 10M clients that is gigabytes churning constantly, for accuracy nobody asked for.
- **Sliding window counter** (weighted blend of this and the previous
  window): O(1) memory, smooths the boundary problem, slightly approximate. The strongest alternative to token bucket; choosing between them is taste, and saying *that* is also a fine answer.

### 2. Where do the counters live?

- **Local to each gateway node**: zero added latency, but a client
  spraying requests across N nodes gets N times the limit, and limits wobble as nodes scale up and down. Fine as a coarse first line only.
- **Centralized (sharded Redis)**: one source of truth, global accuracy,
  costs a ~0.5 ms round trip per request and makes Redis critical infrastructure. The check must be atomic: read-then-write from two gateways interleaves and over-admits, so use an atomic Lua script (or INCR-style operations) so check-and-decrement is one operation.
- **Hybrid, the production answer**: each node keeps a local bucket and
  syncs deltas to the shared store every ~100 ms, trading a small, *bounded* over-admission during the sync gap for removing the round trip from the hot path. Name the bound out loud: at most (nodes × batch window × rate) extra requests.

### 3. The counter store just died. Fail open or fail closed?

- **Fail closed** (deny everything): the limiter, whose job is protecting
  availability, has now taken the whole API down. Almost always wrong.
- **Fail open** (allow everything): honest default, consistent with the
  step 1 thesis: the limiter is protection, not a correctness feature. Pair it with a fallback to node-local limits so you are not *entirely* naked, plus loud alerting.
- The senior-level nuance: the answer flips when the limiter enforces a
  *paid quota* or protects a fragile downstream that will melt without it. "Fail open for abuse limits, degrade to conservative local limits for capacity protection" shows you see both.

### 4. What should rejection actually look like?

- Return 429 early and cheaply, with `Retry-After` and the rate headers:
  well-behaved SDKs back off, and the ill-behaved ones get dropped at your cheapest layer. Rejecting at the gateway is itself load shedding.
- Throttling alternatives worth mentioning: queueing the request briefly
  (good for spiky-but-honest clients, dangerous under sustained overload), and shadow/soft limits (log would-be rejections before enforcing a new rule: how limits get rolled out safely in practice).
- Separate scopes compose: per-user, per-IP (for unauthenticated
  traffic), and a global emergency brake. Check cheapest and coarsest first.

## Step 6: Wrap-up

- **Bottleneck:** the counter store's ops/s; the hybrid design exists to
  keep it off the hot path.
- **Failure modes:** counter store loss (fail open with local fallback),
  and clock skew between nodes gently distorting refill math (bounded, tolerable, worth naming).
- **Evolution:** v1 is a fixed-window counter in one Redis behind the
  gateway, shipped in a week; token buckets, hybrid sync, and a rules UI are all additive.

## Extend this scaffold

- [ ] **Rules engine**: tiers, per-endpoint overrides, and how a rule
  change propagates in seconds without redeploying gateways.
- [ ] **Multi-region limits**: a global "1,000/min" quota with gateways
  on three continents; what does the [latency table](../estimation.md#the-latency-numbers) forbid, and what approximation do you sell instead?
- [ ] **Client SDK behavior**: design the backoff (jittered exponential)
  and explain why `Retry-After` without jitter re-synchronizes the herd.
- [ ] **Observability**: which metrics prove the limiter is working
  (rejection rate by rule, p99 added latency, sync lag), and which alert means it is hurting users?
- [ ] **Exactness on demand**: a billing-grade quota for one premium
  endpoint; what changes when over-admission stops being acceptable?
