# [Non Overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)

**Medium** | **25 minutes** | **Array, Dynamic Programming, Greedy, Sorting**

**Pattern:** [Interval](../patterns/interval/intuition.md), [Greedy Core](../patterns/greedy_core/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Interval scheduling](https://en.wikipedia.org/wiki/Interval_scheduling) · [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

**Practice:** [`practice/non_overlapping_intervals/solution.py`](../../practice/non_overlapping_intervals/solution.py)

Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

Note: Intervals are *non-overlapping* even if they have a common point. For example, `[1, 3]` and `[2, 4]` are overlapping, but `[1, 2]` and `[2, 3]` are non-overlapping.

## Examples

### Example 1

**Input:** `intervals = [[1,2],[2,4],[1,4]]`

**Output:** `1`

**Explanation:** After [1,4] is removed, the rest of the intervals are non-overlapping.

### Example 2

**Input:** `intervals = [[1,2],[2,4]]`

**Output:** `0`

## Constraints

- `1 <= intervals.length <= 100,000`
- `intervals[i].length == 2`
- `-50000 <= starti < endi <= 50000`

## Deriving the Solution

Removals are the flip side of keeping: minimizing removals is maximizing the intervals that survive, and survivors must be pairwise non-overlapping under the shared-boundary rule (`[1,2]` and `[2,3]` coexist). So every solution is really an interval-scheduling question, "how many compatible intervals can be kept?", answered with increasing amounts of structure.

1. **Start literal.** Sort the intervals, then decide keep-or-remove for each
   with recursion over the kept-so-far last end; correct but it revisits the
   same subproblems: see [Brute Force Keep-or-Remove](#brute-force-keep-or-remove).
2. **Cache the states.** Memoize the recursion on the index and the last kept
   end, and the exponential tree collapses to one computation per state: see
   [Top-Down Memoization](#top-down-memoization).
3. **Order by end and commit greedily.** Sorting by end makes one forward
   rule optimal: keep an interval exactly when it starts at or after the last
   kept end. One pass decides everything: see
   [Greedy Earliest End](#greedy-earliest-end).
4. **Count removals directly.** The same pass can tally removals instead of
   keeps: overwrite the running end whenever the current interval overlaps,
   which is the smallest bookkeeping the rule allows: see
   [Greedy Removal Tally](#greedy-removal-tally).

## Solutions

### Brute Force Keep-or-Remove

#### Derivation

The most direct reading sorts the intervals by start (so compatibility has a fixed direction) and then walks them, deciding at each interval whether it belongs to the kept set. Sorting by start lets `prev_end`, the end of the most recently kept interval, summarize everything about the past:

1. Sort `intervals` by start.
2. Define `keep_from(ch, prev_end)`: the maximum number of intervals keepable
   from position `ch` on, given that everything kept so far ends at
   `prev_end`.
3. Skip branch: `keep_from(ch + 1, prev_end)`, this interval is removed.
4. Keep branch: allowed only when `intervals[ch]` starts at or after
   `prev_end` (touching endpoints do not overlap), and yields
   `1 + keep_from(ch + 1, end)`.
5. The answer to the problem is `n - keep_from(0, -infinity)`.

Nothing is remembered between calls, so identical `(ch, prev_end)` questions are re-answered once per route that reaches them.

#### Walkthrough

Trace the recursion on Example 1: `intervals = [[1,2],[2,4],[1,4]]`, which sorts by start to `[[1,2],[1,4],[2,4]]`. The trace shows the pair of branches at each reached state; `prev_end` starts at `-infinity`:

```text
keep_from(0, -inf)   s[0]=[1,2]: keepable
  keep branch: 1 + keep_from(1, 2) = 1 + 1 = 2
    keep_from(1, 2)  s[1]=[1,4]: starts 1 < 2 -> keep branch dead
      skip: keep_from(2, 2)
        keep_from(2, 2)  s[2]=[2,4]: starts 2 >= 2 -> keepable
          keep: 1 + keep_from(3, 4) = 1 + 0 = 1
          skip: keep_from(3, 2) = 0
          -> max(0, 1) = 1
      -> max(1, 0) = 1
  skip branch: keep_from(1, -inf)
    keep_from(1, -inf)  s[1]=[1,4]: keepable
      keep: 1 + keep_from(2, 4) = 1 + 0 = 1
        keep_from(2, 4)  s[2]=[2,4]: 2 < 4 -> skip only -> 0
      skip: keep_from(2, -inf)
        keep_from(2, -inf)  s[2]=[2,4]: keepable
          keep: 1 + keep_from(3, 4) = 1 + 0 = 1
          skip: keep_from(3, -inf) = 0
          -> max(0, 1) = 1
      -> max(1, 1) = 1
  -> max(2, 1) = 2
answer = 3 - 2 = 1
```

The maximum keepable set here has size `2` (`[1,2]` and `[2,4]`): the root's keep branch adds its own interval to `keep_from(1, 2)`'s `1`, totalling `2`, against the skip branch's `1`, so `keep_from(0, -inf) = max(2, 1) = 2` and the answer is `3 - 2 = 1`, matching the expected Output for Example 1. The trap this trace exists to flag: `keep_from(1, 2)` itself returns only `1` (its keep branch dies on `1 < 2`), and reading that partial value as the whole keep branch gives `max(1, 1) = 1` kept and a phantom `2` removals; the root's own `+ 1` must be added back before the max. On Example 2 (`[[1,2],[2,4]]`) every keep branch succeeds, `keep_from` returns `2`, and the removal count is `0`.

#### Solution

The code is the walkthrough's two branches around the compatibility test.

```python
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda interval: interval[0])

        def keep_from(ch: int, prev_end: int) -> int:
            if ch == len(intervals):
                return 0
            skip = keep_from(ch + 1, prev_end)
            start, end = intervals[ch]
            keep = 0
            if start >= prev_end:
                keep = 1 + keep_from(ch + 1, end)
            return max(skip, keep)

        return len(intervals) - keep_from(0, float("-inf"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each reached state forks into up to two branches, so the call tree doubles along star chains of mutually compatible intervals; each node does constant work.

##### Space Complexity: `O(n)`

The recursion stack reaches depth `n`; sorting is in-place.

#### Key Insights

- Sorting by start is what lets one number (`prev_end`) summarize the kept set: later intervals only ever need to know how far the past reaches.
- The keep condition `start >= prev_end` encodes the shared-boundary rule: `[1,2]` followed by `[2,4]` is compatibility, not conflict.
- The keep branch explores a pruned subtree but the tree is still exponential; the recursion merely enumerates keep-sets.

### Top-Down Memoization

#### Derivation

The recursion re-answers questions, yet `keep_from(ch, prev_end)` depends only on the pair: every route reaching a state gets the same answer. But the state space is a snag: `prev_end` ranges over interval ends, not positions, so a naive `(ch, prev_end)` memo can still hold many states per index. Because the array is sorted by start, only ends of already-kept intervals ever arrive as `prev_end`, and the memo keys on exactly those observed pairs; the computation per state is constant, and distinct states per index are bounded by the number of distinct ends reachable, at most `n`:

1. Keep the recursion verbatim from the Brute Force.
2. Before computing, return the stored answer for `(ch, prev_end)` from
   `memo`.
3. Otherwise compute, store under `(ch, prev_end)`, and return.
4. The answer is `n - keep_from(0, -infinity)` as before.

#### Walkthrough

Trace the memoized recursion on Example 1's sorted input `[[1,2],[1,4],[2,4]]`, showing which states compute and which hit:

```text
keep_from(0, -inf)  miss
  keep branch: 1 + keep_from(1, 2)
    keep_from(1, 2)  miss   s[1]=[1,4]: 1 < 2, keep dead
      skip: keep_from(2, 2)  miss
        keep: 1 + keep_from(3, 4) = 1 + 0 = 1     base: (3, *) -> 0
        skip: keep_from(3, 2) = 0
        -> 1        memo[(2,2)] = 1
    -> 1        memo[(1,2)] = 1
  -> 2
  skip branch: keep_from(1, -inf)  miss
    keep: 1 + keep_from(2, 4)  miss
      skip: keep_from(3, 4) = 0
      -> 0        memo[(2,4)] = 0
    -> 1
    skip: keep_from(2, -inf)  miss
      keep: 1 + keep_from(3, 4) = 1
      skip: 0
      -> 1        memo[(2,-inf)] = 1
    -> 1        memo[(1,-inf)] = 1
  -> max(2, 1) = 2
```

The answer is `3 - 2 = 1` removal, matching the expected Output for Example 1. On this input every computed state is distinct, so the memo saves nothing; its value appears when many keep-chains converge on the same `(ch, prev_end)`, which longer mixed inputs produce in numbers.

#### Solution

The code is the branching recursion with the memo wrapped around it.

```python
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda interval: interval[0])
        memo = {}

        def keep_from(ch: int, prev_end: int) -> int:
            if ch == len(intervals):
                return 0
            if (ch, prev_end) in memo:
                return memo[(ch, prev_end)]

            skip = keep_from(ch + 1, prev_end)
            start, end = intervals[ch]
            keep = 0
            if start >= prev_end:
                keep = 1 + keep_from(ch + 1, end)
            memo[(ch, prev_end)] = max(skip, keep)
            return memo[(ch, prev_end)]

        return len(intervals) - keep_from(0, float("-inf"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each index pairs with at most `n + 1` distinct `prev_end` values (the ends of already-processed intervals plus the initial `-infinity`), each computed once with constant work.

##### Space Complexity: `O(n^2)`

The memo holds one entry per computed state; the recursion stack adds depth `n`.

#### Key Insights

- Caching helps even with a non-integer state: dictionary keys do not care that `prev_end` is an interval end rather than an index.
- The memo's savings are input-dependent: on short or already-compatible inputs the extra structure buys nothing, which the walkthrough honestly shows.
- The quadratic state count is what the greedy removes next: ordering by end makes the best keep-set extendable one interval at a time, with no branching left.

### Greedy Earliest End

#### Derivation

The memoized recursion still branches because it keeps choice alive: at each interval, keep or remove. Sorting by *end* kills the choice. The earliest-finishing interval conflicts with the fewest others, so an optimal keep-set can always include it; having committed to it, every interval that starts before its end is excluded, and the same argument re-runs on the rest. One forward pass with a running `prev_end` and no backtracking:

1. Sort `intervals` by end.
2. Take the first interval: `prev_end = end`, `kept = 1`.
3. For each later interval, if `start >= prev_end`, keep it:
   `kept += 1`, `prev_end = end`.
4. Return `len(intervals) - kept`.

#### Invariant

After processing each interval, `prev_end` is the minimum possible last end among all keep-sets of maximum size for the prefix processed so far:

$$ \text{prev\_end} = \min \{\, \text{last end} : K \text{ a maximum-size keep-set of the prefix} \,\} $$

```text
prev_end = smallest achievable "last kept end"
           among maximum-size keep-sets of the processed prefix
```

Induction on the pass: the seed takes the globally earliest end, which heads some maximum keep-set (exchange argument: swap any set's first member for it, nothing later starts earlier). The inductive step holds at each interval: if `start >= prev_end`, adjoining it keeps the set maximum and never raises the last end more than any alternative, because `end` is the smallest end available among compatible candidates; if `start < prev_end`, no maximum keep-set of the prefix can contain this interval alongside what the invariant already certifies, since everything compatible with the certified prefix ends no later than `prev_end`. At the end the maximum keep count is `kept`, and removals are their complement.

#### Walkthrough

Trace the greedy on Example 1: `intervals = [[1,2],[2,4],[1,4]]`, which sorts by end to `[[1,2],[2,4],[1,4]]` (ties in end keep the input's relative order, so `[2,4]` precedes `[1,4]`):

```text
sorted by end: [1,2]  [2,4]  [1,4]
seed     [1,2]  kept=1  prev_end=2
[2,4]    start 2 >= 2 -> keep     kept=2  prev_end=4
[1,4]    start 1 < 4  -> remove   kept=2
kept=2 -> removals = 3 - 2 = 1
```

The kept set is `[1,2]` and `[2,4]`, the removed interval is `[1,4]`, and the function returns `1`, matching the expected Output for Example 1. On Example 2, `[[1,2],[2,4]]` (already end-sorted), the seed keeps `[1,2]`, `[2,4]` starts at `2 >= 2` and is kept too, so `kept=2` and the function returns `0`.

#### Solution

The code is the walkthrough's pass: sort by end, seed, then keep-or-remove per interval.

```python
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda interval: interval[1])

        kept = 0
        prev_end = float("-inf")
        for start, end in intervals:
            if start >= prev_end:
                kept += 1
                prev_end = end

        return len(intervals) - kept
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the sweep is one linear pass of a comparison per interval.

##### Space Complexity: `O(1)`

Two running values beyond the in-place sort.

#### Key Insights

- Sorting by end, not start, is the move: ends are what conflicts are measured against, and the earliest end leaves the most room behind it.
- The greedy commits and never revisits, which is exactly the exchange argument: any optimal set can be rearranged to include the earliest-ending interval without shrinking.
- This is the classic activity-selection solution wearing a removals costume; recognizing the flip is the whole problem.

### Greedy Removal Tally

#### Derivation

The keep-counting pass tracks `kept` and reads removals as a difference. The tempting inline is to count removals directly: walk the end-sorted intervals, and whenever the current one overlaps the running window, count a removal and overwrite the running end with the current interval's end. The overwrite is where the inline breaks: it silently *removes the previous window-holder*, but that holder may be the seed interval, whose end was the smallest so far, and adopting a larger end then squeezes every later interval. The counterexample is Example 1's intervals reordered, `[[1,2],[1,4],[2,4]]`: the stable end-sort keeps exactly that order (the shared end `4` preserves the input's relative order), so after seeding `[1,2]`, the overlap with `[1,4]` overwrites the window to `4`, which then conflicts with `[2,4]` and forces a second removal where one suffices. The failure is tie-order dependent: on Example 1's literal order the end-sort runs `[[1,2],[2,4],[1,4]]`, the window reaches `4` through a keep, and the naive tally happens to return the correct `1`. The fix that stays a tally is to overwrite only when the newcomer genuinely replaces the window-holder, which requires remembering whether the current window end belongs to an already-removed interval. That extra state is the whole content of the keep counter, laundered: tracking `kept` (or equivalently, only advancing the window on non-overlaps) is the honest minimal form. The tally below is therefore the keep counter with the subtraction folded into the seed, correct because the window advances only on genuine adoptions:

1. Sort `intervals` by end.
2. Sweep with `prev_end`, the end of the last *kept* interval, seeded at the
   first interval's end; `removed = 0`.
3. Per later interval: if `start >= prev_end`, keep it and advance
   `prev_end`; otherwise increment `removed` and leave `prev_end` alone.
4. Return `removed`.

#### Walkthrough

Trace the tally on Example 1: end-sorted `[[1,2],[2,4],[1,4]]`:

```text
seed     [1,2]  prev_end=2  removed=0
[2,4]    start 2 >= 2  -> keep, prev_end=4
[1,4]    start 1 < 4   -> removed=1, prev_end holds at 4
removed=1
```

The seed `[1,2]` endures, `[2,4]` advances the window, and the final overlap removes `[1,4]` without touching the window. The function returns `1`, matching the expected Output for Example 1; on Example 2 (`[[1,2],[2,4]]`) it returns `0`. The holding window on removal is the invariant doing the work the naive overwrite violated: a removed interval's end must never become the standard the surviving intervals are judged by.

#### Solution

The code is the tally with the hold-on-removal rule: the window moves only for kept intervals.

```python
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda interval: interval[1])

        removed = 0
        prev_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= prev_end:
                prev_end = end
            else:
                removed += 1
        return removed
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the sweep is one linear pass.

##### Space Complexity: `O(1)`

A counter and a running end.

#### Key Insights

- The tally and the keep counter are now the same algorithm read from two sides: `removed + kept = n`, with the window advancing only on keeps in both.
- The overwrite bug class is worth naming: any greedy sweep that lets a *removed* element set the standard for future comparisons can cascade one removal into many, which is exactly what the naive tally does on the reordered input `[[1,2],[1,4],[2,4]]`.
- The seed deserves the same scrutiny as the loop: seeding from `intervals[0]` is safe here only because the first end-sorted interval is always kept by any maximum keep-set, per the exchange argument in [Greedy Earliest End](#greedy-earliest-end).

## Comparison of Solutions

The practice harness's `practice/non_overlapping_intervals/reference.py` implements the **Greedy Earliest End** solution.

### Time Complexity

- **Brute Force Keep-or-Remove**: `O(2^n)` - two branches per interval over the keep-set search.
- **Top-Down Memoization**: `O(n^2)` - one computation per index-and-end state.
- **Greedy Earliest End**: `O(n log n)` - sort, then one linear pass.
- **Greedy Removal Tally**: `O(n log n)` - the keep pass with the subtraction folded in.

### Space Complexity

- **Brute Force Keep-or-Remove**: `O(n)` - recursion stack.
- **Top-Down Memoization**: `O(n^2)` - the memo over states.
- **Greedy Earliest End**: `O(1)` - two running values.
- **Greedy Removal Tally**: `O(1)` - a counter and a running end.

### Trade-offs

- The brute force states the keep-set search directly and serves as the oracle, at exponential cost.
- The memoized version is comfortably fast at these constraints but pays quadratic memory for choice the greedy never needs.
- Greedy Earliest End is the smallest correct thing: one sort key, one comparison, one counter, with the exchange argument as its only proof burden.
- The tally variant reads the same sweep from the removals side; its only trap is historical, the overwrite that let removed intervals set the window, and the hold-on-removal rule is what keeps it honest.

### When to Use Each

- **Brute Force Keep-or-Remove**: as the derivational baseline and correctness oracle on tiny inputs.
- **Top-Down Memoization**: when a provably exhaustive search is wanted and quadratic memory is acceptable.
- **Greedy Earliest End** (recommended): the interview answer: sort by end, keep what fits, return the complement.
- **Greedy Removal Tally**: as a study companion: compare it against Greedy Earliest End on hostile inputs to see the invariant working.

### Optimization Notes

- The sort key is the whole algorithm: keying by start instead of end admits greedy passes that under-keep (an interval can end late and block many others), which is why the DP versions sort by start and the greedy sorts by end.
- The shared-boundary rule lives in one character: `start >= prev_end` keeps touching intervals, `start > prev_end` would wrongly remove `[1,2]` before `[2,3]`.
- The tally's hold-on-removal rule is the one line to watch: overwriting the window on a removal (the naive inline) lets a removed interval's end squeeze every later interval, a documented wrong-answer class (reorder Example 1 to `[[1,2],[1,4],[2,4]]` and the naive tally returns `2`).
- Both greedy passes agree with the memoized search whenever the tally's invariant holds; a disagreement on random inputs is the fastest way to detect a broken sort key or comparison.
