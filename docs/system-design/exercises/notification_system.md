# Exercise: Notification System

Notification delivery is the batch's exercise in at-least-once semantics wearing a product face: multi-channel fan-out, retry storms, and deduplication boundaries, where the interesting design work is deciding exactly which component owns delivery truth. It is on the list because every "just send an email" sketch dies on the first bounced retry.

## The brief

```text
System: Notification service for a social platform (likes, comments, follows, system notices), greenfield.
In scope: Multi-channel delivery (push, email, in-app feed) with per-user channel preference and quiet hours; digest batching for email; per-user rate limits; delivery-status tracking for the sender's UI.
Out of scope: Notification content templating UX; marketing campaigns and segmentation; read receipts; user-level muting UI.
Scale: 15M DAU; 50M notification events per day peak, burst 5,000 per second during viral moments; 60% push, 25% in-app, 15% email; digest window 15 minutes; push provider SLA p95 30 s.
Non-functional requirements: At-least-once delivery with user-visible deduplication (a duplicate within 24 hours is a bug); in-app badge updates within 5 s of the event; quiet hours deferred to the next window and never dropped; sender status eventually accurate (minutes of lag acceptable).
Fixed givens: Push providers are external with hard per-app rate ceilings (name them as opaque); the event stream arrives on a durable ordered log already; per-user rate limits are fixed policy (10 pushes per hour); device tokens rotate and the registry is a separate service.
```

Guided mode: before starting the clock, pre-read the extension checklist at the bottom of this page, then run the exact same single prompt from the [interviewer page](../mock_interview.md).

??? note "Walkthrough: what a strong answer covered (open after your session)"

- Stated the delivery-semantics position explicitly: which component is allowed to claim "delivered", and why everything upstream is at-least-once.
- Fanned out channels after a single deduplication decision, and said where the idempotency key lives (event id, not channel attempt).
- Addressed the retry-vs-storm tradeoff with backoff and a poison-queue answer for permanently failing endpoints.
- Sized the digest buffer and quiet-hours deferral store, and said what happens on restart mid-window.
- Named the rate-limit enforcement point and reconciled "10 pushes per hour" with a 5,000-events-per-second viral burst for one user.
- Traced the status pipeline: which transitions exist, which are observable by the sender, and why terminal failure is a state, not an absence.
- Answered the 10x probe with a concrete backlog policy: what lags first, what sheds, what never drops.
- Closed with failure modes: the log replaying a day of events, a push provider hard-down, and the token registry serving stale tokens.

## Extend this scaffold

- [ ] Design the deduplication store for a 24-hour window and check its memory at the stated event rate.
- [ ] Work out the exact ordering guarantees a single user observes across channels when one event fans out three ways.
- [ ] Add a dedup-store outage scenario: what duplicates leak, how the UI masks them, how the store repopulates.
- [ ] Spec the interaction between quiet hours and digest so a viral evening does not empty the morning digest.
