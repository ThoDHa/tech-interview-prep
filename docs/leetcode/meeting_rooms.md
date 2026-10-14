# [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)

**Easy** | **15 minutes** | **Array, Sorting**

**Pattern:** [Interval](../patterns/interval/intuition.md)

**Algorithm:** [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Interval scheduling](https://en.wikipedia.org/wiki/Interval_scheduling)

**Practice:** [`practice/meeting_rooms/solution.py`](../../practice/meeting_rooms/solution.py)

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/meeting-rooms/); read it free on [NeetCode](https://neetcode.io/problems/meeting-schedule).

Given an array of meeting time interval objects consisting of start and end times `[[start_1,end_1],[start_2,end_2],...] (start_i < end_i)`, determine if a person could add all meetings to their schedule without any conflicts. The intervals may be provided in any order.

**Note:** (0,8),(8,10) is not considered a conflict at 8

## Examples

### Example 1

**Input:** `intervals = [(0,30),(5,10),(15,20)]`

**Output:** `false`

**Explanation:** * `(0,30)` and `(5,10)` will conflict
* `(0,30)` and `(15,20)` will conflict

### Example 2

**Input:** `intervals = [(5,8),(9,15)]`

**Output:** `true`

## Constraints

- `0 <= intervals.length <= 500`
- `0 <= intervals[i].start < intervals[i].end <= 1,000,000`

## Deriving the Solution

One person can attend every meeting exactly when no two meetings overlap in time, so the whole problem is a pairwise conflict question: do any two intervals intersect? Meetings arrive in arbitrary order, and the shared-boundary rule says `(0,8)` and `(8,10)` do not conflict, which makes the comparison strictly one-sided. The solutions differ only in which pairs they compare.

1. **Start literal.** Compare every pair of meetings and report whether any
   two overlap. Straightforward, but `O(n^2)` comparisons on an input a sort
   would linearize: see [Brute Force Pair Scan](#brute-force-pair-scan).
2. **Sort then scan neighbors.** After sorting by start, a conflict can only
   involve adjacent meetings: if each meeting starts at or after the previous
   one ends, the whole schedule is conflict-free, because start order makes
   every earlier meeting end no later than its neighbor's start: see
   [Sort and Adjacent Scan](#sort-and-adjacent-scan).

## Solutions

### Brute Force Pair Scan

#### Derivation

The most direct reading checks the definition: a schedule is attendable when no two meetings overlap, so test every pair. Two intervals `[a.start, a.end)` and `[b.start, b.end)` overlap exactly when each starts before the other ends; the shared-boundary rule falls out of strict comparisons:

1. For every pair `(i, j)` with `i < j`, compare `intervals[i]` and
   `intervals[j]`.
2. The pair conflicts when `intervals[i].start < intervals[j].end` and
   `intervals[j].start < intervals[i].end`.
3. Return `false` on the first conflict; `true` if none exists.

The early return prunes some work but the worst case touches every pair.

#### Walkthrough

Trace the pair scan on Example 1: `intervals = [(0,30),(5,10),(15,20)]`. Each row is one pair check:

| Pair | First | Second | `first.start < second.end`? | `second.start < first.end`? | Conflict? |
|------|-------|--------|------------------------------|------------------------------|-----------|
| `(0, 1)` | `(0,30)` | `(5,10)` | `0 < 10` yes | `5 < 30` yes | **yes** |

The very first pair conflicts: `(5,10)` begins while `(0,30)` is still running. The scan stops and the function returns `false`, matching the expected Output for Example 1. On Example 2, `[(5,8),(9,15)]`, the single pair passes both tests (`5 < 15` yes, `9 < 8` no), so no conflict exists and the function returns `true`.

#### Solution

The code is the walkthrough's nested pair loop around the two-sided overlap test.

```python
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        n = len(intervals)
        for i in range(n):
            for j in range(i + 1, n):
                first, second = intervals[i], intervals[j]
                # Strict comparisons: a meeting may begin exactly when the
                # previous one ends.
                if first.start < second.end and second.start < first.end:
                    return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every pair of the `n` meetings is checked once, `n * (n - 1) / 2` comparisons at the worst.

##### Space Complexity: `O(1)`

Loop indices only; nothing is stored.

#### Key Insights

- The overlap test is two-sided by nature: each interval must start before the other ends, and both strict inequalities encode the no-conflict-at-the-boundary rule.
- No order information is used, so the scan re-compares meetings a sorted pass would never pair; that waste is the next solution's target.
- The early return keeps the best case fast (a conflict among early pairs) but leaves the `O(n^2)` worst case intact.

### Sort and Adjacent Scan

#### Derivation

The pair scan's waste is testing pairs that order already clears. Sort the meetings by start. Then a conflict, if one exists, must show up between neighbors: if every meeting starts at or after the previous one ends, any two non-adjacent meetings are automatically compatible, because the earlier one ends no later than the intermediate one starts. One adjacent pass therefore decides the whole schedule:

1. Sort `intervals` by `start`.
2. For each consecutive pair, compare `intervals[i - 1].end` against
   `intervals[i].start`.
3. If a meeting starts strictly before the previous one ends, return
   `false`.
4. The scan finishing clean returns `true`.

#### Walkthrough

Trace the sorted scan on Example 1: `intervals = [(0,30),(5,10),(15,20)]`, which start-sorting leaves in the same order:

```text
sorted by start: (0,30)  (5,10)  (15,20)
pair 1: prev end 30 vs next start 5   5 < 30 -> conflict -> return false
```

The first adjacency already conflicts, so the function returns `false`, matching the expected Output for Example 1. On Example 2, `[(5,8),(9,15)]` sorts to the same order, and the single adjacency checks `9 < 8`, which is false, so no meeting starts before its predecessor ends and the function returns `true`.

#### Solution

The code is the walkthrough's sort and adjacent comparison.

```python
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        intervals.sort(key=lambda interval: interval.start)
        for i in range(1, len(intervals)):
            # A meeting may start exactly when the previous one ends.
            if intervals[i].start < intervals[i - 1].end:
                return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the adjacency sweep is one linear pass of one comparison per meeting.

##### Space Complexity: `O(1)`

The sort is in-place and the scan keeps one index.

#### Key Insights

- Sorting reduces a two-sided, all-pairs test to a one-sided adjacent test: start order guarantees `intervals[i - 1].start <= intervals[i].start`, so only the end of the previous meeting matters.
- Adjacency suffices by transitivity: a meeting that starts after its neighbor's start but before the neighbor's end would be caught; if it clears, everything before the neighbor is even earlier.
- This is the one-person special case of Meeting Rooms II, which asks how many rooms a conflicting schedule needs instead of whether one suffices.

## Comparison of Solutions

The practice harness's `practice/meeting_rooms/reference.py` implements the **Sort and Adjacent Scan** solution.

### Time Complexity

- **Brute Force Pair Scan**: `O(n^2)` - every pair is compared.
- **Sort and Adjacent Scan**: `O(n log n)` - sorting dominates a linear sweep.

### Space Complexity

- **Brute Force Pair Scan**: `O(1)` - indices only.
- **Sort and Adjacent Scan**: `O(1)` - in-place sort plus one index.

### Trade-offs

- The brute force needs no ordering and exits early on conflicts, and at the constraint cap of 500 meetings its quadratic worst case is affordable; the real cost is conceptual: it tests pairs the sorted pass proves irrelevant.
- The sorted scan pays one sort to collapse the question to `n - 1` comparisons, and its code is the shorter of the two.

### When to Use Each

- **Brute Force Pair Scan**: as the definitional baseline and an oracle for the sorted version on small inputs.
- **Sort and Adjacent Scan** (recommended): the answer in every practical setting: one sort key, one comparison, and the transitivity argument makes it obviously right.

### Optimization Notes

- The boundary rule lives in the comparison direction: `intervals[i].start < intervals[i - 1].end` treats a start equal to the previous end as legal, per the problem's note on `(0,8),(8,10)`.
- Sorting by start is what licenses the adjacent-only check; sorting by end would need a different argument, since a late-starting meeting could still conflict with an earlier, longer one.
- For the empty or single-meeting inputs the constraints allow, both versions return `true` without special cases: the loops simply never fire.
