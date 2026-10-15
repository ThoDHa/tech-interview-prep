# Exercise: Nearby Friends

Nearby friends is the moving-data exercise: high-frequency location writes, geo-sharded reads, and a privacy boundary that is a product requirement, not a compliance afterthought. It is on the list because it forces spatial indexing and freshness to be designed together, and the TTL decision is the make-or-break.

## The brief

```text
System: Nearby-friends feature for a running-tracking social app, greenfield.
In scope: Share live location with accepted friends only; discover which friends are within 1 km; background refresh on movement; per-friend visibility controls (pause, blur to neighborhood).
Out of scope: Public discovery or strangers; route history and playback; heatmap features; push notifications on proximity events.
Scale: 8M DAU, 600k concurrent runners peak; location pings every 5 s while moving (worst case 120 pings per user per run); friend graphs average 80 friends; a proximity query per ping batch, 5 queries per second per active user burst during races; friend pairs effectively colocated in the same city 95% of the time.
Non-functional requirements: Proximity results under 5 s stale; location writes durable only inside a 30-minute TTL window (history is explicitly disposable); visibility changes take effect within 30 s; no cross-city query may touch another city's shard.
Fixed givens: Geohash precision 6 (~1.2 km x 0.6 km cells) is the sanctioned starting vocabulary; the friend graph is a separate service with its own cache; runs average 45 minutes; the client knows its city.
```

Guided mode: before starting the clock, pre-read the extension checklist at the bottom of this page, then run the exact same single prompt from the [interviewer page](../mock_interview.md).

??? note "Walkthrough: what a strong answer covered (open after your session)"

- Named the write path's real shape (sustained per-user 5-second pings) and did the arithmetic for the peak race before naming stores.
- Chose the spatial index and said why geohash prefix cells answer the 1 km question without a secondary query.
- Placed the TTL at the storage layer and stated what "history is disposable" buys: memory sizing, deletion cost, and failover behavior.
- Kept the friend-graph lookup off the hot ping path with a stated cache design and an invalidation answer for visibility changes.
- Said what the privacy boundary enforces technically: neighborhood blur as a write-side transform, not a read-side filter, and why that order matters.
- Sharded by city and answered the traveling-user edge (a runner crossing a city line mid-run) without a cross-shard scatter.
- Answered the 10x probe (a city-wide race event) with fan-in arithmetic on the hottest cells and a stated degradation (coarser refresh, not errors).
- Closed with failure modes: the location store failing over warm versus cold, the friend-graph cache expiring en masse, and a client stuck in a motion-detection loop.

## Extend this scaffold

- [ ] Size the location store for the peak race arithmetic at the stated TTL and check the memory claim.
- [ ] Work out the blur transform precisely: what is stored, what a friend's query sees, and how a pause differs from a blur.
- [ ] Design the city-crossing handoff so a run never produces a cross-shard query and never goes invisible mid-handoff.
- [ ] Add a motion-detection failure on the client (continuous pings while stationary) and state the server-side defense.
