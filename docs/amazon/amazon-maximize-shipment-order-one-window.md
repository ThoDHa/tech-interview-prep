# [Maximize Shipment Order by Sorting One Window](https://www.fastprep.io/problems/amazon-maximize-shipment-order-one-window)

**Hard** | **NN minutes** | **Array, Stack, Segment Tree, Sorting**

shipmentOrder is a permutation of 1..n. Choose exactly one contiguous window of length windowSize, sort that window in ascending order, and return the lexicographically largest complete array obtainable.

## Examples

### Example 1

**Input:** `shipmentOrder = [5,1,4,3,2]`, `windowSize = 3`

**Output:** `[5,1,3,4,2]`

**Explanation:** Sorting positions 1 through 3 preserves the longest and then largest prefix.

## Constraints

- `N/A (FastPrep lists no constraints)`

## Deriving the Solution

Sorting a window in ascending order can never make the array lexicographically larger. Wherever the sorted window first differs from what it replaced, it places the smallest value still left in the window, and that value is at most the one it displaced. So every candidate answer is the original array, or a slightly damaged copy of it, and the task is really: which single window damages the array least? The page's constraint block is unparseable, so the artifacts assume `1 <= windowSize <= n` (a window must exist) and treat `shipmentOrder` as a permutation of `1..n` with `n` large enough that an `O(n log n)` plan is wanted; everything below uses only that.

1. **Start literal.** Try every window start, sort a copy, and keep the lexicographically largest result: correct, and `(n - w + 1) * w log w` work: see [Brute Force Window Simulation](#brute-force-window-simulation).
2. **Rank the candidates without sorting them.** A sorted window agrees with the original up to a break position and sorts from there; the candidate with the latest break wins, and among equal breaks the earliest start wins. Walking the agreement per start decides every candidate in `O(w)`: see [Agreement-Prefix Ranking](#agreement-prefix-ranking).
3. **Precompute the breaks.** The break position of a start is a yes-or-no question at each window position, answerable from two precomputed arrays (last descent before a position, next strictly smaller value to the right). Each position then contributes one interval of starts it serves, and painting those intervals largest-break-first hands every start its answer in near-linear time: see [Painted Agreement Intervals](#painted-agreement-intervals).

## Solutions

### Brute Force Window Simulation

#### Derivation

The statement's most literal reading: the answer is the best of `(n - w + 1)` concrete arrays, so build each one and compare:

1. For each `start` from `0` through `count - width`: copy `shipmentOrder`, replace the slice `start:start + width` with its sorted version.
2. Keep the lexicographically largest copy seen.
3. Return it.

The identity candidate (a window that is already sorted) participates naturally: its copy equals the original, which is the largest any candidate can be.

#### Walkthrough

Example 1 (`shipmentOrder = [5,1,4,3,2]`, `windowSize = 3`) has three windows:

```text
start 0   sort [5,1,4] -> [1,4,5]   result [1,4,5,3,2]
start 1   sort [1,4,3] -> [1,3,4]   result [5,1,3,4,2]
start 2   sort [4,3,2] -> [2,3,4]   result [5,1,2,3,4]
```

Comparing the three results position by position, `[5,1,3,4,2]` beats `[5,1,2,3,4]` at index 2 and both beat `[1,...]` at index 0, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, shipmentOrder: List[int], windowSize: int) -> List[int]:
        count, width = len(shipmentOrder), windowSize
        best = None
        for start in range(count - width + 1):
            candidate = shipmentOrder[:]
            candidate[start : start + width] = sorted(
                shipmentOrder[start : start + width]
            )
            if best is None or candidate > best:
                best = candidate
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n - w + 1) * w log w)`

Each of the `n - w + 1` starts sorts a window of `w` values and compares two length-`n` arrays.

##### Space Complexity: `O(n)`

One candidate copy and the running best, each a full array.

#### Key Insights

- The simulation is the definition of the answer, which makes it the oracle every faster approach is checked against.
- Most of the work is wasted: sorting each window from scratch repeats nearly identical work at neighboring starts.
- A candidate can never beat the original array; sorting only ever moves a smaller value forward.

### Agreement-Prefix Ranking

#### Derivation

The brute force sorts every window just to compare the results. Compare the results structurally instead. A result with window start `s` equals the original everywhere outside `[s, s + w)`, and inside the window the sorted order agrees with the original on a prefix: position `k` still holds `values[k]` exactly while the values before `k` inside the window are the smallest ones, ascending, and no value from `k` onward is smaller. Let `e(s)` be the first position where the sorted window differs from the original (the break), with `e(s) = s` when even the window's own first position changes and `e(s) = s + w` for a window already sorted:

1. Two candidates with starts `s < t`: candidate `t` keeps the original on `[0, t)`, so if candidate `s` breaks before `t`, it loses at its own break, where it placed a strictly smaller value.
2. A candidate with a later break therefore beats every candidate with an earlier break, and among candidates sharing the same break `E`, the earliest start wins: past `E` each sorted window places the order statistics of its suffix `values[E..window_end)`, the later start's suffix is a strict superset of the earlier start's, so the later candidate places an element-wise smaller-or-equal value across the shared stretch `[E, s + w)`; when those values tie, the later candidate then holds the ascending arrangement of exactly the cells the earlier candidate holds in original order, and ascending is the lexicographically least arrangement of a multiset.
3. So the winner is the start maximizing `e(s)`, earliest on ties, and only that one window needs sorting.
4. To compute `e(s)` for one start: sweep the window's suffix minima right to left into `suffix_min`, then walk `k` upward from `s + 1` while the values `values[s..k-1]` are ascending and `values[k-1] <= suffix_min[k]`; the first failure is `e(s)`. The walk reaching the window's last position means the window itself is sorted, so the original array is the answer and the scan can stop.
5. Otherwise sort the winning window and return.

#### Walkthrough

Example 1 (`shipmentOrder = [5,1,4,3,2]`, `windowSize = 3`), the per-start agreement walks:

```text
start 0   window [5,1,4]   sorted[0]=1 vs 5        break e=0
start 1   window [1,4,3]   sorted[0]=1 == 1        agree
                           sorted[1]=3 vs 4        break e=2
start 2   window [4,3,2]   sorted[0]=2 vs 4        break e=2
```

The latest break is `2`, shared by starts 1 and 2; the earliest start wins, so window `[1,4,3]` sorts to `[1,3,4]` and the answer is `[5,1,3,4,2]`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, shipmentOrder: List[int], windowSize: int) -> List[int]:
        values = shipmentOrder
        count, width = len(values), windowSize
        best_start, best_break = 0, 0
        for start in range(count - width + 1):
            window_end = start + width
            suffix_min = values[window_end - 1]
            mins = [0] * width
            for offset in range(width - 1, -1, -1):
                suffix_min = min(suffix_min, values[start + offset])
                mins[offset] = suffix_min
            agreement = start
            for offset in range(1, width):
                if (
                    values[start + offset - 1] > values[start + offset]
                    or values[start + offset - 1] > mins[offset]
                ):
                    break
                agreement = start + offset
            if agreement == start + width - 1:
                return values
            if agreement > best_break:
                best_break, best_start = agreement, start
        return (
            values[:best_start]
            + sorted(values[best_start : best_start + width])
            + values[best_start + width :]
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n - w + 1) * w)`

Each start builds a suffix-minimum row and walks at most `w` agreement positions; one final sort of `w` values is absorbed by the same bound.

##### Space Complexity: `O(n)`

The result assembly copies the array; the per-start `mins` row adds `O(w)`.

#### Key Insights

- The break position compresses each candidate to one number, and that number orders the candidates completely: latest break first, earliest start on ties.
- The walk reaching a window's last position is exactly the sorted-window test, and it returns the original array immediately: no damaged candidate can tie a window that sorts to itself, because a damaged window breaks at least one position earlier.
- A damaged window's walk value is at most `start + width - 2`, a sorted window's is `start + width - 1`; that one-position gap is why the earliest-tie rule can safely prefer the sorted window.
- The walk never sorts: it only checks the two conditions (ascending prefix, prefix max at most suffix min) that make a sorted window agree with the original.

### Painted Agreement Intervals

#### Derivation

The ranking walk repeats nearly the same questions at neighboring starts. Ask the questions per position instead of per start. Position `k` (with `last_agreed = k - 1`) is a valid break candidate for start `s` exactly when:

- the values `values[s..k-1]` ascend, which holds precisely when `s` sits after the last descent at or before `k - 1`;
- every value from `k` to the window end `s + w - 1` is at least `values[k - 1]`, which holds precisely when the next strictly smaller value after `k - 1` lies beyond `s + w - 1`;
- the window covers `k`: `s >= k - w + 1`.

All three are interval conditions on `s`, so each `k` serves one contiguous range of starts. A window already sorted is handled up front (it returns the original array), and after that every start's break is the largest valid `k` serving it:

1. Build `last_descent_before[p]` (largest `j < p` with `values[j] > values[j + 1]`, else `-1`) in one forward pass.
2. Build `next_smaller_right[p]` (smallest `j > p` with `values[j] < values[p]`, else `count`) with a monotonic stack.
3. For each `k` from `count - 1` down to `1`, compute the serving interval `lo = max(last_descent_before[k - 1] + 1, k - width + 1, 0)` to `hi = min(k - 1, next_smaller_right[k - 1] - width, count - width)`, and paint every unpainted start in `[lo, hi]` with `break_after[s] = k`. Painting in decreasing `k` order with a next-unpainted pointer (path-compressed) gives each start the largest valid `k` in near-linear total time; starts never painted keep `break_after[s] = s`.
4. Return the original array if any window has no internal descent; otherwise take the earliest start with the largest `break_after`, sort its window, and return.

#### Walkthrough

Example 1 (`shipmentOrder = [5,1,4,3,2]`, `windowSize = 3`). Descents sit at `0`, `2`, `3`, so `last_descent_before` reads `[-1, 0, 0, 2, 3]` and `next_smaller_right` reads `[1, 5, 3, 4, 5]`:

```text
k=1   last_agreed=0   interval [max(0,-2,0), min(0,-2,2)] = [0,-2]   empty
k=2   last_agreed=1   interval [max(1, 0,0), min(1, 2,2)] = [1, 1]   paint s=1 -> break 2
k=3   last_agreed=2   interval [max(1, 1,0), min(2, 0,2)] = [1, 0]   empty
k=4   last_agreed=3   interval [max(3, 2,0), min(3, 1,2)] = [3, 1]   empty

break_after = [0, 2, 2]   (start 0 unpainted, keeps its own start)
```

No window is descent-free, so the largest break `2` decides, earliest start `1` wins, and sorting `[1,4,3]` gives `[5,1,3,4,2]`, matching the expected Output.

#### Solution

The code is the three interval conditions written once per `k`, painted largest break first.

```python
from typing import List


class Solution:
    def solve(self, shipmentOrder: List[int], windowSize: int) -> List[int]:
        values = shipmentOrder
        count, width = len(values), windowSize

        last_descent_before = [-1] * count
        for position in range(1, count):
            last_descent_before[position] = last_descent_before[position - 1]
            if values[position - 1] > values[position]:
                last_descent_before[position] = position - 1

        for start in range(count - width + 1):
            if last_descent_before[start + width - 1] < start:
                return values

        next_smaller_right = [count] * count
        monotonic_stack: List[int] = []
        for position in range(count):
            while monotonic_stack and values[monotonic_stack[-1]] > values[position]:
                next_smaller_right[monotonic_stack.pop()] = position
            monotonic_stack.append(position)

        break_after = list(range(count))
        next_unpainted = list(range(count + 1))

        def first_unpainted(start: int) -> int:
            while next_unpainted[start] != start:
                next_unpainted[start] = next_unpainted[next_unpainted[start]]
                start = next_unpainted[start]
            return start

        for agreement_end in range(count - 1, 0, -1):
            last_agreed = agreement_end - 1
            low = max(
                last_descent_before[last_agreed] + 1,
                agreement_end - width + 1,
                0,
            )
            high = min(
                last_agreed,
                next_smaller_right[last_agreed] - width,
                count - width,
            )
            start = first_unpainted(low)
            while start <= high:
                break_after[start] = agreement_end
                next_unpainted[start] = start + 1
                start = first_unpainted(start + 1)

        best_start, best_break = 0, 0
        for start in range(count - width + 1):
            if break_after[start] > best_break:
                best_break, best_start = break_after[start], start
        return (
            values[:best_start]
            + sorted(values[best_start : best_start + width])
            + values[best_start + width :]
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The two precomputations and the interval painting are linear (each start is painted once, with near-constant pointer hops), leaving the final `O(w log w)` window sort as the dominant term.

##### Space Complexity: `O(n)`

The three arrays over positions, the pointer array, and the result assembly.

#### Key Insights

- Reversing the loop (for each position, which starts does it serve?) turns `n` overlapping window walks into `n` disjoint paint operations.
- The identity early-out is not just an optimization: a sorted window is the original array, and nothing beats it, so the painting can assume every window breaks.
- `next_smaller_right` from a monotonic stack is the whole min condition: the sorted window agrees past `k - 1` exactly when no smaller value interrupts before the window ends.

## Comparison of Solutions

### Time Complexity

- **Brute Force Window Simulation**: `O((n - w + 1) * w log w)` - every window sorted and every result compared.
- **Agreement-Prefix Ranking**: `O((n - w + 1) * w)` - each start walks its agreement once, then one window is sorted.
- **Painted Agreement Intervals**: `O(n log n)` - linear precompute and paint, one window sorted at the end.

### Space Complexity

- **Brute Force Window Simulation**: `O(n)` - a candidate copy and the running best.
- **Agreement-Prefix Ranking**: `O(n)` - the result assembly plus a per-start suffix-minimum row.
- **Painted Agreement Intervals**: `O(n)` - position arrays, paint pointers, and the result assembly.

### Trade-offs

- **Brute Force Window Simulation**: the definition written down and the oracle for everything else; the sort-per-window cost rules it out at scale.
- **Agreement-Prefix Ranking**: removes the sorting from the ranking, but neighboring starts still re-walk overlapping positions.
- **Painted Agreement Intervals**: pays two classic precomputations to answer every start's break from intervals, and sorts exactly one window.

### When to Use Each

- **Brute Force Window Simulation**: for tiny inputs, and always as the independent checker for the other two.
- **Agreement-Prefix Ranking**: when you want the structural rule (latest break, earliest start) without extra preprocessing.
- **Painted Agreement Intervals (Recommended)**: the interview answer at scale: precompute once, paint once, sort once.

### Optimization Notes

- **Painted Agreement Intervals** is the recommended choice: the dominant cost is the single `O(w log w)` sort of the winning window.
- The break conditions decompose cleanly because the array is a permutation: distinct values make the descent test strict and the next-smaller scan unambiguous.
- The identity early-out must run before painting: a sorted window never paints past `start + width - 1`, so with the early-out dropped its undercounted break loses the argmax to a start whose painted-or-default break is larger, and sorting that window returns a damaged candidate instead of the original.
- Working assumption recorded for review: the page's constraint block is unparseable, so the gauntlet assumes `1 <= windowSize <= n`; `windowSize = 1` and `windowSize = n` both appear as cases.
