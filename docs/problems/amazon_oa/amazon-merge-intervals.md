# [Merge Intervals](https://www.fastprep.io/problems/amazon-merge-intervals)

**Easy** | **NN minutes** | **Intervals, Sorting**

Given an array of closed intervals where intervals[i] = [start_i, end_i], merge every pair of overlapping intervals.

Return the non-overlapping intervals that cover every interval in the input, sorted by start time. Intervals that share an endpoint are considered overlapping.

## Examples

### Example 1

**Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`

**Output:** `[[1,6],[8,10],[15,18]]`

**Explanation:** Intervals [1,3] and [2,6] overlap, so they merge into [1,6].

### Example 2

**Input:** `intervals = [[1,4],[4,5]]`

**Output:** `[[1,5]]`

**Explanation:** The intervals share endpoint 4, so they merge into [1,5].

### Example 3

**Input:** `intervals = [[8,10],[1,4],[2,3],[15,18],[6,9],[3,7],[17,20],[12,12]]`

**Output:** `[[1,10],[12,12],[15,20]]`

**Explanation:** The intervals are intentionally unsorted. After sorting by start time, [1,4], [2,3], [3,7], [6,9], and [8,10] form one connected overlap chain and merge into [1,10]. Interval [12,12] remains separate, while [15,18] and [17,20] merge into [15,20].

## Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

## Solutions

### Brute Force

#### Derivation

The most literal reading of merging is to keep fusing pairs until nothing merges anymore: find any two intervals that overlap, replace them with their union, and restart the scan, because the freshly grown interval may now reach intervals it did not touch before. Two closed intervals overlap exactly when neither lies entirely to one side of the other, which is `first[0] <= second[1] and second[0] <= first[1]`. Restarting after every merge is what makes the transitive chains come out right, where `A` overlaps `B` and `B` overlaps `C` but `A` and `C` never touch:

1. Copy the input into `result` so the caller's list is left untouched.
2. Scan every pair `(first_idx, second_idx)` with `second_idx > first_idx`.
3. On the first overlapping pair, fuse it: `result[first_idx]` becomes
   `[min(first[0], second[0]), max(first[1], second[1])]`, `result.pop(second_idx)`, and the scan restarts from the top.
4. When a complete pass finds no overlapping pair, the intervals are pairwise
   disjoint; a final `result.sort` by start meets the output contract, which
   fusing alone does not (a fuse keeps its slot, so surviving intervals sit in
   scan order, not start order).

#### Walkthrough

Trace the fuse-and-restart loop on Example 1: `intervals = [[1,3],[2,6],[8,10],[15,18]]`. The copy leaves `result` in the input order, and the scan looks for the first overlapping pair:

```text
pass 1   (0,1)  [1,3] vs [2,6]    1 <= 6 and 2 <= 3 -> overlap
                fuse: [min(1,2), max(3,6)] = [1,6], pop [2,6], restart
         result = [[1,6],[8,10],[15,18]]
pass 2   (0,1)  [1,6] vs [8,10]   8 <= 6 fails          -> no overlap
         (0,2)  [1,6] vs [15,18]  15 <= 6 fails         -> no overlap
         (1,2)  [8,10] vs [15,18] 15 <= 10 fails        -> no overlap
         nothing merged: stop
```

Pass 2 is the transitivity check in miniature: the grown interval `[1,6]` is tested against the untouched tail and found disjoint, so the loop exits with `result = [[1,6],[8,10],[15,18]]`, matching the expected Output. (Example 2 needs the same single fuse, with the touching test `1 <= 5 and 4 <= 4` firing on the shared endpoint `4`.)

#### Solution

The code is the walkthrough's loop: scan, fuse the first overlap, restart, until a pass changes nothing.

```python
from typing import List


class Solution:
    def solve(self, intervals: List[List[int]]) -> List[List[int]]:
        result = [interval[:] for interval in intervals]

        merged_something = True
        while merged_something:
            merged_something = False
            for first_idx in range(len(result)):
                for second_idx in range(first_idx + 1, len(result)):
                    first, second = result[first_idx], result[second_idx]
                    if first[0] <= second[1] and second[0] <= first[1]:
                        first[0] = min(first[0], second[0])
                        first[1] = max(first[1], second[1])
                        result.pop(second_idx)
                        merged_something = True
                        break
                if merged_something:
                    break

        result.sort(key=lambda interval: interval[0])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

Each merge removes one interval, so there are at most `n - 1` merges, and every merge restarts an `O(n^2)` pair scan from the top. The final start-sort adds `O(n log n)`, which the scan loop dwarfs.

##### Space Complexity: `O(n)`

The `result` copy holds up to `n` intervals; no other storage grows with the input.

#### Key Insights

- Merging rests on one primitive, the pairwise overlap test, applied repeatedly; everything else is bookkeeping for transitivity.
- Restarting the scan after each fuse is the price of not imposing any order on the input, and it is what makes chains like `[2,3]`, `[3,7]`, `[6,9]` collapse correctly.
- The `<=` comparisons fold the shared-endpoint rule into the same test: `[1,4]` and `[4,5]` overlap because `4 <= 4`.

### Sort and Merge

#### Derivation

The Brute Force compares every pair because overlapping intervals can sit anywhere in the list. Sorting removes the scatter: once the intervals are ordered by start time, every group that should merge becomes a contiguous run, so one linear pass with a single comparison per interval suffices:

1. Sort the intervals by start time; `sorted` returns a new list, so the caller's order is untouched.
2. Seed `merged` with a copy of the first interval; it is guaranteed to appear in the output, possibly with an extended end.
3. For each later interval, compare its `start` against the end of the last interval in `merged`:
   - Overlap (`start <= last[1]`): extend `last[1]` to `max(last[1], end)`.
   - Disjoint (`start > last[1]`): append the interval as a new entry.

The `max` in the merge is not decoration: sorted starts do not imply sorted ends, so a fully nested interval like `[1,10]` followed by `[2,3]` must not shrink the running end.

#### Overlap Condition

Two closed intervals intersect exactly when each starts no later than the other ends:

$$ [a_1, b_1] \cap [a_2, b_2] \ne \emptyset \iff \max(a_1, a_2) \le \min(b_1, b_2) $$

```text
[a1, b1] intersect [a2, b2] is non-empty
    if and only if  max(a1, a2) <= min(b1, b2)
```

Sorting by start collapses the symmetric test into a one-sided one. With `a1 <= a2` guaranteed, `max(a1, a2) = a2`, so the condition reduces to `start <= last[1]`, a single comparison against the running end. The `<=` treats touching intervals such as `[1,4]` and `[4,5]` as overlapping; using `<` would emit them separately.

#### Walkthrough

Example 3 is the input where the sort does visible work: `intervals = [[8,10],[1,4],[2,3],[15,18],[6,9],[3,7],[17,20],[12,12]]`. Sorting by start produces `[1,4],[2,3],[3,7],[6,9],[8,10],[12,12],[15,18],[17,20]`, and the pass then walks it with one overlap-or-append decision per interval:

```text
seed      merged = [[1,4]]
(2,3)     2 <= 4    overlap: last[1] = max(4, 3) = 4    merged = [[1,4]]
(3,7)     3 <= 4    overlap: last[1] = max(4, 7) = 7    merged = [[1,7]]
(6,9)     6 <= 7    overlap: last[1] = max(7, 9) = 9    merged = [[1,9]]
(8,10)    8 <= 9    overlap: last[1] = max(9, 10) = 10  merged = [[1,10]]
(12,12)   12 > 10   disjoint: append                    merged = [[1,10],[12,12]]
(15,18)   15 > 12   disjoint: append                    merged = [[1,10],[12,12],[15,18]]
(17,20)   17 <= 18  overlap: last[1] = max(18, 20) = 20 merged = [[1,10],[12,12],[15,20]]
```

The chain `[1,4],[2,3],[3,7],[6,9],[8,10]` never pairwise overlaps as input, yet the running end absorbs all five of them; `(12,12)` is the degenerate zero-length interval and passes through intact. The final `merged = [[1,10],[12,12],[15,20]]` matches the expected Output for Example 3. (Examples 1 and 2 run the same pass; Example 2 turns on `4 <= 4`, the shared endpoint.)

#### Solution

The code is the walkthrough's pass: sort by start, seed `merged`, then one overlap-or-append decision per interval.

```python
from typing import List


class Solution:
    def solve(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals_sorted = sorted(intervals, key=lambda interval: interval[0])

        merged: List[List[int]] = [list(intervals_sorted[0])]
        for start, end in intervals_sorted[1:]:
            last = merged[-1]
            if start <= last[1]:
                last[1] = max(last[1], end)
            else:
                merged.append([start, end])

        return merged
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the `n` intervals by start dominates; the merge pass that follows is a single `O(n)` sweep.

##### Space Complexity: `O(n)`

The sorted copy and the output list each hold up to `n` intervals; sorting adds `O(log n)` to `O(n)` auxiliary space depending on the implementation.

#### Key Insights

- Sorting by start is what reduces an apparently pairwise problem to a linear sweep: every mergeable group becomes contiguous.
- Comparing only against `merged[-1]` is correct precisely because the sort guarantees its end is the only boundary the next interval can violate.
- The `max` keeps a nested interval from shrinking the running end, and the `<=` folds the touching-endpoints rule into the same branch, so no special case is needed.

### Sweep Line

#### Derivation

Sort and Merge keeps each interval whole. Ask instead what happens on the number line itself: moving left to right, an interval opens at its start and closes at its end, and a merged block is exactly a maximal stretch where at least one interval is open. [Sweep a vertical line](https://en.wikipedia.org/wiki/Sweep_line_algorithm) across the number line, tracking how many intervals `depth` are currently open:

1. Collect all starts and all ends into two independently sorted arrays, `starts` and `ends`.
2. Walk the two arrays with pointers `start_idx` and `end_idx`: a start at or before the current end opens an interval (`depth += 1`); a start after the current end means some interval closes (`depth -= 1`).
3. Each time `depth` falls back to `0`, the current overlapping cluster is complete, spanning from `cluster_start` to the end that just closed. Record it and move `cluster_start` to the next pending start.
4. Flush the final cluster after the loop, which closes against the largest end, `ends[-1]`.

The `<=` comparison again keeps the depth nonzero across a shared endpoint, so touching intervals stay in one cluster.

#### Walkthrough

Run the sweep on Example 3, the same input the Sort and Merge walkthrough used, so the two lenses can be compared directly. The endpoints separate into `starts = [1, 2, 3, 6, 8, 12, 15, 17]` and `ends = [3, 4, 7, 9, 10, 12, 18, 20]`, with `cluster_start = 1`:

```text
starts[0]=1  <= ends[0]=3    open    depth 0 -> 1
starts[1]=2  <= ends[0]=3    open    depth 1 -> 2
starts[2]=3  <= ends[0]=3    open    depth 2 -> 3   shared endpoint, still open
starts[3]=6  >  ends[0]=3    close   depth 3 -> 2
             >  ends[1]=4    close   depth 2 -> 1
             <= ends[2]=7    open    depth 1 -> 2
starts[4]=8  >  ends[2]=7    close   depth 2 -> 1
             <= ends[3]=9    open    depth 1 -> 2
starts[5]=12 >  ends[3]=9    close   depth 2 -> 1
             >  ends[4]=10   close   depth 1 -> 0   emit [1, 10]; cluster_start = 12
starts[5]=12 <= ends[5]=12   open    depth 0 -> 1   shared endpoint, still open
starts[6]=15 >  ends[5]=12   close   depth 1 -> 0   emit [12, 12]; cluster_start = 15
starts[6]=15 <= ends[6]=18   open    depth 0 -> 1
starts[7]=17 <= ends[6]=18   open    depth 1 -> 2
s == 8, loop ends            flush [cluster_start, ends[-1]] = [15, 20]
```

The depth is the concurrency the single-pass view hides: the chain of five never sits open all at once, but the sweep depth peaks at `3` around time `3`, where `[1,4]`, `[2,3]`, and `[3,7]` meet at the shared endpoint, and the cluster `[1,10]` ends exactly when the last of them closes. The two `<=` events at `3` and `12` are the touching cases keeping clusters alive. The sweep returns `[[1,10],[12,12],[15,20]]`, matching the expected Output for Example 3.

#### Solution

The code is the walkthrough's event loop: compare `starts[start_idx]` against `ends[end_idx]`, adjust `depth`, and emit a cluster whenever it returns to zero.

```python
from typing import List


class Solution:
    def solve(self, intervals: List[List[int]]) -> List[List[int]]:
        starts = sorted(interval[0] for interval in intervals)
        ends = sorted(interval[1] for interval in intervals)

        merged: List[List[int]] = []
        depth = 0
        start_idx = 0
        end_idx = 0
        interval_count = len(intervals)
        cluster_start = starts[0]

        while start_idx < interval_count:
            if starts[start_idx] <= ends[end_idx]:
                depth += 1
                start_idx += 1
            else:
                depth -= 1
                if depth == 0:
                    merged.append([cluster_start, ends[end_idx]])
                    cluster_start = starts[start_idx]
                end_idx += 1

        merged.append([cluster_start, ends[-1]])
        return merged
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the two endpoint arrays dominates; the sweep advances `start_idx` and `end_idx` monotonically, so the walk itself is `O(n)`.

##### Space Complexity: `O(n)`

The two endpoint arrays and the output each use `O(n)` space.

#### Key Insights

- Splitting intervals into independent start and end streams reframes merging as a balanced-parentheses depth problem: a cluster is one matched region.
- The cluster boundary is exactly the moment `depth` returns to zero, which makes the merge condition explicit rather than implicit in a comparison against the previous result.
- This view answers concurrency questions ("how many intervals are open at once?") for free, which is why it generalizes to variants like counting the maximum overlapping intervals.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^3)` - up to `n` merges, each restarting an `O(n^2)` pair scan.
- **Sort and Merge**: `O(n log n)` - one sort plus a linear merge pass.
- **Sweep Line**: `O(n log n)` - two endpoint sorts plus a linear sweep.

### Space Complexity

- **Brute Force**: `O(n)` - a working copy of the intervals.
- **Sort and Merge**: `O(n)` - the sorted copy plus the output.
- **Sweep Line**: `O(n)` - two endpoint arrays plus the output.

### Trade-offs

- **Brute Force** needs no ordering insight and reads directly off the definition of merging, but rescanning the list after every merge makes it the slowest by a wide margin.
- **Sort and Merge** is the shortest fast solution and the easiest to get right; it gives up nothing meaningful and is the default choice.
- **Sweep Line** matches the asymptotics while exposing interval depth, which doubles as machinery for concurrency questions, at the cost of more bookkeeping.

### When to Use Each

- **Brute Force**: as a correctness cross-check or when the overlap relation is too complex for endpoint sorting to order.
- **Sort and Merge (Recommended)**: the interview default: optimal, five lines of logic, and the sort does all the structural work.
- **Sweep Line**: when the same input must also answer depth or concurrency questions, or when the next follow-up is "how many intervals overlap at the busiest moment".

### Optimization Notes

- Both fast approaches pay one `O(n log n)` sort and then work linearly; choosing between them is about what else the sweep must answer, not about speed.
- The Sort and Merge pass extends `merged[-1]` in place instead of allocating a new interval per merge, and it copies the rows it seeds from so the caller's input stays untouched.
- A common pitfall in the merge pass is dropping the `max`: sorted starts do not sort ends, so `last[1] = max(last[1], end)` is what protects a nested interval like `[2,3]` from shrinking a running end of `10`.
- In the Sweep Line, the emit branch can move `cluster_start` to `starts[start_idx]` unconditionally, because the loop only runs while a start remains pending; that start is exactly where the next cluster begins.
