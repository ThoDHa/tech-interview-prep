# Exercise: Search Typeahead

Typeahead is the read-heavy counterpoint to every write-heavy exercise in this batch: tiny payloads, extreme query rates, and freshness pressure the moment a product team wants trending suggestions. It is on the list because prefix-shaped queries plus top-k precomputation force the cache-versus-recompute tradeoff to be stated with numbers rather than hand-waved.

## The brief

```text
System: Search typeahead for a large e-commerce site's search box, greenfield.
In scope: prefix completion over the product and query vocabulary; top-k suggestions ranked by a popularity signal; typo tolerance on the final query only; per-user recent-search bias.
Out of scope: Full search results ranking; query logs analytics product; multi-language stemming; sponsored suggestions.
Scale: 40M DAU; 2,000 typeahead requests per second peak per region, bursts to 3x during promotions; payload under 2 kB; queries bimodal: 70% head prefixes under 8 characters, long tail to 60; vocabulary 20M terms; popularity signal refreshed every 10 minutes.
Non-functional requirements: p99 suggestion latency under 60 ms end to end; 99.95% availability (degrade to empty suggestions, never errors); popularity may lag up to 30 minutes; per-user bias computed from a read-optimized profile, no online ML.
Fixed givens: Top-k is k=8 fixed; popularity signal arrives as a pre-aggregated stream (no window math in this system); regions are independent (no cross-region consistency); deletion of vocabulary terms may take up to 24 hours to disappear from suggestions.
```

Guided mode: before starting the clock, pre-read the extension checklist at the bottom of this page, then run the exact same single prompt from the [interviewer page](../mock_interview.md).

??? note "Walkthrough: what a strong answer covered (open after your session)"

- Clarified that "degrade to empty suggestions" converts an availability problem into a latency problem, and said which layer catches the fallback.
- Estimated the request rate arithmetic out loud (peak times burst multiplier) before naming components.
- Sketched the two-stage shape (cheap prefix lookup, ranked blend) and said where the p99 budget is spent in each stage.
- Named the prefix structure choice with its memory implication and did not pretend the whole vocabulary fits anywhere unsharded.
- Addressed the popularity refresh path: what a 10-minute cycle means for staleness users can observe, and how a rolling update avoids a thundering recompute.
- Placed per-user bias on the response path with a stated budget, and said what is dropped first under load (bias, then typo tolerance, then suggestions themselves).
- Answered the 10x promotion-day probe with a concrete shedding order and cache-hit arithmetic, not "we scale horizontally".
- Closed with failure modes: cache cluster loss, popularity pipeline stall, and vocabulary poisoning.

## Extend this scaffold

- [ ] Size the suggestion cache for the head prefixes and check whether it fits one node's memory at the stated request rate.
- [ ] Design the typo-tolerance path so it cannot become the p99 outlier on 60-character tail queries.
- [ ] Work out how a 24-hour deletion lag is enforced: who owns the tombstone, which layer checks it, what the user sees meanwhile.
- [ ] Add a datacenter-loss scenario and state which degradation levers fire in what order.
