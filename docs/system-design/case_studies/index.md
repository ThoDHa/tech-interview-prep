# Case Studies

These are scaffolded workthroughs, not finished essays. Each one runs the [6-step method](../method.md) on a classic interview prompt, gives you the requirements and architecture, hides the estimation answers behind collapsible blocks so you can attempt them first, sketches the deep dives in bullets rather than prose, and ends with a checklist of aspects deliberately left for you to work out. The gaps are the curriculum.

## How to use these

1. **Attempt before revealing.** Every "Answer" block is collapsed for a
   reason. Do the estimation on paper, then check. Being wrong first is the fastest way to remember.
2. **Talk, don't read.** After working through a study once, redo it out
   loud with a 45-minute timer and the page closed. The [method's time budget](../method.md#the-time-budget) is your script.
3. **Extend at least one.** Each study ends with an "extend this scaffold"
   checklist. Picking two or three items and designing them yourself, writing the tradeoffs down, is worth more than reading all five studies twice.
4. **Keep [Building Blocks](../building_blocks.md) open** the first time
   through. The studies name components without re-explaining them.

## The five studies

Ordered by difficulty; each introduces concerns the previous one did not.

| Study | Core lessons | New concerns it introduces |
|-------|-------------|----------------------------|
| [URL Shortener](url_shortener.md) | The canonical warm-up: clean scoping, key generation, a heavy read skew | Hash vs counter key generation, cache-first reads, redirect semantics |
| [Rate Limiter](rate_limiter.md) | A deep dive on one [building block](../building_blocks.md#rate-limiting) | Algorithm choice, distributed counters, failing open vs closed |
| [News Feed](news_feed.md) | The classic read-path problem | Fan-out on write vs read, the celebrity problem, feed ranking hooks |
| [Chat System](chat_system.md) | Real-time, stateful connections | WebSockets, message ordering, delivery states, online presence |
| [Web Crawler](web_crawler.md) | The canonical throughput problem: nobody waits for any single page | URL frontier and priority, Bloom-filter dedup, politeness and robots.txt, freshness scheduling |

## Roadmap: case studies not yet written

This section is a scaffold, and this list is the honest edge of it. Five of these classics now exist as exercise briefs in the [exercise bank](../exercises/index.md): those topics link straight to their briefs, and running one against the [mock interviewer](../mock_interview.md) is the strongest way to practice them. The two deferred topics stay unlinked until their briefs exist. Until a case study exists for any of them, attempting the topic yourself with the [method](../method.md) and the [building blocks](../building_blocks.md) remains exactly the right exercise.

- **[Search typeahead / autocomplete](../exercises/search_typeahead.md)**: prefix data structures
  ([tries](../../patterns/trie/intuition.md) at scale), precomputed top-k, extreme read QPS on tiny payloads.
- **[Notification system](../exercises/notification_system.md)**: multi-channel delivery (push, SMS, email),
  batching and rate limits per user, at-least-once plus idempotency in the wild.
- **[Ticketmaster / seat booking](../exercises/seat_booking.md)**: the strong-consistency counterexample to
  every feed system: contention on hot rows, holds and expiry, no overselling.
- **[Nearby friends / proximity](../exercises/nearby_friends.md)**: geospatial indexing (geohash, quadtrees),
  moving data with short TTLs, privacy boundaries.
- **Video streaming**: upload pipelines, transcoding as async work, chunked
  delivery and adaptive bitrate, CDN economics at their most extreme.
- **Distributed key-value store**: build the database instead of using one;
  consistent hashing, replication, and quorums from the inside.
- **[Metrics / monitoring system](../exercises/metrics_monitoring.md)**: time-series write floods, downsampling
  and retention, and why you never read raw points at query time.
