# Building Blocks

This is the component vocabulary of system design: what each standard piece does, what it costs, and when to reach for it. Read it once end to end, then use it as a reference during [case studies](case_studies/index.md). Every block ends with the interview question it exists to answer, because that is how the knowledge gets used: not recited, but deployed when the interviewer pushes on a box in your diagram.

A component only belongs in your design if a requirement or a number from [estimation](estimation.md) justifies it. Vocabulary is not a shopping list.

## Load balancers

A load balancer spreads incoming requests across a pool of identical servers, which is what makes "just add more servers" possible at all. It also quietly provides the first layer of fault tolerance: health checks pull dead servers out of rotation.

```
            ┌────────────┐        ┌────────┐
 clients ──▶│  load       │──────▶│ app 1  │
            │  balancer   │──────▶│ app 2  │   health checks:
            │             │───X──▶│ app 3  │◀── failed, removed
            └────────────┘        └────────┘
```

The distinction worth knowing:

| | Layer 4 (transport) | Layer 7 (application) |
|--|--------------------|------------------------|
| Sees | IPs and ports, TCP/UDP | Full HTTP: paths, headers, cookies |
| Can do | Fast, dumb spreading of connections | Route `/api/video` to the video pool, sticky sessions, TLS termination |
| Cost | Very little; millions of connections | More CPU per request, more configuration |

Common spreading policies: round robin, least connections, and hashing on a key (client IP, user id) when you need the same client to keep landing on the same server. Server-side state is what makes that stickiness necessary, which is why stateless app servers are the default advice: any server can take any request, and scaling and failure both get easy.

**The interview question this answers:** "You said add more servers. How do requests find them, and what happens when one dies?"

## Caching

A cache is fast memory in front of a slow store, and it works for the same reason [hashing](../patterns/hashing/intuition.md) works: pay memory to stop redoing lookups. At system scale the payoff is huge because real traffic is skewed: a small hot set absorbs most reads (see the [cache sizing example](estimation.md#example-2-cache-sizing-with-the-8020-rule)).

Where a cache goes matters less than how it stays correct. The three write policies:

| Policy | How it works | Tradeoff |
|--------|--------------|----------|
| Cache-aside | App reads cache; on miss, reads DB and fills cache. Writes go to DB and *invalidate* the cache entry | Default choice. Simple; first read after a write is a miss; brief staleness possible |
| Write-through | Writes go to cache, cache writes to DB synchronously | Cache never stale; every write pays double latency |
| Write-back | Writes go to cache only; flushed to DB later in batches | Fastest writes; a crashed cache node *loses data*, so only for loss-tolerant counters and the like |

Eviction: memory is finite, so something must go. **LRU** (evict the least recently used) is the standard answer and a Grind75 problem in its own right; LFU and TTL-based expiry are the common variants. TTLs also double as a staleness bound: "cached for at most 60 seconds" is a consistency statement product people can approve.

Two failure patterns to name before the interviewer does:

- **Thundering herd / cache stampede.** A hot key expires, and 10,000
  concurrent requests all miss and hit the database at once. Fixes: request coalescing (only one request refills, the rest wait), slightly randomized TTLs so keys do not expire in unison, and serving the stale value while one request refreshes it.
- **Cold cache.** A restarted cache has a 0% hit rate, and the database
  suddenly sees traffic it has not felt in months. Warm caches gradually or shed load while the hit rate recovers.

**The interview question this answers:** "Your read QPS is 100x your write QPS. What do you do, and what breaks when the cache fails?"

## Databases

### SQL vs NoSQL, framed honestly

The honest framing is not "old vs new" or "slow vs fast". It is: what does your data look like, and which guarantees are you willing to pay for?

| | Relational (Postgres, MySQL) | NoSQL (DynamoDB, Cassandra, Mongo, ...) |
|--|------------------------------|------------------------------------------|
| Data model | Tables, joins, foreign keys | Key-value, document, or wide-column; joins are your problem |
| Transactions | ACID across rows and tables | Usually limited (per-item or per-partition) |
| Query flexibility | Ad-hoc queries, aggregations | Efficient only along access paths you designed for |
| Scaling story | Excellent vertically and with read replicas; *sharding is manual and painful* | Horizontal partitioning is the native design |
| Schema | Enforced up front | Flexible, enforced by application code |

Two corrections to popular myths, worth saying in an interview:

- A single well-provisioned Postgres or MySQL instance with read replicas
  comfortably serves *most businesses that will ever exist*. Tens of thousands of QPS on one primary is normal. "We might need scale someday" does not justify giving up joins and transactions today.
- NoSQL is not schemaless in practice; the schema moves into your code, and
  the query model moves into your table design. You trade up-front rigidity for the obligation to know your access patterns in advance.

Default honestly stated: start relational; reach for NoSQL when a specific table's write volume or size exceeds a single primary and its natural partition key is obvious (events, messages, feeds).

### Replication

Replication keeps copies of the data on multiple nodes, for two distinct reasons: surviving a node's death, and serving more reads.

```
            writes                reads
              │                     │
              ▼                     ▼
         ┌─────────┐   async   ┌─────────┐
         │ primary │──────────▶│ replica │  (and more replicas)
         └─────────┘  log ship └─────────┘
```

Single-leader replication (one primary takes writes, replicas follow) is the workhorse. The two costs to know:

- **Replication lag.** With asynchronous replication a replica is slightly
  behind. A user who writes and then reads from a replica may not see their own write. Fixes: read-your-own-writes routing (send that user's reads to the primary briefly) or synchronous replication, which trades write latency for freshness.
- **Failover.** When the primary dies, a replica must be promoted, and
  deciding *which* node and *when* without splitting the brain is exactly the problem consensus solves (below).

### Sharding / partitioning

When one machine cannot hold the data or the write load, you split the data across machines by some key. Each strategy has a characteristic pain:

| Strategy | How | The pain |
|----------|-----|----------|
| Range (by key ranges, e.g. A-F, G-M) | Easy range scans | Hot ranges: new users, recent timestamps all land on one shard |
| Hash (hash(key) mod N) | Even spread | Range queries scatter to all shards; resharding moves nearly everything |
| Consistent hashing (hash ring) | Even spread *and* adding a node moves only ~1/N of keys | More machinery; still no range queries |
| Directory (lookup service maps key to shard) | Total flexibility | The directory is itself a component that can fail and must scale |

The deeper pains are strategy-independent, and naming them is senior-level signal: cross-shard queries and transactions become slow or impossible, a bad partition key creates one hot shard doing all the work (a celebrity user, a viral post), and resharding a live system is a migration project, not a config change. The partition key is the single most consequential schema decision in a sharded design: it must match the dominant access pattern ("all messages for a conversation live on one shard").

**The interview question this answers:** "This table gets 50,000 writes per second and holds 100 TB. Now what?"

#### Consistent hashing

The hash row's pain ("resharding moves nearly everything") has a standard fix, and interviewers probe for it by name. The problem with `hash(key) mod N` is the N: with ten shards, adding an eleventh remaps almost every key, so the "config change" becomes a full data migration. Consistent hashing removes N from the equation. Hash keys *and* nodes onto the same ring, and assign each key to the first node clockwise from its position. Adding a node now steals only the keys that fall between its counterclockwise neighbor and itself, carved from its clockwise neighbor's former range, about 1/N of the keyspace; removing a node hands its keys to the next one the same way. No global re-shuffle.

One position per node still leaves the ring lumpy: random placement puts some nodes in charge of oversized arcs. Real deployments give each physical node many positions around the ring, called **virtual nodes**, which averages out the lump and lets a machine with twice the capacity appear twice as often and take twice the load. This is the mechanism inside Dynamo-style stores, distributed caches, and modern load balancers, and it is what makes the table's "~1/N of keys move" claim true in practice.

**The interview question this answers:** "You said adding a shard only moves a fraction of the data. Why, and what happens without consistent hashing?"

## Message queues and streams

A queue decouples the component that produces work from the one that does it. The producer enqueues and moves on; consumers process at their own pace; the queue absorbs bursts.

```
 producers ──▶ [ ▒▒▒▒▒ queue ▒▒▒▒▒ ] ──▶ consumer pool
   (fast, spiky)     buffers            (steady, scalable)
```

What a queue buys you: burst absorption (write spikes become a longer queue instead of an outage), retries and dead-letter handling for failed work, independent scaling of producers and consumers, and fan-out of one event to many consumers. What it costs: the work is now *asynchronous*, so the caller gets "accepted" rather than "done", and you must design for the delay.

Delivery guarantees, because interviewers love this: **at-least-once** is the practical default, which means duplicates happen, which means consumers must be **idempotent** (processing the same message twice is harmless). Exactly-once end to end is not achievable in general across arbitrary systems; what frameworks sell as exactly-once is at-least-once delivery plus deduplication or transactional processing. Saying that sentence correctly is worth a lot.

Queues (RabbitMQ, SQS) delete a message once consumed. **Streams / logs** (Kafka, Kinesis) instead keep an ordered, replayable log that many consumer groups read at their own positions; ordering holds *per partition*, not globally. Reach for a stream when multiple systems need the same events, or when replay matters (rebuilding a cache, backfilling analytics).

**The interview question this answers:** "Uploads spike to 20x normal for one hour a day. Do you provision 20x the workers?"

## CDNs

A content delivery network caches content on servers physically near users. It exists because of the physics in the [latency table](estimation.md#the-latency-numbers): a user in Sydney is 200 ms round trip from a Virginia datacenter, and no amount of clever code changes the speed of light. A CDN edge node 5 ms away serves the cached copy instead, and as a bonus your origin only sees the misses.

Best for static, shared content: images, video, JS/CSS, and (increasingly) cacheable API responses. The design questions that come with it: cache invalidation (versioned URLs like `app.3f2a1.js` sidestep it entirely: new content gets a new URL), TTL choice, and what fraction of traffic the CDN absorbs (a 90%+ hit rate for media is normal, and it turns the [bandwidth math](estimation.md#bandwidth-math) from impossible to routine).

**The interview question this answers:** "Your users are global and your servers are in one region. Why is the app slow in Australia, and what do you do about it?"

## Object storage

Object storage (S3, GCS, and friends) stores immutable blobs by key, with effectively unlimited capacity, extreme durability (eleven nines is the usual claim, meaning loss is designed to be a once-in-geologic-time event), and modest latency. It is not a filesystem and not a database: no partial updates, no queries, just put/get/delete by key.

The standard pattern: **the database stores metadata and a pointer; the blob lives in object storage; the CDN serves it.** Uploads and downloads go *directly* between the client and object storage using presigned URLs, so the bytes never flow through your app servers, which would otherwise be an expensive, pointless proxy.

The [storage walkthrough](estimation.md#storage-sizing-a-walkthrough) shows why this split is forced: media is petabytes while metadata is terabytes, three orders of magnitude apart, and they have completely different access patterns.

**The interview question this answers:** "Where do the photos actually live, and does an upload really need to pass through your API servers?"

## Consistency models

Once data is replicated, "what does a read return?" becomes a real question. The two ends of the spectrum:

- **Strong consistency:** every read reflects the latest completed write,
  as if there were one copy. Costs coordination on every operation: higher latency, lower availability.
- **Eventual consistency:** replicas converge given time; a read may be
  stale for a bit. Cheap and fast, and completely fine for like counts, view counters, and feeds; unacceptable for account balances and inventory you can oversell.

Useful middle grounds exist and are worth naming: **read-your-own-writes** (a user always sees their own actions, everyone else can lag) and **monotonic reads** (a user never sees time go backwards). Most products need one of these, not full strong consistency, and knowing that is exactly the kind of tradeoff the round is probing for.

**CAP, stated correctly:** when a network partition happens in a replicated system, you must choose between consistency (refuse some requests rather than serve possibly stale data) and availability (keep answering, accepting staleness or conflicts). Partition tolerance is not an optional third feature to trade away: partitions are a fact of networks, so the *only* choice CAP gives you is C or A, *during* a partition. In normal operation the sharper tradeoff is latency vs consistency: coordinating replicas on every write costs round trips even when nothing is broken.

**The interview question this answers:** "User A posts a comment and user B does not see it for two seconds. Is that a bug? What in your design decides that?"

## Consensus, in one paragraph

Consensus protocols (Raft, Paxos) let a cluster of unreliable machines agree on one value or one ordered log despite crashes, so long as a majority of nodes are up and can talk. What that buys you in practice: safe **leader election** (exactly one primary after a failover, never two nodes both believing they are in charge), and strongly consistent metadata stores (etcd, ZooKeeper) that everything else can hang coordination on: locks, configuration, shard maps. In an interview you almost never design a consensus protocol; you *point* at one: "failover is handled by a Raft-based coordinator, so promotion is safe and split-brain is excluded." The cost is majority round trips, which is why you run consensus over small metadata, not over your data path.

**The interview question this answers:** "The primary dies. Who decides which replica takes over, and why can't two replicas both decide it's them?"

## Advanced replication and coordination

These blocks go one tier deeper than the replication basics under [Databases](#databases): what happens when there is no leader to replicate from, how to keep one logical write consistent across services, and whether to split the system into services at all. Interviewers reach for this tier at senior level, usually one block at a time.

### Quorums and leaderless replication

Single-leader replication concentrates every write through one node, which makes it a bottleneck to shard around and a node whose death pauses writes. **Leaderless** replication (Dynamo, Cassandra, Riak) drops the leader: clients write to several replicas at once, and **quorums** keep the copies coherent. With N replicas, each write must be acknowledged by W of them, and each read consults R of them. The algebra: keep W + R > N and every read overlaps at least one replica that took the write, so the freshest copy is among the answers and the reader picks it by version, with no leader and no synchronous coordination. Dynamo's classic configuration (N=3, W=2, R=2) tolerates one replica being down or slow on both the read and the write path.

The knobs are a tunable consistency dial, and narrating that tradeoff is the point: W=N makes every read fresh but writes pay the slowest replica; W=1 flips the bill onto reads, which must then consult all N. The cost leaderless operation never escapes is conflict handling: two clients can write the same key to different replicas concurrently, and overlapping quorums do not impose a total order. The system must resolve this (last-write-wins timestamps or version vectors), and lagging replicas catch up through read repair and anti-entropy background sync, which is why these stores are eventually consistent by design rather than by accident.

**The interview question this answers:** "You picked a database where any replica can accept writes. How do reads avoid stale data, and what happens when two clients write the same key at the same time?"

### Two-phase commit vs sagas

Once a logical write spans two services (an order touches orders, payments, and inventory), the question becomes how they commit together.

**Two-phase commit (2PC)** is the direct answer: a coordinator asks every participant to *prepare* (apply the change but hold the locks), and only when all agree does it send *commit*. It is atomic, and the costs are why you rarely see it between services: locks are held across the entire prepare phase, one slow participant slows the whole transaction, and a coordinator that dies mid-flight leaves participants holding locks with no way to know the outcome. In practice you meet 2PC inside a single database's internals, not across a service mesh.

**Sagas** are the practical answer between services: run each step as a local transaction, publish an event when it completes, and let the next service react. When a step fails, run **compensating transactions** for the steps already done: if payment succeeded but inventory reservation failed, refund. You give up atomicity and isolation across the whole flow and gain availability and independence, at the price of writing and testing compensation paths for every step.

The interview-ready sentence: 2PC buys atomicity at the cost of availability and latency; sagas buy availability at the cost of application-managed cleanup. Choose by asking what an intermediate state costs the business: money movement wants atomic guarantees, order flow usually tolerates a refund.

**The interview question this answers:** "Placing an order touches three services and the payment fails halfway through. What does your system do?"

### Microservices vs the monolith

This is an architecture tradeoff, and the strong answer names the forces on both sides instead of picking a fashion.

- **The monolith:** one deployable, one database, in-process calls. Every
  operation is a function call: fast, transactional, debuggable in a single stack trace, with one pipeline to operate. It hurts when many teams trip over a single deploy train, when one module's load profile forces the whole system to scale together, and when a shared schema lets every feature quietly couple to every other.
- **Microservices:** each service deploys, scales, and fails on its own,
  teams own their service end to end, and each service picks the storage that fits its access pattern. The costs are everything this page has taught you to fear: network calls where function calls used to be, distributed transactions (sagas, above), partial-failure handling on every hop, and an operational bill (service discovery, orchestration, distributed tracing) paid from day one.

The honest default for an interview sketch: a well-modularized monolith, splitting out a service only when a specific force justifies it, such as a distinct scaling profile, an independently shipping team, or a distinct availability requirement. "Six services because real systems have six services" is the boxes-without-numbers mistake wearing a different hat.

**The interview question this answers:** "Why is this four services instead of one, and what breaks between them?"

## Rate limiting

A rate limiter caps how many requests a client may make in a window, protecting the system from abuse, runaway clients, and honest overload. The two algorithms worth knowing cold:

- **Token bucket.** A bucket holds up to `B` tokens and refills at `r`
  tokens/second; each request spends one token, and an empty bucket means rejection (or queueing). Allows short bursts up to `B` while enforcing the long-run rate `r`, with O(1) state per client: a count and a timestamp. This is the industry default.
- **Sliding window.** A fixed window ("100 requests per minute, reset on
  the minute") is simple but allows 2x bursts straddling the boundary. The sliding window log keeps a timestamp per request for exactness at O(n) memory; the sliding window *counter* approximates by weighting the previous window's count by its remaining overlap, which is accurate enough and O(1).

At scale the interesting question is not the algorithm but where the counters live: per-node limits are cheap but a client can shop across nodes; a shared store (Redis) gives global limits at the cost of a network hop on every request. This tension gets a full treatment in the [rate limiter case study](case_studies/rate_limiter.md).

**The interview question this answers:** "One misbehaving client is sending 50,000 requests per second. How do you protect everyone else?"

## Observability

You cannot operate what you cannot see, and interviewers increasingly probe for this in wrap-up. The three pillars, each answering a different question:

| Pillar | Answers | Example |
|--------|---------|---------|
| Metrics | "Is the system healthy, in aggregate?" | p99 latency, error rate, queue depth, cache hit rate |
| Logs | "What exactly happened in this case?" | Structured events with request ids |
| Traces | "Where did this request's 800 ms go?" | One request's path across services, with per-hop timing |

Two habits that mark an experienced answer: quote **percentiles, not averages** (an average of 50 ms hides the p99 of 2 seconds that your heaviest users hit on every request), and alert on **symptoms users feel** (error rate, latency) rather than causes (CPU), because causes without symptoms are not incidents. Health checks and dashboards for queue depth and replication lag are how the failure modes named elsewhere on this page actually get caught.

**The interview question this answers:** "You've shipped it. How do you know it's working, and what pages you at 3 a.m.?"

## Where to go next

These blocks are the nouns; the [method](method.md) is the grammar. The [case studies](case_studies/index.md) are where you practice putting them into sentences under time pressure.
