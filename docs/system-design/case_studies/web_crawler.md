# Case Study: Web Crawler

"Design a web crawler" is the purest batch system in the interview repertoire: nobody waits on a single page, so latency leaves the requirements and throughput, cost, and fairness take over, and politeness shapes the design more than any scaling number. A scaffolded workthrough of the [6-step method](../method.md); attempt each collapsed answer first.

## Step 1: Requirements

**Functional:**

- Start from a seed set (and sitemaps); fetch pages, extract outlinks,
  and keep going. Agree on the shape of time: a one-shot crawl of a fixed corpus, or a continuous service. (This scaffold: the continuous one.)
- Store page content for the index pipeline to consume.
- Obey robots.txt and per-host rate limits: functional, not optional. A
  crawler that ignores them gets blocked, and the crawl is dead.
- Freshness: re-fetch pages when they change, more often when they change often.

**Non-functional:**

- Scale: refresh ~5 billion pages per month across tens of millions of
  hosts.
- No latency SLO to humans; the SLOs are throughput, freshness (how stale
  a served copy may be), and politeness (per-host caps, absolute).
- Availability over consistency, trivially: a lost or duplicated URL
  record costs one delayed or wasted fetch. The friendliest CAP question in the section; say so.
- Fault tolerance: any component can die and the crawl resumes; that
  works only because the schedule of remaining work is durable state.

## Step 2: Estimation

Do each one on paper before expanding the answer.

**Prompt A: What fetch rate does a monthly refresh need?**

??? note "Answer"
    5 × 10^9 / 2.6 × 10^6 s ≈ 2,000 fetches/s average, call it 5,000/s at peak.

    The aggregate is a red herring: the binding constraint is the per-host politeness cap (~1 request every few seconds, or whatever robots.txt dictates), which horizontal scaling cannot relax.

    Conclusion: aggregate QPS is trivial, and the fleet will be latency-bound (mostly waiting on origins), not CPU-bound. The design problem is scheduling under a per-host cap: the frontier (deep dive 1).

**Prompt B: What does a month of crawling cost?**

??? note "Answer"
    Average page ≈ 200 KB of HTML: the write stream is 2,000/s × 200 KB ≈ 400 MB/s ≈ 3.2 Gbps sustained, ~8 Gbps at peak (the [bandwidth math](../estimation.md#bandwidth-math)).

    5 × 10^9 × 2 × 10^5 B = 10^15 B = 1 PB of raw HTML per month; extracted text is ~10% of that: ~100 TB.

    Conclusion: petabyte-scale, append-only, rarely read back: textbook [object storage](../building_blocks.md#object-storage) with the metadata-pointer pattern; the extracted text is what the index searches.

## Step 3: API and data model

No human calls the crawler; its customer is the index pipeline:

```
PUT /pages  {url_hash, text, blob_ref, fetched_at, outlinks[]}
            -> consumed by the index pipeline

Url:    url_hash (PK), canonical_url, host, status (new|due|fetched|error),
        priority, last_crawled_at, next_crawl_at, change_rate, error_count
Page:   url_hash, blob_ref, content_hash, fetched_at
Robots: host -> {rules, crawl_delay, fetched_at}      (TTL, re-fetched)
```

The access patterns decide everything: point lookups by `url_hash` (dedup and scheduling), grouping by `host` (politeness and robots live at host granularity), and a steady scan of due URLs. The lifecycle in `status` is the point: a URL is a recurring appointment, and `next_crawl_at` and `change_rate` are the columns the freshness story hangs on (deep dive 4).

## Step 4: High-level architecture

```
             seed URLs, sitemaps
                      │
                      ▼
  ┌─────────────────────────────┐        ┌──────────────────────┐
  │ URL frontier                │ seen?  │ dedup store          │
  │ priority + per-host queues  │◀──────▶│ Bloom filter         │
  │ (sharded by host)           │        │ + URL database       │
  └──────────────┬──────────────┘        └──────────▲───────────┘
                 │ due URL, host within its budget  │ new URLs
                 ▼                                  │
  ┌─────────────────────────────┐                   │
  │ fetcher workers: politeness │  robots.txt:      │
  │ caps, DNS, size/time limits │◀─per-host cache   │
  └──────────────┬──────────────┘                   │
                 │ raw HTML                         │
                 ▼                                  │
  ┌─────────────────────────────┐                   │
  │ parser / extractor          │                   │
  │ text, outlinks, hash        │ ── blob ──▶ content store
  └───┬─────────────────────────┘            (object storage)
      │ extracted text
      ▼
  index pipeline
```

Life of a URL: the frontier picks the highest-priority due URL whose host has budget left; the fetcher checks robots, resolves DNS, fetches under size and time caps; the parser extracts text, outlinks, and a content hash. Blobs go to object storage, text to the index pipeline, each outlink runs past the dedup store, and unseen ones enter the frontier with a priority and a `next_crawl_at`. This is the [queue pattern](../building_blocks.md#message-queues-and-streams) end to end, and the queue is not an optimization; it is the schedule.

## Step 5: Deep dives

Bullet sketches, not scripts. Practice expanding each into two spoken minutes.

### 1. The frontier: BFS versus priority

- A single FIFO (BFS from the seeds) fails on both axes: politeness (a
  hot domain's URLs enter the queue together, so popularity gets hammered) and quality (BFS orders by discovery, not importance).
- Two orthogonal fixes: a **priority score** decides *which* URL matters
  next (inlink counts, staleness: age × change rate), and **per-host queues** enforce politeness.
- Shard the frontier by host
  ([consistent hashing](../building_blocks.md#consistent-hashing)): one shard owns a host's queue, budget, and in-flight count, so politeness needs no cross-node coordination. The [sharding](../building_blocks.md#sharding-partitioning) lesson with a twist: the natural key is the *host*, not the URL.
- The frontier is not a buffer; it is the schedule: lose it and you
  re-crawl blind. It is durable, replicated state.

### 2. Dedup at scale: the set versus the Bloom filter

- "Have I seen this URL before?" is asked for every outlink of every
  page: order 10^5 times per second, over a hundred billion URLs. It is the [hashing](../../patterns/hashing/intuition.md) tradeoff of memory for lookups at its limit.
- The naive set: even 16-byte truncated hashes cost 1.6 TB before
  pointer and load-factor overhead: no fit in RAM, and a disk lookup per outlink is death by latency.
- The Bloom filter: ~10 bits per URL is 125 GB for 100 billion URLs at
  ~1% false positives. The error asymmetry makes it safe: a false positive *skips* a URL (slightly incomplete crawl), never a duplicate fetch; false negatives are impossible.
- The hybrid: Bloom "maybe seen" → check the authoritative URL database.
  Many crawlers eat the 1%: bits only flip 0 to 1, so a false positive is permanent until the filter is rebuilt from the URL database. Quote the memory arithmetic cold; it is the entire argument.

### 3. Politeness and robots.txt

- robots.txt is fetched once per host, cached for hours to days, and its
  Disallow rules and Crawl-delay are obeyed. The RFC 9309 failure cases differ: 404/410 means unrestricted crawling is allowed, while a 5xx is treated as disallow-all, the conservative default.
- The per-host cap is the [rate limiter](rate_limiter.md) pattern per
  host, with one difference worth saying aloud: a service may choose to fail open or closed, but an over-crawling crawler gets its IP range banned. The failure mode is not an outage; it is exile.
- Adaptive backoff: a wave of 429/503 responses halves that host's budget
  and retries with exponential spacing. The budget lives on the shard that owns the host's queue (deep dive 1): politeness is enforced at dequeue time by not popping from a host whose next-allowed time is in the future. Per-host queues and politeness are the same mechanism.
- Identity: an honest User-Agent string with a contact URL, so a site
  administrator can ask you to slow down before they block you.

### 4. Fault tolerance and re-crawl scheduling

- Fetcher death mid-fetch: claim URLs under a time-boxed lease; a dead
  worker's leases expire and its URLs return to due. At-least-once, harmlessly: the lease claim is idempotent on `url_hash`, and a re-fetch overwrites the old row (latest-wins on content hash), never duplicating.
- Poison URLs: 404s, timeouts, decompression bombs. Cap bytes and
  seconds per fetch, count errors per URL, retire a URL after N failures into a low-priority retry lane. Without this, 0.1% bad URLs become 100% of a retry storm.
- The URL store's consistency requirements are the loosest here: a lost
  record delays a re-crawl by a cycle, a duplicate wastes one fetch. That arithmetic justifies a cheap, eventually consistent store ([leaderless, W=1](../building_blocks.md#quorums-and-leaderless-replication)) over paying coordination for unneeded correctness.
- Re-crawl scheduling is a freshness-versus-effort market: `next_crawl_at`
  follows each URL's observed change rate. Uniform re-crawling spends 10x the fetches for a fraction of the freshness: a small share of pages (news, prices, feeds) carries most of the value, and the long tail is stable for months: spend the crawl budget where the changes are.

## Step 6: Wrap-up

- **Bottleneck:** the frontier and dedup store: six-figure random
  operations per second on URL keys. The fetch fleet is latency-bound by politeness: thousands of open connections, each waiting on an origin.
- **Failure modes:** fetcher fleet loss (leases expire, the crawl
  resumes, nothing corrupts); frontier or URL store degradation (degrade to a *slower* crawl, never an impolite one); robots source outage (serve conservative cached defaults, keep crawling politely).
- **Evolution:** v1 is one polite BFS over a seed list with a robots
  dictionary, and it works for a real corpus. v2 adds the sharded frontier, the Bloom filter, and object storage. v3 is where the value concentrates: freshness scheduling, near-duplicate detection, and a rendering tier for JS-heavy pages.

## Extend this scaffold

Deliberately left for you. Design each with the same method:

- [ ] **URL canonicalization**: `http`/`https`, `www`, tracking params:
  two "different" URLs, one page. Where does it run, and at what cost?
- [ ] **Near-duplicate pages**: mirrors and boilerplate; shingling or
  simhash over a petabyte a month. Cluster first, index one representative.
- [ ] **Rendering JavaScript**: client-rendered pages cost ~10x per
  fetch; who gets the headless-browser tier, and when?
- [ ] **Crawl traps**: infinite calendars and faceted navigation that
  generate unbounded URLs; cap per-host expansion before one site eats the frontier.
- [ ] **Focused crawling**: how does topic relevance enter the priority
  score, and what happens when importance and politeness disagree?
- [ ] **Multi-region crawling**: one host, two continents: coordinate
  politeness budgets globally, or partition hosts by region?
