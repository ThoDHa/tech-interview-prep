# [Maximum Concurrent Processes (Bar Raiser Round)](https://www.fastprep.io/problems/amazon-max-concurrent-processes)

**Medium** | **NN minutes** | **Intervals, Sorting**

🍇 FastPrep match note: This version is based on a reported Amazon SDE2 full-time onsite Bar Raiser round prompt and should match the core task about 90-95%: given process running intervals, return the maximum number running at the same time.

The main uncertainty is whether the original wording explicitly counted endpoints as running; the reported example only reaches 3 if time 3 belongs to both [1, 3] and [3, 6], so we make the inclusive endpoint rule explicit and add a few practice examples and constraints for clarity.

You are given a list of processes. Each process has a running interval represented as [start, end].

A process is considered running at every integer time from start through end, inclusive.

Return the maximum number of processes running at the same time.

## Examples

### Example 1

**Input:** `intervals = [[1, 3], [2, 5], [3, 6]]`

**Output:** `3`

**Explanation:** At time 3, all three processes are running. Since intervals are inclusive, both [1, 3] and [3, 6] include time 3.

### Example 2

**Input:** `intervals = [[1, 2], [3, 4], [5, 6]]`

**Output:** `1`

**Explanation:** No two processes overlap, so the maximum number of concurrent processes is 1.

### Example 3

**Input:** `intervals = [[1, 10], [2, 3], [4, 5], [6, 7]]`

**Output:** `2`

**Explanation:** The long-running process overlaps with each shorter process, but the shorter processes do not overlap with one another.

### Example 4

**Input:** `intervals = [[1, 4], [2, 6], [4, 8], [6, 9]]`

**Output:** `3`

**Explanation:** At time 4, [1, 4], [2, 6], and [4, 8] are all running because interval endpoints are inclusive.

## Constraints

- `1 <= intervals.length <= 100000`
- `0 <= start <= end <= 1000000000`
- `All start and end values are integers.`
- `Intervals are inclusive: [start, end].`

## Solutions

### Start-Time Pair Scan

#### Derivation

The running count cannot change except when a process begins or stops occupying time: it only ever rises at a start. Between those moments the count is constant, so the maximum over all integer times is attained at some process's `start`. That observation shrinks "the maximum number running at the same time" to a finite set of candidate instants, one per process, each checked against every interval:

1. Set `peak = 0`.
2. For each process's `start`, count the intervals whose
   `other_start <= start <= other_end` (the inclusive rule lives in the
   `<=` comparisons).
3. Raise `peak` to that count.
4. Return `peak`.

#### Walkthrough

Example 4 is the case that punishes treating endpoints as exclusive, so it is the one to trace:

```text
intervals = [[1,4], [2,6], [4,8], [6,9]]

start 1   [1,4] covers 1                                -> 1 running
start 2   [1,4] and [2,6] cover 2                       -> 2 running
start 4   [1,4], [2,6], and [4,8] all cover 4           -> 3 running
start 6   [2,6], [4,8], and [6,9] all cover 6           -> 3 running

peak = 3
```

The count of `3` at `start 4` is only correct because `1 <= 4 <= 4` holds for `[1, 4]`: an inclusive endpoint keeps a process running at its final instant. The function returns `3`, matching the expected Output for Example 4.

#### Solution

The code is the candidate loop with the membership count inlined.

```python
from typing import List


class Solution:
    def solve(self, intervals: List[List[int]]) -> int:
        """Return the maximum number of processes running at the same time.

        Time:  O(n^2): each of the n starts is checked against all n
            intervals.
        Space: O(1) beyond the input.
        """
        peak = 0
        for start, _ in intervals:
            running_at_start = sum(
                1
                for other_start, other_end in intervals
                if other_start <= start <= other_end
            )
            peak = max(peak, running_at_start)
        return peak
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each of the `n` candidate starts is tested against all `n` intervals with two comparisons per test.

##### Space Complexity: `O(1)`

Only `peak` and the per-candidate count are stored; the input is read in place.

#### Key Insights

- The maximum is always attained at some process's `start`, because the count only changes at starts (rising) and expiries (falling), so checking starts alone covers every candidate maximum.
- Both comparisons are `<=`: the inclusive-interval rule is exactly the difference between this problem and its half-open cousins.
- The scan is a natural oracle: every faster solution on this page must agree with it on every input, and a disagreement localizes the bug to a boundary rule.

### Event Sweep

#### Derivation

Checking every start re-counts overlapping processes from scratch. The count is really a step function on the timeline: it rises by one when a process begins occupying time and falls by one when it stops. The classic [sweep line](https://en.wikipedia.org/wiki/Sweep_line_algorithm) materializes that function: each process contributes a `+1` event at `start` and a `-1` event at `end + 1`, the first integer time it no longer covers. Sorting the events and walking them while tracking the running `depth` makes the answer the maximum depth:

1. Build `events`: `[start, 1]` and `[end + 1, -1]` for every process.
2. Sort `events` by time, with the delta ascending as the tie-break so a
   `-1` precedes a `+1` at the same event time.
3. Sweep: `depth += delta` per event, tracking `peak = max(peak, depth)`.
4. Return `peak`.

The tie-break is load-bearing here even though endpoints are inclusive: a process covering `[1, 4]` departs at event time `5`, the same instant a process starting at `5` arrives. Processing the arrival first would momentarily stack a departed process onto its successor and inflate `peak`; the ascending delta sorts `-1` before `+1` and gets the handoff right for free.

#### Invariant

After processing every event bearing a given event time `t`, `depth` equals the number of processes whose interval contains the integer time `t`:

```text
depth after all events at time t
    = (processes with start <= t) - (processes with end + 1 <= t)
    = the number of processes running at integer time t
```

Each event type preserves it: a `+1` at `start` records a process beginning to occupy time exactly then, and a `-1` at `end + 1` removes a process whose last occupied instant was `end`, so its removal is one tick late by design. The ascending-delta tie-break guarantees that within one event time the departure lands before the arrival, so no prefix of the group ever overstates the occupancy. Between consecutive event times the count is constant, and `depth` never exceeds the true maximum at any prefix, so the maximum over all prefixes equals the maximum over all times, which is the answer.

#### Walkthrough

Example 1 is the shared-endpoint case the inclusive rule creates; its `-1` events sit one tick past each `end`:

```text
intervals = [[1,3], [2,5], [3,6]]
events sorted: (1,+1) (2,+1) (3,+1) (4,-1) (6,-1) (7,-1)

(1,+1)   depth = 1
(2,+1)   depth = 2
(3,+1)   depth = 3   peak = 3   [1,3] still runs at time 3: its -1 waits at 4
(4,-1)   depth = 2
(6,-1)   depth = 1
(7,-1)   depth = 0
```

The peak of `3` is reached at time `3`, where all three intervals genuinely overlap under the inclusive rule; writing the departures at `end` instead of `end + 1` would have collapsed the peak to `2`. The function returns `3`, matching the expected Output for Example 1. On Example 2, the events sort to `(1,+1) (3,-1) (3,+1) (5,-1) (5,+1) (7,-1)` and the depth never exceeds `1`, matching its expected Output of `1` as well.

#### Solution

The code is the event list, the delta-keyed sort, and the depth walk.

```python
from typing import List


class Solution:
    def solve(self, intervals: List[List[int]]) -> int:
        """Return the maximum number of processes running at the same time.

        Time:  O(n log n): building the 2n events is linear and the sort
            dominates; the sweep is one pass.
        Space: O(n) for the event list.
        """
        events: List[List[int]] = []
        for start, end in intervals:
            events.append([start, 1])
            events.append([end + 1, -1])
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

The `2n` events are built in one pass and sorted once; the sweep is a linear walk.

##### Space Complexity: `O(n)`

The event list holds two entries per process.

#### Key Insights

- The sweep forgets the processes entirely: only the step function matters, which makes it the shortest correct formulation of the problem.
- `end + 1` is where the inclusive rule lives; it converts "occupies through `end`" into "departs before `end + 1`" without any special casing in the loop.
- The `(time, delta)` ascending sort encodes both boundary behaviors at once: shared endpoints keep the departed process counted (its event moved to `end + 1`), while exact handoffs like `[1, 4]` and `[5, 9]` retire before the newcomer arrives.
- Taking the maximum after every event is safe because the tie-break guarantees `depth` never overstates the true occupancy at any prefix.

### Sorted Starts Against Expiry Times

#### Derivation

The sweep sorts `2n` events, yet only two facts per process matter: when it starts and when it expires. Two sorted arrays of those facts, merged with one pointer, do the same work without an event list. Walking the `start_times` in order, every expiry time at or before the current `start` belongs to a process that has already stopped occupying time, so those are retired (each retirement drops `running` by one) before the new process raises the count:

1. Build `start_times`, all starts sorted, and `expiry_times`, all `end + 1`
   values sorted.
2. Walk `start_times` with `running = 0`, `expired_position = 0`, and
   `peak = 0`.
3. For each `start`: while `expiry_times[expired_position] <= start`, retire
   it (`expired_position` advances, `running` drops by one).
4. Then `running += 1` and raise `peak`; the answer is `peak`.

Retiring before counting is the same handoff discipline as the sweep's tie-break: a process expiring exactly at `start` must not be counted as concurrent with the process beginning at `start`.

#### Walkthrough

Example 4 again, where the pointer work is visible:

```text
start_times  = [1, 2, 4, 6]      expiry_times = [5, 7, 9, 10]

start 1   no expiry <= 1                    running 1   peak 1
start 2   no expiry <= 2                    running 2   peak 2
start 4   no expiry <= 4                    running 3   peak 3
start 6   expiry 5 <= 6: retire             running 2
          expiry 7 > 6: stop                running 3   peak 3
```

At `start 6`, the retirement of expiry `5` removes `[1, 4]` (which stopped occupying time after `4`), while `[2, 6]`, `[4, 8]`, and `[6, 9]` all contain `6`, so the count climbs back to `3`. The function returns `3`, matching the expected Output for Example 4.

#### Solution

The code is the two arrays, the retirement loop, and the count.

```python
from typing import List


class Solution:
    def solve(self, intervals: List[List[int]]) -> int:
        """Return the maximum number of processes running at the same time.

        Time:  O(n log n): two sorts dominate; the merge walk retires each
            expiry at most once across the whole run.
        Space: O(n) for the two sorted arrays.
        """
        start_times = sorted(interval[0] for interval in intervals)
        expiry_times = sorted(interval[1] + 1 for interval in intervals)

        running = 0
        expired_position = 0
        peak = 0
        for start in start_times:
            while (expired_position < len(expiry_times)
                   and expiry_times[expired_position] <= start):
                expired_position += 1
                running -= 1
            running += 1
            peak = max(peak, running)
        return peak
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the two arrays dominates; the walk performs at most `2n` pointer steps in total, since `expired_position` only ever advances.

##### Space Complexity: `O(n)`

The `start_times` and `expiry_times` arrays each hold `n` values.

#### Key Insights

- Sorting starts and expiries independently destroys process identity, and nothing is lost: concurrency is a property of the two timelines.
- Storing `end + 1` in `expiry_times` is the one place the inclusive rule appears; the loop body then uses a plain `<=` with no special case.
- The retirement loop is monotone, so the whole merge is linear after sorting: this is the event sweep with the per-process event pairs collapsed into two sorted columns.

## Comparison of Solutions

### Time Complexity

- **Start-Time Pair Scan**: `O(n²)` - every candidate start is counted against every interval.
- **Event Sweep**: `O(n log n)` - one sort of `2n` events, then a linear walk.
- **Sorted Starts Against Expiry Times**: `O(n log n)` - two sorts, then a linear merge with a monotone pointer.

### Space Complexity

- **Start-Time Pair Scan**: `O(1)` - only counters, reading the input in place.
- **Event Sweep**: `O(n)` - two events per process.
- **Sorted Starts Against Expiry Times**: `O(n)` - one sorted array per timeline.

### Trade-offs

- **Start-Time Pair Scan**: the problem stated as a definition and a reliable oracle for the faster variants, at a quadratic price.
- **Event Sweep**: one uniform event formulation whose tie rule carries both boundary behaviors, but it allocates and sorts `2n` records.
- **Sorted Starts Against Expiry Times**: the same linearithmic bound with half the records and a tighter constant, at the cost of reasoning about retire-before-count ordering instead of an explicit event list.

### When to Use Each

- **Start-Time Pair Scan**: tiny inputs, or as the cross-check the linearithmic solutions must agree with.
- **Event Sweep** (Recommended): the interview default: it generalizes directly to weighted or streaming variants, and the invariant is one sentence.
- **Sorted Starts Against Expiry Times**: when only the count is needed and the leaner two-array form reads better, or when the event list's allocation matters.

### Optimization Notes

- Moving the departure to `end + 1` is the whole inclusive-endpoint fix: writing `(end, -1)` returns `2` on Example 1 where the expected Output is `3`.
- The ascending-delta tie sort is equally load-bearing: with arrivals processed before departures at the same event time, a handoff like `[1, 4]` and `[5, 9]` momentarily reports two running processes that never coexisted.
- Coordinates reach `10^9`, which rules out arrays indexed by time; every linear-time-in-span idea must become an event list, a coordinate compression, or a two-pointer merge.
- All three solutions must agree on every input; a disagreement almost always localizes to a `<=` versus `<` comparison or to where the `+ 1` was applied.
