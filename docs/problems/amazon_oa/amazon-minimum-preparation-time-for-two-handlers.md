# [Minimum Preparation Time for Two Handlers](https://www.fastprep.io/problems/amazon-minimum-preparation-time-for-two-handlers)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

A work queue workList must be processed in order by two handlers. Each value in workList is a work type from 1 through m.

For work type t, the first time a handler processes that type, or whenever the handler's previous job was a different type, that handler pays longPrepTime[t]. If the handler's previous job was the same type, that handler pays shortPrepTime[t] instead.

Each job must be assigned to exactly one of the two handlers, and jobs must be processed in the order they appear. Return the minimum total preparation time.

## Examples

### Example 1

**Input:** `workList = [1, 2, 2]`, `longPrepTime = [4, 5]`, `shortPrepTime = [2, 3]`

**Output:** `12`

**Explanation:** Assign work type 1 to the first handler, then assign both type-2 jobs to the second handler. The total cost is 4 + 5 + 3 = 12.

### Example 2

**Input:** `workList = [1, 1, 1]`, `longPrepTime = [4]`, `shortPrepTime = [2]`

**Output:** `8`

**Explanation:** Use the same handler for all three jobs to pay one long preparation and two short preparations.

## Constraints

- `workList[i] identifies a work type between 1 and m`
- `longPrepTime and shortPrepTime contain one entry per work type.`
- `Jobs must be processed in order.`

## Solutions

### Assign Every Job to Both Handlers

#### Derivation

The most literal search branches per job: the next job goes to handler A or handler B, and each branch's cost follows the rule (short preparation when the handler's own previous job had the same type, long otherwise). A recursion over job index, handler A's last type, and handler B's last type explores every assignment:

1. Recurse from job 0 with both handlers idle.
2. At each job, price giving it to either handler and branch.
3. Return the cheapest complete assignment.

#### Walkthrough

Example 1, `workList = [1, 2, 2]`: giving job 0 to A costs the long time 4; giving both type-2 jobs to B costs 5 then the short time 3, total `4 + 5 + 3 = 12`. Any split of the type-2 pair across handlers pays the long time twice (5 and 5), totaling at least 14, so 12 wins, matching the expected output. Example 2, `[1, 1, 1]`: one handler runs all three jobs for `4 + 2 + 2 = 8`.

#### Solution

```python
from typing import List, Optional, Tuple


class Solution:
    def solve(
        self,
        workList: List[int],
        longPrepTime: List[int],
        shortPrepTime: List[int],
    ) -> int:
        """Return the minimum total preparation time over all assignments.

        Time:  O(2^n): one branch per job and handler.
        Space: O(n) recursion depth.
        """

        def explore(
            index: int,
            last_a: Optional[int],
            last_b: Optional[int],
        ) -> int:
            if index == len(workList):
                return 0
            work_type = workList[index] - 1
            cost_a = (
                shortPrepTime[work_type]
                if last_a == work_type
                else longPrepTime[work_type]
            )
            cost_b = (
                shortPrepTime[work_type]
                if last_b == work_type
                else longPrepTime[work_type]
            )
            return min(
                cost_a + explore(index + 1, work_type, last_b),
                cost_b + explore(index + 1, last_a, work_type),
            )

        return explore(0, None, None)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Two branches per job; only toy queues run this rung.

##### Space Complexity: `O(n)`

The recursion depth.

#### Key Insights

- Each handler's cost depends only on its own previous job type; the two handlers are interchangeable otherwise.
- The brute force is the oracle for the memoized rung.

### Memoized Pair State

#### Derivation

The branching tree repeats states: what matters after a prefix of jobs is the pair (handler A's last type, handler B's last type), and the number of reachable pairs per index is at most `m^2` (work types 1..m, plus idle). Memoizing on `(index, last_a, last_b)` collapses the exponential tree onto those states, and each state does constant work:

1. Memoize the recursion on the triple.
2. The last type of only one handler changes per step, so transitions stay `O(1)` per branch.

#### Walkthrough

Example 1 again: at index 1 the states reached are `(A=1, B=idle)` and `(A=idle, B=1)`, symmetric twins costing identically from then on; the memo returns the second one's answer from the first's computation. The answer path is the same 12 as the brute force.

#### Solution

```python
from functools import lru_cache
from typing import List, Optional


class Solution:
    def solve(
        self,
        workList: List[int],
        longPrepTime: List[int],
        shortPrepTime: List[int],
    ) -> int:
        """Return the minimum total preparation time over all assignments.

        Time:  O(n * m^2): each (index, last_a, last_b) state computed once.
        Space: O(n * m^2) for the memo table.
        """

        @lru_cache(maxsize=None)
        def explore(
            index: int,
            last_a: int,
            last_b: int,
        ) -> int:
            if index == len(workList):
                return 0
            work_type = workList[index] - 1
            cost_a = (
                shortPrepTime[work_type]
                if last_a == work_type
                else longPrepTime[work_type]
            )
            cost_b = (
                shortPrepTime[work_type]
                if last_b == work_type
                else longPrepTime[work_type]
            )
            return min(
                cost_a + explore(index + 1, work_type, last_b),
                cost_b + explore(index + 1, last_a, work_type),
            )

        return explore(0, -1, -1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * m^2)`

At most `m + 1` values per handler slot (m types plus the idle marker) and one index dimension; two transitions per state.

##### Space Complexity: `O(n * m^2)`

The memo table plus recursion depth.

#### Key Insights

- The idle marker (`-1`) never equals a work type, so the first job per handler always pays the long time.
- Because jobs arrive in order, the index alone fixes the future; the pair state is the only history needed.

## Comparison of Solutions

### Time Complexity

- **Assign Every Job to Both Handlers**: `O(2^n)` - the definition as a search.
- **Memoized Pair State**: `O(n * m^2)` - polynomial in types and jobs.

### Space Complexity

- **Assign Every Job to Both Handlers**: `O(n)`.
- **Memoized Pair State**: `O(n * m^2)`.

### Trade-offs

- The brute force needs no argument beyond correctness by enumeration.
- The memoized rung's work is bounded by the state space, not the tree size.

### When to Use Each

- **Assign Every Job to Both Handlers**: cross-checking the memoized rung on small queues.
- **Memoized Pair State**: any real queue.

### Optimization Notes

- The state space can shrink further: only the type of the handler that took the previous job matters for the next job's cheapest continuation, so a rolling dictionary over pair states replaces the full table.
- When `shortPrepTime[t] >= longPrepTime[t]` for some type, that type's short branch is never profitable and can be pruned.
