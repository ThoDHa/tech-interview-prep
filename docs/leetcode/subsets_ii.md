# [Subsets II](https://leetcode.com/problems/subsets-ii/)

**Medium** | **25 minutes** | **Array, Backtracking, Bit Manipulation**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Power set](https://en.wikipedia.org/wiki/Power_set) · [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

**Practice:** [`practice/subsets_ii/solution.py`](../../practice/subsets_ii/solution.py)

You are given an array `nums` of integers, which may contain duplicates. Return all possible subsets.

The solution must **not** contain duplicate subsets. You may return the solution in **any order**.

## Examples

### Example 1

**Input:** `nums = [1,2,1]`

**Output:** `[[],[1],[1,2],[1,1],[1,2,1],[2]]`

### Example 2

**Input:** `nums = [7,7]`

**Output:** `[[],[7],[7,7]]`

## Constraints

- `1 <= nums.length <= 11`
- `-20 <= nums[i] <= 20`

## Deriving the Solution

A subset is determined by which values it contains and how many copies of each, not by which input positions were used: two index choices that take the same multiset of values spell the same subset, and the answer must report each distinct subset exactly once. Every solution below answers the question the duplicates pose differently: enumerate everything and drop the repeats after the fact, or make the repeats impossible to produce.

1. **Start literal.** Run the choose-or-skip decision tree of plain Subsets
   over every index, normalize each completed subset to a sorted tuple, and
   let a set drop the repeats. Correct, but the tree still walks every branch,
   including branches that can only re-derive a subset another branch already
   produced: see [Brute Force](#brute-force).
2. **Spot the waste.** The duplicate branches are not random. In a sorted
   input, equal values sit side by side, and a branch that takes a later copy
   while skipping an earlier one spells exactly the subset that taking the
   earlier copy already produced.
3. **Prune with an order rule.** Sort `nums` first and, inside one loop level,
   never choose a value whose identical left neighbor was passed over. The
   emitted subsets then take a prefix of every run of equal values, one
   representative each, with no set needed: see
   [Sorted Backtracking](#sorted-backtracking).
4. **Collapse each run to one decision.** The skip rule still walks the
   interchangeable copies one by one. Counting each distinct value's
   multiplicity replaces the whole run with a single decision, "how many
   copies join the subset?", which enumerates the distinct subsets directly:
   see [Distinct-Value Counting](#distinct-value-counting).
5. **Let the library enumerate.** The whole spec is "every sorted combination
   of every size, repeats dropped". [`itertools.combinations`](https://docs.python.org/3/library/itertools.html#itertools.combinations)
   over the sorted input, deduplicated by `dict.fromkeys`, states it in one
   expression: see
   [Library One-Liner with `itertools.combinations`](#library-one-liner-with-itertoolscombinations).

## Solutions

### Brute Force

#### Derivation

The most literal reading treats duplicates as a filtering problem: generate every index-based subset the same way plain Subsets does, and throw the repeated ones away. A set is the natural filter, but the key needs care, because there are two distinct sources of repetition. Equal values swapped for one another produce different index paths with equal value lists, and the same values chosen at different positions produce different value orders, as Example 1's paths `[1,2]` and `[2,1]` show. Both collapse to one key if each completed subset is recorded as a sorted tuple:

1. Define `choose_or_skip(index, current_subset)` and launch it as
   `choose_or_skip(0, [])`.
2. Base case: when `index == len(nums)`, add
   `tuple(sorted(current_subset))` to `unique_subsets` and return.
3. Otherwise recurse twice: first skip `nums[index]`, then choose it
   (`current_subset.append`, recurse, `current_subset.pop`).
4. Convert every kept tuple back to a list and return them in the set's
   arbitrary order, which the any-order contract permits.

#### Walkthrough

Let us run the full tree by hand on Example 1: `nums = [1,2,1]`. Each call first skips `nums[index]`, then takes it; each leaf records the sorted tuple of the values chosen along its path:

```text
choose_or_skip(0, [])
  skip 1 -> choose_or_skip(1, [])
    skip 2 -> choose_or_skip(2, [])
      skip 1 -> leaf  ()
      take 1 -> leaf  (1,)
    take 2 -> choose_or_skip(2, [2])
      skip 1 -> leaf  (2,)
      take 1 -> leaf  tuple(sorted([2,1])) = (1, 2)
  take 1 -> choose_or_skip(1, [1])
    skip 2 -> choose_or_skip(2, [1])
      skip 1 -> leaf  (1,)                       repeat, set absorbs
      take 1 -> leaf  (1, 1)
    take 2 -> choose_or_skip(2, [1, 2])
      skip 1 -> leaf  (1, 2)                     repeat, set absorbs
      take 1 -> leaf  (1, 1, 2)
```

The eight leaves collapse to six distinct tuples, which is exactly the six subsets of Example 1's expected Output (`[1,2,1]` appears under its sorted spelling `(1,1,2)`; the elements of a subset may be reported in any order). The cost is visible in the tree: the two `repeat` leaves were walked in full only to be discarded, and most subtrees below them would suffer the same fate.

#### Solution

The code is the walkthrough's skip-then-take tree, with the sorted-tuple record at the leaves.

```python
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        unique_subsets = set()

        def choose_or_skip(index, current_subset):
            if index == len(nums):
                # Sorting the values makes equal subsets hash equal:
                # [1,2] and [2,1] must land on one key, not two.
                unique_subsets.add(tuple(sorted(current_subset)))
                return
            choose_or_skip(index + 1, current_subset)
            current_subset.append(nums[index])
            choose_or_skip(index + 1, current_subset)
            current_subset.pop()

        choose_or_skip(0, [])
        return [list(subset) for subset in unique_subsets]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n log n)`

The decision tree has `2^n` leaves and every leaf sorts its completed subset at `O(n log n)` before hashing it. The set only saves the conversion work at the end; it never saves any of the walking.

##### Space Complexity: `O(2^n × n)`

The set pins one tuple of up to `n` values per distinct subset, at most `2^n` of them, and the recursion stack adds `O(n)`.

#### Key Insights

- The dedup key must normalize element order, not just identity of indices:
  recording raw tuples would return both `[1,2]` and `[2,1]`, which are the same subset.
- The set cleans up the answer but cannot shrink the search: every duplicate
  branch is still walked in full, which is the waste the next solutions prune.
- Sorting each subset at record time is the brute force's quiet `log n`
  surcharge; the Sorted Backtracking section moves that sort to the input,
  once, and reuses it as pruning structure.

### Sorted Backtracking

#### Derivation

The brute force recognizes duplicates only after walking them and pays a per-subset sort to make them recognizable. Both costs shrink if the normalization happens once, up front: sort `nums`, and then any path's chosen values are already in nondecreasing order (indices ascend over sorted values), so two paths spell the same subset exactly when they produce the same list. That makes the duplicates structural: a duplicate is always a branch that, at some loop level, takes a later copy of a value while an identical earlier copy sits untaken at the same level. Bar that one case and no set is needed:

1. Sort `nums` ascending so every run of equal values is contiguous.
2. Define `backtrack(start_index, current_subset)`; on entry, record a copy
   `current_subset[:]` into `result`.
3. For each `i` from `start_index` on: if `i > start_index` and
   `nums[i] == nums[i - 1]`, skip this iteration; otherwise append `nums[i]`,
   recurse with `backtrack(i + 1, current_subset)`, and pop.
4. Launch `backtrack(0, [])`; `result` holds every distinct subset.

#### Invariant

The dedup rests on the prefix property the skip rule enforces:

```text
every emitted subset takes a prefix of each run of equal values:
when nums[i - 1] == nums[i], index i is chosen on a path
only if index i - 1 was chosen on it too
```

Each branch preserves it. Recursion always resumes at `i + 1` after taking `i`, so whenever a path arrives at level `start_index` inside a run, it has already taken every earlier index of that run, and taking `nums[start_index]` extends the prefix. Inside a level's loop, reaching iteration `i` means `i - 1` was passed over at this level; choosing `nums[i]` while `nums[i] == nums[i - 1]` would take a later copy while an equal earlier copy stays out, and `continue` bars exactly that case. At the leaves, two distinct paths differ in some run's prefix length, and a subset's multiset is determined by its per-run prefix lengths, so distinct paths emit distinct subsets: the tree itself is the dedup, no set required.

#### Walkthrough

Let us run the pruned tree on Example 1, whose sorted form is `nums = [1,1,2]`. Each call records first, then loops; the two skip events are marked, and they are the whole dedup:

```text
backtrack(0, [])                    record []
  i=0  take 1 -> [1]
  backtrack(1, [1])                 record [1]
    i=1  i == start_index: take 1 -> [1, 1]
    backtrack(2, [1, 1])            record [1, 1]
      i=2  take 2 -> [1, 1, 2]
      backtrack(3, [1, 1, 2])       record [1, 1, 2]    loop empty
      pop 2 -> [1, 1]
    pop 1 -> [1]
    i=2  take 2 -> [1, 2]
    backtrack(3, [1, 2])            record [1, 2]       loop empty
    pop 2 -> [1]
  pop 1 -> []
  i=1  nums[1] == nums[0], i > start_index -> SKIP
  i=2  take 2 -> [2]
  backtrack(3, [2])                 record [2]          loop empty
  pop 2 -> []
```

Reading the `record` events in order gives `[[], [1], [1,1], [1,1,2], [1,2], [2]]`: six distinct subsets, the same set as Example 1's expected Output. The skip at `i=1` is the branch that would have spelled `[1]` a second time through the input's second copy, and note that `i=1` under `backtrack(1, [1])` was allowed to take the second `1`: there `i == start_index`, so the run's prefix grew to `[1,1]` legitimately.

#### Solution

The code is the walkthrough's tree: record on entry, sort once outside, skip the equal left sibling inside a level.

```python
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums = sorted(nums)
        result = []

        def backtrack(start_index, current_subset):
            result.append(current_subset[:])
            for i in range(start_index, len(nums)):
                # Taking a later copy while an equal earlier copy sits
                # untaken at this level re-derives an existing subset.
                if i > start_index and nums[i] == nums[i - 1]:
                    continue
                current_subset.append(nums[i])
                backtrack(i + 1, current_subset)
                current_subset.pop()

        backtrack(0, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

The invariant makes the tree hold exactly one node per distinct subset, so the work is one `O(n)` copy per node; when all values are distinct this is the full `2^n`-node tree of plain Subsets, and duplicates only shrink it.

##### Space Complexity: `O(2^n × n)`

The result holds one list of up to `n` values per distinct subset, and the recursion stack adds `O(n)` depth. The sort is in-place on a fresh list and needs no extra bookkeeping beyond `current_subset`.

#### Key Insights

- Sorting the input replaces two mechanisms at once: it makes duplicate
  subsets produce identical value lists, and it makes duplicates adjacent so a one-line comparison can prune them before they are walked.
- The `i > start_index` half of the guard is load-bearing: without it, a
  fresh level after taking the first copy of a run would skip the second, and legitimate subsets like `[1,1]` would become unreachable.
- Recording on every node, not only at leaves, still holds exactly as in
  plain Subsets; the skip rule only removes nodes, it does not change which nodes count as answers.

### Distinct-Value Counting

#### Derivation

The skip rule is correct but fragile: drop the `i > start_index` half and duplicates flood back, and either way the tree still visits every copy of a run one by one. The deeper repair changes what a decision is. A subset of `nums` is, per distinct value `v`, a choice of how many of its copies to include, from `0` up to `v`'s multiplicity. Walking the distinct values in a fixed order and making that one decision per value enumerates every distinct subset exactly once, because there is no longer any way to express the same subset twice: copies of a value are interchangeable, and they are decided in a single stroke.

1. Build `counts = Counter(nums)` and `distinct_values = list(counts)`.
2. Define `backtrack(value_index, current_subset)`; when
   `value_index == len(distinct_values)`, record `current_subset[:]` into
   `result` and return.
3. Otherwise take `value = distinct_values[value_index]` and, for each
   `copies` from `0` through `counts[value]`, extend `current_subset` with
   `copies` copies of `value`, recurse with `value_index + 1`, then pop those
   `copies` elements back off.
4. Launch `backtrack(0, [])`; `result` holds every distinct subset.

Note what disappeared: no sort, no comparison rule. The input's order is irrelevant because the decision order is `distinct_values`' order, fixed once.

#### Walkthrough

Let us decide copy counts by hand on Example 1: `nums = [1,2,1]`, so `counts = {1: 2, 2: 1}` and `distinct_values = [1, 2]`. The tree forks on how many `1`s join (three options), then on how many `2`s (two options):

```text
backtrack(0, [])        value 1, counts[1] = 2 -> copies 0..2
  copies=0 -> []
    value 2: copies=0 -> []           record []
             copies=1 -> [2]          record [2]
  copies=1 -> [1]
    value 2: copies=0 -> [1]          record [1]
             copies=1 -> [1, 2]       record [1, 2]
  copies=2 -> [1, 1]
    value 2: copies=0 -> [1, 1]       record [1, 1]
             copies=1 -> [1, 1, 2]    record [1, 1, 2]
```

Six decisions chains, six recorded subsets: exactly Example 1's expected Output. Nothing was ever discarded, because the shape of the tree admits no duplicate: each value's contribution was decided once, as a count, rather than once per interchangeable copy.

#### Solution

The code is the walkthrough's count loop: extend with `copies` copies, recurse, pop them back.

```python
from collections import Counter
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        counts = Counter(nums)
        distinct_values = list(counts)
        result = []

        def backtrack(value_index, current_subset):
            if value_index == len(distinct_values):
                result.append(current_subset[:])
                return
            value = distinct_values[value_index]
            for copies in range(counts[value] + 1):
                current_subset.extend([value] * copies)
                backtrack(value_index + 1, current_subset)
                # Pop exactly `copies` elements; del current_subset[-copies:]
                # would delete the whole list when copies == 0 (-0 == 0).
                for _ in range(copies):
                    current_subset.pop()

        backtrack(0, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

The tree has exactly one node per distinct subset and each node copies at most `n` values into `result`; the multiplicity loop distributes those same nodes, adding no overhead beyond the counter build.

##### Space Complexity: `O(2^n × n)`

The result holds every distinct subset; `counts` and `distinct_values` use `O(k)` for `k` distinct values, and the recursion stack reaches depth `O(k)`, both dwarfed by the output.

#### Key Insights

- Making duplicates unrepresentable beats making them forbidden: one
  decision per value removes the entire class of bug the skip rule guards against.
- The sort is gone because the multiplicity view is order-agnostic; only
  the fixed order of `distinct_values` matters, and any fixed order works.
- The pop-back must remove exactly `copies` elements. The tempting
  `del current_subset[-copies:]` silently clears the whole list when `copies == 0`, because `-0` is `0` and `[-0:]` is the full-list slice.

### Library One-Liner with `itertools.combinations`

#### Derivation

The from-scratch recursions above implement a short spec: for every size from `0` to `n`, every nondecreasing draw of that many values from `nums`, with repeated draws dropped. [`itertools.combinations`](https://docs.python.org/3/library/itertools.html#itertools.combinations) over the sorted input produces exactly those draws, size by size, but combinations treat the input's equal values as distinct positions, so a size can yield the same tuple more than once (from Example 1's second copy of `1`). The drop is one dedup pass, and `dict.fromkeys` dedupes while keeping first occurrence, so the output stays in a tidy size-then-value order; a `set` would be equally correct, since the answer's order is free, but scrambles it:

1. Sort `nums`.
2. For each `size` from `0` to `len(nums)`, iterate
   `dict.fromkeys(combinations(nums, size))`, which keeps the first tuple of
   each distinct spelling.
3. Convert each kept tuple to a list and collect them in one flat list.

#### Walkthrough

Let us read off what each size contributes on Example 1, whose sorted form is `[1,1,2]`:

```text
size=0  combinations -> ()                    kept: ()
size=1  combinations -> (1,), (1,), (2,)      kept: (1,), (2,)
size=2  combinations -> (1,1), (1,2), (1,2)   kept: (1,1), (1,2)
size=3  combinations -> (1,1,2)               kept: (1,1,2)
```

The duplicate `(1,)` and `(1,2)` spellings, each reachable through either of the input's two `1` positions, collapse in the `fromkeys` pass. Concatenating the kept tuples gives six subsets: `[], [1], [2], [1,1], [1,2], [1,1,2]`, the same set as Example 1's expected Output.

#### Solution

The spec of the Derivation, written as one comprehension.

```python
from itertools import combinations
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums = sorted(nums)
        return [
            list(subset)
            for size in range(len(nums) + 1)
            for subset in dict.fromkeys(combinations(nums, size))
        ]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

Across all sizes, `combinations` materializes every index combination, `sum(C(n, size)) = 2^n` tuples of up to `n` values, duplicates included, and each passes through the dedup dict at `O(n)` hash cost. Dropping duplicates is bookkeeping, not saving: the generator still enumerates them all.

##### Space Complexity: `O(2^n × n)`

The dedup dict holds one size's tuples at a time, up to `C(n, n/2)` of them, and the returned list holds all distinct subsets; both are bounded by the `O(2^n × n)` output.

#### Key Insights

- `combinations` is index-based, so duplicated values yield duplicate
  tuples; the dedup is not optional decoration but the problem's core requirement.
- Unlike Sorted Backtracking and Distinct-Value Counting, this one-liner
  regenerates duplicates and throws them away, paying brute-force enumeration cost for brute-force work.
- Sorting first is what keeps the output readable: each size's tuples arrive
  nondecreasing, so first-occurrence dedup lands the result in a stable,
  ordered shape instead of a hash order.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n × n log n)` - walks all `2^n` index paths and sorts
  every completed subset before it can be hashed.
- **Sorted Backtracking**: `O(2^n × n)` - one `O(n)` copy per node of the
  deduplicated tree, which holds exactly one node per distinct subset.
- **Distinct-Value Counting**: `O(2^n × n)` - one `O(n)` copy per distinct
  subset, with duplicate branches never created at all.
- **Library One-Liner with `itertools.combinations`**: `O(2^n × n)` - builds
  all `2^n` index combinations across every size, duplicates included.

### Space Complexity

- **Brute Force**: `O(2^n × n)` - the set pins every distinct subset as a
  tuple until the final conversion.
- **Sorted Backtracking**: `O(2^n × n)` - the result plus `O(n)` recursion
  stack.
- **Distinct-Value Counting**: `O(2^n × n)` - the result, plus `O(k)` for the
  counter over `k` distinct values and the recursion stack.
- **Library One-Liner with `itertools.combinations`**: `O(2^n × n)` - the
  returned subsets, with one size's worth of tuples alive in the dedup dict.

### Trade-offs

- **Brute Force**: nothing subtle to get wrong beyond the sorted-tuple key,
  but it walks every duplicate branch in full and pays a per-subset sort to
  recognize what it could have prevented.
- **Sorted Backtracking**: the canonical form; one sort and a one-line guard
  buy a tree proportional to the answer, at the price of a subtle
  `i > start_index` condition that is easy to drop by accident.
- **Distinct-Value Counting**: removes both the sort and the fragile guard by
  changing what a decision is, but it restructures the recursion around
  values rather than indices and needs a counter.
- **Library One-Liner with `itertools.combinations`**: the shortest correct
  code and a deterministic order, but it enumerates duplicates just to
  discard them, so its tree is the brute force's, not the answer's.

### When to Use Each

- **Brute Force**: as the correctness baseline and the fastest thing to write
  when the input is tiny and the answer's shape is uncertain.
- **Sorted Backtracking** (recommended): the interview default: it is the
  plain Subsets tree plus one sort and one guarded `continue`, and the same
  pattern transfers directly to Combination Sum II.
- **Distinct-Value Counting**: when the skip rule feels like a trap to
  defuse, or whenever the input is better described by multiplicities than by
  positions.
- **Library One-Liner with `itertools.combinations`**: for scripts and
  one-off analysis where brevity and determinism beat shaving the duplicate
  branches.

### Optimization Notes

- Sorting once at the input beats sorting per subset: the brute force pays
  `O(n log n)` per leaf to normalize keys, while the same sort done up front
  becomes the structure the skip rule prunes with.
- The `i > start_index` half of the skip guard is what separates "second copy
  at a deeper level" (legal, builds `[1,1]`) from "second copy beside its
  skipped twin" (illegal, duplicates `[1]`). Getting that condition backwards
  in either direction produces either missing or duplicate subsets.
- In the counting recursion, undo the loop body with a counted `pop` loop;
  `del current_subset[-copies:]` looks equivalent and wipes the entire list
  when `copies == 0`, because `-0` indexes from the start.
- With `n <= 11`, the distinct-subset count is at most a few thousand, so
  every approach here finishes instantly; the differences that matter are
  clarity and extensibility, not milliseconds.
