# [Maximum Rating Threshold Count](https://www.fastprep.io/problems/amazon-maximum-rating-threshold-count)

**Medium** | **NN minutes** | **Array, Sorting**

Given a nonempty integer array ratings, return the largest integer k such that at least k entries in ratings are greater than or equal to k.

## Examples

### Example 1

**Input:** `ratings = [3,0,6,1,5]`

**Output:** `3`

**Explanation:** Three ratings are at least 3: 3, 5, and 6. Four ratings are not at least 4, so the maximum threshold count is 3.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-maximum-rating-threshold-count; fill them in. -->

## Solutions

### Descending Threshold Scan

#### Derivation

The most literal reading asks the question threshold by threshold. The answer `threshold` must satisfy two conditions at once: at least `threshold` ratings are >= `threshold`, and no larger value manages that. Testing candidates from the largest possible value downward makes the first success the answer, and the scan needs no bookkeeping beyond a running count:

1. Let `total` be the number of entries; the answer can never exceed `total`.
2. For each `threshold` from `total` down to `1`, count `qualifying`, the
   entries >= `threshold`.
3. Return the first `threshold` where `qualifying >= threshold`.
4. If no positive threshold qualifies, return `0`.

#### Walkthrough

Let us run the descending scan by hand on Example 1: `ratings = [3,0,6,1,5]`, so `total = 5` and the candidates run from `5` down:

```text
threshold = 5   qualifying = 2   (6 and 5)    2 >= 5? no
threshold = 4   qualifying = 2   (6 and 5)    2 >= 4? no
threshold = 3   qualifying = 3   (3, 6, 5)    3 >= 3? yes -> return 3
```

The scan stops at the first success: three ratings clear the bar of 3, and no higher threshold clears its own bar, so the function returns 3, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's loop: one full count per candidate threshold, stopping at the first that qualifies.

```python
from typing import List


class Solution:
    def solve(self, ratings: List[int]) -> int:
        total = len(ratings)
        for threshold in range(total, 0, -1):
            qualifying = 0
            for rating in ratings:
                if rating >= threshold:
                    qualifying += 1
            if qualifying >= threshold:
                return threshold
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each of up to `n` candidate thresholds triggers a fresh count over all `n` entries.

##### Space Complexity: `O(1)`

Only the `threshold` and `qualifying` counters are kept.

#### Key Insights

- Testing candidates from `total` down to `1` means the first success is the largest qualifying threshold, so no maximum tracking is needed.
- The fallback return `0` covers inputs such as `[0]` where even a threshold of 1 fails.
- The approach never reorders or copies the input, which keeps it simple at the price of repeated scanning.

### Sort Descending and Scan

#### Derivation

The descending scan pays because every restart recounts all entries from scratch. Sorting removes the recounting: in descending order, the entries that are >= `threshold` are, whenever at least `threshold` of them exist, exactly the first `threshold` entries of `ordered`. The condition "at least k entries are >= k" therefore collapses into the single indexed comparison `ordered[threshold - 1] >= threshold`. Because the k-th largest value falls as k grows while the bar `k` rises, once the comparison fails it keeps failing, so the qualifying thresholds form a prefix and one early-out sweep finds its end:

1. Sort `ratings` into `ordered`, highest first.
2. Sweep the boundary `threshold` upward from `0`.
3. Advance while `threshold < total` and `ordered[threshold] >= threshold + 1`
   (the entry just past the current prefix must clear the bar of a prefix one longer).
4. Return the `threshold` reached; it is the largest k with at least k entries >= k.

#### Walkthrough

Let us sort Example 1 by hand: `ordered = [6,5,3,1,0]`, and sweep the boundary upward:

```text
threshold = 0   ordered[0] = 6 >= 1? yes -> threshold = 1
threshold = 1   ordered[1] = 5 >= 2? yes -> threshold = 2
threshold = 2   ordered[2] = 3 >= 3? yes -> threshold = 3
threshold = 3   ordered[3] = 1 >= 4? no  -> stop
```

The sweep stops at `threshold = 3`: the top three entries (6, 5, 3) all clear the bar of 3, but the fourth largest entry (1) fails the bar of 4. The function returns 3, matching the expected Output for Example 1.

#### Solution

The code is the boundary sweep from the walkthrough: the qualifying count is read off the sorted order instead of being recomputed.

```python
from typing import List


class Solution:
    def solve(self, ratings: List[int]) -> int:
        ordered = sorted(ratings, reverse=True)
        threshold = 0
        while threshold < len(ordered) and ordered[threshold] >= threshold + 1:
            threshold += 1
        return threshold
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the boundary sweep that follows touches each entry at most once.

##### Space Complexity: `O(n)`

`sorted` builds a new list of `n` entries, leaving the caller's input untouched.

#### Key Insights

- Sorting converts "count how many entries are >= k" into a direct prefix lookup, eliminating the brute force's repeated counting.
- The monotonicity (the k-th largest value falls while the bar k rises) guarantees the qualifying thresholds form a prefix, so a single early-out sweep suffices.
- This computation is exactly the H-Index on the ratings, which is why the sorted scan reads like that classic problem.

### Bucket Count Sweep

#### Derivation

The sort spends `O(n log n)` ordering entries whose exact values above `total` cannot matter: a rating larger than the entry count qualifies for every threshold up to `total` exactly as a rating of exactly `total` does. Clamping every rating to at most `total` shrinks the value domain to `total + 1` possible values, so a bucket array can hold their counts, and a high-to-low sweep accumulates the same "how many entries are >= threshold" totals the sorted scan read off one index at a time, in linear time:

1. Allocate `buckets` of size `total + 1` and place each rating in
   `buckets[min(rating, total)]`.
2. Sweep `threshold` from `total` down to `1`, adding `buckets[threshold]` into
   `qualifying`, the running count of entries >= `threshold`.
3. Return the first `threshold` where `qualifying >= threshold`.
4. Return `0` when the sweep finishes without a success.

#### Walkthrough

Let us bucket Example 1: `ratings = [3,0,6,1,5]` with `total = 5`. The clamped ratings are `[3,0,5,1,5]` (the 6 clamps to 5), so `buckets = [1,1,0,1,0,2]`, where the index holds the clamped value and the entry holds its count. The sweep accumulates from the top:

```text
threshold = 5   qualifying += buckets[5] = 2   2 >= 5? no
threshold = 4   qualifying += buckets[4] = 0   2 >= 4? no
threshold = 3   qualifying += buckets[3] = 1   3 >= 3? yes -> return 3
```

The accumulated `qualifying` of 3 counts exactly the entries >= 3 (3, 5, and the clamped 6), so the function returns 3, matching the expected Output for Example 1.

#### Solution

The code is the bucket fill and the accumulating sweep from the walkthrough.

```python
from typing import List


class Solution:
    def solve(self, ratings: List[int]) -> int:
        total = len(ratings)
        buckets = [0] * (total + 1)
        for rating in ratings:
            buckets[min(rating, total)] += 1

        qualifying = 0
        for threshold in range(total, 0, -1):
            qualifying += buckets[threshold]
            if qualifying >= threshold:
                return threshold
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass fills the buckets and one pass sweeps the `n` thresholds, each step constant time.

##### Space Complexity: `O(n)`

The bucket array holds `n + 1` counters.

#### Key Insights

- Ratings above the entry count are interchangeable for counting purposes, so clamping at `total` bounds the value domain without losing any qualifying information.
- Counting-sort thinking (bucket tally plus accumulation) replaces comparison sorting, dropping the time bound from `O(n log n)` to `O(n)`.
- The descending accumulation reuses the previous threshold's count, which is exactly the work the brute force was repeating.
- The bucket sweep assumes non-negative ratings, the domain the examples use; a negative rating cannot clear any positive threshold, but it would index `buckets` out of range and needs an explicit guard if the input allowed one.

## Comparison of Solutions

### Time Complexity

- **Descending Threshold Scan**: `O(n²)` - every candidate threshold triggers a fresh count over all entries.
- **Sort Descending and Scan**: `O(n log n)` - sorting dominates; the boundary sweep is linear.
- **Bucket Count Sweep**: `O(n)` - one bucket-filling pass and one threshold sweep.

### Space Complexity

- **Descending Threshold Scan**: `O(1)` - two counters, no auxiliary structures.
- **Sort Descending and Scan**: `O(n)` - the sorted copy of the ratings.
- **Bucket Count Sweep**: `O(n)` - `n + 1` bucket counters.

### Trade-offs

- **Descending Threshold Scan**: simplest to reason about and non-mutating, but the quadratic recounting makes it impractical for large inputs.
- **Sort Descending and Scan**: one sort turns every threshold question into a single comparison, and the sorted copy keeps the caller's data intact; the sort cost remains.
- **Bucket Count Sweep**: optimal time, but it leans on the integer value domain and the clamp trick, which makes it slightly less obvious to verify at a glance.

### When to Use Each

- **Descending Threshold Scan**: tiny inputs, or as the reference oracle when testing a faster implementation.
- **Sort Descending and Scan**: the natural interview answer: clear, fast enough for the given bounds, and easy to extend to prefix queries such as "how many entries are >= k for every k?".
- **Bucket Count Sweep**: large integer inputs where the linear bound matters.

### Optimization Notes

- The bucket sweep is the counting-sort specialization of the sorted scan; both exploit the same monotonicity, one through order and one through accumulation.
- The clamp `min(rating, total)` is the standard H-Index move: values above the entry count can never differentiate thresholds, so their exact size carries no information.
- Watch the off-by-one direction: `ordered[threshold]` is compared against `threshold + 1` because Python indices are zero-based while the threshold is one-based.
