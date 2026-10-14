# [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)

**Medium** | **25 minutes** | **Array, Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/koko_eating_bananas/solution.py`](../../practice/koko_eating_bananas/solution.py)

You are given an integer array `piles` where `piles[i]` is the number of bananas in the `ith` pile. You are also given an integer `h`, which represents the number of hours you have to eat all the bananas.

You may decide your bananas-per-hour eating rate of `k`. Each hour, you may choose a pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, you may finish eating the pile but you can not eat from another pile in the same hour.

Return the minimum integer `k` such that you can eat all the bananas within `h` hours.

## Examples

### Example 1

**Input:** `piles = [1,4,3,2], h = 9`

**Output:** `2`

**Explanation:** With an eating rate of 2, you can eat the bananas in 6 hours. With an eating rate of 1, you would need 10 hours to eat all the bananas (which exceeds h=9), thus the minimum eating rate is 2.

### Example 2

**Input:** `piles = [25,10,23,4], h = 4`

**Output:** `25`

## Constraints

- `1 <= piles.length <= 10,000`
- `piles.length <= h <= 1,000,000,000`
- `1 <= piles[i] <= 1,000,000,000`

## Deriving the Solution

The eating rate admits an obvious feasibility test: given rate `k`, the hours needed are the sum over piles of the ceiling of `pile / k`, and `k` works exactly when that sum is at most `h`. The question "find the minimum `k` that works" is therefore a search over the half-line of rates `1, 2, 3, ...`, and the only thing that matters is the shape of the answer set: raising the rate never increases hours needed, so the working rates form a suffix of the line. Every solution searches that line; they differ in the stride.

1. **Start literal.** Try `k = 1`, then `2`, then `3`, returning the first rate
   that finishes in time. Correct, but `h` can be a billion hours and the
   answer can be a billion bananas per hour: see
   [Linear Scan](#linear-scan).
2. **Spot the structure.** The linear scan never uses its own history: it
   already knows rate `k` works, yet it still probes `k + 1` as if nothing were
   learned. A monotone feasibility test over an ordered line is the definition
   of binary search territory.
3. **Search the answer space itself.** Halve the interval `[1, max(piles)]` on
   each feasibility probe: too slow means go faster, in time means remember the
   rate and try slower. `O(n log m)` instead of `O(n * m)`: see
   [Binary Search on the Answer](#binary-search-on-the-answer).

## Solutions

### Linear Scan

#### Derivation

The most literal reading tries every candidate rate in increasing order and returns the first feasible one. Feasibility at rate `k` is computed exactly as the problem describes: each pile takes `ceil(pile / k)` hours because a pile cannot be split across hours, so the total is the sum of ceilings:

1. For `k = 1, 2, 3, ...`:
2. Compute `hours(k) = sum(ceil(pile / k) for pile in piles)`.
3. Return the first `k` with `hours(k) <= h`.

The answer exists because `k = max(piles)` finishes each pile in one hour, using at most `len(piles) <= h` hours.

#### Walkthrough

Trace the scan on Example 1: `piles = [1,4,3,2]`, `h = 9`. Each row shows the rate, the per-pile hour counts, and the total:

```text
k=1   hours = 1 + 4 + 3 + 2 = 10   10 <= 9? no
k=2   hours = 1 + 2 + 2 + 1 = 6    6  <= 9? yes -> return 2
```

Rate `1` overspends by one hour, and rate `2` finishes with three hours to spare, so the scan returns `2`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's rate-by-rate probe.

```python
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        k = 1
        while True:
            hours = sum((pile + k - 1) // k for pile in piles)
            if hours <= h:
                return k
            k += 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k_min)`

Every rate below the answer is probed, each probe costing a pass over the `n` piles; with pile sizes up to `10^9` this is astronomically slow.

##### Space Complexity: `O(1)`

Only the running rate and its hour total are stored.

#### Key Insights

- Ceilings via integer arithmetic: `(pile + k - 1) // k` avoids
  floating-point `math.ceil` and its precision limits at `10^9`.
- The feasibility test is shared verbatim with the binary search version;
  only the search strategy differs.
- The scan's failure is not the test but the stride, which ignores that
  feasibility is monotone.

### Binary Search on the Answer

#### Derivation

The linear scan re-derives from scratch what it already knows. Feasibility is monotone: if rate `k` finishes in time, so does every `k' > k`, since `hours(k)` is a non-increasing function of `k`. The feasible rates are therefore a suffix `[k_min, max(piles)]` of the candidate line, and finding the left edge of a sorted-shaped space is exactly what [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) does:

1. Bracket the answer: `left = 1`, `right = max(piles)` (the always-feasible rate).
2. While `left < right`, probe `mid = (left + right) // 2`.
3. If `hours(mid) <= h`, the answer is `mid` or slower: keep it,
   `right = mid`.
4. Otherwise `mid` is too slow to finish: `left = mid + 1`.
5. When `left == right`, the interval has collapsed onto `k_min`: return `left`.

The loop is the "find first true" pattern: `right` always holds a feasible rate and `left - 1` an infeasible one, so convergence cannot skip the boundary.

#### Walkthrough

Trace the search on Example 2: `piles = [25,10,23,4]`, `h = 4`. Four piles and four hours mean every pile must take exactly one hour, so the answer should be `max(piles)`; the search discovers it in four probes:

```text
left=1   right=25   mid=13   hours = 2 + 1 + 2 + 1 = 6   6 <= 4? no  -> left=14
left=14  right=25   mid=19   hours = 2 + 1 + 2 + 1 = 6   6 <= 4? no  -> left=20
left=20  right=25   mid=22   hours = 2 + 1 + 2 + 1 = 6   6 <= 4? no  -> left=23
left=23  right=25   mid=24   hours = 2 + 1 + 2 + 1 = 6   6 <= 4? no  -> left=25
left=25  right=25   loop ends -> return 25
```

Every probe here is dominated by pile `25`, which needs two hours at any rate below `25`; the search rides that fact to the right edge and returns `25`, matching the expected Output for Example 2. On Example 1 the same probes would find rate `2` feasible and walk `right` down to it, and the boundary at exactly `h` hours (rate `1` needs `10 > 9`, rate `2` needs `6 <= 9`) is what the `<=` in the probe encodes.

#### Solution

The code is the walkthrough's bracket, probe, and collapse, with `hours_needed` as its own helper since it is the invariant both this solution and the linear scan share.

```python
from typing import List


def hours_needed(piles: List[int], k: int) -> int:
    """Total hours to eat `piles` at rate `k`: one ceiling per pile."""
    return sum((pile + k - 1) // k for pile in piles)


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left, right = 1, max(piles)
        while left < right:
            mid = (left + right) // 2
            if hours_needed(piles, mid) <= h:
                # mid works: the answer is mid or anything slower
                right = mid
            else:
                left = mid + 1
        return left
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log m)`

The interval halves on every probe, giving `O(log m)` probes where `m = max(piles)`, and each probe is an `O(n)` pass over the piles. For the constraint sizes (`n = 10^4`, `m = 10^9`) that is about `10^4 * 30` work, trivially fast.

##### Space Complexity: `O(1)`

Only the search boundaries and the probe's hour total are stored.

#### Key Insights

- Searching the answer space, not the input, is the move: the piles are never
   sorted or searched, only summed.
- The probe must test `<= h`, not `< h`: finishing in exactly `h` hours is on
  time.
- The bracket `[1, max(piles)]` needs no upper refinement: any faster rate
  behaves identically to `max(piles)`, one hour per pile, so nothing beyond it
  can be minimal.
- This "binary search on a monotone predicate" template recurs everywhere a
  threshold hides in a problem: capacity to ship, minimum pedestal size,
  maximum subarray sum bounded by a budget.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n * k_min)` - every slower rate is probed in full.
- **Binary Search on the Answer**: `O(n log m)` - `O(log m)` probes, each `O(n)`.

### Space Complexity

- **Linear Scan**: `O(1)` - running rate and hour total.
- **Binary Search on the Answer**: `O(1)` - bracket boundaries and probe total.

### Trade-offs

- Both share the same feasibility test and constant space; the difference is
  purely the search strategy over the rate line.
- The scan's simplicity is genuine but deceptive: at constraint sizes it does
  not terminate in any practical time, so it is not a usable baseline.
- The binary search pays only a bounded loop invariant to gain eleven orders of
  magnitude at `m = 10^9`.

### When to Use Each

- **Linear Scan**: As the correctness oracle in tests of the real solution, on
  inputs small enough to finish.
- **Binary Search on the Answer**: Always, in practice; the interview and
  production answer (recommended here).

### Optimization Notes

- `(pile + k - 1) // k` is the exact integer ceiling; `math.ceil(pile / k)`
  converts through floats and can misround near `10^9`.
- `max(piles)` is computed once for the bracket; recomputing it per probe would
  waste a pass per iteration.
- The loop condition `left < right` (not `<=`) is what makes termination clean:
  the interval is half-open in spirit, collapsing to the single boundary rate.
