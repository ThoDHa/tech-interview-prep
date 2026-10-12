# [Select Least Resource Tasks](https://www.fastprep.io/problems/amazon-select-least-resource-tasks)

**unknown difficulty** | **NN minutes** | **unknown categories**

Amazon's Elastic Container Service schedules tasks dynamically. You are given an integer array resourceConsumption, where resourceConsumption[i] is the resource consumption of one task.

Repeat the following process until no tasks remain:

Select the remaining task with the lowest resource consumption. If multiple tasks have the same lowest value, select the one with the smallest current index.Add the selected task's resource consumption to the total.Remove the selected task and its adjacent remaining tasks, if they exist.Return the total resource consumption of all selected tasks.

Complete the function selectLeastResourceTasks, which receives resourceConsumption and returns the total as an int.

## Examples

### Example 1

**Input:** `resourceConsumption = [4, 3, 2, 1]`

**Output:** `4`

**Explanation:** The lowest value is 1, so it is selected and removed with its left neighbor 2. The remaining tasks are [4, 3]. Next, 3 is selected and removed with 4. The total is 1 + 3 = 4.

### Example 2

**Input:** `resourceConsumption = [6, 4, 9, 10, 34, 56, 54]`

**Output:** `68`

**Explanation:** First select 4 and remove it with adjacent values 6 and 9. The remaining tasks are [10, 34, 56, 54]. Next select 10 and remove 10 and 34. Finally select 54 and remove 56 and 54. The total selected consumption is 4 + 10 + 54 = 68.

## Constraints

- `3 <= n <= 2000`
- `1 <= resourceConsumption[i] <= 10^5`

## Solutions

### List Simulation

#### Derivation

The most literal reading of the problem is to run the process exactly as the statement describes: hold the remaining tasks in a list, find the lowest-consumption task, add it to the total, and cut it and its neighbors out. Python list deletion splices a contiguous slice in one operation, which matches the removal rule perfectly:

1. Copy `resourceConsumption` into `remaining` so the input stays untouched.
2. While `remaining` is non-empty, find `lowest_position`, the position of the
   smallest value, breaking ties by smallest position (`min` over positions
   keyed by value returns the first minimum, which is the smallest index).
3. Add `remaining[lowest_position]` to `total`.
4. Delete the slice from `max(0, lowest_position - 1)` through
   `lowest_position + 1` inclusive, removing the task and its existing
   neighbors in one splice.
5. When the loop ends, return `total`.

#### Walkthrough

Example 2 removes three blocks of three, two, and two tasks:

```text
remaining = [6, 4, 9, 10, 34, 56, 54]   total = 0
round 1   min 4 at position 1           total = 4
          delete positions 0..2         remaining = [10, 34, 56, 54]
round 2   min 10 at position 0          total = 14
          delete positions 0..1         remaining = [56, 54]
round 3   min 54 at position 1          total = 68
          delete positions 0..1         remaining = []
return 68
```

Each round's `min` scan reads the list exactly as the scheduler would survey the fleet, and the splice models the neighbor removal without any index bookkeeping. The loop ends with `total = 68`, the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def selectLeastResourceTasks(self, resourceConsumption: List[int]) -> int:
        remaining = list(resourceConsumption)
        total = 0
        while remaining:
            lowest_position = min(range(len(remaining)),
                                  key=lambda position: remaining[position])
            total += remaining[lowest_position]
            del remaining[max(0, lowest_position - 1):lowest_position + 2]
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every round performs an `O(n)` minimum scan plus an `O(n)` slice deletion, and each round removes at least one task, so there are at most `n` rounds.

##### Space Complexity: `O(n)`

The `remaining` copy holds all tasks.

#### Key Insights

- The removal rule deletes a contiguous span of the surviving sequence, so a single slice deletion captures "the task and its adjacent remaining tasks" with no neighbor pointers.
- Taking the first minimum position automatically implements the tie rule (smallest current index), because deletions preserve the relative order of the survivors.
- Correct but quadratic: with `n` up to 2000 this stays fast enough, but the repeated minimum scans invite a better ordering.

### Sorted Greedy with Linked-List Neighbors

#### Derivation

The simulation re-finds the minimum every round, yet the selection order never depends on the removals: removing a block deletes elements but never reorders the survivors, so the tasks consumed in ascending `(value, index)` order would be selected in exactly that order if no removal ever interfered. The only interference is death: a task may already have been cut as the neighbor of an earlier-selected task, in which case the simulation would never have selected it. So the plan is to walk the tasks in sorted `(value, index)` order, skip the dead, and reproduce each removal instantly with a doubly linked list:

1. Build `left_neighbor` and `right_neighbor` arrays over positions, with
   `-1` marking the ends, plus `alive` flags.
2. Iterate `candidate` over positions sorted by
   `(resourceConsumption[position], position)`, the simulation's selection order.
3. Skip `candidate` when it is not `alive`: it died as someone's neighbor.
4. Otherwise add its consumption to `total`, kill the candidate and its
   current neighbors `left` and `right`, and splice the block out by linking
   `block_left` (the neighbor before `left`) directly to `block_right` (the
   neighbor after `right`).
5. Return `total`.

Why is the alive candidate always the one the simulation would pick? Every task earlier in the sorted order is dead by the time `candidate` is processed, so `candidate` holds the smallest `(value, index)` among the living, exactly the simulation's next selection; and any task skipped as dead was removed strictly earlier in the sorted walk, which is precisely the round in which the simulation removes it as a neighbor.

#### Walkthrough

Example 2 again. The sorted order by `(value, index)` is `4, 10, 54, 56, 34, 9, 6` at positions `1, 3, 6, 5, 4, 2, 0`. Initially `left_neighbor = [-1, 0, 1, 2, 3, 4, 5]` and `right_neighbor = [1, 2, 3, 4, 5, 6, -1]`:

```text
candidate 1 (value 4)    alive -> total = 4
          block spans positions 0..2, link -1 to 3:  left_neighbor[3] = -1
candidate 3 (value 10)   alive -> total = 14
          block spans positions 3..4, link -1 to 5:  left_neighbor[5] = -1
candidate 6 (value 54)   alive -> total = 68
          left = 5, right = -1, kill 5 and 6
candidate 5 (value 56)   dead, skip
candidate 4 (value 34)   dead, skip
candidate 2 (value 9)    dead, skip
candidate 0 (value 6)    dead, skip
return 68
```

The three alive candidates are exactly the three tasks the simulation selected, and the skips are exactly the tasks that died as neighbors. The walk returns `68`, the expected Output. (On Example 1 the walk selects `1` at position 3 and then `3` at position 1, both alive, for `total = 4`.)

#### Solution

```python
from typing import List


class Solution:
    def selectLeastResourceTasks(self, resourceConsumption: List[int]) -> int:
        task_count = len(resourceConsumption)
        left_neighbor = [position - 1 for position in range(task_count)]
        right_neighbor = [position + 1 if position + 1 < task_count else -1
                          for position in range(task_count)]
        alive = [True] * task_count
        total = 0
        for candidate in sorted(range(task_count),
                                key=lambda position: (resourceConsumption[position], position)):
            if not alive[candidate]:
                continue
            total += resourceConsumption[candidate]
            left = left_neighbor[candidate]
            right = right_neighbor[candidate]
            block_left = left_neighbor[left] if left != -1 else -1
            block_right = right_neighbor[right] if right != -1 else -1
            alive[candidate] = False
            if left != -1:
                alive[left] = False
            if right != -1:
                alive[right] = False
            if block_left != -1:
                right_neighbor[block_left] = block_right
            if block_right != -1:
                left_neighbor[block_right] = block_left
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the positions dominates; the greedy walk performs constant work per position (at most one block splice of pointer updates).

##### Space Complexity: `O(n)`

The two neighbor arrays, the `alive` flags, and the sorted position list each hold `n` entries.

#### Key Insights

- Selection order is stable under block removals: the sorted `(value, index)` sequence restricted to the living tasks is the simulation's schedule, so one sort replaces every minimum scan.
- The doubly linked list makes each three-task block removal `O(1)`: relinking the outer survivors is the entire cost of a deletion that a plain list would pay `O(n)` to perform.
- The `alive` check is what keeps the two orders honest: a dead candidate is skipped, never counted, and its death is backdated to the round that killed it.
- Equal values must be broken by original index in the sort, matching the tie rule; breaking them arbitrarily can select the wrong twin of a pair.

## Comparison of Solutions

### Time Complexity

- **List Simulation**: `O(n^2)` - up to `n` rounds, each an `O(n)` minimum scan plus an `O(n)` splice.
- **Sorted Greedy with Linked-List Neighbors**: `O(n log n)` - one sort dominates; every position costs constant work afterward.

### Space Complexity

- **List Simulation**: `O(n)` - the `remaining` copy of the tasks.
- **Sorted Greedy with Linked-List Neighbors**: `O(n)` - neighbor arrays, alive flags, and the sorted order.

### Trade-offs

- **List Simulation**: mirrors the statement so directly that correctness is immediate, but it pays for a full survey of the fleet on every round.
- **Sorted Greedy with Linked-List Neighbors**: pays one sort up front and then constant work per task, at the price of trusting an invariant (selection order survives removals) that takes a moment to prove.

### When to Use Each

- **List Simulation**: the right first move in an interview or on tiny inputs, and the reference implementation to test the faster version against.
- **Sorted Greedy with Linked-List Neighbors (Recommended)**: the production choice for the given `n <= 2000` and the only shape that scales to much larger fleets.

### Optimization Notes

- The sort key `(resourceConsumption[position], position)` encodes the tie rule in one expression; sorting only by value would misorder equal-value tasks.
- The splice must read `block_left` and `block_right` from the neighbor arrays before overwriting the `alive` flags, since the block boundaries are defined through the still-intact links.
- The greedy walk needs no heap: a heap would reinsert survivors lazily and still rely on the same alive check, while the sort fixes the entire order in one pass.
