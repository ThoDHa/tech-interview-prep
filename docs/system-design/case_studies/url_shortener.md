# Case Study: URL Shortener

The canonical warm-up prompt: "Design bit.ly." It looks trivial and is chosen precisely because it is not: it packs key generation, a brutal read skew, caching, and redirect semantics into a system small enough to finish in 45 minutes. This is a scaffolded workthrough of the [6-step method](../method.md): attempt each collapsed answer before opening it.

## Step 1: Requirements

The requirements you should extract in the first five minutes (in a real round you would draw these out with questions; here they are given):

**Functional:**

- Given a long URL, return a short link (e.g. `sho.rt/x7Qb2Kp`).
- Visiting the short link redirects to the original URL.
- Optional, agree on scope: custom aliases, expiration. (This scaffold
  treats both as out of scope and lists them in the extension checklist.)

**Non-functional:**

- Scale: 100 million new links per month; reads outnumber writes ~100:1.
- Redirect latency: low, ideally tens of milliseconds; this *is* the
  product.
- Availability over consistency: a duplicate short link being generated is
  survivable, a broken redirect page is the product being down.
- Links live effectively forever (assume 5 years of retention).

## Step 2: Estimation

Do each one on paper before expanding the answer.

**Prompt A: What are the write and read QPS, average and peak?**

??? note "Answer"
    Writes: 100M/month over ~2.6 × 10^6 seconds ≈ 40/s average, call it 100/s at peak.

    Reads at 100:1 ≈ 4,000/s average, ~10,000/s at peak.

    Conclusion: writes are almost nothing; the entire design is about the read path.

**Prompt B: How much storage after 5 years?**

??? note "Answer"
    Per row: short key (~7 B), long URL (~200 B average), user id, timestamps, flags: round to ~500 B with index overhead.

    100M/month × 12 × 5 = 6 billion rows. 6 × 10^9 × 500 B = 3 TB.

    Conclusion: 3 TB over five years fits on one machine. Sharding is not a storage necessity here; if you shard, it is for write isolation or availability, and you should say so rather than sharding by reflex.

**Prompt C: How long must the short key be?**

??? note "Answer"
    Base62 (a-z, A-Z, 0-9) per character. 62^6 ≈ 57 billion; 62^7 ≈ 3.5 trillion.

    6 billion links over 5 years means 6 characters is uncomfortably tight (only ~10x headroom), so use 7: 3.5 trillion keys is ~500x headroom.

    Conclusion: 7 base62 characters. Knowing 62^7 ≈ 3.5 × 10^12 cold is worth it; deriving it (62^7 ≈ 64^7 = 2^42 ≈ 4 × 10^12) is even better.

## Step 3: API and data model

```
POST /links        {long_url}         -> {short_key}
GET  /:short_key                      -> 302 redirect to long_url

Link: short_key (PK), long_url, created_at, owner_id, click_count?
```

The access pattern is a pure key-value lookup by `short_key`. No joins, no ranges, no transactions across rows. Note that out loud: it means nearly any storage engine can serve this, so the database choice will be about operational preference, not capability.

## Step 4: High-level architecture

```
              write path (100/s)
 client ──▶ ┌───────────────┐      ┌──────────────┐
            │ load balancer │────▶ │  app servers  │──▶ key gen
            └───────────────┘      └──────┬───────┘
                                          ▼
              read path (10,000/s)   ┌─────────┐  miss   ┌──────────┐
 client ──▶ GET /x7Qb2Kp ──▶ app ──▶ │  cache  │───────▶ │ database │
                                     └─────────┘         └──────────┘
                 ◀── 302 redirect ──── hit (most of the time)
```

Life of a read: request hits an app server, which checks the cache (cache-aside); on a hit it returns the redirect immediately; on a miss it reads the database, fills the cache, and redirects. Popular links are overwhelmingly skewed, so a modest cache absorbs most of the 10,000/s.

Life of a write: generate a key (deep dive 1), insert the row, return the short link. At 100/s peak this path needs no cleverness at all.

## Step 5: Deep dives

Bullet sketches, not scripts. Practice expanding each into two spoken minutes.

### 1. How do you generate the short key?

- **Hash the URL** (e.g. MD5, take the first 7 base62 chars): same URL
  dedupes to the same key for free, but truncation collides, so you must check-and-retry on collision, and two users shortening the same URL now share click analytics. Workable, slightly messy.
- **Counter + base62 encoding**: a global counter assigns each link a
  unique number, encoded in base62. No collisions ever. Two costs: the counter is a single point of contention (fix: a coordination service hands each app server a *range* of, say, 100,000 ids to burn through locally), and sequential keys are enumerable (fix: XOR/bit-mix the counter before encoding, or accept it: these are public links).
- Reasonable default: counter with pre-allocated ranges; it is the option
  with zero collision handling on the hot path.

### 2. 301 or 302 redirect?

- **301 (permanent)**: browsers cache it and skip your server on repeat
  visits. Less load for you, but you lose visibility of those clicks, and you can never change or expire the destination for that browser.
- **302/307 (temporary)**: every click hits your servers. More load
  (already cheap here), full analytics, links stay mutable and expirable.
- The tradeoff is exactly "server load vs analytics and control", and for
  a link business analytics *is* the revenue, so 302 is the defensible default. Saying that sentence is the whole point of the question.

### 3. The cache and the hot-key problem

- Cache-aside with LRU fits perfectly: reads dominate, and immutable
  values mean invalidation is nearly a non-issue (only deletes/expiry invalidate).
- Size it with the [80/20 logic](../estimation.md#example-2-cache-sizing-with-the-8020-rule):
  even caching just the day's popular links (a few GB) absorbs most reads.
- One link going viral is a *single hot key*: replicate that entry across
  cache nodes or in app-server local memory for a few seconds. Mention [thundering herd](../building_blocks.md#caching) on expiry and the coalescing fix.

### 4. Does the database ever need sharding?

- Storage said no (3 TB); write QPS said no (100/s). One primary plus
  replicas for read spillover and failover is honest and sufficient.
- If pushed ("10x everything"): shard by hash of `short_key`; the workload
  is pure point lookups, so hash sharding has no downside for queries, and consistent hashing eases growth. The key-generation scheme already guarantees global uniqueness, so shards never coordinate on writes.

## Step 6: Wrap-up

- **Bottleneck:** the cache tier and its hit rate; the database only
  matters on misses.
- **Failure mode:** cache cluster loss sends 10,000/s to a database sized
  for a fraction of that: request coalescing and replicas are the mitigation. A dead key-range allocator stops *writes* but, notably, not redirects: the product degrades gracefully.
- **Evolution:** v1 is one database and one cache; analytics, expiry, and
  multi-region are additive later.

## Extend this scaffold

Deliberately left for you. Design each with the same method:

- [ ] **Click analytics**: counting 10,000 clicks/s without writing to the
  hot path (hint: a [queue](../building_blocks.md#message-queues-and-streams) and batch aggregation).
- [ ] **Expiration and cleanup**: TTLs, lazy deletion vs a sweeper job, and
  what a 410 response should look like.
- [ ] **Custom aliases**: uniqueness now involves user choice; what
  changes in the API, storage, and abuse surface?
- [ ] **Abuse handling**: malware and phishing URLs; where does scanning
  sit, and what happens to already-shortened links that turn bad?
- [ ] **Multi-region**: redirects served from the region nearest the
  clicker; what replicates where, and how stale may a region be?
- [ ] **Rate limiting the write API**: apply the
  [rate limiter study](rate_limiter.md) to your own front door.
