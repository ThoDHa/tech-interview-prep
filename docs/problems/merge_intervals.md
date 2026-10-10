# [Merge Intervals](https://leetcode.com/problems/merge-intervals/)

**Medium** | **30 minutes** | **Array, Sorting**

**Pattern:** [Interval](../patterns/interval/intuition.md)

**Algorithm:** [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Sweep line algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/merge_intervals/solution.py`](../../practice/merge_intervals/solution.py)

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the intervals in the input. Touching intervals such as `[1,4]` and `[4,5]` are considered overlapping. The answer may be returned in any order.

## Examples

### Example 1

**Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`

**Output:** `[[1,6],[8,10],[15,18]]`

**Explanation:** Intervals `[1,3]` and `[2,6]` overlap, so they merge into `[1,6]`.

### Example 2

**Input:** `intervals = [[1,4],[4,5]]`

**Output:** `[[1,5]]`

**Explanation:** Intervals `[1,4]` and `[4,5]` touch at `4`, so they merge into `[1,5]`.

## Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

## Deriving the Solution

Merging is a question of transitive overlap: `[1,3]` and `[2,6]` merge directly, and a chain of pairwise overlaps can pull intervals that never touch each other into one block. Every solution below is a strategy for finding those chains; they differ in how much order they impose on the input first.

1. **Start literal.** Repeatedly scan for any overlapping pair, fuse it, and
   restart, until a full pass finds nothing left to merge. Correct but `O(n^3)`: see [Brute Force](#brute-force).
2. **Name the structure.** The fuse-and-restart loop is implicitly computing
   connected components of an overlap graph. Building that graph explicitly and collapsing each component makes the transitivity visible, but still compares every pair: `O(n^2)`: see [Graph Connected Components](#graph-connected-components).
3. **Impose order.** Both slow approaches compare every pair because overlapping
   intervals can sit anywhere in the list. Sorting by start makes every mergeable group contiguous, so one linear pass with a single comparison per interval finishes in `O(n log n)`: see [Sort and Merge](#sort-and-merge).
4. **Sweep instead.** The same sort through a different lens: sort starts and
   ends separately and walk the number line counting how many intervals are open; a merged block ends exactly when the count returns to zero: see [Sweep Line](#sweep-line).

## Solutions

### Brute Force

#### Derivation

Without any sorting insight, the most direct idea is to keep fusing overlapping pairs until none remain. Two intervals overlap exactly when neither ends before the other begins, which is `a[0] <= b[1] and b[0] <= a[1]`:

1. Copy the intervals so the original input is not mutated.
2. Scan every pair `(i, j)`. The moment a pair overlaps, replace interval `i`
   with the union (`min` of starts, `max` of ends) and remove interval `j`.
3. Restart the scan after each merge, since the freshly grown interval may now
   overlap intervals it did not touch before.
4. Stop once a complete scan finds no overlapping pair; the remaining intervals
   are pairwise disjoint.

This needs no sort: it relies only on repeatedly applying the overlap test until the list stabilizes. Restarting after every merge is what makes it correct for chains where `A` overlaps `B` and `B` overlaps `C` but `A` and `C` do not.

#### Walkthrough

Trace the Brute Force on Example 1: `intervals = [[1,3],[2,6],[8,10],[15,18]]`. First the input is copied into `result`, then the outer `while` loop runs full pair scans until one finds nothing to merge.

**Pass 1.** Scan pairs `(i, j)` looking for the first overlap:

| `i` | `j` | `a = result[i]` | `b = result[j]` | overlap? `a[0] <= b[1] and b[0] <= a[1]` | Action |
|-----|-----|-----------------|-----------------|------------------------------------------|--------|
| `0` | `1` | `[1,3]` | `[2,6]` | `1 <= 6 and 2 <= 3` → `True` | Fuse: `a` becomes `[min(1,2), max(3,6)] = [1,6]`, then `pop(1)` removes `[2,6]` |

The moment that overlap fuses, both inner loops `break` and the pass restarts. After Pass 1, `result = [[1,6],[8,10],[15,18]]` and `merged_something = True`, so the `while` loop goes around again.

**Pass 2.** Now scan the shrunken list for any remaining overlap:

| `i` | `j` | `a = result[i]` | `b = result[j]` | overlap? | Action |
|-----|-----|-----------------|-----------------|----------|--------|
| `0` | `1` | `[1,6]` | `[8,10]` | `1 <= 10 and 8 <= 6` → `False` | none |
| `0` | `2` | `[1,6]` | `[15,18]` | `1 <= 18 and 15 <= 6` → `False` | none |
| `1` | `2` | `[8,10]` | `[15,18]` | `8 <= 18 and 15 <= 10` → `False` | none |

No pair overlaps, so `merged_something` stays `False` and the `while` loop exits.

The method returns `result = [[1,6],[8,10],[15,18]]`, which matches the example's expected Output `[[1,6],[8,10],[15,18]]`.

#### Solution

The code is the walkthrough's fuse-and-restart loop, with `merged_something` recording whether a pass changed anything.

```python
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Copy so the input is left untouched.
        result = [interval[:] for interval in intervals]

        # Repeatedly scan for any overlapping pair and fuse it, until a full
        # pass finds nothing left to merge.
        merged_something = True
        while merged_something:
            merged_something = False
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    a, b = result[i], result[j]
                    # Two intervals overlap (touching counts) when neither
                    # lies entirely to one side of the other.
                    if a[0] <= b[1] and b[0] <= a[1]:
                        a[0] = min(a[0], b[0])
                        a[1] = max(a[1], b[1])
                        result.pop(j)
                        merged_something = True
                        break
                if merged_something:
                    break

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

Each successful merge removes one interval, so there are at most `n - 1` merges. Every merge triggers a fresh `O(n^2)` pair scan from the top, giving `O(n^3)` in the worst case.

##### Space Complexity: `O(n)`

The `result` copy holds up to `n` intervals; no other storage grows with the input.

#### Key Insights

- Reduces merging to one primitive operation: find any overlapping pair and fuse
  it, then repeat.
- Restarting the scan after each merge handles transitive chains correctly,
  since a grown interval can absorb intervals it previously missed.
- Simple to reason about but wasteful: it rescans the whole list after every
  single merge, which the sorting approach eliminates entirely.

### Sort and Merge

#### Derivation

The Brute Force is slow for one reason: overlapping intervals can be arbitrarily far apart in the list, so it must keep comparing every pair. Sorting removes the scatter. After [sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) intervals by their start times, every group of intervals that should merge becomes a contiguous run, so a single linear pass suffices:

1. **Sort by start time.** Processing left to right then visits intervals in
   chronological order of their starts.
2. **Seed the result with the first interval.** It is guaranteed to appear in
   the output, possibly with an extended end.
3. **Scan and merge.** For each subsequent interval, compare its start against
   the end of the last interval in the result:
   - **Overlap** (`start <= last_end`): extend the last interval's end to
     `max(last_end, end)` so it absorbs the current one.
   - **Disjoint** (`start > last_end`): append the current interval as a new
     entry.

Because the list is sorted by start, the last appended interval always has the smallest end among the candidates we still need to compare against, so checking only against `merged[-1]` is sufficient. Touching intervals are handled by the `<=` comparison, which treats a shared endpoint as an overlap.

#### Overlap Condition

Two closed intervals intersect exactly when each starts no later than the other ends:

$$ [a_1, b_1] \cap [a_2, b_2] \ne \emptyset \iff \max(a_1, a_2) \le \min(b_1, b_2) $$

```text
[a1, b1] intersect [a2, b2] is non-empty
    if and only if  max(a1, a2) <= min(b1, b2)
```

and their union, when they do intersect, is:

$$ [a_1, b_1] \cup [a_2, b_2] = \bigl[\min(a_1, a_2),\ \max(b_1, b_2)\bigr] $$

```text
[a1, b1] union [a2, b2] = [min(a1, a2), max(b1, b2)]
    when the two intervals intersect
```

Sorting by start collapses the symmetric test into a one-sided one. With \(a_1 \le a_2\) guaranteed, \(\max(a_1, a_2) = a_2\), so the condition reduces to `start <= last[1]`: a single comparison against the running end. That is the entire payoff of the sort.

The `<=` treats touching intervals such as \([1,5]\) and \([5,8]\) as overlapping, merging them to \([1,8]\); using `<` would emit them separately. The `max` in the merge is not redundant either: sorted starts do **not** imply sorted ends, so a fully nested interval like \([1,10]\) followed by \([2,3]\) must not shrink the running end.

#### Walkthrough

Trace the pass on Example 1: `intervals = [[1,3],[2,6],[8,10],[15,18]]`. The sort runs first; here the starts `1, 2, 8, 15` already ascend, so it leaves the order unchanged and its work is invisible on this input. `merged` is then seeded with the first interval, and each later interval makes one overlap-or-append decision against `merged[-1]`:

```text
sort             intervals = [[1,3],[2,6],[8,10],[15,18]]   starts already ascend
seed             merged = [[1,3]]
(2,6)    2 <= 3    overlap: last[1] = max(3, 6) = 6     merged = [[1,6]]
(8,10)   8 >  6    disjoint: append [8,10]              merged = [[1,6],[8,10]]
(15,18)  15 > 10   disjoint: append [15,18]             merged = [[1,6],[8,10],[15,18]]
```

The one merge extends the running end in place: `[1,3]` absorbs `[2,6]` by raising `last[1]` to `max(3, 6) = 6`. On Example 2 the same rule handles touching: `[4,5]` starts exactly at the running end `4`, the `<=` test counts that as overlap, and the result is `[[1,5]]`.

The pass returns `merged = [[1,6],[8,10],[15,18]]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's pass: sort, seed `merged`, then one overlap-or-append decision per interval.

```python
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        # Sort by start time so overlapping intervals become adjacent.
        intervals.sort(key=lambda interval: interval[0])

        merged = [intervals[0]]
        for start, end in intervals[1:]:
            last = merged[-1]
            if start <= last[1]:
                # Overlap: extend the current interval's end.
                last[1] = max(last[1], end)
            else:
                # Disjoint: start a fresh interval.
                merged.append([start, end])

        return merged
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the `n` intervals by start time dominates at `O(n log n)`. The single merge pass over the sorted intervals adds `O(n)`, so the total is `O(n log n)`.

##### Space Complexity: `O(n)`

The output list holds up to `n` intervals when none overlap. Sorting adds `O(log n)` to `O(n)` auxiliary space depending on the implementation, which the output term dominates.

#### Key Insights

- Sorting by start time is what reduces an apparently pairwise problem to a
  single linear sweep.
- Comparing only against `merged[-1]` is correct precisely because the sort
  guarantees its end is the relevant boundary for the next interval.
- The `<=` overlap test folds the touching-endpoints rule into the same branch,
  so no special case is needed.

### Sweep Line

#### Derivation

Sort and Merge keeps each interval whole. Ask instead what happens on the number line itself: moving left to right, an interval opens at its start and closes at its end, and a merged block is exactly a maximal stretch where at least one interval is open. Decouple the endpoints and [sweep a vertical line](https://en.wikipedia.org/wiki/Sweep_line_algorithm) across the number line, tracking how many intervals are currently open:

1. **Separate and sort endpoints.** Collect all starts and all ends into two
   independently sorted arrays.
2. **Sweep with a depth counter.** Walk the two arrays with pointers `s` and
   `e`. A start at or before the current end opens an interval (`depth += 1`); a start after the current end means the current interval must close (`depth -= 1`).
3. **Close clusters at depth zero.** Each time `depth` falls back to `0`, the
   current overlapping cluster is complete, spanning from the cluster's first start to the closing end. Record it and begin the next cluster at the next pending start.
4. **Flush the final cluster** after the loop, which closes against the largest
   end.

The `<=` comparison again treats touching intervals as overlapping, keeping the depth nonzero across a shared endpoint.

#### Walkthrough

Trace the sweep on Example 1: `intervals = [[1,3],[2,6],[8,10],[15,18]]`. The endpoints are pulled apart and sorted independently, then each loop iteration compares the next pending start against the next pending end:

```text
starts = [1, 2, 8, 15]    ends = [3, 6, 10, 18]    cluster_start = 1

starts[0]=1  <= ends[0]=3    open    depth 0 -> 1
starts[1]=2  <= ends[0]=3    open    depth 1 -> 2
starts[2]=8  >  ends[0]=3    close   depth 2 -> 1
starts[2]=8  >  ends[1]=6    close   depth 1 -> 0   emit [1,6];  cluster_start = 8
starts[2]=8  <= ends[2]=10   open    depth 0 -> 1
starts[3]=15 >  ends[2]=10   close   depth 1 -> 0   emit [8,10]; cluster_start = 15
starts[3]=15 <= ends[3]=18   open    depth 0 -> 1
s == n, loop ends            flush [cluster_start, ends[-1]] = [15, 18]
```

The first cluster shows the depth logic: `[1,3]` and `[2,6]` are both open at depth `2`, and only when both have closed (`depth` back to `0` at end `6`) is `[1,6]` emitted. The loop consumes starts only, so the final cluster is still open when `s` reaches `n`; the flush closes it against the largest end, `18`.

The sweep returns `merged = [[1,6],[8,10],[15,18]]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's event loop: compare `starts[s]` against `ends[e]`, adjust `depth`, and emit a cluster whenever it returns to zero.

```python
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        starts = sorted(interval[0] for interval in intervals)
        ends = sorted(interval[1] for interval in intervals)

        merged: List[List[int]] = []
        depth = 0
        s = e = 0
        n = len(intervals)
        cluster_start = starts[0]

        while s < n:
            if starts[s] <= ends[e]:
                # A new interval opens before the current cluster closes.
                depth += 1
                s += 1
            else:
                # An interval closes; the cluster ends when depth returns to 0.
                depth -= 1
                if depth == 0:
                    merged.append([cluster_start, ends[e]])
                    if s < n:
                        cluster_start = starts[s]
                e += 1

        # The final cluster closes against the largest end.
        merged.append([cluster_start, ends[-1]])
        return merged
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Building the two endpoint arrays is `O(n)`, and sorting them is `O(n log n)`, which dominates. The sweep advances each pointer at most `n` times for `O(n)`.

##### Space Complexity: `O(n)`

The two endpoint arrays and the output each use `O(n)` space.

#### Key Insights

- Splitting intervals into independent start and end streams reframes merging as
  a balanced-parentheses depth problem.
- The cluster boundary is exactly the moment `depth` returns to zero, which makes
  the merge condition explicit rather than implicit in a comparison against the previous result.
- This view generalizes naturally to related problems such as counting maximum
  concurrent intervals, where the depth counter is the answer.

### Graph Connected Components

#### Derivation

The Brute Force handles transitive chains implicitly, by restarting its scan after every merge. Making the transitivity explicit gives a cleaner model: treat overlap as a graph relation and merge by finding connected components:

1. **Build the overlap graph.** Add an undirected edge between every pair of
   intervals that overlap, where `overlaps(a, b)` is `a[0] <= b[1] and b[0] <= a[1]`.
2. **Find connected components.** Run [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) from each unvisited
   node to collect every interval reachable through a chain of overlaps.
3. **Collapse each component.** A component must merge into a single interval
   spanning from its minimum start to its maximum end, since overlap is transitive within the component.

This approach needs no sort and makes the transitive nature of merging explicit: two intervals that do not overlap directly still merge when a chain connects them.

#### Walkthrough

Trace the three phases on Example 1: `intervals = [[1,3],[2,6],[8,10],[15,18]]`. The pair scan tests all six pairs with `overlaps(a, b)`:

```text
(0,1)  [1,3]  vs [2,6]     1 <= 6  and 2 <= 3    -> edge 0-1
(0,2)  [1,3]  vs [8,10]    8 <= 3  fails          no edge
(0,3)  [1,3]  vs [15,18]   15 <= 3 fails          no edge
(1,2)  [2,6]  vs [8,10]    8 <= 6  fails          no edge
(1,3)  [2,6]  vs [15,18]   15 <= 6 fails          no edge
(2,3)  [8,10] vs [15,18]   15 <= 10 fails         no edge

graph = [[1], [0], [], []]
```

The main loop then runs `dfs` from each unvisited node and collapses each component to its extreme endpoints:

```text
i=0  dfs: stack [0] -> visit 0, push 1 -> visit 1    component = [0, 1]
     lo = min(1, 2) = 1   hi = max(3, 6) = 6         result = [[1,6]]
i=1  already visited, skipped
i=2  dfs: component = [2]  lo = 8,  hi = 10          result = [[1,6],[8,10]]
i=3  dfs: component = [3]  lo = 15, hi = 18          result = [[1,6],[8,10],[15,18]]
```

The single edge `0-1` chains `[1,3]` and `[2,6]` into one component, and the min/max collapse produces `[1,6]`; the two isolated nodes pass through as themselves. The method returns `result = [[1,6],[8,10],[15,18]]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough in three phases: the pair scan that builds `graph`, the stack-based `dfs`, and the min/max collapse per component.

```python
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        n = len(intervals)

        def overlaps(a: List[int], b: List[int]) -> bool:
            return a[0] <= b[1] and b[0] <= a[1]

        # Build an overlap graph: an edge connects every overlapping pair.
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if overlaps(intervals[i], intervals[j]):
                    graph[i].append(j)
                    graph[j].append(i)

        visited = [False] * n
        result: List[List[int]] = []

        def dfs(node: int, component: List[int]) -> None:
            stack = [node]
            while stack:
                current = stack.pop()
                if visited[current]:
                    continue
                visited[current] = True
                component.append(current)
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append(neighbor)

        for i in range(n):
            if not visited[i]:
                component: List[int] = []
                dfs(i, component)
                lo = min(intervals[index][0] for index in component)
                hi = max(intervals[index][1] for index in component)
                result.append([lo, hi])

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Building the overlap graph compares all `O(n^2)` pairs. The depth-first search visits each node and edge once, which is bounded by the `O(n^2)` edges in the worst case, so the total remains `O(n^2)`.

##### Space Complexity: `O(n^2)`

The adjacency list can store up to `O(n^2)` edges when many intervals mutually overlap. The visited array, recursion-free stack, and output add `O(n)`.

#### Key Insights

- Merging is fundamentally about transitive overlap, which the connected-
  components framing captures directly.
- An explicit stack avoids Python recursion-depth limits on long overlap chains.
- The quadratic pair scan makes this the least efficient option, but it
  illustrates the structural reason intervals merge and adapts cleanly when the overlap relation is more complex than a simple endpoint comparison.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^3)` - up to `n` merges, each restarting an `O(n^2)` pair
  scan.
- **Sort and Merge**: `O(n log n)` - one sort plus a linear merge pass.
- **Sweep Line**: `O(n log n)` - two endpoint sorts plus a linear sweep.
- **Graph Connected Components**: `O(n^2)` - compares every pair to build edges.

### Space Complexity

- **Brute Force**: `O(n)` - a working copy of the intervals.
- **Sort and Merge**: `O(n)` - the output list, with `O(log n)` to `O(n)` for
  sorting.
- **Sweep Line**: `O(n)` - two endpoint arrays plus the output.
- **Graph Connected Components**: `O(n^2)` - the adjacency list of overlap edges.

### Trade-offs

- **Brute Force** gains a sort-free, easily derivable model (fuse any overlapping
  pair, repeat) but gives up efficiency by rescanning the list after every merge.
- **Sort and Merge** is the most direct of the fast solutions and the easiest to
  get right; it gives up nothing meaningful and is the default choice.
- **Sweep Line** matches the asymptotics while exposing interval depth, which is
  reusable for concurrency-style variants, at the cost of more bookkeeping.
- **Graph Connected Components** trades efficiency for an explicit model of
  transitive overlap, which is valuable mainly as a conceptual stepping stone.

### When to Use Each

- **Brute Force**: As a teaching baseline or when sorting is somehow unavailable;
  too slow for the upper constraint of `10^4` intervals.
- **Sort and Merge**: The default for this problem and almost every interview
  setting (recommended).
- **Sweep Line**: When the same input must also answer depth or concurrency
  questions, so the endpoint sweep does double duty.
- **Graph Connected Components**: When teaching or reasoning about the transitive
  structure of overlap, not for performance.

### Optimization Notes

- Sorting is what collapses the Brute Force's repeated pair scans into a single
  linear pass: once starts are ordered, overlaps become adjacent.
- The Sort and Merge pass mutates `merged[-1]` in place to extend the end, which
  avoids allocating a new interval per merge.
- The Sweep Line keeps starts and ends in separate sorted arrays so each pointer
  advances monotonically, guaranteeing the linear sweep.
- The Graph approach uses an explicit stack rather than recursion to stay safe on
  long overlap chains that would otherwise risk a stack overflow.
