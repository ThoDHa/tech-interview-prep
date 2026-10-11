# [Select K Paired Indices for Maximum Score](https://www.fastprep.io/problems/amazon-select-k-paired-array-score)

**Medium** | **NN minutes** | **Array, Sorting, Heap, Greedy**

Select exactly k shared indices from two equal-length arrays. The score is the sum of selected values from first multiplied by the minimum selected value from second.

Return the maximum score.

## Examples

### Example 1

**Input:** `first = [1,3,3,2]`, `second = [2,1,3,4]`, `k = 3`

**Output:** `12`

**Explanation:** Case 1 exercises the documented deterministic contract.

### Example 2

**Input:** `first = [4,2,3,1,1]`, `second = [7,5,10,9,6]`, `k = 1`

**Output:** `30`

**Explanation:** Case 2 exercises the documented deterministic contract.

### Example 3

**Input:** `first = [2,1,14,12]`, `second = [11,7,13,6]`, `k = 3`

**Output:** `168`

**Explanation:** Case 3 exercises the documented deterministic contract.

## Constraints

- `1 <= k <= first.length == second.length <= 100000.`
- `All values are positive integers.`
- `The answer fits a signed 32-bit integer.`

## Solutions

### Brute Force over Index Combinations

#### Derivation

The literal reading of the problem asks one question: of all the ways to pick exactly `k` shared indices, which selection scores highest? The statement rules out nothing, so the honest first answer tries them all. Python's `itertools.combinations` produces every `k`-index selection of the `n` positions, and scoring one selection is two aggregations over its `k` indices followed by one product:

1. Iterate `indices` over `combinations(range(len(first)), k)`.
2. For each selection compute `paired_sum`, the sum of the chosen `first` values,
   and `minimum_second`, the smallest chosen `second` value.
3. Keep the largest `paired_sum * minimum_second` in `best_score` and return it.

#### Walkthrough

Example 1 has `n = 4` and `k = 3`, so `combinations` yields `C(4, 3) = 4` selections:

| `indices` | `first` values | `paired_sum` | `second` values | `minimum_second` | score |
| --- | --- | --- | --- | --- | --- |
| `(0, 1, 2)` | `1, 3, 3` | `7` | `2, 1, 3` | `1` | `7` |
| `(0, 1, 3)` | `1, 3, 2` | `6` | `2, 1, 4` | `1` | `6` |
| `(0, 2, 3)` | `1, 3, 2` | `6` | `2, 3, 4` | `2` | `12` |
| `(1, 2, 3)` | `3, 3, 2` | `8` | `1, 3, 4` | `1` | `8` |

The winning selection drops index `1`: its `first` value `3` is attractive, but its `second` value `1` would drag the minimum down. `best_score` ends at `12`, the expected Output.

#### Solution

```python
from itertools import combinations
from typing import List


class Solution:
    def maximumPairedScore(self, first: List[int], second: List[int], k: int) -> int:
        best_score = 0
        for indices in combinations(range(len(first)), k):
            paired_sum = sum(first[index] for index in indices)
            minimum_second = min(second[index] for index in indices)
            best_score = max(best_score, paired_sum * minimum_second)
        return best_score
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(n, k) × k)`

There are `C(n, k)` selections and each is scored with two passes over its `k` indices.

##### Space Complexity: `O(k)`

One selection tuple at a time; the score itself is two running aggregates.

#### Key Insights

- The minimum `second` value is what punishes a selection, so attractive `first` values mislead on their own: index `1` holds a joint-largest `first` value yet poisons the product.
- Correct but explosive: `C(n, k)` grows past toy sizes immediately, which motivates the structured sweep below.
- Scoring is order-free: only the multiset of chosen indices matters, so combinations (not permutations) suffice.

### Sort by Second with Min-Heap

#### Derivation

The brute force re-decides the whole selection for every candidate, yet the score's structure splits the decision in two. Whichever index supplies the minimum `second` value, the remaining `k - 1` slots should simply hold the largest available `first` values: for a fixed minimum, the product is maximized by maximizing the sum, and the only eligible partners are indices with `second >= value_second`.

Sorting the pairs by `second` descending turns that eligibility rule into "among the pairs already processed": when the sweep reaches a pair, every pair with a greater `second` has been seen. A min-heap of capacity `k - 1` holds the largest `first` values among those processed pairs, and a running `window_sum` tracks their total, so evaluating one pair is constant time and maintaining the top set is `O(log k)`:

1. Pair the arrays and sort the pairs by `second` descending.
2. Sweep the sorted pairs, keeping `largest_values` (the min-heap of at most `k - 1`
   largest `first` values among processed pairs) and `window_sum` (their sum).
3. At each pair, when `k - 1` earlier pairs exist (`len(largest_values) == k - 1`),
   evaluate the candidate `(window_sum + value_first) * value_second` and keep the best.
4. Push `value_first` onto the heap and add it to `window_sum`; whenever the heap
   exceeds `k - 1` entries, pop the smallest and subtract it from `window_sum`.

#### Walkthrough

Example 3 (`first = [2, 1, 14, 12]`, `second = [11, 7, 13, 6]`, `k = 3`) exercises both the waiting phase and the scoring phase. Sorted by `second` descending, the pairs are `(2, 11)`, `(14, 13)`, `(1, 7)`, `(12, 6)`. A candidate needs `k - 1 = 2` earlier partners, so the first two pairs only feed the heap:

```text
pair (2, 11)   heap size 0 < 2: no candidate
               push 2    largest_values = [2]      window_sum = 2
pair (14, 13)  heap size 1 < 2: no candidate
               push 14   largest_values = [2, 14]  window_sum = 16
pair (1, 7)    candidate (16 + 1) x 7  = 119   best_score = 119
               push 1 -> window_sum = 17, size 3 > 2: pop 1 -> window_sum = 16
pair (12, 6)   candidate (16 + 12) x 6 = 168   best_score = 168
               push 12 -> window_sum = 28, size 3 > 2: pop 2 -> window_sum = 26
```

The two early skips lose nothing: a selection whose minimum `second` is `13` would need two partners with `second >= 13`, and only one such pair exists. The sweep ends with `best_score = 168`, the expected Output.

#### Solution

The code is the sweep from the walkthrough: the heap-size guard gates the candidate, then the push-and-trim keeps exactly `k - 1` values.

```python
import heapq
from typing import List


class Solution:
    def maximumPairedScore(self, first: List[int], second: List[int], k: int) -> int:
        pairs = sorted(zip(first, second), key=lambda pair: pair[1], reverse=True)
        largest_values: List[int] = []
        window_sum = 0
        best_score = 0
        for value_first, value_second in pairs:
            if len(largest_values) == k - 1:
                candidate_score = (window_sum + value_first) * value_second
                best_score = max(best_score, candidate_score)
            heapq.heappush(largest_values, value_first)
            window_sum += value_first
            if len(largest_values) > k - 1:
                window_sum -= heapq.heappop(largest_values)
        return best_score
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the `n` pairs dominates; the sweep pushes and pops each value at most once, at `O(log k)` per heap operation.

##### Space Complexity: `O(n)`

The sorted pair list; the heap itself never holds more than `k - 1` values.

#### Key Insights

- The only structural choice is which index supplies the minimum `second`; given that choice, the rest of the selection is greedy on `first`.
- The current pair always belongs to the selection and supplies the minimum; the heap holds only candidates for the other `k - 1` slots.
- Ties in `second` need no special casing: when two selected pairs share the minimum, the pair sorted later evaluates the same selection, because the earlier tie already sits in the heap.
- Before the heap fills, no valid selection has that minimum, so skipping those pairs is correctness, not an optimization.

## Comparison of Solutions

### Time Complexity

- **Brute Force over Index Combinations**: `O(C(n, k) × k)` - every selection enumerated and scored.
- **Sort by Second with Min-Heap**: `O(n log n)` - one sort plus a linear sweep with bounded heap work.

### Space Complexity

- **Brute Force over Index Combinations**: `O(k)` - one selection tuple at a time.
- **Sort by Second with Min-Heap**: `O(n)` - the sorted pair list dominates the `O(k)` heap.

### Trade-offs

- **Brute Force over Index Combinations**: nearly impossible to get wrong and a ready-made correctness oracle, but `C(n, k)` selections rule out anything past toy sizes.
- **Sort by Second with Min-Heap**: a single pass after one sort, but it leans on the min-supplier decomposition argument and on the `k - 1` capacity bookkeeping being exactly right.

### When to Use Each

- **Brute Force over Index Combinations**: validating the fast solution against small random inputs, or an interview where `n` is tiny and the clock is short.
- **Sort by Second with Min-Heap (Recommended)**: the real OA constraints (`n` up to `100000`): the only rung of the ladder that scales.

### Optimization Notes

- Sorting by `second` only (the `key=lambda pair: pair[1]`) keeps equal-`second` pairs in input order, which the tie argument needs nothing more of.
- The guard `len(largest_values) == k - 1` also handles `k = 1`: the heap stays empty and every pair is scored alone, which is exactly the maximum single product.
- `window_sum` avoids re-summing the heap for every candidate: each `first` value is added once on push and subtracted once on eviction.
