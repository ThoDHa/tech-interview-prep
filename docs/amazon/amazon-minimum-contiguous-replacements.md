# [Minimum Contiguous Replacements](https://www.fastprep.io/problems/amazon-minimum-contiguous-replacements)

**Medium** | **NN minutes** | **Array, Hash Table, Union Find**

You are given an array arr of integers. In one operation, choose two distinct values x and y that currently appear in the array, then replace every occurrence of x with y.

Return the minimum number of operations needed to make the array valid.

An array is valid if every distinct value forms exactly one contiguous block. Values do not all need to become the same.

For example, [1,1,2,2,3] is valid, while [1,2,1,3] is not valid because value 1 appears in two separated blocks.

Function Description Complete minOperations.

int arr[n]: the array to transformReturns int: the minimum number of replacement operations.

## Examples

### Example 1

**Input:** `arr = [1,2,1]`

**Output:** `1`

**Explanation:** Replace every occurrence of 2 with 1, producing [1,1,1].

### Example 2

**Input:** `arr = [1,2,3,1,2,3]`

**Output:** `2`

**Explanation:** One valid sequence is to replace all 2s with 1, then replace all 3s with 1.

### Example 3

**Input:** `arr = [1,2,1,2]`

**Output:** `1`

**Explanation:** Replacing every occurrence of either value with the other makes the array one contiguous block.

## Constraints

- `1 <= arr.length <= 1000`
- `1 <= arr[i] <= 1000`

## Solutions

### Brute Force with Recursive Search

#### Derivation

The most literal reading tracks what an operation does to *values*: replacing every `x` with `y` makes the two values indistinguishable, so afterward the array cannot tell whether `x` was valid on its own. Two separated blocks of `x` glued through a merge into `y` can end up as one block of `y`s. That suggests a search: try every replacement, recurse on the result, and keep the cheapest path to a valid array. Memoizing on the array's tuple keeps repeated shapes from being re-explored:

1. `is_valid` condenses `arr` into blocks of equal values and checks that no two
   blocks share a value; a valid array costs `0`.
2. Otherwise, for every ordered pair of distinct current values `(x, y)`, build
   `replaced` (every `x` becomes `y`) and score `1 + search(replaced)`.
3. `functools.lru_cache` memoizes `search` on the tuple, so an array reachable by
   different orders of the same merges is solved once.
4. Return the minimum over all pairs.

#### Walkthrough

Example 1, `arr = [1, 2, 1]`, explores only one level before every branch terminates:

```text
min_operations((1, 2, 1))
  is_valid?  blocks 1 2 1 -> value 1 twice: no
  try (1 -> 2):  (2, 2, 2)  blocks 2 -> valid            score 1 + 0 = 1
  try (2 -> 1):  (1, 1, 1)  blocks 1 -> valid            score 1 + 0 = 1
  minimum = 1
```

Both single merges produce a constant array, so the search returns `1`, the expected Output. Example 2 needs depth two: `[1, 2, 3, 1, 2, 3]` has no one-merge fix (merging any pair leaves the third value split in two blocks), and merging two values first then the last one reaches a constant array for a total of `2`. Example 3 behaves like Example 1: `[1, 2, 1, 2]` yields `1` either way.

#### Solution

The code is the memoized search from the derivation, with `is_valid` supplying the stop condition.

```python
from functools import lru_cache
from typing import List, Tuple


class Solution:
    def solve(self, arr: List[int]) -> int:
        return self.min_operations(tuple(arr))

    def min_operations(self, state: Tuple[int, ...]) -> int:
        @lru_cache(maxsize=None)
        def search(current: Tuple[int, ...]) -> int:
            if self.is_valid(current):
                return 0
            values = set(current)
            best = len(values) - 1
            for source_value in values:
                for target_value in values:
                    if source_value == target_value:
                        continue
                    replaced = tuple(
                        target_value if item == source_value else item
                        for item in current
                    )
                    best = min(best, 1 + search(replaced))
            return best

        return search(state)

    def is_valid(self, state: Tuple[int, ...]) -> bool:
        block_values: List[int] = []
        for item in state:
            if not block_values or block_values[-1] != item:
                block_values.append(item)
        return len(block_values) == len(set(block_values))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(v × d^2 × S)`

With `v` array positions, `d` distinct values, and `S` distinct reachable states: each memoized state tries every ordered pair of distinct values and rebuilds the tuple in `O(v)`, and `S` itself grows exponentially with the array length, so the search stays a reference tool rather than a production plan.

##### Space Complexity: `O(v × S)`

The memo stores `S` tuples of length `v` plus the recursion stack.

#### Key Insights

- The search is exact: it never returns fewer operations than the best replacement sequence achieves, which makes it the reference for checking faster approaches.
- Memoization is what separates this from factorial blow-up: merge orders that produce the same value pattern are explored once.
- Exponential state growth is still unmanageable at the constraint limits, which is what the next solution removes.

### Interval Overlap Union-Find

#### Derivation

The search re-solves whole arrays, but validity has a static characterization no search needs. Call two values *conflicting* when their occurrence spans in `arr` overlap: some occurrence of `x` sits between two occurrences of `y` (or the reverse), so no ordering of positions can hold both values in single blocks. An operation merges two value classes into one, which resolves every conflict inside the merged class, and conflicts between classes survive. So validity is exactly "no two remaining classes conflict", and the question becomes: how many merges does it take to leave the value classes conflict-free? A connected group of `s` mutually conflicting values can always be cleared with `s - 1` merges by folding every member into a seed, and fewer would leave two of its classes distinct and still in conflict. The answer is therefore the number of distinct values minus the number of conflict components:

1. Scan `arr` once and record each value's `spans`, the first and last index
   where it occurs.
2. For every pair of distinct values, union the two when their spans overlap
   (`first_a <= last_b and first_b <= last_a`).
3. Count the surviving `components`.
4. Return `len(spans) - components`.

#### Walkthrough

Example 1, `arr = [1, 2, 1]`, produces spans `1 -> (0, 2)` and `2 -> (1, 1)`, and the pair test decides the union:

```text
spans: value 1 = (0, 2), value 2 = (1, 1)
overlap? 0 <= 1 and 1 <= 2 -> yes: union(1, 2)
components = 1
answer = 2 values - 1 component = 1
```

One operation, the expected Output. Example 2, `arr = [1, 2, 3, 1, 2, 3]`, gives spans `1 -> (0, 3)`, `2 -> (1, 4)`, `3 -> (2, 5)`; all three pairs overlap, one component forms, and `3 - 1 = 2` matches the expected Output. Example 3, `arr = [1, 2, 1, 2]`, gives `1 -> (0, 2)`, `2 -> (1, 3)`, one overlapping pair, `2 - 1 = 1`.

#### Solution

The code is the span scan, the pairwise overlap union, and the subtraction.

```python
from typing import Dict, List, Tuple


class Solution:
    def solve(self, arr: List[int]) -> int:
        spans = self.occurrence_spans(arr)
        uf = UnionFind(len(spans))
        value_list = list(spans)
        for first_pos in range(len(value_list)):
            for second_pos in range(first_pos + 1, len(value_list)):
                first_value = value_list[first_pos]
                second_value = value_list[second_pos]
                first_start, first_end = spans[first_value]
                second_start, second_end = spans[second_value]
                if first_start <= second_end and second_start <= first_end:
                    uf.union(first_pos, second_pos)
        return len(value_list) - uf.components

    def occurrence_spans(self, arr: List[int]) -> Dict[int, Tuple[int, int]]:
        spans: Dict[int, Tuple[int, int]] = {}
        for position, item in enumerate(arr):
            if item in spans:
                start, _ = spans[item]
                spans[item] = (start, position)
            else:
                spans[item] = (position, position)
        return spans


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, item: int) -> int:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first: int, second: int) -> None:
        first_root, second_root = self.find(first), self.find(second)
        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1
        self.components -= 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + d^2 × α(d))`

One scan records the spans of the `d` distinct values, and the pairwise overlap test runs near-constant union and find operations per pair.

##### Space Complexity: `O(d)`

The span dictionary plus the union-find parent and rank arrays, both over values rather than positions.

#### Key Insights

- Two values conflict exactly when their occurrence spans overlap, a purely static test that needs no simulation of replacement sequences.
- The conflict graph's connected components, not its edge count, set the cost: one merge absorbs an entire component once a seed value is chosen.
- Union-Find with path compression and union by rank makes the component count a near-linear afterthought to the span scan.

### Sorting by Span Start with Sweep Merging

#### Derivation

The union-find solution pays `d^2` pair tests to build a graph whose components a sweep would find for free. [Intervals](https://en.wikipedia.org/wiki/Intervals) whose overlap defines the components have a standard merge: sort by start, then grow the current merged interval while the next one starts at or before its end. The sweep discovers the same components as the pairwise union, in `O(d log d)`:

1. Build the span list from one scan of `arr`, as before.
2. Sort the spans by start index (ties in any order; nested and equal spans merge
   the same way).
3. Sweep: the first span seeds `components = 1`; every span starting at or before
   the running `merged_end` extends it (`merged_end = max(merged_end, end)`);
   every span starting after it opens a new component.
4. Return the component count.

#### Walkthrough

Example 2, `arr = [1, 2, 3, 1, 2, 3]`, produces three spans that the sweep folds into one component:

```text
spans sorted by start: (0, 3) for 1, (1, 4) for 2, (2, 5) for 3
seed (0, 3)            components = 1, merged_end = 3
(1, 4)   1 <= 3        merged_end = max(3, 4) = 4
(2, 5)   2 <= 4        merged_end = max(4, 5) = 5
components = 1 -> answer = 3 - 1 = 2
```

Two operations, the expected Output. Example 1, `arr = [1, 2, 1]`, sorts to `(0, 2)` for 1 and `(1, 1)` for 2: the seed sets `merged_end = 2`, the second span starts inside it, and `2 - 1 = 1`. Example 3, `arr = [1, 2, 1, 2]`, sorts to `(0, 2)` and `(1, 3)`: the second span starts at 1, at or before 2, and again `2 - 1 = 1`.

#### Solution

The code is the sort-and-sweep from the derivation, sharing the span scan with the union-find version.

```python
from typing import Dict, List, Tuple


class Solution:
    def solve(self, arr: List[int]) -> int:
        spans = self.occurrence_spans(arr)
        ordered_spans = sorted(spans.values())
        components = 1
        merged_end = ordered_spans[0][1]
        for span_start, span_end in ordered_spans[1:]:
            if span_start <= merged_end:
                merged_end = max(merged_end, span_end)
            else:
                components += 1
                merged_end = span_end
        return len(ordered_spans) - components

    def occurrence_spans(self, arr: List[int]) -> Dict[int, Tuple[int, int]]:
        spans: Dict[int, Tuple[int, int]] = {}
        for position, item in enumerate(arr):
            if item in spans:
                start, _ = spans[item]
                spans[item] = (start, position)
            else:
                spans[item] = (position, position)
        return spans
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + d log d)`

One scan builds the spans and sorting the `d` intervals dominates the linear sweep that follows.

##### Space Complexity: `O(d)`

The span dictionary and its sorted list.

#### Key Insights

- Overlapping intervals form connected components, and sorting by start turns component discovery into one growing-interval sweep.
- The sweep reaches the same count as the pairwise unions without building the conflict graph at all.
- Interval merging is the classic tool here, which is why the page reads as interval overlap in disguise: values are intervals, validity is disjointness.

## Comparison of Solutions

### Time Complexity

- **Brute Force with Recursive Search**: `O(d^3 × v^d)` - exponential exploration of replacement sequences, memoized on the array tuple.
- **Interval Overlap Union-Find**: `O(n + d^2 × α(d))` - one span scan plus pairwise overlap tests with near-constant unions.
- **Sorting by Span Start with Sweep Merging**: `O(n + d log d)` - the same spans, components found by one sorted sweep.

### Space Complexity

- **Brute Force with Recursive Search**: `O(v × v^d)` - the memo of reachable array tuples dominates.
- **Interval Overlap Union-Find**: `O(d)` - span dictionary and union-find arrays over values.
- **Sorting by Span Start with Sweep Merging**: `O(d)` - span dictionary plus the sorted interval list.

### Trade-offs

- **Brute Force with Recursive Search**: exact by construction and the easiest to trust, but unusable beyond a dozen or so distinct values.
- **Interval Overlap Union-Find**: turns validity into a static graph property with near-linear work; the pairwise test is the quadratic piece.
- **Sorting by Span Start with Sweep Merging**: the same answer with the graph skipped entirely; the only cost is trusting that overlap components are what merges buy.

### When to Use Each

- **Brute Force with Recursive Search**: tiny inputs or as the reference oracle when testing the faster approaches.
- **Interval Overlap Union-Find**: when the conflict structure itself matters (which value conflicts with which) or when the page's Union Find tag should be honored visibly.
- **Sorting by Span Start with Sweep Merging (Recommended)**: the interview answer at the stated constraints: linear scan, one sort over distinct values, and a sweep you can trace by hand.

### Optimization Notes

- Compressing `arr` to spans before any pair work shrinks the quadratic factor from positions to distinct values, which is what keeps the union-find version comfortable at `n = 1000`.
- The sweep needs no second comparison for ties: equal spans merge regardless of order, and `merged_end = max(merged_end, span_end)` absorbs nested intervals.
- In fixed-width languages, positions fit easily in 32 bits, so integer width is a non-issue here; the statement's int return needs no long.

