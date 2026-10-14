# [Car Fleet](https://leetcode.com/problems/car-fleet/)

**Medium** | **25 minutes** | **Array, Stack, Sorting, Monotonic Stack**

**Pattern:** [Stack](../patterns/stack/intuition.md)

**Algorithm:** [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

**Practice:** [`practice/car_fleet/solution.py`](../../practice/car_fleet/solution.py)

There are `n` cars traveling to the same destination on a one-lane highway.

You are given two arrays of integers `position` and `speed`, both of length `n`. 
* `position[i]` is the position of the `ith car` (in miles)
* `speed[i]` is the speed of the `ith` car (in miles per hour)

The **destination** is at position `target` miles.

A car can **not** pass another car ahead of it. It can only catch up to another car and then drive at the same speed as the car ahead of it.

A **car fleet** is a non-empty set of cars driving at the same position and same speed. A single car is also considered a car fleet.

If a car catches up to a car fleet the moment the fleet reaches the destination, then the car is considered to be part of the fleet.

Return the number of **different car fleets** that will arrive at the destination.

## Examples

### Example 1

**Input:** `target = 10, position = [1,4], speed = [3,2]`

**Output:** `1`

**Explanation:** The cars starting at 1 (speed 3) and 4 (speed 2) become a fleet, meeting each other at 10, the destination.

### Example 2

**Input:** `target = 10, position = [4,1,0,7], speed = [2,2,1,1]`

**Output:** `3`

**Explanation:** The cars starting at 4 and 7 become a fleet at position 10. The cars starting at 1 and 0 never catch up to the car ahead of them. Thus, there are 3 car fleets that will arrive at the destination.

## Constraints

- `n == position.length == speed.length`.
- `1 <= n <= 100,000`
- `0 < target <= 1,000,000`
- `1 <= speed[i] <= 1,000,000`
- `0 <= position[i] < target`
- All the values of `position` are **unique**.

## Deriving the Solution

Cars on a one-lane road can never pass, so a faster car behind a slower one is absorbed at the catch-up moment and the two travel on as one fleet. The number of fleets that reach the target is therefore a property of the arrival times alone: sorting the cars by position and asking, for each car, whether it catches the fleet ahead of it. Every solution below reduces the problem to those arrival times; they differ in how the catch-up question is answered.

1. **Start literal.** Sort by position, then for each car walk backward through
   the cars ahead to find the first one it does not catch. Quadratic in the
   worst case of a long fleet chain: see [Stack of Fleets](#stack-of-fleets).
2. **Spot the waste.** Once a car catches a fleet, it inherits that fleet's
   arrival time, and the merged fleet's time is always the maximum seen so far.
   A merge can never make an earlier fleet later, so the whole scan needs to
   remember only one number.
3. **Compare arrival times, not trajectories.** Compute each car's time to
   target, `(target - position) / speed`; walking closest-to-target first, a car
   with a strictly larger time than the current fleet's time starts a new fleet,
   otherwise it merges. One pass, `O(n log n)` overall: see
   [Single-Pass Counter](#single-pass-counter).

## Solutions

### Stack of Fleets

#### Derivation

The literal simulation of "can I catch the fleet ahead?" tracks, for each car from the target backward, the fleet directly ahead of it. Catch physics: a car at `pos` with speed `spd` catches a fleet ahead whose arrival time is `t_ahead` exactly when its own arrival time `(target - pos) / spd` is `<= t_ahead` (if it never catches up before the target, it drives alone but arrives as part of the same stream only if it merges at or before the target). Keeping every distinct fleet's arrival time on a stack makes that comparison available for the car behind:

1. Sort the cars by starting position, closest to the target first.
2. For each car, compute `time = (target - position) / speed`.
3. If the fleet stack is empty, or `time > stack[-1]` (this car never catches
   the fleet directly ahead), push `time`: a new fleet is born.
4. Otherwise leave the stack alone: the car merges into the fleet ahead.
5. The stack depth at the end is the number of fleets.

#### Walkthrough

Trace the stack on Example 2: `target = 10`, `position = [4,1,0,7]`, `speed = [2,2,1,1]`, which the sort reorders to closest-first `[7, 4, 1, 0]`:

```text
car at 7  time = (10-7)/1 = 3.0   stack empty            push -> [3.0]
car at 4  time = (10-4)/2 = 3.0   3.0 <= 3.0, catch      stack [3.0]
car at 1  time = (10-1)/2 = 4.5   4.5 > 3.0, never       push -> [3.0, 4.5]
car at 0  time = (10-0)/1 = 10.0  10.0 > 4.5, never      push -> [3.0, 4.5, 10.0]
```

The car at `4` arrives at exactly `3.0`, the same moment as the fleet ahead, so per the problem's tie rule it joins that fleet and the stack does not grow. Two cars never catch anything and found fleets of their own. The stack holds three times, so three fleets arrive, matching the expected Output `3` for Example 2.

#### Solution

The code is the sorted walk with the fleet times kept on an explicit stack.

```python
from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        fleet_times = []
        for pos, spd in cars:
            time = (target - pos) / spd
            # Arriving after the fleet ahead means never catching it
            if not fleet_times or time > fleet_times[-1]:
                fleet_times.append(time)
        return len(fleet_times)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the walk over sorted cars with its constant-time stack peek is linear.

##### Space Complexity: `O(n)`

The sorted pairs and the stack of fleet times are both linear in the worst case (no fleet ever merges).

#### Key Insights

- Arrival times fully encode catch-ups: two cars merge iff the trailing one's
  time is `<=` the fleet time ahead.
- The tie rule lives in the comparison: `time > fleet_times[-1]` counts
  equal-time arrivals as merges, exactly as the problem demands.
- The stack never pops here, which hints that only the top (or, as the next
  solution shows, a single running maximum) is ever consulted.

### Single-Pass Counter

#### Derivation

The stack version pushes a time only when it exceeds the previous top, so the stack contents are, at every step, the running record of strictly increasing arrival times: each new top is a new maximum. A value that only ever needs the running maximum does not need a stack at all, just one accumulator:

1. Sort the cars by position, closest to the target first.
2. Keep `fleet_time`, the arrival time of the most recently founded fleet.
3. For each car's `time`: if `time > fleet_time`, increment `fleets` and set
   `fleet_time = time`; otherwise the car merges and nothing changes.

Because merges only ever lower a car's effective arrival time to the fleet time ahead, comparing against `fleet_time` (not the immediately preceding car's raw time) is what a merged chain requires: a car catching a fleet adopts the fleet's slower time.

#### Walkthrough

Trace the counter on Example 1: `target = 10`, `position = [1,4]`, `speed = [3,2]`, sorted closest-first as `[4, 1]`:

```text
                 fleet_time = 0.0   fleets = 0
car at 4  time = (10-4)/2 = 3.0    3.0 > 0.0   -> fleets = 1, fleet_time = 3.0
car at 1  time = (10-1)/3 = 3.0    3.0 > 3.0 is false -> merge, no change
```

The trailing car arrives at exactly `3.0` too, catching the leader at the destination, so it merges and `fleets` stays `1`, matching the expected Output `1` for Example 1. On Example 2 the same walk sets `fleet_time` to `3.0`, then `4.5`, then `10.0`, incrementing once per strict increase for a total of `3`.

#### Solution

The code is the walkthrough's sorted walk with the accumulator.

```python
from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        fleets = 0
        fleet_time = 0.0
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > fleet_time:
                fleets += 1
                fleet_time = time
        return fleets
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The position sort dominates; the scan itself is a single linear pass with constant work per car.

##### Space Complexity: `O(n)`

The sorted `(position, speed)` pairs; the accumulator itself is `O(1)`. (An index sort into a pre-existing pairing would make this `O(1)` auxiliary beyond the sort.)

#### Key Insights

- The stack of fleet times is, in disguise, a running maximum: seeing that lets
  the whole structure collapse into two scalars.
- Comparing raw times against `fleet_time` (the post-merge fleet speed) rather
  than the previous car's raw time is what makes merged chains count as one
  fleet.
- Python's `zip` pairs each car with its speed before sorting, so no separate
  index bookkeeping is needed.

## Comparison of Solutions

### Time Complexity

- **Stack of Fleets**: `O(n log n)` - the sort dominates the linear stack walk.
- **Single-Pass Counter**: `O(n log n)` - the sort dominates the linear scan.

### Space Complexity

- **Stack of Fleets**: `O(n)` - one stack entry per fleet in the no-merge worst case.
- **Single-Pass Counter**: `O(n)` for the sorted pairs, `O(1)` for the scan state.

### Trade-offs

- Both approaches share the same asymptotics; they differ in bookkeeping only.
- The stack keeps every fleet time, which generalizes to queries needing the
  full fleet profile (sizes, speeds, positions).
- The counter is the minimal state that answers the count, at the cost of
  discarding everything but that number.

### When to Use Each

- **Stack of Fleets**: When a follow-up needs the fleets themselves (their
  arrival times, membership counts), not just how many.
- **Single-Pass Counter**: When only the count is required, which is the
  problem as stated; the cleanest code wins (recommended here).

### Optimization Notes

- Sorting descending by position pairs each car with the fleet directly ahead
  of it; sorting ascending would pair it with the fleet behind, which answers
  nothing.
- Floats are safe here: division compares well at these magnitudes, and exact
  ties (catch at the target) need only `>` versus `<=` care, not epsilon logic.
- `zip(position, speed)` before sorting keeps each car's data together; sorting
  `position` alone would lose the speed pairing.
