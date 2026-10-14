# [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)

**Medium** | **25 minutes** | **Array, Two Pointers, Greedy, Sorting, Heap (Priority Queue), Prefix Sum**

**Pattern:** [Interval](../patterns/interval/intuition.md), [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Sweep line algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm) · [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/meeting_rooms_ii/solution.py`](../../practice/meeting_rooms_ii/solution.py)

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/meeting-rooms-ii/); read it free on [NeetCode](https://neetcode.io/problems/meeting-schedule-ii).

Given an array of meeting time interval objects consisting of start and end times `[[start_1,end_1],[start_2,end_2],...] (start_i < end_i)`, find the minimum number of rooms required to schedule all meetings without any conflicts.

**Note:** `(0,8),(8,10)` is **NOT** considered a conflict at 8.

## Examples

### Example 1

**Input:** `intervals = [(0,40),(5,10),(15,20)]`

**Output:** `2`

**Explanation:** room1: `(0,40)`
room2: `(5,10),(15,20)`

### Example 2

**Input:** `intervals = [(4,9)]`

**Output:** `1`

## Constraints

- `0 <= intervals.length <= 100,000`
- `0 <= intervals[i].start < intervals[i].end <= 1,000,000`

## Deriving the Solution

Meetings that overlap in time cannot share a room, so the minimum room count is the maximum number of meetings running at once: the deepest concurrency the schedule ever reaches. Every solution below counts that peak; they differ in whether the count emerges from simulating room assignments, from pairing starts against ends, from freeing rooms with a heap, or from walking a timeline of events.

1. **Start literal.** Take the meetings in start order and put each into the
   first room whose occupant has left; open a new room only when none fits.
   The simulation is honest but each assignment may scan every room: see
   [First-Fit Room Scan](#first-fit-room-scan).
2. **Separate times from rooms.** Only two orders matter: meetings begin in
   start order and free rooms in end order. Merging those two sorted
   timelines with two pointers counts rooms in use without tracking which
   meeting sits where: see [Chronological Ordering](#chronological-ordering).
3. **Free rooms with a heap.** The room a new meeting wants is the one whose
   meeting ends soonest, and "soonest end" is exactly what a min-heap
   answers in `O(log n)`: pop the freed room, push the new end, and the heap
   size tracks rooms in use: see
   [Min-Heap of End Times](#min-heap-of-end-times).
4. **Count the timeline directly.** A meeting's start is a `+1` demand and its
   end a `-1` release; sweeping both kinds of event in time order and reading
   the running depth counts the peak without any room identity at all: see
   [Event Sweep](#event-sweep).

## Solutions

### First-Fit Room Scan

#### Derivation

The most direct reading simulates a coordinator. Meetings arrive in start order (sorting first guarantees no meeting starts before one already placed), and each is dropped into the first room whose meeting has ended; a new room opens only when every room is still busy:

1. Sort `intervals` by `start`.
2. Keep `rooms`, a list of the end times of the meetings occupying each room.
3. For each meeting in order, scan `rooms` for the first end time
   `<= start`; if found, reuse that room and update its end.
4. If no room fits, append a new end to `rooms`.
5. The answer is the final size of `rooms`.

#### Walkthrough

Trace the placement on Example 1: `intervals = [(0,40),(5,10),(15,20)]`, which start-sorting leaves in the same order. Each row is one meeting's placement:

```text
rooms = []
(0,40)   rooms empty            -> new room      rooms = [40]
(5,10)   first end 40 > 5       -> new room      rooms = [40, 10]
(15,20)  first end 40 > 15,
         second end 10 <= 15    -> reuse room 1  rooms = [40, 20]
```

`(0,40)` and `(5,10)` genuinely overlap, so two rooms open; `(15,20)` lands in the room `(5,10)` vacated at time 10. The final `rooms` holds `2` entries, matching the expected Output for Example 1. On Example 2, `[(4,9)]` opens a single room and the function returns `1`.

#### Solution

The code is the walkthrough's placement loop: first-fit scan, append on failure.

```python
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        intervals.sort(key=lambda interval: interval.start)

        rooms: List[int] = []
        for interval in intervals:
            placed = False
            for r, end in enumerate(rooms):
                if end <= interval.start:
                    rooms[r] = interval.end
                    placed = True
                    break
            if not placed:
                rooms.append(interval.end)
        return len(rooms)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Start-sorting costs `O(n log n)`, and each of the `n` placements may scan all `O(n)` rooms in the worst case, when every meeting overlaps every other and no room is ever reused.

##### Space Complexity: `O(n)`

`rooms` holds one end time per open room, up to `n`.

#### Key Insights

- The simulation proves its own optimality visually on small inputs: the room count only grows when a meeting arrives while every open room is genuinely busy.
- The waste is the scan: finding the earliest-ending room among open ones is a repeated search, which the heap solution turns into a peek.
- Room identity does not survive the run (rooms are reused and their end times overwritten), which is fine here but is exactly what the chronological solution discards on purpose.

### Chronological Ordering

#### Derivation

The first-fit scan tracks which meeting sits in which room, yet the count never needs room identities: a room frees when a meeting ends, and a room is taken when a meeting starts. So two timelines suffice: the starts, in order, each demanding a room; and the ends, in order, each releasing one. Two pointers merge them: every start before the earliest unprocessed end takes a fresh room, and every start at or after it can reuse the room that end just freed:

1. Build `starts`, all meeting start times sorted, and `ends`, all end times
   sorted.
2. Walk the starts with `rooms_used = 0` and `end_ptr = 0`.
3. For each `start`: if `start < ends[end_ptr]`, no room is free, so
   `rooms_used += 1`; otherwise the earliest end has released its room, so
   `end_ptr += 1`.
4. `rooms_used` at the end is the peak, because it only ever grew while
   meetings stacked up.

The shared-boundary rule lives in the strict comparison: a start equal to the earliest end reuses the freed room, per the problem's `(0,8),(8,10)` note.

#### Walkthrough

Trace the merge on Example 1: `intervals = [(0,40),(5,10),(15,20)]` gives `starts = [0, 5, 15]` and `ends = [10, 20, 40]`:

```text
start 0  vs ends[0]=10   0 < 10   -> rooms_used = 1
start 5  vs ends[0]=10   5 < 10   -> rooms_used = 2
start 15 vs ends[0]=10   15 >= 10 -> end_ptr = 1   (room freed)
```

The count rises to `2` while the first two meetings stack up, and at `start 15` the end `10` has released a room: the freed room is taken by `(15,20)` without raising `rooms_used`, so the final count is `2`, matching the expected Output for Example 1. The pointer swap is worth reading closely: after `end_ptr` advances, the next meeting would be compared against `ends[1] = 20`, and any start before 20 would open a genuinely new room. On Example 2, `[(4,9)]` yields `starts = [4]`, `ends = [9]`, one strict comparison, and the function returns `1`.

#### Solution

The code is the walkthrough's merge: one pass over sorted starts against the sorted ends.

```python
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        starts = sorted(interval.start for interval in intervals)
        ends = sorted(interval.end for interval in intervals)

        rooms_used = 0
        end_ptr = 0
        for start in starts:
            if start < ends[end_ptr]:
                rooms_used += 1
            else:
                end_ptr += 1
        return rooms_used
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Two sorts dominate; the merge is one pass with at most `2n` pointer steps.

##### Space Complexity: `O(n)`

The `starts` and `ends` arrays each hold `n` times.

#### Key Insights

- Sorting starts and ends independently destroys meeting identity, and nothing is lost: concurrency is a property of the two timelines, not of which meeting is which.
- The count never decreases in this formulation, so the final value is the peak; tracking a maximum is unnecessary because rooms are only "taken" here, never explicitly released.
- This is the two-person handshake view of the heap solution: the end pointer is a queue of freed rooms, dequeued in the same earliest-first order the heap would produce.

### Min-Heap of End Times

#### Derivation

The chronological merge frees rooms through a sorted array it must prebuild. A min-heap produces the same earliest-end order online: the heap holds the end time of the meeting currently occupying each open room, so its root is always the room freeing soonest. Start-sorted meetings arrive one at a time; each either reuses the root's room (the root's end is `<= start`) or opens a new room (the heap grows by one). The heap's size is the number of open rooms, and its maximum over the run is the answer:

1. Sort `intervals` by `start`.
2. Keep `heap`, a min-heap of end times, one entry per open room.
3. For each meeting: if `heap[0] <= start`, pop (the room frees just in
   time); push the meeting's `end`.
4. The answer is the maximum size `heap` reaches, which is its size at the
   end, since entries leave only when replaced.

#### Invariant

The heap always contains exactly one end time per open room, and `heap[0]` is the earliest end among them:

$$ \text{heap} = \{\, \text{end} : \text{a currently open room's meeting ends at end} \,\}, \quad \text{heap}[0] = \min(\text{heap}) $$

```text
heap = one entry per open room, holding that room's meeting end time
heap[0] = the earliest end among all open rooms
```

Each step preserves this: a start-sorted meeting has the latest start so far, so the only rooms it could reuse are those whose meetings ended by `start`, and `heap[0] <= start` certifies the earliest-ending one has; popping it before pushing keeps the entry-per-room correspondence exact. When a new meeting finds `heap[0] > start`, every open room is busy at `start`, which is when the heap legitimately grows. At the end, the heap size equals the number of rooms the schedule needed, because that many meetings were simultaneously open at some point and no two of them ever shared a room.

#### Walkthrough

Trace the heap through Example 1: `intervals = [(0,40),(5,10),(15,20)]`, start-sorted as given. Interior heap lists are shown as CPython keeps them (the root `heap[0]` is leftmost):

```text
heap = []
(0,40)   heap empty, nothing to free   push 40   heap = [40]          size 1
(5,10)   heap[0]=40 > 5: no room free  push 10   heap = [10, 40]      size 2
(15,20)  heap[0]=10 <= 15: free        pop 10    heap = [40]
         (room reused)                 push 20   heap = [20, 40]      size 2
```

The peak size is `2`: the first two meetings overlap and occupy two rooms, and the third reuses the room freed at time 10. The function returns `2`, matching the expected Output for Example 1. On Example 2, `[(4,9)]` pushes once and the function returns `1`.

#### Solution

The code is the walkthrough's per-meeting step: free the root when its end has passed, then push the new end.

```python
import heapq
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        intervals.sort(key=lambda interval: interval.start)

        heap: List[int] = []
        for interval in intervals:
            if heap and heap[0] <= interval.start:
                # The room freeing soonest is free for this meeting.
                heapq.heappop(heap)
            heapq.heappush(heap, interval.end)
        return len(heap)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting is `O(n log n)` and each of the `n` meetings costs one `O(log n)` pop and one `O(log n)` push against a heap that never exceeds `n` entries.

##### Space Complexity: `O(n)`

The heap holds one entry per open room, at most `n`.

#### Key Insights

- The heap is the first-fit scan with the linear search replaced: the root is the best room by definition, and testing it alone suffices, because if the soonest-free room is still busy, every room is.
- End times, not intervals, sit in the heap: room identity is irrelevant, only when each open room frees.
- The final heap size equals the peak because a room is opened (the push without a pop) exactly when all current rooms are provably busy at that start.

### Event Sweep

#### Derivation

All three previous solutions keep some structure over meetings, but the answer is a number on the timeline: the deepest point of a step function that rises by one at each start and falls by one at each end. Plotting that function is the classic sweep line: turn each meeting into two events, sort the events by time, and walk them, adding one for a start and subtracting one for an end. The running depth is the number of meetings in progress; its maximum is the room count:

1. Build `events`: `(start, +1)` and `(end, -1)` for every meeting.
2. Sort events by time, with ends before starts at equal times, honoring the
   shared-boundary rule.
3. Sweep: `depth += delta` per event, tracking `peak = max(peak, depth)`.
4. The answer is `peak`.

The tie rule is the one subtlety: at time `t` a meeting ending at `t` and another starting at `t` share the room, so the `-1` must process first; encoding the delta as the secondary sort key does it for free, because `-1 < 1`.

#### Walkthrough

Trace the sweep on Example 1: `intervals = [(0,40),(5,10),(15,20)]` produce the events, which sort (time, then delta ascending, so ends first) to the order below:

```text
events sorted: (0,+1) (5,+1) (10,-1) (15,+1) (20,-1) (40,-1)
(0,+1)    depth = 1
(5,+1)    depth = 2   peak = 2
(10,-1)   depth = 1
(15,+1)   depth = 2   peak = 2
(20,-1)   depth = 1
(40,-1)   depth = 0
```

The depth climbs to `2` while `(0,40)` and `(5,10)` overlap, dips when `(5,10)` ends, and returns to `2` for `(15,20)`: the peak is `2`, matching the expected Output for Example 1. On Example 2, `[(4,9)]` sweeps `(4,+1)` then `(9,-1)`, peaking at `1`.

#### Solution

The code is the event list, the delta-keyed sort, and the depth walk.

```python
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        events: List[tuple] = []
        for interval in intervals:
            events.append((interval.start, 1))
            events.append((interval.end, -1))
        # Ends sort before starts at the same time: -1 < 1 encodes the
        # shared-boundary rule.
        events.sort()

        depth = 0
        peak = 0
        for _, delta in events:
            depth += delta
            peak = max(peak, depth)
        return peak
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

`2n` events are sorted, then swept in one pass.

##### Space Complexity: `O(n)`

The event list holds two entries per meeting.

#### Key Insights

- The sweep forgets meetings entirely: only the step function matters, which makes it the shortest correct formulation of the problem.
- The tie rule is where the boundary convention lives; sorting `(time, delta)` pairs processes `-1` before `+1` at equal times without any extra branch.
- This is the prefix-sum idea in event form: `depth` at any instant is the sum of all deltas up to that instant, and the answer is its maximum prefix value.

## Comparison of Solutions

The practice harness's `practice/meeting_rooms_ii/reference.py` implements the **Min-Heap of End Times** solution.

### Time Complexity

- **First-Fit Room Scan**: `O(n^2)` - each placement may scan every open room.
- **Chronological Ordering**: `O(n log n)` - two sorts, then a linear merge.
- **Min-Heap of End Times**: `O(n log n)` - sort plus one heap pop and push per meeting.
- **Event Sweep**: `O(n log n)` - one sort of `2n` events, then a linear walk.

### Space Complexity

- **First-Fit Room Scan**: `O(n)` - one end time per open room.
- **Chronological Ordering**: `O(n)` - the separate `starts` and `ends` arrays.
- **Min-Heap of End Times**: `O(n)` - one heap entry per open room.
- **Event Sweep**: `O(n)` - two events per meeting.

### Trade-offs

- The first-fit scan is the problem acted out room by room, which makes it the easiest to trust and extend (room identity survives, so "which meetings shared room 3" stays answerable), at a quadratic price.
- Chronological Ordering sorts two arrays and merges them with two pointers: no auxiliary logic beyond one comparison, but it answers only the count.
- The min-heap keeps the rooms' frees in a structure that also extends to streaming input and to variants needing room identity, at the cost of heap machinery.
- The event sweep is the least attached to meetings and the easiest to generalize to weighted or multi-room variants, but its correctness rests on getting the tie rule right.

### When to Use Each

- **First-Fit Room Scan**: as the simulation baseline and an oracle for the linearithmic versions on small inputs.
- **Chronological Ordering**: when only the count is needed and the two-pointer merge reads clearest.
- **Min-Heap of End Times** (recommended): the interview default: it answers the question asked, generalizes to follow-ups (smallest room number, meeting assignment), and its invariant is one sentence.
- **Event Sweep**: when the problem grows more timeline-shaped (maximum overlap of anything, weighted intervals, boundary-sensitive counting), or as the quick cross-check.

### Optimization Notes

- All three linearithmic answers agree on every input; a disagreement is a bug, most often a boundary-rule slip (`<=` versus `<`) or a tie-rule slip in the sweep.
- The heap variant can skip the pop when ties are impossible (`intervals[i].start < intervals[i - 1].end` guaranteed), but the guarded form is the safe default and costs the same asymptotically.
- The chronological merge's final-count-is-peak trick (rooms never released, only counted) is easy to break by adding a release decrement; if the variant ever needs an online peak, track `max` explicitly.
- The event sweep's `(time, delta)` sort key encodes the shared-boundary rule; sorting deltas descending at equal times would count a shared-boundary handoff as two rooms, the classic wrong answer on inputs like `(0,8),(8,10)`.
