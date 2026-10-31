# [Minimum Completion Time for DAG Dependencies](https://www.fastprep.io/problems/amazon-minimum-dag-completion-time)

**Medium** | **NN minutes** | **Graph, Topological Sort, Dynamic Programming**

Each task has a positive duration. A dependency [before,after] means task after may start only after task before finishes. The dependency graph is acyclic.

Any number of currently available tasks may run in parallel. Return the minimum time needed to finish every task.

## Examples

### Example 1

**Input:** `durations = [3,2,5]`, `dependencies = [[0,2],[1,2]]`

**Output:** `8`

**Explanation:** Tasks 0 and 1 run together; task 2 then finishes at time 8.

### Example 2

**Input:** `durations = [2,4,3,7]`, `dependencies = [[0,1],[0,2]]`

**Output:** `7`

**Explanation:** The independent seven-unit task is the final task to finish.

### Example 3

**Input:** `durations = []`, `dependencies = []`

**Output:** `0`

**Explanation:** No tasks require zero time.

## Constraints

- `0 <= durations.length <= 100000.`
- `1 <= durations[i] <= 10^9.`
- `The dependency graph is a DAG.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
