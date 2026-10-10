# [Course Order and Cycle](https://www.fastprep.io/problems/amazon-course-order-and-cycle)

**Hard** | **NN minutes** | **Graph, Breadth First Search, Depth First Search, Topological Sort**

There are numCourses courses numbered from 0 through numCourses - 1. Each row [course, prerequisite] means the prerequisite must be completed before the course.

Return a two-row result [order, cycle]:

If all courses can be completed, return the lexicographically smallest valid topological order in order and an empty cycle.If completion is impossible, return an empty order and one directed cycle in cycle. Do not repeat the first course at the end.To make cycle selection deterministic, inspect starting courses in increasing order and each course's outgoing neighbors in increasing order. Return the active-path segment closed by the first back edge encountered.

## Examples

### Example 1

**Input:** `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`

**Output:** `[[0,1,2,3],[]]`

**Explanation:** Course 0 is first. Courses 1 and 2 then become available, and the smaller course is chosen first.

### Example 2

**Input:** `numCourses = 3`, `prerequisites = [[1,0],[2,1],[0,2]]`

**Output:** `[[],[0,1,2]]`

**Explanation:** The directed edges form 0 -> 1 -> 2 -> 0, so no topological order exists.

## Constraints

- `1 <= numCourses <= 10^5.`
- `0 <= prerequisites.length <= 2 * 10^5.`
- `Every prerequisite row contains two distinct valid course numbers.`
- `No prerequisite edge appears more than once.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
