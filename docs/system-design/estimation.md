# Back-of-Envelope Estimation

Estimation is the step that turns "design Twitter" from art into engineering. The goal is never precision: it is getting the *order of magnitude* right, fast, out loud, so the numbers can drive design decisions. If your estimate says 5,000 requests per second and reality is 8,000, your design does not change. If you are off by 100x, it does.

Two habits make this easy: round everything to the nearest power of ten, and finish every calculation with a conclusion ("so a single database handles this" or "so we need a CDN").

## The latency numbers

You need a feel for how long things take, because latency budgets decide what a request is allowed to touch. These are honest 2020s magnitudes; individual systems vary, but the *ratios* between rows are what matter.

| Operation | Typical time | Handy comparison |
|-----------|-------------:|------------------|
| L1 cache reference | ~1 ns | The baseline |
| L2 cache reference | ~4 ns | |
| Mutex lock/unlock | ~20 ns | |
| Main memory (RAM) reference | ~100 ns | 100x slower than L1 |
| Read 1 MB sequentially from RAM | ~20 to 50 µs | |
| NVMe SSD random read (4 KB) | ~20 to 100 µs | ~1,000x slower than a RAM reference |
| Read 1 MB sequentially from NVMe SSD | ~200 µs to 1 ms | |
| Network round trip, same datacenter | ~0.5 ms | The unit of distributed work |
| HDD seek | ~5 to 10 ms | Why spinning disks lost the random-read war |
| Read 1 MB sequentially from HDD | ~5 to 10 ms | |
| Round trip, same continent (SF to NYC) | ~60 to 70 ms | |
| Round trip, transatlantic (NYC to London) | ~70 to 90 ms | |
| Round trip, halfway around the world | ~150 to 250 ms | |

The conclusions worth memorizing, because they *are* design decisions:

- **RAM is roughly 1,000x faster than SSD, which is roughly 100x faster
  than a cross-country round trip.** Cache in memory, store on SSD, and never make a user's click wait on more sequential cross-region hops than you must.
- **A same-datacenter round trip (~0.5 ms) is cheap but not free.** A
  request that fans out to 5 internal services sequentially has spent 2.5 ms before doing any work. Fan out in parallel.
- **Geography is physics.** Light in fiber travels about 200,000 km/s, and
  routes are not straight lines, so a 150 ms round trip to another continent cannot be optimized away by better code. That single fact is the entire justification for CDNs and multi-region deployments.
- **A human notices ~100 ms.** A latency budget of 200 ms for a page leaves
  room for one ocean crossing, or a handful of datacenter hops plus real work, but not both.

## Powers of two and unit shortcuts

Storage math runs on powers of two; do the conversions once and reuse them.

| Power | Exact | Approximation | Name |
|-------|-------|---------------|------|
| 2^10 | 1,024 | ~10^3 (thousand) | KB |
| 2^20 | ~1.05 million | ~10^6 (million) | MB |
| 2^30 | ~1.07 billion | ~10^9 (billion) | GB |
| 2^40 | ~1.1 trillion | ~10^12 (trillion) | TB |
| 2^50 | | ~10^15 | PB |

The working rule: **treat 2^10 as 10^3 and never look back.** The error is under 3% per step, far below the noise in your other assumptions. Also worth knowing: 2^32 is about 4.3 billion, which is why 32-bit counters overflow and why IPv4 ran out; and a 64-bit number or pointer is 8 bytes, which is where most of your "per-row metadata" bytes go.

## QPS arithmetic

Requests per second is the number that sizes almost everything. Three conversions cover it:

| Fact | Rounded form | Use |
|------|--------------|-----|
| 1 day = 86,400 s | ~10^5 s | Daily volume to per-second rate |
| 1 month | ~2.6 × 10^6 s | Monthly volume, retention windows |
| 1 year | ~3 × 10^7 s | Storage growth |

Which gives the single most-used shortcut in the room:

```
1 million per day  ≈ 12 per second
1 billion per day  ≈ 12,000 per second
```

(10^6 / 86,400 ≈ 11.6; round to 12, or to 10 if you are rounding the other inputs down anyway.)

Two adjustments turn an average into a real capacity number:

- **Peak factor.** Traffic is not uniform. Peak-hour load is typically 2x
  to 5x the daily average; state your factor ("I'll assume peak is 3x average") rather than silently using the mean.
- **Read/write split.** Always compute reads and writes separately. A
  100:1 read-to-write ratio and a 1:1 ratio are different systems.

## Storage sizing: a walkthrough

The pattern: items per day, times size per item, times retention, times replication. Worked for a Twitter-like service:

```
┌────────────────────────────────────────────────────────────────┐
│  Assumptions (state them out loud):                            │
│    500 million tweets/day                                      │
│    text + metadata per tweet ≈ 0.5 KB                          │
│      (280 chars ≈ 280 B, plus ids, timestamps, counters)       │
│    10% of tweets carry media, ~500 KB average                  │
│                                                                │
│  Text:   500M × 0.5 KB = 250 GB/day                            │
│          × 365          ≈ 90 TB/year                           │
│                                                                │
│  Media:  50M × 0.5 MB  = 25 TB/day                             │
│          × 365          ≈ 9 PB/year                            │
│                                                                │
│  × 3 replication        ≈ 27 PB/year raw for media             │
└────────────────────────────────────────────────────────────────┘

Conclusion: text is a rounding error next to media. The database
stores text and pointers; the media itself belongs in object
storage behind a CDN. The estimate just made an architecture
decision for you.
```

That last line is the point of the exercise. If an estimate does not end in a sentence starting with "so" or "therefore", it was arithmetic for its own sake.

## Bandwidth math

Bandwidth is storage math with a clock attached: bytes per day divided by ~10^5 seconds. One conversion trap to avoid out loud: storage is quoted in bytes, network links in *bits*. Multiply by 8.

```
Media ingest from the walkthrough above:
  25 TB/day ÷ 86,400 s ≈ 290 MB/s ≈ 2.3 Gbps average ingest
  × 3 peak factor       ≈ 7 Gbps at peak
```

Egress is usually the bigger number (every upload is viewed many times) and is the CDN's job; see the first worked example below.

## Worked estimation examples

Do these yourself on paper before reading the traces. The style matches the worked traces in the pattern guides: every line is a step you could say out loud.

### Example 1: Photo-sharing app, full pass (QPS, storage, bandwidth)

**Prompt**: 50 million DAU. Average user views 20 photos/day; 1 in 5 users uploads one photo a day. Size the system.

```
┌────────────────────────────────────────────────────────────────┐
│  Reads:                                                        │
│    50M users × 20 views = 1B views/day                         │
│    1B/day ≈ 12,000/s average                                   │
│    × 2.5 peak           ≈ 30,000/s peak read QPS               │
│                                                                │
│  Writes:                                                       │
│    50M × 0.2 uploads = 10M uploads/day ≈ 120/s, ~300/s peak    │
│    read:write ratio  ≈ 100:1  → read-dominated, cache-heavy    │
│                                                                │
│  Storage:                                                      │
│    photo ≈ 2 MB original + 0.5 MB of thumbnails ≈ 2.5 MB       │
│    10M/day × 2.5 MB = 25 TB/day ≈ 9 PB/year before replication │
│                                                                │
│  Egress bandwidth:                                             │
│    most views hit thumbnails ≈ 100 KB                          │
│    12,000/s × 100 KB = 1.2 GB/s ≈ 10 Gbps average              │
│    → far too much to serve from app servers; CDN required,     │
│      and at a 90% CDN hit rate origin serves ~1 Gbps           │
└────────────────────────────────────────────────────────────────┘

Conclusions: metadata DB sees modest QPS (tens of thousands),
photos live in object storage, a CDN is not optional, and the
upload path can be 100x less provisioned than the read path.
```

### Example 2: Cache sizing with the 80/20 rule

**Prompt**: A news site has 10 million articles, ~50 KB each rendered, and serves 100 million article reads/day. How much cache memory buys a high hit rate?

```
┌────────────────────────────────────────────────────────────────┐
│  Total corpus: 10M × 50 KB = 500 GB   (too big to cache fully  │
│  in one node, and unnecessary)                                 │
│                                                                │
│  80/20 assumption: 20% of articles get ~80% of reads.          │
│  Hot set: 2M × 50 KB = 100 GB → fits in a small cache          │
│  cluster (e.g. a few 32 to 64 GB nodes), for ~80% hit rate.    │
│                                                                │
│  Recency is even more skewed for news: today's articles        │
│  dominate. 1 day of articles (say 10K × 50 KB = 500 MB)        │
│  might alone cover half the traffic.                           │
│                                                                │
│  Load check: 100M reads/day ≈ 1,200/s average, ~4,000/s peak.  │
│  At 80% hit rate the database sees ~800/s at peak: one         │
│  well-indexed primary with a replica handles that.             │
└────────────────────────────────────────────────────────────────┘

Conclusion: ~100 GB of cache turns a scary-sounding 100M-read
day into a database load a single replica pair can carry.
```

### Example 3: How many app servers?

**Prompt**: Peak load is 30,000 QPS of lightweight, IO-bound API requests (~50 ms each, mostly waiting on cache and DB). How many servers?

```
┌────────────────────────────────────────────────────────────────┐
│  Per-server throughput: IO-bound services on modern hardware   │
│  commonly sustain ~500 to a few thousand QPS per node          │
│  (concurrency hides the 50 ms waits; CPU is the real limit).   │
│  Assume 1,000 QPS/server to keep the math honest.              │
│                                                                │
│  Bare minimum: 30,000 / 1,000 = 30 servers                     │
│                                                                │
│  Real provisioning:                                            │
│    × 2 headroom (target ~50% utilization at peak, so a         │
│      traffic spike or a deploy doesn't tip you over)           │
│    + tolerate losing a zone: spread over 3 zones so any        │
│      2 can carry the load                                      │
│  → ~60 servers across 3 availability zones                     │
└────────────────────────────────────────────────────────────────┘

Conclusion: the answer the interviewer wants is not "30". It is
"30 to satisfy the math, ~60 to survive a bad day", because the
gap between those two numbers is where reliability lives.
```

## Sanity-checking your own numbers

Before moving on from any estimate, spend ten seconds cross-checking:

- **Compare to something real.** "9 PB/year" should trigger a gut check:
  large photo services do store exabytes over their lifetime, so the magnitude is plausible. "9 PB/day of tweets" should trigger alarm.
- **Check the ratio, not just the value.** Reads should exceed writes for a
  feed; ingest should be far below egress for anything media-heavy. If a ratio comes out inverted, a step is wrong.
- **Redo one step in the other direction.** 12,000/s × 10^5 s should land
  back near 1B/day. Round-tripping catches dropped zeros, which are the only estimation errors that actually matter.
