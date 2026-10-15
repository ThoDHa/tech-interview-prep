# Exercise: Metrics Monitoring

Metrics monitoring is the write-heavy inversion: ingestion that never stops, aggregation that must happen on the way in, and reads that only ever want windows and rollups. It is on the list because downsampling is a retention-policy design disguised as a query optimization, and the cardinality bomb is the failure mode every strong answer names unprompted.

## The brief

```text
System: Metrics and monitoring platform for a mid-size infrastructure fleet, greenfield.
In scope: Time-series ingestion of gauge, counter, and timer metrics; per-host and per-service dashboards over fixed windows (1 minute, 1 hour, 1 day); alerting on threshold and rate-of-change rules; 13-month retention for downsampled series.
Out of scope: Log aggregation and tracing; ad-hoc query language; anomaly detection and ML baselining; custom dashboard sharing.
Scale: 4,000 hosts emitting 200 series each, 15-second scrape interval, so ~53k series per second and ~200k active series total with churn; series cardinality 50M named series over 13 months; dashboard queries touch 500 series over a 1-day window; alert rules evaluate every 30 seconds.
Non-functional requirements: Ingestion never drops (back-pressure all the way to the scraper, degrades nowhere else); one-minute data live for 48 hours raw then 5-minute rollups for 13 months; alert evaluation lag under 60 seconds behind ingestion; dashboard p95 under 2 seconds.
Fixed givens: Downsample operations fixed per type (count, sum, min, max, mean, p50, p99) and computed at write time, never at query time; the fleet is one region; scrapers retry with jitter and are the only drop-point allowed.
```

Guided mode: before starting the clock, pre-read the extension checklist at the bottom of this page, then run the exact same single prompt from the [interviewer page](../mock_interview.md).

??? note "Walkthrough: what a strong answer covered (open after your session)"

- Did the ingestion arithmetic first (series per second times payload) and named the write path's single-digit components before any storage choice.
- Designed in-write downsampling and stated which aggregates survive each retention tier, tying it to the 48-hour and 13-month givens.
- Named the cardinality bomb unprompted (deployment labels churning the series namespace) and gave a cap plus an explicit consequence when hit.
- Separated the alerting read path from dashboards and justified the 60-second evaluation lag with a stream-side evaluator, not a polling query fan-out.
- Sized one 1-day dashboard query (500 series times window points) and said why it meets the 2-second p95 from the rollup tiers.
- Kept the no-drop invariant honest: back-pressure to scrapers as the only degradation, with the retry-with-jitter given doing the buffering.
- Answered the 10x probe (fleet doubling plus a retry storm) with a stated shedding boundary that still never silently drops inside the pipeline.
- Closed with failure modes: the rollup job stalling (what coarsens, what alerts), a hot-partition series, and clock skew across scrapers.

## Extend this scaffold

- [ ] Work out the exact storage bytes per series per day at each tier and check the 13-month claim at 50M series.
- [ ] Design the cardinality cap's rejection behavior end to end: what the emitter sees, what the dashboard shows, what the alert does.
- [ ] Add a multi-region fleet and state which givens break first and what the redesign costs.
- [ ] Spec p99 aggregation across downsampled tiers and verify the composed estimate stays honest.
