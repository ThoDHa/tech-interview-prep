# [Capacity To Ship Packages Within D Days](https://www.fastprep.io/problems/amazon-capacity-to-ship-packages-within-d-days)

**Medium** | **NN minutes** | **Array, Binary Search**

A conveyor belt has packages that must be shipped from one port to another within days days.

The i-th package has weight weights[i]. Packages are loaded in the given order: you may not rearrange them. Each day, you load the conveyor with packages whose total weight does not exceed the ship's capacity, then ship that day's load.

Return the least ship capacity that can move every package within days days.

## Examples

### Example 1

**Input:** `weights = [1,2,3,4,5,6,7,8,9,10]`, `days = 5`

**Output:** `15`

**Explanation:** Capacity 15 ships as [1,2,3,4,5], [6,7], [8], [9], and [10]. Capacity 14 needs more than 5 days.

### Example 2

**Input:** `weights = [3,2,2,4,1,4]`, `days = 3`

**Output:** `6`

**Explanation:** Capacity 6 ships as [3,2], [2,4], and [1,4].

## Constraints

- `1 <= weights.length <= 5 * 10^4.`
- `1 <= weights[i] <= 500.`
- `1 <= days <= weights.length.`

## Solutions

### Linear Capacity Scan

#### Derivation

The most literal reading tries capacities in increasing order and returns the first one
that ships everything in time. Where does the line start? The heaviest package needs a
day of its own at best, so no capacity below `max(weights)` can ever work. What does one
candidate cost? Exactly what the problem describes: load packages in the given order,
close the day the moment the next package would overflow, and count the days this greedy
packing needs:

1. Set `capacity = max(weights)`, the smallest candidate that can carry the heaviest
   package.
2. Compute `shipping_days(weights, capacity)`: walk `weights` in order keeping the
   running `current_load`; when `current_load + weight` would exceed `capacity`, close
   the day and start a new one holding `weight` alone.
3. While `shipping_days(weights, capacity) > days`, increment `capacity` by one.
4. Return the first `capacity` whose day count fits within `days`.

The loop terminates: at `capacity = sum(weights)` every package fits into one day, and
one day is always within `days`.

#### Walkthrough

Trace the scan on Example 2: `weights = [3,2,2,4,1,4]`, `days = 3`. Each row shows the
probed capacity, the greedy day loads it produces, and whether the day count fits:

```text
capacity=4   [3] [2,2] [4] [1] [4]     5 days   5 <= 3? no
capacity=5   [3,2] [2] [4,1] [4]       4 days   4 <= 3? no
capacity=6   [3,2] [2,4] [1,4]         3 days   3 <= 3? yes -> return 6
```

Capacity 6 packs the loads `[3,2]`, `[2,4]`, and `[1,4]`, the exact split from the
example's explanation, and its count of 3 is the first to fit within `days = 3`, so the
scan returns `6`, matching the expected Output.

#### Solution

The code is the walkthrough's probe: the greedy packing helper plus the unit-step scan.

```python
from typing import List


def shipping_days(weights: List[int], capacity: int) -> int:
    """Days needed to ship `weights` in order when each day's load stays within `capacity`."""
    total_days = 1
    current_load = 0
    for weight in weights:
        if current_load + weight > capacity:
            total_days += 1
            current_load = weight
        else:
            current_load += weight
    return total_days


class Solution:
    def solve(self, weights: List[int], days: int) -> int:
        capacity = max(weights)
        while shipping_days(weights, capacity) > days:
            capacity += 1
        return capacity
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × m)`

`n` is the package count and `m` is the number of probed capacities, the answer minus
`max(weights)`; every probe is an `O(n)` greedy pass.

##### Space Complexity: `O(1)`

Only the running load, the day counter, and the probe capacity are stored.

#### Key Insights

- The package order is fixed, so a day's load is forced: the greedy packing leaves no
  choice to optimize, and the only question is how many days the forced packing takes.
- Feasibility is monotone in capacity: raising it can only merge day loads, never split
  them. The scan climbs this monotone slope one unit at a time, which is correct but
  slow.
- Starting at `max(weights)` is a correctness requirement, not an optimization: below it
  the heaviest package cannot ship, and the greedy day count stops meaning anything.

### Binary Search on the Answer

#### Derivation

The scan's failure is not its feasibility test but its stride: it probes
`capacity + 1` after learning everything `capacity` could teach. Because raising a
capacity can only merge day loads, `shipping_days` never grows as `capacity` grows, so
the capacities that finish within `days` form a suffix of the line
`[max(weights), sum(weights)]`. Finding the left edge of a monotone suffix is exactly
what [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) does, the
same move [Koko Eating Bananas](../koko_eating_bananas.md) makes over eating rates:

1. Bracket the answer: `left = max(weights)` (the smallest meaningful capacity) and
   `right = sum(weights)` (always feasible: one day carries everything).
2. While `left < right`, probe `mid = (left + right) // 2`.
3. If `shipping_days(weights, mid) <= days`, the answer is `mid` or anything larger:
   keep it, `right = mid`.
4. Otherwise `mid` spreads the packages over too many days: `left = mid + 1`.
5. When `left == right`, the bracket has collapsed onto the least workable capacity:
   return `left`.

#### Walkthrough

Trace the search on Example 1: `weights = [1,2,3,4,5,6,7,8,9,10]`, `days = 5`. The
bracket starts at `left = 10`, `right = 55`; each row is one probe with its greedy day
loads:

```text
left=10  right=55  mid=32   [1,2,3,4,5,6,7] [8,9,10]          2 days  2 <= 5? yes -> right=32
left=10  right=32  mid=21   [1,2,3,4,5,6] [7,8] [9,10]        3 days  3 <= 5? yes -> right=21
left=10  right=21  mid=15   [1,2,3,4,5] [6,7] [8] [9] [10]    5 days  5 <= 5? yes -> right=15
left=10  right=15  mid=12   [1,2,3,4] [5,6] [7] [8] [9] [10]  6 days  6 <= 5? no  -> left=13
left=13  right=15  mid=14   [1,2,3,4] [5,6] [7] [8] [9] [10]  6 days  6 <= 5? no  -> left=15
left=15  right=15  loop ends -> return 15
```

The feasible probe at `mid = 15` produced the split `[1,2,3,4,5]`, `[6,7]`, `[8]`,
`[9]`, `[10]`, exactly the schedule in the example's explanation, and the two
infeasible probes proved everything from 10 to 14 needs six days (the day count only
shrinks as capacity grows). The collapsed bracket returns `15`, matching the expected
Output.

#### Solution

The code is the walkthrough's bracket, probe, and collapse, with `shipping_days` as its
own helper since it is the invariant both this solution and the linear scan share.

```python
from typing import List


def shipping_days(weights: List[int], capacity: int) -> int:
    """Days needed to ship `weights` in order when each day's load stays within `capacity`."""
    total_days = 1
    current_load = 0
    for weight in weights:
        if current_load + weight > capacity:
            total_days += 1
            current_load = weight
        else:
            current_load += weight
    return total_days


class Solution:
    def solve(self, weights: List[int], days: int) -> int:
        left, right = max(weights), sum(weights)
        while left < right:
            mid = (left + right) // 2
            if shipping_days(weights, mid) <= days:
                right = mid
            else:
                left = mid + 1
        return left
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log s)`

`s = sum(weights)` sizes the bracket, so the search makes `O(log s)` probes and each
probe is an `O(n)` greedy pass. At the constraint sizes (`5 × 10^4` packages of weight
up to `500`) that is a few million operations.

##### Space Complexity: `O(1)`

Only the bracket boundaries and the probe's running load are stored.

#### Key Insights

- The search runs over the answer space, not the input: `weights` is never sorted or
  indexed by the search, only fed to the feasibility probe.
- The probe must test `<= days`: finishing in exactly `days` days is on time, and that
  boundary is the whole answer for Example 1.
- `max(weights)` and not `1` is the honest lower bracket: the heaviest package has to
  fit somewhere, no matter how many days are available.
- This is the same binary search on a monotone predicate as
  [Koko Eating Bananas](../koko_eating_bananas.md): a threshold hides in the problem, a
  greedy test reads it, and the search halves the candidate line per probe.

## Comparison of Solutions

### Time Complexity

- **Linear Capacity Scan**: `O(n × m)` - every capacity below the answer is probed in
  full, each probe an `O(n)` pass.
- **Binary Search on the Answer**: `O(n log s)` - `O(log s)` probes over a bracket
  sized by `s = sum(weights)`, each probe `O(n)`.

### Space Complexity

- **Linear Capacity Scan**: `O(1)` - probe capacity, day counter, and running load.
- **Binary Search on the Answer**: `O(1)` - bracket boundaries and the probe's load.

### Trade-offs

- Both solutions share the same greedy feasibility test and constant space; the stride
  is the only difference.
- The scan is genuinely simple, but the answer can sit tens of thousands of capacity
  units above `max(weights)`, so the unit stride is not usable at the constraint sizes.
- The binary search pays only the bracket invariant (`right` always holds a feasible
  capacity, everything below `left` is ruled out) and gains orders of magnitude.

### When to Use Each

- **Linear Capacity Scan**: as a correctness oracle when testing the real solution, on
  inputs small enough to finish.
- **Binary Search on the Answer (Recommended)**: always in practice; it is the
  interview answer and the one that scales.

### Optimization Notes

- The greedy pass is the shared engine: keep it in one helper so both search
  strategies call the same, tested code.
- `(left + right) // 2` cannot overflow in Python, but in fixed-width languages
  compute `mid` as `left + (right - left) // 2`.
- The `<=` in the probe is load-bearing: switching it to `<` makes exact-`days`
  schedules look infeasible and walks the answer one step too high.
