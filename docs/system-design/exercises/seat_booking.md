# Exercise: Seat Booking

Seat booking is the strong-consistency counterexample in this batch: one hot inventory row, real money, and a checkout funnel that must never oversell. It is on the list because every eventually-consistent reflex a feed system rewards is wrong here, and the exercise is saying precisely where the consistency line sits and what it costs.

## The brief

```text
System: Ticket booking for a mid-size cinema chain's app and web site, greenfield.
In scope: Seating map browse per showing; hold-and-expire seat selection; payment and confirmation; overbooking prevention across concurrent clients; basic booking history.
Out of scope: Pricing and promotions engine; refunds and exchanges; seat recommendations; loyalty integration.
Scale: 300 cinemas, 12 showings per screen per day, 200 seats average; 2M DAU browsing; a blockbuster opening sells out a 200-seat room in under 90 seconds with 20,000 concurrent viewers hammering the same showing; holds expire after 7 minutes.
Non-functional requirements: No oversell ever (hard invariant); hold placement under 300 ms p99 for the hot showing; browse availability visually fresh within 10 s; payment may take minutes; confirmation idempotent under client retry.
Fixed givens: Payment is an external provider with webhook completion; seat holds are per (showing, seat); the 90-second sellout is the acceptance test; inventory truth lives in one relational store the design may shard by showing but not by seat.
```

Guided mode: before starting the clock, pre-read the extension checklist at the bottom of this page, then run the exact same single prompt from the [interviewer page](../mock_interview.md).

??? note "Walkthrough: what a strong answer covered (open after your session)"

- Restated the invariant (no oversell, no double-hold) and named the component that enforces it, distinguishing it from everything that merely observes availability.
- Chose the concurrency mechanism for the hot row (locking, atomic conditional write, or queue) and said why the other two lose, with the p99 budget spent on that choice.
- Separated the browse path from the booking path and let browse be eventually consistent with a stated staleness bound.
- Designed hold expiry as a first-class path: what fires it, what it returns to the pool, and how a payment racing an expiry is arbitrated.
- Handled payment webhooks idempotently and answered what the user sees during each webhook-outcome branch, including the duplicate-retry case.
- Said what the 20,000-concurrent browse load does to the hot showing's data and kept it off the transactional path.
- Answered the 10x probe (a nationwide event onsale) with a queueing or virtual-room answer rather than "more database".
- Closed with failure modes: payment provider down mid-hold, expiry worker crash, and the relational store failing over.

## Extend this scaffold

- [ ] Work out the exact SQL or storage-level primitive for the atomic hold and verify it survives the 90-second sellout arithmetic.
- [ ] Design the expiry sweeper so a crashed worker cannot strand seats, including the reconciliation pass at showing start.
- [ ] Add a payment-provider outage scenario: which holds convert to what state, what the user and the cinema operator each see.
- [ ] Extend to adjacent-seat parties and state how group holds change the contention profile.
