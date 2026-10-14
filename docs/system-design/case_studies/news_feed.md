# Case Study: News Feed

"Design the Twitter/Instagram feed" is the classic read-path problem: a write happens once, and then millions of reads want it, personalized, in milliseconds. The entire study orbits one decision (do the work at write time or at read time?), which makes it the best rehearsal there is for tradeoff-first answers. A scaffolded workthrough of the [6-step method](../method.md); attempt each collapsed answer first.

## Step 1: Requirements

**Functional:**

- Users publish posts (text, media pointer).
- Users follow other users.
- A user's feed shows recent posts from everyone they follow, newest
  first. (Ranked feeds: out of scope, but leave a hook; see the extension checklist.)
- Feeds paginate (infinite scroll).

**Non-functional:**

- Scale: 100 million DAU. Average user follows 200 accounts; a small
  number of accounts have tens of millions of followers.
- Feed load latency: under ~200 ms feels instant-ish; this is the app's
  home screen.
- Eventual consistency is fine: a post appearing in followers' feeds a few
  seconds after publishing is normal and expected. Say this explicitly; it buys you enormous design freedom.
- Read-heavy by construction (quantified next).

## Step 2: Estimation

**Prompt A: Read and write QPS. Assume each DAU loads their feed 10 times a day, and 10% of DAU publish one post a day.**

??? note "Answer"
    Feed reads: 10^8 × 10 = 10^9/day ≈ 12,000/s average, ~30,000/s peak.

    Posts: 10^7/day ≈ 120/s average, ~300/s peak.

    Ratio: reads outnumber post-writes by ~100:1. Conclusion: it is worth doing significant extra work *per write* to make *reads* cheap. That one sentence is the justification for everything in step 4.

**Prompt B: If every post is pushed into each follower's precomputed feed (fan-out on write), how many feed insertions per second is that?**

??? note "Answer"
    10M posts/day × 200 followers average = 2 × 10^9 insertions/day ≈ 24,000/s average, ~60,000/s at peak.

    Conclusion: fan-out multiplies write volume by the average follower count: 300/s of posts becomes tens of thousands of cache inserts per second. Absorb it asynchronously (queue + workers), and notice the multiplier is *unbounded* for celebrity accounts: one post by a 30M-follower account is 30 million insertions. That single observation forces the hybrid design in deep dive 1.

**Prompt C: Memory to keep every active user's precomputed feed in cache: 300 entries per user, post ids only.**

??? note "Answer"
    An entry is a post id plus a timestamp/score: ~16 to 30 B; call it 30 B with structure overhead.

    10^8 users × 300 × 30 B ≈ 900 GB, call it ~1 TB.

    Conclusion: too big for one node, trivial for a sharded cache cluster (e.g. 20 nodes × 64 GB). Storing *ids only* is what makes this feasible: full rendered posts at ~1 KB would be ~30 TB. Precompute the skeleton, hydrate the flesh on read.

## Step 3: API and data model

```
POST /posts                {text, media_key}      -> {post_id}
GET  /feed?cursor=...      -> [post views], next_cursor
POST /follows              {followee_id}

Post:    id, author_id, text, media_key, created_at
Follow:  follower_id, followee_id     (indexed both directions)
Feed:    user_id -> [post_id, ...]    (precomputed, cache-resident)
```

The two directions of the follow table matter: "whom do I follow" builds feeds on read; "who follows me" drives fan-out on write. Feeds paginate by cursor (a timestamp/id watermark), never by page number: new posts arriving between requests shift offsets, and cursors are immune.

## Step 4: High-level architecture

```
 write path:
 author ──▶ post service ──▶ post DB (sharded by author)
                 │
                 └──▶ queue ──▶ fan-out workers ──▶ feed cache
                                (look up followers,    user 1: [ids...]
                                 insert post id into   user 2: [ids...]
                                 each follower's list)

 read path:
 reader ──▶ feed service ──▶ feed cache (get id list)
                 │
                 └──▶ post/user storage + cache (hydrate ids
                      into content, authors, counts) ──▶ response
```

Life of a post: store it (durable, source of truth), enqueue a fan-out job, return success immediately. Workers read the follower list and push the post id onto each follower's cached feed. Seconds of lag here is invisible, which is why the eventual-consistency agreement in step 1 mattered.

Life of a feed load: fetch the id list from the feed cache (one shard lookup), hydrate ~20 posts' content from the post cache/DB in *parallel*, assemble, return. Two cache round trips ≈ a few ms: the 200 ms budget is spent on network to the phone, not on your backend.

## Step 5: Deep dives

### 1. Fan-out on write vs fan-out on read

- **On write (push)**: precompute every follower's feed as posts arrive.
  Reads are O(1) list fetches: perfect for the 100:1 read skew. Costs: the write amplification from Prompt B, wasted work for dormant users, and celebrity posts create insertion storms.
- **On read (pull)**: store nothing precomputed; on feed load, fetch
  recent posts from all ~200 followees and merge (a [k-way merge](../../patterns/k_way_merge/intuition.md) at scale). Writes are trivial; every read costs 200 scatter-gather lookups: too slow for the home screen at this read volume.
- **The hybrid, which is the real answer**: push for normal accounts;
  for accounts above a follower threshold (say 1M), do not fan out: readers *pull* celebrity posts at read time and merge them into their cached feed. Also skip pushing to users inactive for 30+ days and rebuild their feed lazily on return. State the rule, the threshold, and *why* each side gets its treatment: that is the whole interview.

### 2. What is the feed cache, concretely?

- Per-user bounded list (e.g. Redis list/sorted set keyed by user id,
  capped at ~300 ids, sharded by user id so a feed read is one shard hit).
- Ids only; hydration is a separate, heavily cached concern (hot posts
  and hot authors are cached once globally, not per feed).
- Eviction: dormant users' lists expire via TTL; the rebuild path (pull
  + merge) doubles as both cold-start and cache-recovery logic, so
  losing a feed cache node degrades latency, not correctness.

### 3. The celebrity problem, beyond the hybrid rule

- Insertion storm was solved by pull, but *read* hot spots remain: 30M
  people hydrating the same new post id hits the same post shard. Fix: the global hot-post cache in front of post storage, replicated across cache nodes precisely because single-key traffic can exceed one node's capacity.
- Follower-list reads for fan-out are also skewed (200 on average, 30M
  in the tail): fan-out workers should stream the follower list in batches, not load it in one query.
- The general lesson to say out loud: sharding handles *volume*, but
  never *skew*; skew is handled by replication of the hot item.

### 4. Deletes, edits, and the lies your cache tells

- A deleted post's id is already in millions of cached feeds. Chasing
  every copy is absurd: instead, filter at hydration time (the id resolves to nothing / a tombstone, so it silently drops from the response). Feed lists self-clean as they age out.
- Edits are easy by contrast: feeds store ids, hydration fetches current
  content, so edits are visible immediately everywhere. This asymmetry (deletes need tombstones, edits are free) falls directly out of the ids-only decision in Prompt C, and noticing that connection is strong signal.
- Out-of-order arrival (fan-out worker retries, queue redelivery):
  sorted-set feeds keyed by post timestamp make insertion idempotent and order-independent: at-least-once delivery plus an idempotent consumer, exactly as the [queues block](../building_blocks.md#message-queues-and-streams) prescribes.

## Step 6: Wrap-up

- **Bottleneck:** fan-out worker throughput at peak; the queue absorbs
  bursts, and lag is measured in seconds of feed staleness, which is the metric to watch.
- **Failure modes:** feed cache node loss (rebuild via pull path, slow
  but correct), queue backlog (feeds go stale, product still works), post DB shard loss (posts unavailable at hydration: feeds render with gaps rather than failing).
- **Evolution:** v1 for a small product is pure pull with no feed cache
  at all, and it is *correct*, just slow at scale; push, then the hybrid, are optimizations you add when the read numbers demand them.

## Extend this scaffold

- [ ] **Ranked feeds**: replace "newest first" with a scoring function;
  where does scoring run (write time? read time? both?), and what does that do to the fan-out decision?
- [ ] **Likes and counters**: 1B+ like events/day on hot posts without
  serializing on one row (sharded counters, approximate counts).
- [ ] **Media**: wire in
  [object storage + CDN](../building_blocks.md#object-storage) for images and video; what changes in the post write path?
- [ ] **Follow/unfollow dynamics**: an unfollow should stop showing that
  author; when and where does the cached feed get corrected?
- [ ] **A "new posts" indicator**: how do you know the feed has fresh
  content without loading it (and without polling storms)?
- [ ] **Ads or injected content**: slots resolved at hydration time; what
  does that do to pagination cursors?
