# [Frequently Bought Together](https://www.fastprep.io/problems/amazon-frequently-bought-together)

**Medium** | **NN minutes** | **Array, String, Hash Table, Sorting**

Amazon's Retail Analytics team wants to discover which pairs of items are most often bought together so they can create Frequently Bought Together bundles.

During a short observation window, each customer order is recorded as a space-separated list of SKU strings, for example "B07 B08 B09". Within a single order, the same SKU may repeat, but repeats count only once toward a bundle.

Your task is to find the pair of distinct SKUs that appears in the highest number of orders. If several pairs tie for first place, return the lexicographically smallest pair, comparing the first SKU and then the second SKU.

## Examples

### Example 1

**Input:** `orders = ["B07 B08 B09", "B07 B08", "B08 B09"]`

**Output:** `["B07", "B08"]`

**Explanation:** Order-level pairs:

{B07, B08}, {B07, B09}, {B08, B09}{B07, B08}{B08, B09}The global counts are {B07, B08} -> 2, {B07, B09} -> 1, and {B08, B09} -> 2. The highest count is tied between {B07, B08} and {B08, B09}, so the lexicographic tie-break gives {B07, B08}.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-frequently-bought-together; fill them in. -->

## Solutions

### Brute Force Candidate Enumeration

#### Derivation

The most literal reading of the problem gives a two-phase plan: a qualifying pair must share at least one order, so first collect every pair of distinct SKUs that co-occurs somewhere, then measure each candidate by asking, for every order, whether both members appear in it. The "repeats count only once" rule is a deduplication duty inside each order, and a set of SKUs per order discharges it before any pair is formed:

1. Split every order into `order_skus`, a list of sets of SKU strings, so repeated
   SKUs within one order collapse to a single entry.
2. Enumerate each order's pairs over its `sorted(skus)` tokens, storing every pair
   as `(first_sku, second_sku)` with `first_sku < second_sku`; a `seen_pairs` set
   keeps each candidate exactly once in `candidate_pairs`.
3. For each candidate pair, rescan every set in `order_skus` and count the orders
   holding both members as `pair_count`.
4. Track `best_pair` and `best_count`, replacing on a higher count, or on an equal
   count with a lexicographically smaller pair; return `best_pair` as a list.

#### Walkthrough

Example 1 is small enough to trace end to end. The three orders deduplicate into these sets, and the candidate list gathers each co-occurring pair once:

```text
orders[0]  "B07 B08 B09" -> skus {B07, B08, B09}
orders[1]  "B07 B08"     -> skus {B07, B08}
orders[2]  "B08 B09"     -> skus {B08, B09}

candidate_pairs (in first-seen order, tokens sorted):
  (B07, B08), (B07, B09), (B08, B09)
```

Each candidate then rescans all three orders, with two constant-time set lookups per order:

```text
count (B07, B08):  order 0 yes, order 1 yes, order 2 no   -> 2
count (B07, B09):  order 0 yes, order 1 no,  order 2 no   -> 1
count (B08, B09):  order 0 yes, order 1 no,  order 2 yes  -> 2
```

The scan for the best pair sets `best_pair = (B07, B08)` with `best_count = 2`, then reaches `(B08, B09)` with the same count of 2. The tie-break compares the tuples: `("B07", "B08") < ("B08", "B09")`, so `best_pair` stays unchanged and the function returns `["B07", "B08"]`, matching the expected Output.

#### Solution

The code is the two phases of the walkthrough: one pass to collect `candidate_pairs`, one pass per candidate to count and select.

```python
from typing import List, Set, Tuple


class Solution:
    def findFrequentBundlePair(self, orders: List[str]) -> List[str]:
        order_skus = [set(order.split()) for order in orders]

        candidate_pairs: List[Tuple[str, str]] = []
        seen_pairs: Set[Tuple[str, str]] = set()
        for skus in order_skus:
            ordered_skus = sorted(skus)
            for first_pos in range(len(ordered_skus)):
                for second_pos in range(first_pos + 1, len(ordered_skus)):
                    pair = (ordered_skus[first_pos], ordered_skus[second_pos])
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        candidate_pairs.append(pair)

        best_pair: Tuple[str, str] = ("", "")
        best_count = 0
        for pair in candidate_pairs:
            pair_count = sum(
                1 for skus in order_skus
                if pair[0] in skus and pair[1] in skus
            )
            if pair_count > best_count or (
                pair_count == best_count and pair < best_pair
            ):
                best_count = pair_count
                best_pair = pair

        return list(best_pair)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C × n)`

Where `C` is the number of distinct co-occurring pairs (`C ≤ n × k × (k − 1) / 2` for `n` orders of at most `k` SKUs each): building the per-order sets is one pass over the input, and each of the `C` candidates rescans all `n` orders with constant-time set lookups.

##### Space Complexity: `O(n × k + C)`

The per-order SKU sets hold every token once, and the candidate list plus `seen_pairs` hold up to `C` pairs.

#### Key Insights

- Storing each pair as `(first_sku, second_sku)` with `first_sku < second_sku` canonicalizes the unordered pair, so tuple comparison in Python implements the "first SKU, then second SKU" tie-break directly.
- Deduplicating SKUs per order before pairing enforces the "repeats count only once" rule without any special-case logic.
- Every candidate co-occurs in at least one order by construction, so the first count always beats the initial `best_count` of 0 and the selection loop needs no empty-check on non-empty input.
- The approach is correct but re-reads every order once per candidate pair, which is the waste the next approach removes.

### Hash Map Pair Counting

#### Derivation

The brute force rescans all orders once per candidate pair, yet a single pass over the orders can tally every pair at once. A [hash map](https://en.wikipedia.org/wiki/Hash_table) keyed by the canonically ordered pair accumulates, in one sweep, exactly the counts the brute force recomputes; one final scan over the map's entries then applies the max-count-then-lexicographic selection:

1. For each order, split it and deduplicate into `distinct_skus`, sorted so the
   double loop emits pairs already in `(first_sku, second_sku)` order.
2. Increment `pair_counts[(first_sku, second_sku)]` for every pair the double
   loop produces, so each order contributes at most once per pair.
3. Scan `pair_counts`: replace `best_pair` when a count is higher, or when a
   count ties and the pair compares smaller.
4. Return `best_pair` as a list.

#### Walkthrough

The same three orders stream through the map one at a time. Each line shows the pairs an order emits and the map state after they land:

```text
order 0  distinct B07, B08, B09 -> emit (B07,B08), (B07,B09), (B08,B09)
         pair_counts = {(B07,B08): 1, (B07,B09): 1, (B08,B09): 1}
order 1  distinct B07, B08      -> emit (B07,B08)
         pair_counts = {(B07,B08): 2, (B07,B09): 1, (B08,B09): 1}
order 2  distinct B08, B09      -> emit (B08,B09)
         pair_counts = {(B07,B08): 2, (B07,B09): 1, (B08,B09): 2}
```

The final scan visits `(B07,B08)` first and sets `best_pair` with count 2; `(B07,B09)` loses on count; `(B08,B09)` ties at 2 but `("B07", "B08") < ("B08", "B09")`, so `best_pair` holds. The function returns `["B07", "B08"]`, matching the expected Output.

#### Solution

The code is the streaming tally from the walkthrough, followed by the selection scan.

```python
from typing import Dict, List, Tuple


class Solution:
    def findFrequentBundlePair(self, orders: List[str]) -> List[str]:
        pair_counts: Dict[Tuple[str, str], int] = {}
        for order in orders:
            distinct_skus = sorted(set(order.split()))
            for first_pos in range(len(distinct_skus)):
                for second_pos in range(first_pos + 1, len(distinct_skus)):
                    pair = (distinct_skus[first_pos], distinct_skus[second_pos])
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1

        best_pair: Tuple[str, str] = ("", "")
        best_count = 0
        for pair, pair_count in pair_counts.items():
            if pair_count > best_count or (
                pair_count == best_count and pair < best_pair
            ):
                best_count = pair_count
                best_pair = pair

        return list(best_pair)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × k²)`

Each order of at most `k` distinct SKUs contributes at most `k × (k − 1) / 2` pair increments, and the final selection scan visits each distinct pair once.

##### Space Complexity: `O(P)`

Where `P` is the number of distinct pairs across all orders: the map holds one counter per pair, plus at most `k` scratch tokens per order.

#### Key Insights

- Counting pairs once per order in a hash map replaces the brute force's per-candidate rescans with a single pass over the input.
- Sorting each order's distinct SKUs before pairing means every map key is already in lexicographic order, which makes the final tie-break a plain tuple comparison.
- The selection scan keeps only `best_pair` and `best_count`, so the map is the only structure that grows with input size.
- Orders with fewer than two distinct SKUs emit no pairs and drop out of the tally naturally.

## Comparison of Solutions

### Time Complexity

- **Brute Force Candidate Enumeration**: `O(C × n)` - each of up to `C` candidate pairs rescans every order with constant-time set lookups.
- **Hash Map Pair Counting**: `O(n × k²)` - one pass emitting at most `k × (k − 1) / 2` pairs per order, then one scan of the distinct pairs.

### Space Complexity

- **Brute Force Candidate Enumeration**: `O(n × k + C)` - per-order SKU sets plus the candidate list and `seen_pairs` set.
- **Hash Map Pair Counting**: `O(P)` - one counter per distinct pair, with per-order scratch released each iteration.

### Trade-offs

- **Brute Force Candidate Enumeration**: the most direct transcription of the problem statement and easy to reason about, but its per-candidate rescans make it quadratic in the order count for pair-heavy inputs.
- **Hash Map Pair Counting**: does the same bookkeeping in one pass and keeps only the map, at the cost of trusting the dict's per-key costs instead of an explicit membership check.

### When to Use Each

- **Brute Force Candidate Enumeration**: for tiny inputs or as a reference implementation to validate the faster version against.
- **Hash Map Pair Counting (Recommended)**: for any realistic order volume: it is the natural interview answer and scales with the number of distinct pairs rather than with pairs times orders.

### Optimization Notes

- Sorting tokens inside each order (rather than sorting candidate pairs at the end) is what lets tuple comparison decide the tie-break; sorting the final pairs instead would also work but adds an `O(P log P)` step.
- The selection scan runs in one pass because only the best entry survives; a `heapq` of the top pairs would generalize the task to "top k bundles" without changing the tally.
- Repeated SKUs inside one order must be collapsed before pairing, or an order like `"B07 B07 B08"` would inflate `(B07, B08)`; the `set` conversion is the guard.
