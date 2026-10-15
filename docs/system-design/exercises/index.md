# Design Exercises

The [case studies](../case_studies/index.md) teach: they walk a classic prompt through the method with the answers one click away. This bank tests. Each exercise is a design brief and nothing else: a system, a scope, numbers, and a checklist that stays closed until you have delivered the design out loud. The bank exists to convert reading into delivery practice against the [LLM mock interviewer](../mock_interview.md).

## How to run one

1. Open a fresh chat with any capable model and paste the interviewer
   prompt from [The LLM Mock Interviewer](../mock_interview.md).
2. Pick an exercise from the table below. When the interviewer asks for
   the design brief, paste that exercise's brief block.
3. Run the honest 45 minutes: out loud, stage by stage, engaging every
   pushback instead of steering around it.
4. After the session, open the exercise's walkthrough checklist and
   compare it against the design you delivered. The gaps you find there
   are your next practice targets.

## Guided mode

If a cold run feels premature, opt into guided mode: before starting the clock, read the chosen exercise's extension checklist (the list the walkthrough deliberately leaves open). Then run the exact same single prompt. There is no second prompt variant and no coaching mid-session; the pre-read simply seeds the concerns the design should cover.

## The brief format

Every exercise instantiates the same six-field template. The fields carry fixed semantics so the interviewer's probes land the same way across the bank.

| Field | Semantics | Placeholder exemplar |
|-------|-----------|---------------------|
| System | One line naming the system and its flavor (greenfield, legacy rescue, scale-up) | `A URL shortener for a link-in-bio product, greenfield` |
| In scope | Three to four core functional features, phrased as capabilities | `Create short links; redirect; custom aliases; basic click counts` |
| Out of scope | Explicit exclusions the interviewer will honor | `Analytics dashboards; custom domains; link editing` |
| Scale | DAU, concurrency, request character, read/write shape: numbers, not adjectives | `30M DAU, 5k redirects per second peak, read-heavy 100:1, links effectively immutable` |
| Non-functional requirements | Latency targets, availability, durability, consistency expectation, hard constraints | `p99 redirect under 50 ms from cache hit; 99.9% availability; counts may lag minutes` |
| Fixed givens | Facts the interviewer confirms so the candidate need not guess: retention, ratios, assumptions | `Links retained forever; 80/20 hot-tail split; aliases are case-sensitive` |

## The exercises

Batch one, listed with the core concern each brief is built to surface. Each brief is the full exercise: the walkthrough checklist opens only after your session.

| Exercise | Central concern |
|----------|-----------------|
| [Search Typeahead](search_typeahead.md) | Read-heavy fan-out with freshness pressure and prefix-shape queries |
| [Notification System](notification_system.md) | Delivery semantics under fan-out, retry, and deduplication |
| [Seat Booking](seat_booking.md) | Contention on a hot inventory row; consistency versus availability at checkout |
| [Nearby Friends](nearby_friends.md) | High-frequency location writes and geo-sharded reads with privacy bounds |
| [Metrics Monitoring](metrics_monitoring.md) | Write-heavy time-series ingestion, downsampling, and windowed aggregation reads |

Pointers for a session: [the interviewer prompt](../mock_interview.md), [the method](../method.md) it enforces, and the [case studies](../case_studies/index.md) whose scaffolds taught the vocabulary.
