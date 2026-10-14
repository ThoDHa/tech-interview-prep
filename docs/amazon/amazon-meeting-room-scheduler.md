# [Meeting Room Scheduler](https://www.fastprep.io/problems/amazon-meeting-room-scheduler)

**Medium** | **NN minutes** | **Array, Heap, Intervals, Simulation**

Implement a scheduler for roomCount meeting rooms numbered from 0 to roomCount - 1.

Each row meetings[i] = [start, end] is a request for the half-open interval [start, end). Requests appear in nondecreasing start order and are processed in input order. Assign the lowest-numbered available room. If every room overlaps the request, reject it with -1.

Return an array whose ith value is the assigned room number or -1. A rejected request does not reserve a room.

## Examples

### Example 1

**Input:** `roomCount = 2`, `meetings = [[0,10],[5,7],[10,12],[10,15]]`

**Output:** `[0,1,0,1]`

**Explanation:** The first two requests occupy rooms 0 and 1. At time 10, both are free; input order gives the third request room 0 and the fourth room 1.

### Example 2

**Input:** `roomCount = 1`, `meetings = [[1,4],[2,3],[4,5]]`

**Output:** `[0,-1,0]`

**Explanation:** The second request conflicts with [1,4). The room is available again exactly at time 4.

### Example 3

**Input:** `roomCount = 2`, `meetings = [[1,2],[1,2],[1,2]]`

**Output:** `[0,1,-1]`

**Explanation:** Two simultaneous requests take both rooms, so the third request is rejected.

## Constraints

- `1 <= roomCount <= 10^5.`
- `1 <= meetings.length <= 10^5.`
- `meetings[i].length == 2.`
- `0 <= start < end <= 10^9.`
- `Meeting start times are nondecreasing.`

## Solutions

### First-Fit Room Scan

#### Derivation

The literal reading of the problem is the coordinator's own procedure: take the requests in input order (they arrive in nondecreasing start order, so no sorting is needed; input order is already chronological) and give each one the lowest-numbered room whose current meeting has ended. With half-open intervals, a room whose meeting ends exactly at `start` is available, so the availability test is `room_free_at[room] <= start`. Keeping one number per room, the end time of its latest meeting, is all the state this needs:

1. Allocate `room_free_at`, one entry per room, initialized to `0`: every room is free from the beginning of time.
2. For each request `[start, end)`, scan rooms in number order `0` to `room_count - 1`.
3. The first room with `room_free_at[room] <= start` takes the request: record `room`, set `room_free_at[room] = end`, and stop scanning.
4. If no room passes the test, every room overlaps the request: record `-1`. A rejection writes nothing, so no room state changes.

#### Walkthrough

Trace the scan on Example 1: `roomCount = 2`, `meetings = [[0,10],[5,7],[10,12],[10,15]]`. Each row shows the availability array before the request, the rooms inspected, and the state after:

```text
room_free_at = [0, 0]
(0,10)    room 0: 0 <= 10    -> assign 0   room_free_at = [10, 0]
(5,7)     room 0: 10 > 5     busy
          room 1: 0 <= 5     -> assign 1   room_free_at = [10, 7]
(10,12)   room 0: 10 <= 10   -> assign 0   room_free_at = [12, 7]
(10,15)   room 0: 12 > 10    busy
          room 1: 7 <= 10    -> assign 1   room_free_at = [12, 15]
```

The two boundary rules are both visible: `(10,12)` takes room 0 because a meeting ending exactly at `10` frees the room at `10`, and `(10,15)` skips room 0 because `12 > 10`. The assignments `[0, 1, 0, 1]` match the expected Output for Example 1. (Example 2 shows the rejection path: at request `[2,3)` the single room holds `room_free_at = [4]`, the scan finds nothing, and `-1` is recorded without touching the array, so `[4,5)` still gets the room.)

#### Solution

The code is the walkthrough's loop: scan rooms in number order, take the first free one, record `-1` when none fits.

```python
from typing import List


class Solution:
    def solve(self, room_count: int, meetings: List[List[int]]) -> List[int]:
        room_free_at = [0] * room_count
        assignments: List[int] = []

        for start, end in meetings:
            assigned_room = -1
            for room in range(room_count):
                if room_free_at[room] <= start:
                    assigned_room = room
                    room_free_at[room] = end
                    break
            assignments.append(assigned_room)

        return assignments
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × room_count)`

Each of the `m` requests scans up to `room_count` rooms; the worst case (every request rejected) pays the full scan every time.

##### Space Complexity: `O(room_count)`

The `room_free_at` array holds one entry per room, independent of the number of requests.

#### Key Insights

- The problem statement is already an algorithm: input order is start order, and "lowest-numbered available room" is a number-ordered scan with an early break.
- The half-open interval convention puts the availability boundary at `<=`: Example 2 rejects `[2,3)` against a room ending at `4`, then accepts `[4,5)` at that same boundary.
- A rejected request must leave all state untouched; recording `-1` and continuing is the entire rejection logic.
- Correct but quadratic: with `m` and `room_count` both up to `10^5`, the scan can execute `10^10` room checks, which is what the heap version below removes.

### Free and Busy Min-Heaps

#### Derivation

The scan wastes its time in two ways: it re-tests rooms that are still busy, and it re-finds the lowest-numbered free room from scratch. Both are minimum-finding jobs over a changing set, which is what a [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) answers in `O(log room_count)`. Split the rooms into two heaps that together hold every room exactly once: `free_rooms`, ordered by room number, and `busy_rooms`, ordered by end time. A tempting shortcut is a single heap of `(end, room)` pairs, but it hands back the room that frees *soonest*, not the lowest-numbered *available* room: in Example 1 at request `(10,12)` both rooms are free, that heap would pop room 1 (end `7`) and return `1` where the expected output is `0`. Keeping the free set keyed by room number is the fix:

1. Initialize `free_rooms` with every room number and heapify it; start `busy_rooms` empty, holding `(end, room)` pairs for meetings in flight.
2. For each request `[start, end)`, first release: pop every `(end_time, freed_room)` from `busy_rooms` while `end_time <= start`, pushing each `freed_room` back onto `free_rooms`.
3. If `free_rooms` is non-empty, pop its smallest room number, record it, and push `(end, assigned_room)` onto `busy_rooms`.
4. Otherwise record `-1`; nothing moves in either heap.

Each request moves rooms only across the two heaps, and each room crosses at most once per request, so the per-request cost is a handful of logarithmic heap operations instead of a linear scan.

#### Invariant

At the start of each request iteration, the room numbers are partitioned between the two heaps, and membership in `free_rooms` is exactly the availability the current request tests:

$$ \text{rooms}(\text{busy\_rooms}) \sqcup \text{free\_rooms} = \{0, 1, \ldots, \text{room\_count} - 1\} $$

```text
rooms(busy_rooms) disjoint-union free_rooms = {0, 1, ..., room_count - 1}
free_rooms  = rooms whose latest meeting ends at or before the current start
busy_rooms  = the remaining rooms, keyed by the end of their latest meeting
```

The release loop preserves the partition in both directions: a room leaves `busy_rooms` exactly when its end has fallen to `start` or below, which is precisely the condition for joining `free_rooms`. The assign branch moves one room from `free_rooms` to `busy_rooms` under its new end, re-classifying it for later starts. The reject branch moves nothing, honoring the rule that a rejected request reserves no room. Every assigned value in `assignments` was therefore popped from `free_rooms`, so the lowest-numbered free room was chosen at every step.

#### Walkthrough

Run the two heaps on Example 1: `roomCount = 2`, `meetings = [[0,10],[5,7],[10,12],[10,15]]`. Each row shows the release phase, then the assignment, with `free` listed in priority order:

```text
free = [0, 1]                 busy = []
(0,10)    no releases         free = [1]      busy = [(10,0)]   -> 0
(5,7)     (10,0): 10 > 5      free = []       busy = [(7,1), (10,0)]   -> 1
(10,12)   release (7,1), then (10,0)
          free = [1, 0]       busy = []
          pop lowest: 0       free = [1]      busy = [(12,0)]   -> 0
(10,15)   (12,0): 12 > 10     free = []       busy = [(12,0), (15,1)]  -> 1
```

The decisive row is `(10,12)`: both rooms qualify, the release loop pushes `1` first and `0` second, and `free_rooms`, being keyed by room number, still pops `0`. This is the beat where the single-heap shortcut would have returned `1`. The assignments `[0, 1, 0, 1]` match the expected Output for Example 1. (Example 3 rejects its third request: `busy = [(2,0), (2,1)]` has both ends above `start = 1`, nothing releases, and `free` is empty, so `-1` is recorded with the heaps untouched.)

#### Solution

The code is the walkthrough's per-request rhythm: release everything that has ended, then pop the lowest-numbered free room or record `-1`.

```python
import heapq
from typing import List, Tuple


class Solution:
    def solve(self, room_count: int, meetings: List[List[int]]) -> List[int]:
        free_rooms = list(range(room_count))
        heapq.heapify(free_rooms)
        busy_rooms: List[Tuple[int, int]] = []
        assignments: List[int] = []

        for start, end in meetings:
            while busy_rooms and busy_rooms[0][0] <= start:
                _, freed_room = heapq.heappop(busy_rooms)
                heapq.heappush(free_rooms, freed_room)

            if free_rooms:
                assigned_room = heapq.heappop(free_rooms)
                assignments.append(assigned_room)
                heapq.heappush(busy_rooms, (end, assigned_room))
            else:
                assignments.append(-1)

        return assignments
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m log room_count)`

Across the whole run each meeting is pushed onto and popped from `busy_rooms` once, each room enters `free_rooms` at most once per pass, and every heap operation costs `O(log room_count)` on heaps bounded by `room_count` entries.

##### Space Complexity: `O(room_count)`

The two heaps hold each room exactly once between them, regardless of how many requests flow through.

#### Key Insights

- Splitting "which rooms are free" from "which rooms are busy" lets each heap carry the ordering the problem actually asks for: room numbers for choosing, end times for releasing.
- The single-heap shortcut fails because "soonest-ending" and "lowest-numbered" are different orders; Example 1's third request is the counterexample that separates them.
- The release-then-assign order matters: releasing before the availability test is what makes a room ending exactly at `start` available, per the half-open interval rule.
- Rejections are free: with both heaps unchanged, a `-1` costs only the release attempt, which is amortized away by the rooms it frees.

## Comparison of Solutions

### Time Complexity

- **First-Fit Room Scan**: `O(m × room_count)` - up to a full room scan per request.
- **Free and Busy Min-Heaps**: `O(m log room_count)` - a constant number of logarithmic heap operations per request, with releases amortized across the run.

### Space Complexity

- **First-Fit Room Scan**: `O(room_count)` - one availability entry per room.
- **Free and Busy Min-Heaps**: `O(room_count)` - each room lives in exactly one of the two heaps.

### Trade-offs

- **First-Fit Room Scan** is a direct transcription of the rules and trivially correct, but it pays linear work per request and collapses at the stated constraints.
- **Free and Busy Min-Heaps** handles the full constraint range comfortably, at the cost of two coordinated heaps and the discipline of keeping their partition intact; the "lowest-numbered free room" rule is also the one detail a heap translation can silently get wrong.

### When to Use Each

- **First-Fit Room Scan**: to establish the semantics on small inputs, as a correctness cross-check, or whenever `room_count` is small enough that the scan is harmless.
- **Free and Busy Min-Heaps (Recommended)**: the interview answer for the stated constraints: it is the only approach that scales to `10^5` rooms and `10^5` requests.

### Optimization Notes

- The two-heap design is the payoff of asking what each linear scan computes: the busy-room heap answers "what has ended by now", and the free-room heap answers "which of those has the lowest number", each in logarithmic time.
- Release before assigning: doing the release loop first is what makes the `end_time <= start` boundary case (Example 2's `[4,5)`) work without special-casing.
- The release loop is amortized, not free per iteration: every `(end, room)` pair is pushed and popped exactly once over the whole run, so the total release cost is `O(m log room_count)` and not `O(m × room_count log room_count)`.
- If the variant ever asks for the *soonest-ending* free room instead of the lowest-numbered one, only the free heap's key changes; the release loop and the partition invariant stay as they are.
