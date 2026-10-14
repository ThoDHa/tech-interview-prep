# [Maximize Distance to the Closest Occupied Seat](https://www.fastprep.io/problems/amazon-maximize-distance-to-closest-person)

**Easy** | **NN minutes** | **Array, Two Pointers**

You are given an array seats, where seats[i] = 1 means seat i is occupied and seats[i] = 0 means it is empty. At least one seat is empty and at least one seat is occupied.

Choose an empty seat that maximizes its distance to the closest occupied seat, and return the zero-based index of that seat. If several seats have the same maximum distance, return the smallest index.

## Examples

### Example 1

**Input:** `seats = [1,0,0,0,1,1]`

**Output:** `2`

**Explanation:** Seat 2 is two positions from the nearest occupied seat. Every other empty seat is only one position away.

### Example 2

**Input:** `seats = [1,0,0,0]`

**Output:** `3`

**Explanation:** The last seat is three positions from the only occupied seat.

### Example 3

**Input:** `seats = [0,1]`

**Output:** `0`

**Explanation:** Seat 0 is the only empty seat.

### Example 4

**Input:** `seats = [1,0,0,1,0,0,1]`

**Output:** `1`

**Explanation:** Seats 1, 2, 4, and 5 all have nearest-person distance one, so the smallest index is returned.

## Constraints

- `2 <= seats.length <= 20000`
- `seats[i] is 0 or 1.`
- `At least one seat is empty.`
- `At least one seat is occupied.`
- `If several empty seats have the same best distance, return the smallest index.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the question is per seat: stand at every empty seat and look for the nearest occupied one. The distance to the nearest occupied seat is just the smaller of two independent searches, one walking left until it meets a `1` and one walking right until it meets a `1`. Comparing those distances over all empty seats and keeping the best answers the question directly:

1. Sweep every `seat_index`; skip occupied seats.
2. For an empty seat, walk `left` down from `seat_index - 1` to the first occupied
   seat and note the distance; then walk `right` up to the first occupied seat
   and keep the smaller of the two in `nearest_distance`.
3. When `nearest_distance` is strictly greater than `best_distance`, record it
   in `best_distance` and record `seat_index` in `best_seat`.
4. Return `best_seat`.

The strict `>` comparison is what makes ties resolve to the smallest index: a later seat matching the best distance never displaces it.

#### Walkthrough

Example 1: `seats = [1,0,0,0,1,1]`, occupied seats at `0`, `4`, `5`. Each empty seat runs one left scan and one right scan:

```text
seat 1: left  -> occupied 0 (1 away)   right -> occupied 4 (3 away)
        nearest_distance = min(1, 3) = 1    best = (seat 1, distance 1)
seat 2: left  -> occupied 0 (2 away)   right -> occupied 4 (2 away)
        nearest_distance = min(2, 2) = 2    best = (seat 2, distance 2)
seat 3: left  -> occupied 0 (3 away)   right -> occupied 4 (1 away)
        nearest_distance = min(3, 1) = 1    best stays (seat 2, distance 2)
return 2
```

Seat `2` reaches the maximum nearest-occupied distance `2` and the function returns `2`, matching the expected Output for Example 1.

#### Solution

The code is the per-seat double scan from the walkthrough, wrapped in the best-so-far comparison.

```python
from typing import List


class Solution:
    def solve(self, seats: List[int]) -> int:
        seat_count = len(seats)
        best_seat = -1
        best_distance = -1

        for seat_index in range(seat_count):
            if seats[seat_index] == 1:
                continue

            nearest_distance = seat_count
            for left in range(seat_index - 1, -1, -1):
                if seats[left] == 1:
                    nearest_distance = seat_index - left
                    break
            for right in range(seat_index + 1, seat_count):
                if seats[right] == 1:
                    nearest_distance = min(nearest_distance, right - seat_index)
                    break

            if nearest_distance > best_distance:
                best_distance = nearest_distance
                best_seat = seat_index

        return best_seat
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each of the up to `n` empty seats runs two scans that can each cross the whole array.

##### Space Complexity: `O(1)`

Only a handful of scalar trackers are kept; nothing scales with the input.

#### Key Insights

- The problem decomposes cleanly: nearest distance per seat, then a maximum over empty seats.
- Scanning left first and then right means the first occupied seat found in each direction is the nearest in that direction; no further scan is needed.
- The strict `>` when updating `best_distance` is the tie-break rule in disguise: equal-distance seats keep the earliest index.
- Correct but quadratic: on a `20000`-seat row with a long empty stretch, the scans re-walk occupied-seat positions the other seats already learned.

### Two-Pass Nearest Distance

#### Derivation

The brute force's flaw is that every seat re-walks ground other seats already covered. The nearest occupied seat to the left, for instance, is visible from a single left-to-right sweep: remember where the previous occupied seat sat, and each seat's left distance is just its position minus that memory. A right-to-left sweep does the same for the right side. With both arrays filled, the per-seat answer is one `min` of two lookups:

1. Sweep `seat_index` left to right with `previous_occupied` seeded at `-seat_count`
   (so seats before the first occupied one get a left distance larger than any real
   distance) and fill `distance_from_left[seat_index] = seat_index - previous_occupied`,
   refreshing `previous_occupied` at every occupied seat.
2. Sweep back right to left with `next_occupied` seeded at `2 * seat_count` and fill
   `distance_from_right[seat_index] = next_occupied - seat_index`.
3. Over all empty seats, take `nearest_distance = min(distance_from_left, distance_from_right)`,
   tracking `best_seat` with the same strict `>` comparison.
4. Return `best_seat`.

The two sentinel seeds make every seat's pair of distances well defined without a special case for the edge gaps: one side of the `min` is huge exactly where no occupied seat exists on that side.

#### Walkthrough

Example 4: `seats = [1,0,0,1,0,0,1]`, the tie-breaker input. The two sweeps fill one distance array each:

```text
left pass, previous_occupied starts at -7:
  i=0  occupied  previous_occupied = 0   distance_from_left = [0]
  i=1  empty     distance_from_left[1] = 1 - 0 = 1
  i=2  empty     distance_from_left[2] = 2 - 0 = 2
  i=3  occupied  previous_occupied = 3   distance_from_left[3] = 0
  i=4  empty     distance_from_left[4] = 4 - 3 = 1
  i=5  empty     distance_from_left[5] = 5 - 3 = 2
  i=6  occupied  previous_occupied = 6   distance_from_left[6] = 0
  distance_from_left  = [0, 1, 2, 0, 1, 2, 0]

right pass, next_occupied starts at 14:
  i=6  occupied  next_occupied = 6       distance_from_right[6] = 0
  i=5  empty     distance_from_right[5] = 6 - 5 = 1
  i=4  empty     distance_from_right[4] = 6 - 4 = 2
  i=3  occupied  next_occupied = 3       distance_from_right[3] = 0
  i=2  empty     distance_from_right[2] = 3 - 2 = 1
  i=1  empty     distance_from_right[1] = 3 - 1 = 2
  i=0  occupied  next_occupied = 0       distance_from_right[0] = 0
  distance_from_right = [0, 2, 1, 0, 2, 1, 0]

pick loop:
  seat 1: min(1, 2) = 1 > -1   best = (seat 1, distance 1)
  seat 2: min(2, 1) = 1        not strictly greater, best stays seat 1
  seat 4: min(1, 2) = 1        not strictly greater
  seat 5: min(2, 1) = 1        not strictly greater
return 1
```

All four empty seats tie at distance `1`, and the strict `>` comparison holds the sweep at the earliest of them: the function returns `1`, matching the expected Output for Example 4.

#### Solution

The code is the two sweeps plus the pick loop from the walkthrough.

```python
from typing import List


class Solution:
    def solve(self, seats: List[int]) -> int:
        seat_count = len(seats)
        distance_from_left = [0] * seat_count
        distance_from_right = [0] * seat_count

        previous_occupied = -seat_count
        for seat_index in range(seat_count):
            if seats[seat_index] == 1:
                previous_occupied = seat_index
            distance_from_left[seat_index] = seat_index - previous_occupied

        next_occupied = 2 * seat_count
        for seat_index in range(seat_count - 1, -1, -1):
            if seats[seat_index] == 1:
                next_occupied = seat_index
            distance_from_right[seat_index] = next_occupied - seat_index

        best_seat = -1
        best_distance = -1
        for seat_index in range(seat_count):
            if seats[seat_index] == 1:
                continue
            nearest_distance = min(distance_from_left[seat_index],
                                   distance_from_right[seat_index])
            if nearest_distance > best_distance:
                best_distance = nearest_distance
                best_seat = seat_index

        return best_seat
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear sweeps over the seats with constant work per seat.

##### Space Complexity: `O(n)`

Two distance arrays of one entry per seat.

#### Key Insights

- Each sweep needs only one piece of memory, the position of the last occupied seat seen, because "distance to nearest occupied seat on this side" is local to that memory.
- The sentinel seeds (`-seat_count` and `2 * seat_count`) make the edge gaps fall out of the arithmetic: an out-of-range side produces an impossibly large distance that the `min` discards.
- The per-seat answer is now a table lookup, which makes the tie-break logic a single strictly-greater comparison in one pass.
- The distance arrays are the approach's trade: linear extra space buys away all rescanning.

### One-Pass Gap Scan

#### Derivation

The distance arrays answer a per-seat question, but the maximum only ever lands at a few addresses: the ends of a run of empty seats, or its middle. A run of empty seats between occupied seats at positions `previous_occupied` and `next_occupied` is an interior gap: its best seat is the midpoint `(previous_occupied + next_occupied) // 2` (the smaller-indexed of the two middle seats when the gap has even length, exactly the index the tie-break prefers), worth `(next_occupied - previous_occupied) // 2`. A gap hanging off the left edge has no `previous_occupied`, so its best seat is the run's first seat with distance equal to the run length; a gap hanging off the right edge mirrors that. Scanning once and measuring each gap as it closes collects the maximum:

1. Sweep `seat_index` left to right, updating `previous_occupied` at every
   occupied seat.
2. On the first empty seat of a run, mark `run_start` and slide to the run's
   end; `run_end` is the last empty seat.
3. Left-edge gap (`previous_occupied == -1`): `candidate_seat = run_start`,
   `candidate_distance = run_end + 1 - run_start`.
   Interior gap: `candidate_seat = (previous_occupied + run_end + 1) // 2`,
   `candidate_distance = (run_end + 1 - previous_occupied) // 2`.
   Right-edge gap (the run ends at the array's last seat after at least one
   occupied seat): `candidate_seat = run_end`,
   `candidate_distance = run_end - previous_occupied`.
4. Replace `best_seat` only when `candidate_distance` is strictly greater, so
   ties keep the earliest gap's seat.
5. Return `best_seat`.

The midpoint floor and the tie-break interlock: for an interior gap the candidate `(previous_occupied + run_end + 1) // 2` is the leftmost of the two middle seats when the gap has even length, exactly the smaller index the problem demands, and the strict `>` keeps an earlier gap winning any distance tie between gaps.

#### Walkthrough

Example 1: `seats = [1,0,0,0,1,1]`. The scan closes exactly one gap:

```text
seats = [1,0,0,0,1,1]   seat_count = 6
i=0  occupied  previous_occupied = 0
i=1  gap starts  run_start = 1, slide to i=4 (occupied), run_end = 3
     interior gap between occupied 0 and upcoming 4:
       candidate_seat      = (0 + 3 + 1) // 2 = 2
       candidate_distance  = (4 - 0) // 2 = 2
     best_seat = 2, best_distance = 2
i=4  occupied  previous_occupied = 4
i=5  occupied  previous_occupied = 5
return 2
```

The interior midpoint lands on seat `2` at distance `2`, matching the expected Output for Example 1. The edge rules close the other examples: Example 2 (`seats = [1,0,0,0]`) opens with `previous_occupied = 0` and ends in a right-edge gap at `run_end = 3`, so `candidate_distance = 3 - 0 = 3` and the return is `3`; Example 3 (`seats = [0,1]`) opens with `previous_occupied == -1`, so the left-edge rule picks `candidate_seat = run_start = 0` at distance `1`.

#### Solution

The code is the gap-measuring scan from the walkthrough, with the three gap shapes as the three branches.

```python
from typing import List


class Solution:
    def solve(self, seats: List[int]) -> int:
        seat_count = len(seats)
        best_seat = 0
        best_distance = -1
        previous_occupied = -1
        seat_index = 0

        while seat_index < seat_count:
            if seats[seat_index] == 1:
                previous_occupied = seat_index
                seat_index += 1
                continue

            run_start = seat_index
            while seat_index < seat_count and seats[seat_index] == 0:
                seat_index += 1
            run_end = seat_index - 1

            if previous_occupied == -1:
                candidate_seat = run_start
                candidate_distance = run_end + 1 - run_start
            elif seat_index == seat_count:
                candidate_seat = run_end
                candidate_distance = run_end - previous_occupied
            else:
                candidate_seat = (previous_occupied + run_end + 1) // 2
                candidate_distance = (run_end + 1 - previous_occupied) // 2

            if candidate_distance > best_distance:
                best_distance = candidate_distance
                best_seat = candidate_seat

        return best_seat
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The scan advances `seat_index` at every step, occupied or empty, so each seat is examined a constant number of times.

##### Space Complexity: `O(1)`

Only scalar trackers survive between iterations; no auxiliary array exists.

#### Key Insights

- The maximum nearest distance lives at one of a run's edges or its middle, so measuring runs instead of seats collapses the work to one pass with no extra space.
- The interior formulas are the same fact twice: the midpoint seat `(previous_occupied + run_end + 1) // 2` sits at distance `(run_end + 1 - previous_occupied) // 2` from the nearest occupied side.
- The tie-break needs no extra logic beyond the strict `>` because gaps are measured left to right, so an earlier gap's equal-distance seat is recorded first.
- The three branch shapes (left edge, interior, right edge) are where correctness bugs concentrate; each is exercised by one of the page's examples.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - every empty seat runs two scans that can each traverse the array.
- **Two-Pass Nearest Distance**: `O(n)` - two distance sweeps plus one pick sweep.
- **One-Pass Gap Scan**: `O(n)` - one sweep that measures each gap as it closes.

### Space Complexity

- **Brute Force**: `O(1)` - scalar trackers only.
- **Two-Pass Nearest Distance**: `O(n)` - two distance arrays of one entry per seat.
- **One-Pass Gap Scan**: `O(1)` - scalar trackers only.

### Trade-offs

- **Brute Force**: the shortest idea to state and impossible to get wrong, but quadratic time makes it the liability on long rows.
- **Two-Pass Nearest Distance**: linear time with the simplest correctness argument among the fast versions, at the price of two auxiliary arrays.
- **One-Pass Gap Scan**: optimal time and constant space, but its correctness rests on three gap shapes and a midpoint tie-break that each need care.

### When to Use Each

- **Brute Force**: as the reference oracle while designing or testing; also fine when the seat count is tiny.
- **Two-Pass Nearest Distance (Recommended)**: the interview default: linear time, no recursion, and an argument you can defend in two sentences.
- **One-Pass Gap Scan**: when constant space matters or when the interviewer pushes past the two-pass answer; it also adapts naturally to streaming rows where the whole array is never held.

### Optimization Notes

- The tie-break rule ("smallest index wins") is carried entirely by the strict `>` comparison in every approach; weakening it to `>=` fails Example 4.
- In the two-pass version, the sentinel seeds `-seat_count` and `2 * seat_count` remove the edge-gap special cases; any value guaranteed to exceed every real distance works.
- In the one-pass version, prefer the branch order left edge, right edge, interior: the edge checks are cheaper than the midpoint arithmetic and each example pins one branch.
- A common pitfall in the one-pass scan is advancing `seat_index` inside the gap slide and then using the stale value; capture `run_end` before the pick logic reads it.
