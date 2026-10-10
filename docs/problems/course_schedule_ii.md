# [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)

**Medium** | **25 minutes** | **Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md), [Topological Sort](../patterns/topological_sort/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) · [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm)

**Practice:** [`practice/course_schedule_ii/solution.py`](../../practice/course_schedule_ii/solution.py)

You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you **must** take course `b` first if you want to take course `a`.

* For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.

There are a total of `numCourses` courses you are required to take, labeled from `0` to `numCourses - 1`. 

Return a valid ordering of courses you can take to finish all courses. If there are many valid answers, return **any** of them. If it's not possible to finish all courses, return an **empty array**.

## Examples

### Example 1

**Input:** `numCourses = 3, prerequisites = [[1,0]]`

**Output:** `[0,1,2]`

**Explanation:** We must ensure that course 0 is taken before course 1.

### Example 2

**Input:** `numCourses = 3, prerequisites = [[0,1],[1,2],[2,0]]`

**Output:** `[]`

**Explanation:** It's impossible to finish all courses.

## Constraints

- `1 <= numCourses <= 1000`
- `0 <= prerequisites.length <= 1000`
- All `prerequisite` pairs are **unique**.

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See _TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
