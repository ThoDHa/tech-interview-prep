# [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)

**Medium** | **25 minutes** | **Array, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md), [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/combination_sum_ii/solution.py`](../../practice/combination_sum_ii/solution.py)

You are given an array of integers `candidates`, which may contain duplicates, and a target integer `target`. Your task is to return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`.

Each element from `candidates` may be chosen **at most once** within a combination. The solution set must not contain duplicate combinations.

You may return the combinations in **any order** and the order of the numbers in each combination can be in **any order**.

## Examples

### Example 1

**Input:** `candidates = [9,2,2,4,6,1,5]`, `target = 8`

**Output:** `[[1,2,5],[2,2,4],[2,6]]`

**Explanation:** Each element may be used at most once, so `[2,6]` consumes the first `2` and `[2,2,4]` consumes both; `[1,2,5]` is the only other way to reach `8`.

### Example 2

**Input:** `candidates = [1,2,3,4,5]`, `target = 7`

**Output:** `[[1,2,4],[2,5],[3,4]]`

## Constraints

- `1 <= candidates.length <= 100`
- `1 <= candidates[i] <= 50`
- `1 <= target <= 30`

## Deriving the Solution

Two requirements shape every solution: each element may enter a combination at most once, and equal values sitting at different indices must not let the same combination be built twice. The second is the hard one, because combinations are multisets, not index sets: choosing the first `2` versus the second `2` produces the same combination, yet only the first choice may be allowed to build it.

1. **Start literal.** At each element, branch on a binary decision: include
   `candidates[index]` and move to `index + 1`, or exclude it and move on. The exclude branch never revisits an element, so the use-once rule is automatic, but the duplicate values generate duplicate combinations, which a `seen` set of canonical keys must filter after the fact: see [Include-Exclude Backtracking](#include-exclude-backtracking).
2. **Spot the waste.** The filter repairs the output only after the search
   has already paid to build every duplicate leaf; the tree itself never shrinks, because nothing stops two branches from converging on the same multiset.
3. **Fix it by ordering.** Sort `candidates` so equal values sit adjacent,
   then enforce a canonical rule: within one loop level, only the first twin may start a branch (`i > start` skips later ones), so equal values are always consumed as a prefix run of consecutive indices and a duplicate can never be built at all. Sorting also upgrades the overshoot test into a `break` prune: see [Sorted Backtracking with Duplicate Skipping](#sorted-backtracking-with-duplicate-skipping).
4. **Build up instead of searching down.** Collapse each distinct value into
   a `(value, count)` group and grow a table over every sub-target one group at a time, deciding per group how many copies, from `0` up to its `count`, enter each combination; a downward sweep of sub-targets keeps a pass from reading its own writes: see [Count-Grouped Bottom-Up Dynamic Programming](#count-grouped-bottom-up-dynamic-programming).

## Solutions

### Include-Exclude Backtracking

#### Derivation

The most direct reading of the problem is a [binary decision tree](https://en.wikipedia.org/wiki/Backtracking): at each element we either include it or exclude it, and both branches advance the index, which is what enforces "at most once" without any extra bookkeeping. Uniqueness is not automatic, though: two equal values at different indices are distinct elements, so the branches rooted at each of them can both reach the same combination. The only repair available without reordering the input is to record a canonical key for each combination found and keep the first copy:

1. Recurse with the current `index`, the `remaining` target, and the partial
   `current` combination.
2. If `remaining` reaches `0`, canonicalize `current` as `key = tuple(sorted(current))`;
   record a copy only when `key` is not yet in `seen`, then register it.
3. If `remaining` goes negative or `index` runs off the end, abandon the
   branch.
4. Otherwise branch twice: include `candidates[index]` and recurse on
   `index + 1`, then exclude it and recurse on `index + 1`.

The cost of this honesty is that the tree never shrinks: every duplicate is still built, walked to a leaf, and only then discarded.

#### Walkthrough

Example 1 has seven candidates and only one duplicated value, so the filtering is invisible unless the trace includes a collision. The tailored input `candidates = [1,2,2]`, `target = 3` (not an official Example) produces the collision on the very first leaf: the two `2`s are distinct elements, and each can complete `[1]` into `[1,2]`.

```text
backtrack(index=0, remaining=3, current=[])
  include 1 -> backtrack(index=1, remaining=2, current=[1])
    include 2 (first)  -> backtrack(2, 0, [1,2])
                          remaining == 0 -> key (1,2) new -> RECORD [1,2]
    exclude 2 (first)  -> backtrack(2, 2, [1])
      include 2 (second) -> backtrack(3, 0, [1,2])
                            remaining == 0 -> key (1,2) SEEN -> FILTERED
      exclude 2 (second) -> backtrack(3, 2, [1])
                            index off the end -> dead
  exclude 1 -> backtrack(index=1, remaining=3, current=[])
    (no subset of {2,2} reaches 3)                        dead
```

The function returns `[[1,2]]`, which is correct, but the search visited the `[1,2]` leaf twice to produce it once, and on inputs like Example 1 most branches are duplicated in just this way.

#### Solution

The code is the walkthrough's fork: record on a canonical key, otherwise include-then-exclude with both branches advancing `index`.

```python
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        result: List[List[int]] = []
        seen = set()

        def backtrack(index: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                key = tuple(sorted(current))
                if key not in seen:
                    seen.add(key)
                    result.append(current[:])
                return
            if remaining < 0 or index >= len(candidates):
                return

            # Include candidates[index]; either way, move past it: use once.
            current.append(candidates[index])
            backtrack(index + 1, remaining - candidates[index], current)
            current.pop()
            backtrack(index + 1, remaining, current)

        backtrack(0, target, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^N * k)`

Each of the `N` candidates is included or excluded, so the tree has up to `2^N` leaves; canonicalizing each recorded combination costs up to `k log k` for sorting plus `k` to copy, where `k` bounds a combination's length, giving `O(2^N * k)` overall. The `seen` filter removes duplicates from the output but does nothing to the size of the tree that produces them.

##### Space Complexity: `O(N + K)`

The recursion stack and the `current` path reach depth `N`, and the `seen` set holds one key per recorded combination, `K` entries of length up to `k`.

#### Key Insights

- The exclude branch's "never look back" discipline enforces use-once for
  free, but it operates on indices; equal values at different indices sail right through it.
- `tuple(sorted(current))` is the canonical form that makes two index sets
  producing the same multiset collide in `seen`.
- This is the only solution that needs a deduplication structure at all; the
  two below prevent duplicates structurally instead of filtering them.

### Sorted Backtracking with Duplicate Skipping

#### Derivation

The include-exclude tree pays for every duplicate it builds and filters afterward. The duplicates arise for one reason: equal values can be picked out of their relative order, the second twin sometimes entering a combination without the first. Sorting `candidates` puts equal values adjacent, and that unlocks a canonical rule the tree can enforce locally: within any single loop level (the same `start`), only the first twin may start a branch, and later twins are skipped. The second twin is never lost, only repositioned: one level deeper, where `start` has advanced past the first twin, taking it is legal again, which is exactly how a combination holding both twins gets built. Equal values therefore enter every combination as a prefix run of consecutive indices, and since each combination has exactly one such run structure, duplicates can never be built, so no `seen` set is needed.

The steps:

1. Sort `candidates` ascending.
2. Recurse with a `start` index, the running `remaining` target, and the
   partial `current` combination.
3. When `remaining` hits `0`, record a copy of `current` as a valid
   combination.
4. For each `i` from `start` onward: skip `i` when `i > start` and
   `candidates[i] == candidates[i - 1]`; `break` when `candidates[i] > remaining`, since the sort guarantees every later candidate is at least as large; otherwise pick `candidates[i]`, recurse on `i + 1` (each element used at most once), and unpick.

#### Walkthrough

Let us run the pruned search on Example 1: `candidates = [9,2,2,4,6,1,5]` sorts to `[1,2,2,4,5,6,9]`, `target = 8`. Each call loops `i` upward from its `start`; a `take` line descends one level, `skip` kills one branch, and `break` discards the rest of a level in one test.

```text
backtrack(start=0, remaining=8, current=[])
  i=0: take 1 -> backtrack(1, 7, [1])
    i=1: take 2 -> backtrack(2, 5, [1,2])
      i=2: i == start, take 2 -> backtrack(3, 3, [1,2,2])
        i=3: 4 > 3 -> break                  second twin legal: start moved past first
      i=3: take 4 -> backtrack(4, 1, [1,2,4])
        i=4: 5 > 1 -> break
      i=4: take 5 -> backtrack(5, 0, [1,2,5])
                     remaining == 0 -> RECORD [1,2,5]
      i=5: 6 > 5 -> break
    i=2: candidates[2] == candidates[1] and i > start -> skip
    i=3: take 4 -> backtrack(4, 3, [1,4])
      i=4: 5 > 3 -> break
    i=4: take 5 -> backtrack(5, 2, [1,5])
      i=5: 6 > 2 -> break
    i=5: take 6 -> backtrack(6, 1, [1,6])
      i=6: 9 > 1 -> break
    i=6: 9 > 7 -> break
  i=1: take 2 -> backtrack(2, 6, [2])
    i=2: i == start, take 2 -> backtrack(3, 4, [2,2])
      i=3: take 4 -> backtrack(4, 0, [2,2,4])
                   remaining == 0 -> RECORD [2,2,4]
      i=4: 5 > 4 -> break
    i=3: take 4 -> backtrack(4, 2, [2,4])    dead (5 > 2)
    i=4: take 5 -> backtrack(5, 1, [2,5])    dead (6 > 1)
    i=5: take 6 -> backtrack(6, 0, [2,6])
                 remaining == 0 -> RECORD [2,6]
    i=6: 9 > 6 -> break
  i=2: candidates[2] == candidates[1] and i > start -> skip   twin root pruned
  i=3: take 4 -> backtrack(4, 4, [4])         dead (5 > 4)
  i=4: take 5 -> backtrack(5, 3, [5])         dead (6 > 3)
  i=5: take 6 -> backtrack(6, 2, [6])         dead (9 > 2)
  i=6: 9 > 8 -> break
```

Watch what the skip rule does at the top level: after the branch rooted at the first `2` (`i=1`) finishes, `i=2` holds the second `2` and is skipped, because the branch rooted there could only re-derive subsets of `{2,4,5,6,9}` that the first `2`'s branch already enumerated. Both twins still meet inside `[2,2,4]`: at that node `start=2` equals `i=2`, so the second `2` is a fresh first occurrence at its own level and is taken. The leaves were recorded in the order `[1,2,5]`, `[2,2,4]`, `[2,6]`, giving `result = [[1,2,5],[2,2,4],[2,6]]`, matching the expected Output for Example 1 with each combination built exactly once.

#### Solution

The code is the loop from the walkthrough: sort once, then loop, skip twins, `break` on overshoot, choose, recurse on `i + 1`, unchoose.

```python
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sort so equal values sit adjacent and the overshoot test can break.
        candidates.sort()
        result: List[List[int]] = []

        def backtrack(start: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                result.append(current[:])
                return

            for i in range(start, len(candidates)):
                # Within one level only the first twin may start a branch.
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                candidate = candidates[i]
                # Sorted order: once one candidate is too big, the rest are too.
                if candidate > remaining:
                    break
                current.append(candidate)
                # i + 1, not i: each element is used at most once.
                backtrack(i + 1, remaining - candidate, current)
                current.pop()

        backtrack(0, target, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^N * k)`

Each of the `N` candidates is included or excluded, so the worst case is a binary decision tree of `2^N` leaves, and copying each recorded combination of length up to `k` adds a linear factor per leaf. The skip rule and the `break` prune do not change that worst case, but they cut whole levels and subtrees in practice, which is what separates this from the include-exclude version whose tree is never pruned. The initial sort contributes `O(N log N)`, dominated by the exponential term.

##### Space Complexity: `O(N)`

Excluding the output, the recursion stack and the `current` path are both bounded by `N`, since each element may be used at most once; the sort is in place.

#### Key Insights

- The skip guard is `i > start`, not `i > 0`: the comparison against the left
  sibling only means "duplicate" within one level. At a deeper call, `start` has moved past the earlier twin, so `i == start` is a legal first occurrence, and that is precisely how `[2,2,4]` survives.
- Recursing on `i + 1` instead of `i` is the use-once counterpart of
  Combination Sum's reuse-on-the-same-index, and it is what bounds the depth by `N`.
- Sorting does double duty: adjacency makes the duplicate test a single
  comparison, and monotonicity upgrades a `continue`-style overshoot check into a `break` that discards the rest of the level unexamined.

### Count-Grouped Bottom-Up Dynamic Programming

#### Derivation

The backtracking search discovers each combination one element at a time and needs the skip rule to avoid building duplicates. Reformulate instead: a combination is fully described by how many copies of each distinct value it uses. Collapse `candidates` into `counts`, mapping each distinct `value` to its multiplicity `count`, and grow a table over sub-targets one group at a time, deciding for each group how many copies, from `0` up to `count`, enter each combination. Processing groups in ascending value order keeps every stored combination non-decreasing, so uniqueness and canonical order both come from the loop structure rather than from filtering; the Invariant below states the property formally.

The steps:

1. Build `counts` from `candidates`, mapping each distinct value to how many
   times it appears.
2. Initialize `dp[0]` with one empty combination; every other `dp[t]` starts
   empty.
3. For each distinct `value` in ascending order with multiplicity `count`,
   sweep sub-targets `t` from `target` down to `value`.
4. For each `copies` from `1` to `count` (stopping once `copies * value`
   exceeds `t`), extend every combination in `dp[t - copies * value]` with `copies` occurrences of `value` and store the results in `dp[t]`.
5. Return `dp[target]`.

#### Invariant

Let `i` be the number of distinct value groups processed so far. After each pass of the outer loop:

$$ \forall t,\ \forall \textit{combo} \in dp[t]:\quad \textit{combo} = [\,v_1 \le v_2 \le \cdots \le v_m\,] \quad\text{with each value } v \text{ appearing at most } \textit{counts}[v] \text{ times, drawn only from the first } i \text{ groups} $$

```text
for all t, for all combo in dp[t]:
    combo == [v_1 <= v_2 <= ... <= v_m]
    each value v appears at most counts[v] times
    every element drawn from the first i groups
        (i = distinct value groups processed so far; holds after each pass)
```

Two design choices carry the invariant. First, groups are processed in ascending value order and each extension appends at the end, so combinations stay non-decreasing, and since a combination is one exact vector of per-group counts, it is produced exactly once; there is nothing to deduplicate. Second, the inner sweep over `t` runs *downward*, so every `dp[t - copies * value]` read during a pass holds only combinations from earlier groups: a value can never be appended to a combination that already contains it from this same pass. Combined with the cap `copies <= count`, that enforces use-once per element.

Note what breaks without the grouping. A Combination Sum-style sweep that appends one candidate at a time assumes unlimited reuse; with duplicates in the input it produces `dp[t]` entries like `[[1,2],[1,2]]` for `candidates = [1,2,2]`: one entry per index, not per multiset. The `(value, count)` collapse and the bounded `copies` loop are what make the table honest about multiplicities.

#### Walkthrough

Example 2 has no repeated values, so its trace would not exercise the grouping machinery that this solution exists for. The tailored input `candidates = [1,2,2]`, `target = 5` (not an official Example) collapses to groups `1` and `(2, count 2)`, and its only valid combination is `[1,2,2]`. `dp[0]` starts as `[[]]`, every other `dp[t]` empty; the lines below show the entries each pass writes:

```text
start         dp[0] = [[]]                       all other dp[t] empty
group 1       dp[1] = [[1]]                      [] + [1]
              (count is 1, so copies stops after 1)
group (2, 2)  t=5: copies=1 reads dp[3] (empty)
              t=5: copies=2 reads dp[1] -> dp[5] = [[1,2,2]]   [1] + [2,2]
              t=4: copies=2 reads dp[0] -> dp[4] = [[2,2]]     [] + [2,2]
              t=3: copies=1 reads dp[1] -> dp[3] = [[1,2]]     [1] + [2]
              t=2: copies=1 reads dp[0] -> dp[2] = [[2]]       [] + [2]
```

At `t=5`, `copies=2` reads `dp[1] = [[1]]` and appends two `2`s, so `dp[5] = [[1,2,2]]` is returned, matching the input's only valid combination. The downward sweep shows its worth inside this same pass: when `t=5` is processed, `dp[4]` is still empty, and only afterwards does the pass write `[[2,2]]` into it, so the combination `[2,2]` can never be extended by a third `2`, which the group's `count = 2` forbids. Running the same table on Example 2 (`candidates = [1,2,3,4,5]`, `target = 7`) yields `dp[7] = [[1,2,4],[3,4],[2,5]]`, the expected set of combinations.

#### Solution

The code is the table growth from the walkthrough: group once, sweep each group downward, cap copies at the group's count.

```python
from typing import Dict, List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        counts: Dict[int, int] = {}
        for candidate in candidates:
            counts[candidate] = counts.get(candidate, 0) + 1

        # dp[t] holds every combination summing to t; groups are processed in
        # ascending value order, so every stored combination is non-decreasing.
        dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
        dp[0] = [[]]

        for value in sorted(counts):
            count = counts[value]
            # Downward sweep: dp[t - copies * value] only holds earlier groups.
            for t in range(target, value - 1, -1):
                for copies in range(1, count + 1):
                    weight = copies * value
                    if weight > t:
                        break
                    for combo in dp[t - weight]:
                        dp[t].append(combo + [value] * copies)

        return dp[target]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * target * K)`

Summed over all groups, the outer pair of loops runs once per (sub-target, `copies`) pair, `O(N * target)` pairs in total, where `N` is the number of candidates and each group's multiplicity sums back to `N`; each pair copies every combination it reads, which brings the total to `O(N * target * K)`, with `K` bounding the total size of the stored combinations. As with any enumeration problem, the output dominates, and the DP matches rather than beats the search's output-proportional work.

##### Space Complexity: `O(target * K)`

The `dp` table stores, for every sub-target, all combinations reaching it, which is strictly more memory than the search solutions' single path.

#### Key Insights

- Grouping duplicates into `(value, count)` pairs turns the two constraints
  into one mechanism: a bounded `copies` loop is both the use-once rule and the duplicate rule.
- The downward sweep of `t` is load-bearing, not stylistic: reading only
  pre-pass entries is what stops a value from stacking beyond its count.
- Processing groups in ascending value order yields non-decreasing
  combinations, so an equality check against any expected set needs only the outer list sorted, never the contents.
- The table makes every intermediate combination explicit, which trades
  memory for the removal of recursion, the same trade as in Combination Sum's bottom-up DP.

## Comparison of Solutions

### Time Complexity

- **Include-Exclude Backtracking**: `O(2^N * k)` - explores the full binary
  decision tree and filters duplicates only after building them.
- **Sorted Backtracking with Duplicate Skipping**: `O(2^N * k)` - same worst
  case, but the skip rule and the sorted `break` cut whole levels and subtrees in practice.
- **Count-Grouped Bottom-Up Dynamic Programming**: `O(N * target * K)` -
  dominated by copying the combinations stored per sub-target.

### Space Complexity

- **Include-Exclude Backtracking**: `O(N + K)` - recursion path plus the
  `seen` set holding one key per recorded combination.
- **Sorted Backtracking with Duplicate Skipping**: `O(N)` - recursion stack
  and one path, since each element is used at most once.
- **Count-Grouped Bottom-Up Dynamic Programming**: `O(target * K)` - stores
  all combinations for every sub-target.

### Trade-offs

- **Include-Exclude Backtracking** is the easiest to derive and needs no
  reordering of the input, but it pays full price for every duplicate it later throws away and carries the `seen` set on top.
- **Sorted Backtracking with Duplicate Skipping** adds an `O(N log N)` sort
  and one guard to prevent duplicates structurally, making it the leanest and fastest in practice.
- **Count-Grouped Bottom-Up Dynamic Programming** removes recursion and
  states the constraints as explicit counting, but holds every intermediate combination in memory.

### When to Use Each

- **Include-Exclude Backtracking**: As the first intuition, or when the input
  must not be reordered and a one-off set filter is acceptable.
- **Sorted Backtracking with Duplicate Skipping** (recommended): The default
  interview answer; the skip rule is a two-line guard and duplicates never exist.
- **Count-Grouped Bottom-Up Dynamic Programming**: When you want an iterative
  formulation without recursion, or a template that generalizes to bounded-use variants of Combination Sum.

### Optimization Notes

- The duplicate-skip guard must compare `i > start`, not `i > 0`: only the
  first twin at one level may start a branch, while deeper levels must still accept equal values or combinations like `[2,2,4]` would be lost.
- Sorting enables `if candidate > remaining: break`; without sorting the
  overshoot test could only `continue`, leaving the rest of the level to be walked.
- The DP's downward sweep is what caps each value at its count; an upward
  sweep reads entries the same pass just wrote and can stack a value past its multiplicity.
- The two sorted approaches emit each combination already non-decreasing, so
  an equality check needs only the outer list sorted. The include-exclude version emits combinations in input order, so its output needs the full `sorted(map(sorted, result))` canonicalization.
