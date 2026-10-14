# [Insert Interval](https://leetcode.com/problems/insert-interval/)

**Medium** | **25 minutes** | **Array**

**Pattern:** [Interval](../patterns/interval/intuition.md)

**Algorithm:** [Interval pattern](../patterns/interval/intuition.md) · [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/insert_interval/solution.py`](../../practice/insert_interval/solution.py)

You are given an array of non-overlapping intervals where `intervals[i] = [starti, endi]` represent the start and the end of the `ith` interval and `intervals` is sorted in ascending order by `starti`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.

Insert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `starti` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return `intervals` after the insertion.

## Examples

### Example 1

**Input:** `intervals = [[1,3],[6,9]]`, `newInterval = [2,5]`

**Output:** `[[1,5],[6,9]]`

### Example 2

**Input:** `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`

**Output:** `[[1,2],[3,10],[12,16]]`

**Explanation:** Because the new interval `[4,8]` overlaps with `[3,5]`, `[6,7]`, `[8,10]`.

### Example 3

**Input:** `intervals = []`, `newInterval = [5,7]`

**Output:** `[[5,7]]`

## Constraints

- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= starti <= endi <= 10^5`
- `intervals` is sorted by `starti` in ascending order.
- `newInterval.length == 2`
- `0 <= start <= end <= 10^5`

## Deriving the Solution

The problem's gift is stated in the constraints: `intervals` is already sorted by start and non-overlapping. That guarantees the intervals touching `newInterval` form one contiguous block, splitting the list into three contiguous regions: strictly before, overlapping, and strictly after. Every solution below locates that block and collapses it to `[min start, max end]`. None of them sorts: appending `newInterval` and re-sorting would throw away exactly the structure the problem hands us.

1. **Start literal.** Walk the sorted list once with one loop per region: copy the
   intervals ending before `newInterval`, absorb the overlapping block via `min` and `max`, copy the rest. A single `O(n)` pass, which is already optimal for rebuilding the list: see [Linear Scan and Merge](#linear-scan-and-merge).
2. **Reduce to a known problem.** Alternatively, splice `newInterval` into its
   sorted slot (a linear scan, since the list is sorted) and run the standard Merge Intervals sweep over the combined list. Same `O(n)`, familiar shape, but it re-examines intervals the direct walk would copy untouched: see [Insert and Merge](#insert-and-merge).
3. **Trade time for space.** Both passes build a new output list. Mutating the
   input in place drops the auxiliary space to `O(1)`, but every `pop(i)` shifts the tail of the list, degrading the worst case to `O(n²)`: see [In-Place Modification](#in-place-modification).
4. **Cut the comparisons.** Sortedness plus disjointness make the starts *and* the
   ends monotone, so two boundary binary searches can locate the overlap window in `O(log n)` comparisons; rebuilding the answer still costs `O(n)` of copying: see [Binary Search for the Overlap Window](#binary-search-for-the-overlap-window).
5. **Fold it recursively.** The same three cases (before, after, overlap) can be
   applied one interval at a time, peeling the head of the list per recursive call: elegant, but slicing makes it quadratic: see [Recursive Merge](#recursive-merge).
6. **Let the library run the searches.** Those two boundary searches are the
   textbook leftmost and rightmost flavors, and `bisect` ships both. Handing them over deletes twelve lines of `lo`/`hi` loops, including the `(lo + hi + 1) // 2` midpoint that is easy to get wrong, while the three-piece reassembly stays exactly as it was: see [Binary Search with bisect](#binary-search-with-bisect).

## Solutions

### Linear Scan and Merge

#### Derivation

Take the sortedness seriously and ask what `newInterval` does to the list: it splits the intervals into the ones entirely before it, the ones it overlaps, and the ones entirely after it. Because the input is sorted and disjoint, those three groups are contiguous runs, in that order, so a single left-to-right walk with one `while` loop per region handles everything. The before and after runs are copied unchanged; the overlapping run collapses into `newInterval` by widening it with `min` of the starts and `max` of the ends. The [Overlap Condition](#overlap-condition) below justifies why one boundary test per loop is enough. The steps:

1. Copy every interval that ends strictly before `newInterval` starts
   (`intervals[i][1] < newInterval[0]`) into `merged`; these are untouched.
2. Absorb every interval that overlaps `newInterval`
   (`intervals[i][0] <= newInterval[1]`), growing `newInterval` via `min` of starts and `max` of ends, then append the grown interval once.
3. Copy every remaining interval; all of them start strictly after `newInterval`
   ends.

The touching condition uses `<=` so intervals that share an endpoint, such as `[1,5]` and `[5,8]`, merge into `[1,8]`. No sort is needed because the input is already ordered.

#### Overlap Condition

Interval \(i\) overlaps the new interval \([s, e]\) exactly when:

$$ \max(a_i, s) \le \min(b_i, e) $$

```text
intervals[i] overlaps newInterval  if and only if
    max(intervals[i][0], newInterval[0]) <= min(intervals[i][1], newInterval[1])
```

Because the input is sorted by start and never overlaps itself, that single condition partitions the list into three contiguous runs, which is precisely the three `while` loops:

$$ \underbrace{b_i < s}_{\text{strictly before}} \qquad \underbrace{a_i \le e \ \wedge \ b_i \ge s}_{\text{overlapping}} \qquad \underbrace{a_i > e}_{\text{strictly after}} $$

```text
strictly before: intervals[i][1] <  newInterval[0]
overlapping:     intervals[i][0] <= newInterval[1]
                 and intervals[i][1] >= newInterval[0]
strictly after:  intervals[i][0] >  newInterval[1]
```

Each loop tests only the one side that can still change, since the previous loop has already established the other. The middle run absorbs into a single interval:

$$ \Bigl[\ \min\bigl(s,\ \min_i a_i\bigr),\ \ \max\bigl(e,\ \max_i b_i\bigr)\ \Bigr] $$

```text
newInterval = [min(newInterval[0], min of intervals[i][0]),
               max(newInterval[1], max of intervals[i][1])]
              (min and max taken over the overlapping run only)
```

The runs are contiguous only because the input is disjoint and sorted; that is what makes one pass sufficient and why no sort is needed here, unlike in Merge Intervals. Both boundary tests use non-strict comparison, so touching intervals merge rather than staying separate.

#### Walkthrough

Let us watch the Linear Scan and Merge run on Example 1: `intervals = [[1,3],[6,9]]`, `newInterval = [2,5]`. The expected output is `[[1,5],[6,9]]`.

We start with `merged = []`, `i = 0`, and `n = 2`. The trace below shows which of the three loops fires at each step and what changes.

| Step | Loop | Interval at `i` | Condition checked | Action | `newInterval` | `i` | `merged` |
|------|------|-----------------|-------------------|--------|---------------|-----|----------|
| 1 | loop 1 (before) | `[1,3]` | `intervals[0][1] < newInterval[0]`: `3 < 2`? No | loop 1 stops, no append | `[2,5]` | `0` | `[]` |
| 2 | loop 2 (overlap) | `[1,3]` | `intervals[0][0] <= newInterval[1]`: `1 <= 5`? Yes | absorb: start `min(2,1)=1`, end `max(5,3)=5` | `[1,5]` | `1` | `[]` |
| 3 | loop 2 (overlap) | `[6,9]` | `intervals[1][0] <= newInterval[1]`: `6 <= 5`? No | loop 2 stops | `[1,5]` | `1` | `[]` |
| 4 | append | : | : | append grown `newInterval` | `[1,5]` | `1` | `[[1,5]]` |
| 5 | loop 3 (after) | `[6,9]` | `i < n`: `1 < 2`? Yes | append `[6,9]`, advance `i` | `[1,5]` | `2` | `[[1,5],[6,9]]` |

Loop 3's condition `i < n` is now `2 < 2`, which is false, so the loop ends. The function returns `merged = [[1,5],[6,9]]`, which matches the expected Output `[[1,5],[6,9]]`.

#### Solution

The code is the three loops from the walkthrough: copy, absorb, copy.

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        merged = []
        i, n = 0, len(intervals)
        # Add all intervals that end before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            merged.append(intervals[i])
            i += 1
        # Absorb every interval that overlaps newInterval
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        merged.append(newInterval)
        # Add all intervals that start after newInterval ends
        while i < n:
            merged.append(intervals[i])
            i += 1
        return merged
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each interval is examined by exactly one of the three loops, so the total work is linear.

##### Space Complexity: `O(n)`

The `merged` output list holds up to `n + 1` intervals; no other auxiliary storage grows with the input.

#### Key Insights

- Solves the problem head-on by handling the three regions (before, overlapping, after) rather than reducing it to another problem.
- Exploiting the guaranteed sorted order means one linear walk suffices, with no sort.
- Handles every corner case cleanly: empty input, insertion before all or after all intervals, and full overlap.

### Insert and Merge

#### Derivation

The Linear Scan asks you to derive the three-region logic from scratch. If you already know Merge Intervals, there is a reduction instead: a sorted, non-overlapping list with one extra interval spliced into its sorted position is exactly a Merge Intervals input, so the familiar sweep finishes the job. The one trap to avoid is reaching for a sort to place `newInterval`: the input is already ordered, so a linear scan for the first start not less than `newInterval`'s start finds the slot, and sorting would discard the very structure the problem grants. The steps:

1. Scan `i` forward to the first interval whose start is not less than
   `newInterval[0]`, and build `combined = intervals[:i] + [newInterval] + intervals[i:]`, which stays sorted by start.
2. Sweep `combined` once: append each interval to `merged`, or, when it overlaps
   the last kept interval (`merged[-1][1] < interval[0]` fails), extend that interval's end via `max`.

The overlap test `merged[-1][1] < interval[0]` treats a shared endpoint as an overlap, so touching intervals such as `[1,5]` and `[5,8]` merge into `[1,8]`.

#### Walkthrough

Let us run the reduction on Example 2: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`. First the splice: the starts `1` and `3` are less than `4`, and `6` is not, so `i = 2` and `newInterval` slots in between `[3,5]` and `[6,7]`. Then the merge sweep walks `combined`, one interval per line:

```text
splice        i = 2
combined      [[1,2],[3,5],[4,8],[6,7],[8,10],[12,16]]

[1,2]     merged is empty -> append              merged = [[1,2]]
[3,5]     2 < 3, no overlap -> append            merged = [[1,2],[3,5]]
[4,8]     5 < 4 fails, overlap -> end = max(5,8) merged = [[1,2],[3,8]]
[6,7]     8 < 6 fails, overlap -> end = max(8,7) merged = [[1,2],[3,8]]
[8,10]    8 < 8 fails, overlap -> end = max(8,10) merged = [[1,2],[3,10]]
[12,16]   10 < 12, no overlap -> append          merged = [[1,2],[3,10],[12,16]]
```

The sweep chains the merges: `[4,8]` folds into `[3,5]`, and the widened `[3,8]` then swallows `[6,7]` and `[8,10]` (the `8 < 8` failure is the shared-endpoint case merging). The function returns `[[1,2],[3,10],[12,16]]`, matching the expected Output of Example 2.

#### Solution

The code is the splice and the sweep from the walkthrough.

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Drop newInterval into its sorted slot, then it is just Merge Intervals.
        i = 0
        while i < len(intervals) and intervals[i][0] < newInterval[0]:
            i += 1
        combined = intervals[:i] + [newInterval] + intervals[i:]

        merged = []
        for interval in combined:
            # No overlap with the last kept interval: start a new one.
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                # Overlap: extend the last interval's end.
                merged[-1][1] = max(merged[-1][1], interval[1])
        return merged
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The insertion scan, the splice, and the merge sweep each touch every interval at most once.

##### Space Complexity: `O(n)`

The `combined` list and the `merged` output each hold up to `n + 1` intervals.

#### Key Insights

- Reframes the task as Merge Intervals, reusing a sweep you may already know instead of deriving the region logic from scratch.
- Recognizing that the input is pre-sorted is what lets a linear insertion replace a full sort.
- It does redundant work next to the direct walk: it rebuilds the list and re-checks intervals that never touch `newInterval`.

### In-Place Modification

#### Derivation

Both previous approaches build a fresh output list, `O(n)` auxiliary space. If mutating the caller's list is acceptable, the same three-region structure can be executed in place: skip past the before region, absorb the overlapping block by folding each interval into `newInterval` and removing it with `pop`, then `insert` the merged interval into the gap. The space saving has a hidden time cost, since `pop(i)` shifts the entire tail of the list one slot left on every call. The steps:

1. Advance `i` past every interval ending before `newInterval` starts
   (`intervals[i][1] < newInterval[0]`).
2. While the interval at `i` overlaps `newInterval`
   (`intervals[i][0] <= newInterval[1]`), fold it in via `min`/`max` and `intervals.pop(i)`; the next overlapping interval slides down to index `i`.
3. Call `intervals.insert(i, newInterval)` to place the merged interval, and
   return the mutated `intervals`.

#### Walkthrough

Let us run the in-place version on Example 2: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`. Watch the list shrink as each overlapping interval is absorbed and popped, always at the same index `i = 1`:

```text
skip     [1,2] ends 2 < 4 -> i = 1;  [3,5] ends 5 >= 4 -> stop     i = 1
absorb   [3,5]:   3 <= 8 -> newInterval = [3,8],  pop(1)
                  intervals = [[1,2],[6,7],[8,10],[12,16]]
absorb   [6,7]:   6 <= 8 -> newInterval = [3,8],  pop(1)
                  intervals = [[1,2],[8,10],[12,16]]
absorb   [8,10]:  8 <= 8 -> newInterval = [3,10], pop(1)
                  intervals = [[1,2],[12,16]]
stop     [12,16]: 12 <= 10 fails -> absorb loop ends
insert   intervals.insert(1, [3,10])
                  intervals = [[1,2],[3,10],[12,16]]
```

Each `pop(1)` slides the tail left, which is where the quadratic worst case lives: here three pops each shift the remaining intervals. The mutated list `[[1,2],[3,10],[12,16]]` is returned, matching the expected Output of Example 2.

#### Solution

The code is the skip, absorb-and-pop, and insert steps from the walkthrough.

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        i = 0
        # Find the position to insert
        while i < len(intervals) and intervals[i][1] < newInterval[0]:
            i += 1
        # Merge overlapping intervals in-place
        while i < len(intervals) and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            intervals.pop(i)
        intervals.insert(i, newInterval)
        return intervals
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The scan itself visits each interval at most once, but every `pop(i)` shifts the entire tail of the list left by one position. Absorbing `k` overlapping intervals with `n - k` intervals after them costs `O(k × (n - k))` in shifting alone, which is `O(n^2)` in the worst case, such as a new interval that swallows the first half of the list. The final `insert(i, ...)` adds one more `O(n)` shift.

##### Space Complexity: `O(1)`

No new list is allocated; the result reuses the input list, ignoring the input and output storage themselves.

#### Key Insights

- Achieves constant auxiliary space by reusing the input list rather than building a new one.
- The space saving has a time cost: each `pop(i)` shifts the tail of the list, degrading the worst case to quadratic.
- Slightly harder to read because `pop`/`insert` mutate the list while it is being scanned.
- Appropriate only when destroying the caller's input is acceptable.

### Binary Search for the Overlap Window

#### Derivation

The linear approaches spend `O(n)` comparisons just to find the edges of the overlapping block. The sortedness offers more than a single pass: because the intervals are sorted by start *and* disjoint, each interval ends before the next begins, so the end values are ascending too. Both edges of the block are therefore boundaries of monotone predicates, and each can be found by a [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) in `O(log n)` comparisons.

An interval overlaps `newInterval` exactly when both `intervals[i][1] >= newInterval[0]` (it does not end before the new one starts) and `intervals[i][0] <= newInterval[1]` (it does not start after the new one ends). Each condition gets its own search:

1. The first search runs over the ascending end values and finds `first`, the
   leftmost index with `intervals[i][1] >= newInterval[0]`. Ends before `first` are too small to overlap; ends from `first` onward all satisfy the predicate, so the predicate flips exactly once and the search is valid.
2. The second search runs over the ascending start values and finds `last`, the
   rightmost index with `intervals[i][0] <= newInterval[1]`. Starts after `last` are too large to overlap. The midpoint uses `(lo + hi + 1) // 2` because this search rounds toward the right boundary; rounding down would loop forever when `lo` and `hi` are adjacent.
3. Since both predicates flip once over the sorted list, the overlapping intervals
   are exactly the contiguous window `[first, last]`. If `first > last`, the window is empty and `newInterval` overlaps nothing: it slots in unchanged at index `first`. Otherwise one `merged` interval spans `min` of the starts at the window's left edge and `max` of the ends at its right edge, and the result is the untouched prefix, the merged interval, and the untouched suffix.

Both comparisons use `>=` and `<=` so intervals that merely touch `newInterval` at an endpoint, such as `[1,5]` against a new `[5,8]`, land inside the window and merge.

#### Walkthrough

Let us run both searches by hand on Example 2: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`, `n = 5`. The end values are `2, 5, 7, 10, 16` and the start values are `1, 3, 6, 8, 12`, both ascending, as the derivation promised.

```text
first: leftmost i with intervals[i][1] >= 4
lo=0  hi=5   mid=2   intervals[2][1] = 7   >= 4 -> hi = 2
lo=0  hi=2   mid=1   intervals[1][1] = 5   >= 4 -> hi = 1
lo=0  hi=1   mid=0   intervals[0][1] = 2   <  4 -> lo = 1
lo=1  hi=1   loop ends -> first = 1

last: rightmost i with intervals[i][0] <= 8
lo=-1 hi=4   mid=2   intervals[2][0] = 6   <= 8 -> lo = 2
lo=2  hi=4   mid=3   intervals[3][0] = 8   <= 8 -> lo = 3
lo=3  hi=4   mid=4   intervals[4][0] = 12  >  8 -> hi = 3
lo=3  hi=3   loop ends -> last = 3

first = 1 <= last = 3 -> window [1, 3] holds the overlapping intervals
merged = [min(4, intervals[1][0] = 3), max(8, intervals[3][1] = 10)] = [3, 10]
result = intervals[:1] + [[3,10]] + intervals[4:] = [[1,2],[3,10],[12,16]]
```

Note the upward-rounding midpoint at work in the second search: with `lo = 3` and `hi = 4`, `mid = (3 + 4 + 1) // 2 = 4` probes the right candidate, and the failed test pulls `hi` down to `3`; rounding down would have probed index `3` forever. The window `[1, 3]` covers `[3,5]`, `[6,7]`, `[8,10]`, exactly the intervals the Explanation lists, and the assembled result `[[1,2],[3,10],[12,16]]` matches the expected Output of Example 2.

#### Solution

The code is the two boundary searches from the walkthrough, followed by the window test and the three-piece reassembly.

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        n = len(intervals)

        # Leftmost index whose interval ends at or after newInterval starts.
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if intervals[mid][1] >= newInterval[0]:
                hi = mid
            else:
                lo = mid + 1
        first = lo

        # Rightmost index whose interval starts at or before newInterval ends.
        lo, hi = -1, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if intervals[mid][0] <= newInterval[1]:
                lo = mid
            else:
                hi = mid - 1
        last = lo

        if first > last:
            # Empty window: nothing overlaps, newInterval slots in at index first.
            return intervals[:first] + [newInterval] + intervals[first:]

        merged = [
            min(newInterval[0], intervals[first][0]),
            max(newInterval[1], intervals[last][1]),
        ]
        return intervals[:first] + [merged] + intervals[last + 1:]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The two binary searches cost `O(log n)`, but the return statement slices the prefix and suffix into a new list, copying up to `n` interval references. The copying dominates, so the overall bound stays `O(n)`: the searches reduce the comparison work, not the asymptotic total. This approach is about practicing the boundary-search technique, not about beating the linear scan.

##### Space Complexity: `O(n)`

The result list built from the prefix slice, the merged interval, and the suffix slice holds up to `n + 1` intervals; the searches themselves use constant extra space.

#### Key Insights

- Boundary binary searches are predicate design: choose a condition that is monotone over the sorted list, then find where it flips. The left edge is the first index where `end >= newInterval[0]` becomes true; the right edge is the last index where `start <= newInterval[1]` is still true.
- The rightmost-flavored search needs the `(lo + hi + 1) // 2` midpoint; the leftmost flavor rounds down. Mixing them up produces an infinite loop on adjacent bounds.
- Sortedness plus non-overlap make both the starts and the ends monotone, which is exactly why the overlapping intervals form one contiguous window rather than scattered matches.
- There is no asymptotic win here: any solution that returns a new list of up to `n + 1` intervals must spend `O(n)` building it. A true `O(log n)` algorithm exists only when the answer avoids the rebuild, such as counting the overlapping intervals (`last - first + 1`), reporting the merged interval's bounds, or testing whether `newInterval` overlaps anything at all.

### Recursive Merge

#### Derivation

The three regions can also be discovered one interval at a time. Compare `newInterval` against just the head of the list, `intervals[0]`: either the new interval ends before the head starts (it belongs in front, and everything after is untouched), or it starts after the head ends (the head is safe to emit, and the problem [recurses](https://en.wikipedia.org/wiki/Recursion_(computer_science)) on the tail), or the two overlap (fold them together and recurse with the widened interval). This expresses the merge as a fold over the list, at the cost of an `intervals[1:]` slice copy per call. The steps:

1. If `intervals` is empty, the answer is `[newInterval]`.
2. If `newInterval[1] < intervals[0][0]`, the new interval lies entirely before
   the head: prepend it and return.
3. If `newInterval[0] > intervals[0][1]`, the head lies entirely before the new
   interval: keep `intervals[0]` and recurse on `intervals[1:]`.
4. Otherwise they overlap: build `merged` via `min` start and `max` end, and
   recurse on `intervals[1:]` with `merged` in place of `newInterval`.

#### Walkthrough

Let us unwind the recursion on Example 2: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`. Each line is one call, indented by depth, showing which of the three cases fires:

```text
insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8])
  [1,2]: 8 < 1? no; 4 > 2? yes  -> after: [[1,2]] + insert(tail, [4,8])
  insert([[3,5],[6,7],[8,10],[12,16]], [4,8])
    [3,5]: overlap -> merged = [min(4,3), max(8,5)] = [3,8]
    insert([[6,7],[8,10],[12,16]], [3,8])
      [6,7]: overlap -> merged = [3, max(8,7)] = [3,8]
      insert([[8,10],[12,16]], [3,8])
        [8,10]: overlap -> merged = [3, max(8,10)] = [3,10]
        insert([[12,16]], [3,10])
          [12,16]: 10 < 12? yes -> before: return [[3,10],[12,16]]
```

The innermost call hits the "entirely before" case and returns `[[3,10],[12,16]]`; the overlap calls pass that result up unchanged, and the outermost call prepends its kept head `[1,2]`. The final answer is `[[1,2],[3,10],[12,16]]`, matching the expected Output of Example 2.

#### Solution

The code is the three-case comparison from the walkthrough, applied to the head of the list on every call.

```python
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if not intervals:
            return [newInterval]
        if newInterval[1] < intervals[0][0]:
            return [newInterval] + intervals
        elif newInterval[0] > intervals[0][1]:
            return [intervals[0]] + self.insert(intervals[1:], newInterval)
        else:
            merged = [min(newInterval[0], intervals[0][0]), max(newInterval[1], intervals[0][1])]
            return self.insert(intervals[1:], merged)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each interval is consumed by one recursive step, but every level copies the remainder of the list through the `intervals[1:]` slice, adding linear work per interval. Conceptually each interval is handled once; the slicing is what pushes the bound to `O(n^2)`.

##### Space Complexity: `O(n^2)`

The recursion reaches depth `O(n)`, and each frame holds its own `intervals[1:]` slice copy alive until the recursion below it returns, so the live slices across the stack total `O(n^2)` in the worst case.

#### Key Insights

- Expresses the merge declaratively as a fold over the interval list.
- Not idiomatic here: list slicing and deep recursion make it costlier than the iterative passes.
- Risks exceeding Python's default recursion limit at the upper constraint of `10^4` intervals.

### Binary Search with bisect

#### Derivation

The two searches in [Binary Search for the Overlap Window](#binary-search-for-the-overlap-window) are not bespoke: they are the two standard flavors of boundary search, and [`bisect`](https://docs.python.org/3/library/bisect.html) ships both. What moves to the library is only the `lo`/`hi` narrowing, including the `(lo + hi + 1) // 2` midpoint whose upward rounding the hand-rolled version has to justify. What stays is everything that makes this problem this problem: the choice of which key each search runs over, the empty-window test, and the three-piece reassembly of prefix, merged interval, and suffix.

The bridge is the `key` argument, added to `bisect` in Python 3.10. It lets a search read a derived value from each element instead of comparing elements directly, which is exactly what is needed here: one search must see each interval as its end, the other as its start. The two flavors then line up with the two edges:

1. `bisect_left(intervals, newInterval[0], key=lambda iv: iv[1])` returns the
   leftmost index whose end is not less than `newInterval[0]`. That is `first`, the same value the hand-rolled leftmost search computes, since `bisect_left` is defined to land before every entry equal to the target.
2. `bisect_right(intervals, newInterval[1], key=lambda iv: iv[0])` returns the
   first index whose start exceeds `newInterval[1]`, landing after every entry equal to the target. Subtracting one gives `last`, the rightmost index whose start is at or before `newInterval[1]`. The upward-rounding midpoint disappears with the loop that needed it.
3. Test `first > last` for an empty window and slot `newInterval` in at index
   `first` unchanged, exactly as before.
4. Otherwise build `merged` from `min` of the starts at the window's left edge
   and `max` of the ends at its right edge, and return the prefix, the merged interval, and the suffix.

The `left`/`right` distinction carries the endpoint-touching behavior for free. Using `bisect_left` on the ends keeps an interval ending exactly at `newInterval[0]` inside the window, and `bisect_right` on the starts keeps an interval starting exactly at `newInterval[1]` inside it, which is the same non-strict comparison the `>=` and `<=` tests spelled out by hand.

#### Walkthrough

Let us run both calls on Example 2: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`, `n = 5`. Each search sees the list through its own key, and both key sequences are ascending, which is what makes the searches valid:

| index `i` | `0` | `1` | `2` | `3` | `4` |
| --- | --- | --- | --- | --- | --- |
| `intervals[i]` | `[1,2]` | `[3,5]` | `[6,7]` | `[8,10]` | `[12,16]` |
| end key `iv[1]` | `2` | `5` | `7` | `10` | `16` |
| start key `iv[0]` | `1` | `3` | `6` | `8` | `12` |

```text
first = bisect_left(ends = [2,5,7,10,16], 4)
        2 < 4, and 5 is the first value not less than 4  ->  first = 1

last  = bisect_right(starts = [1,3,6,8,12], 8) - 1
        1, 3, 6, 8 are all <= 8; 12 is the first value above 8  ->  4 - 1 = 3

first = 1 <= last = 3 -> window [1, 3] holds the overlapping intervals
merged = [min(4, intervals[1][0] = 3), max(8, intervals[3][1] = 10)] = [3, 10]
result = intervals[:1] + [[3,10]] + intervals[4:] = [[1,2],[3,10],[12,16]]
```

The `bisect_right` call is what handles the shared endpoint at `8`: the interval `[8,10]` starts exactly where `newInterval` ends, and landing to the right of equal values keeps it inside the window rather than excluding it. The window `[1, 3]` covers `[3,5]`, `[6,7]`, `[8,10]`, exactly the intervals the Explanation lists, and the assembled result `[[1,2],[3,10],[12,16]]` matches the expected Output of Example 2.

#### Solution

The same two boundaries and the same reassembly, with the searching delegated to the standard library.

```python
from bisect import bisect_left, bisect_right
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Leftmost index whose interval ends at or after newInterval starts.
        first = bisect_left(intervals, newInterval[0], key=lambda iv: iv[1])
        # Rightmost index whose interval starts at or before newInterval ends.
        last = bisect_right(intervals, newInterval[1], key=lambda iv: iv[0]) - 1

        if first > last:
            # Empty window: nothing overlaps, newInterval slots in at index first.
            return intervals[:first] + [newInterval] + intervals[first:]

        merged = [
            min(newInterval[0], intervals[first][0]),
            max(newInterval[1], intervals[last][1]),
        ]
        return intervals[:first] + [merged] + intervals[last + 1:]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The two `bisect` calls cost `O(log n)` comparisons each, the same as the hand-rolled searches, since `bisect` performs the identical halving. The `key` function adds one call per probe, so `O(log n)` extra calls in total. The return statement still slices the prefix and suffix into a new list, copying up to `n` interval references, and that copying dominates, leaving the bound at `O(n)`.

##### Space Complexity: `O(n)`

The result list built from the prefix slice, the merged interval, and the suffix slice holds up to `n + 1` intervals. `bisect` with a `key` evaluates the key on each probe without materializing a keys list, so the searches themselves stay constant space.

#### Key Insights

- The algorithm is untouched: the same two boundaries over the same two monotone
  keys, which shows the predicate design is the real content and the `lo`/`hi` narrowing was only bookkeeping.
- The `key` argument is what makes `bisect` applicable to a list of intervals at
  all. Without it the searches would need two separately materialized lists of starts and ends, `O(n)` extra space and `O(n)` extra work to build.
- Choosing `bisect_left` for the ends and `bisect_right` for the starts encodes
  the endpoint-touching rule in the function names, replacing the `>=` and `<=` tests and removing the `(lo + hi + 1) // 2` midpoint trap entirely.
- The `- 1` after `bisect_right` is the one place to slip: `bisect` returns
  insertion points, not matching indices, so a rightmost boundary is always the insertion point minus one, and an empty window shows up as `last = -1`.

## Comparison of Solutions

### Time Complexity

- **Linear Scan and Merge**: `O(n)` - a single walk over the three regions exploits the already-sorted input.
- **Insert and Merge**: `O(n)` - a linear insertion plus one merge sweep, with no sort.
- **In-Place Modification**: `O(n^2)` worst case - each `pop(i)` shifts the entire tail of the list, so absorbing many overlapping intervals costs quadratic shifting.
- **Binary Search for the Overlap Window**: `O(n)` - the two boundary searches take only `O(log n)`, but slicing the prefix and suffix into the result still copies up to `n` intervals.
- **Recursive Merge**: `O(n^2)` - each interval is handled once, but the `intervals[1:]` copy at every level adds linear work per step.
- **Binary Search with bisect**: `O(n)` - identical to the hand-rolled searches, since `bisect` halves the same way and the result slicing still copies up to `n` intervals.

### Space Complexity

- **Linear Scan and Merge**: `O(n)` - builds a separate merged output list.
- **Insert and Merge**: `O(n)` - builds a combined list and a separate merged output list.
- **In-Place Modification**: `O(1)` - mutates the input list, ignoring input/output storage.
- **Binary Search for the Overlap Window**: `O(n)` - builds the result from prefix, merged-window, and suffix copies.
- **Recursive Merge**: `O(n^2)` worst case - `O(n)` recursion depth where each frame keeps its own `intervals[1:]` slice copy alive.
- **Binary Search with bisect**: `O(n)` - the same prefix, merged-window, and suffix copies; the `key` argument avoids materializing separate lists of starts and ends.

### Trade-offs

- Linear Scan and Merge gains optimal linear time and a clear three-region structure without mutating the input, at the cost of an extra output list.
- Insert and Merge gains a familiar mental model (reduce to Merge Intervals) but does redundant work by rebuilding the list and re-checking intervals that never touch the new one.
- In-Place Modification gains `O(1)` auxiliary space by mutating the input in place, giving up readability, a non-destructive contract, and the linear time bound (tail-shifting pops make the worst case quadratic).
- Binary Search for the Overlap Window gains `O(log n)` comparison work and a reusable boundary-search technique, but the output rebuild keeps the overall bound at `O(n)`, so it offers no asymptotic advantage over the linear scan.
- Recursive Merge gains an elegant declarative form but gives up practicality, risking recursion-depth limits on large inputs.
- Binary Search with bisect gains roughly a dozen fewer lines and drops the midpoint-rounding trap, giving up the explicit narrowing that makes the boundary predicates visible on the page; it also requires Python 3.10 or later for the `key` argument.

### When to Use Each

- **Linear Scan and Merge**: The recommended default; best balance of clarity and efficiency.
- **Insert and Merge**: When you would rather lean on the familiar Merge Intervals sweep than spell out the three regions.
- **In-Place Modification**: When minimizing extra space is critical and mutating the input is acceptable.
- **Binary Search for the Overlap Window**: When you want to practice boundary binary searches, or when the real question is locating or counting the overlapping intervals rather than rebuilding the list.
- **Recursive Merge**: For academic interest or small inputs only.
- **Binary Search with bisect**: The Pythonic form of the boundary search. Reach for it in real code, and write the hand-rolled loops instead when an interviewer wants the halving spelled out.

### Optimization Notes

- Linear Scan and Merge is the recommended approach: one linear walk over the three regions, with no sort.
- Insert and Merge trades that direct walk for the familiar Merge Intervals sweep; it stays `O(n)` only because the pre-sorted input lets a linear insertion replace a sort.
- The In-Place Modification approach's `pop`/`insert` operations shift the tail of the list on every call, so the auxiliary-space saving is paid for with a quadratic worst-case time bound.
- Binary Search for the Overlap Window cuts the comparisons to `O(log n)` but not the copying; it becomes a genuine `O(log n)` algorithm only when the answer does not require rebuilding the list, such as counting or locating the overlapping intervals.
- Every approach hinges on the same three regions: intervals strictly before, intervals overlapping (merged via `min` start and `max` end), and intervals strictly after.
- Avoid the recursive variant for the upper constraint of `10^4` intervals, where deep recursion can exceed Python's default recursion limit.
- [Binary Search with bisect](#binary-search-with-bisect) replaces the hand-rolled narrowing without changing either bound: `bisect_left` and `bisect_right` on keyed views of the ends and starts compute the same two boundaries, so the win is fewer lines and one fewer place to get the midpoint wrong, not a faster solution.
