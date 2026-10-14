# [Course Schedule](https://www.fastprep.io/problems/amazon-course-schedule)

**Medium** | **NN minutes** | **Graph, Depth First Search, Breadth First Search, Topological Sort**

There are numCourses courses labeled from 0 to numCourses - 1. Each pair [course, prerequisite] means the prerequisite must be completed before the course.

Return true if all courses can be completed, or false if the prerequisite graph contains a cycle.

Interview Follow-upThe interviewer asked follow-up questions about alternative solutions, edge cases, and complexity analysis.

## Examples

### Example 1

**Input:** `numCourses = 2`, `prerequisites = [[1,0]]`

**Output:** `true`

### Example 2

**Input:** `numCourses = 2`, `prerequisites = [[1,0],[0,1]]`

**Output:** `false`

**Explanation:** Each course requires the other first, creating a cycle.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-course-schedule; fill them in. -->

## Solutions

### Brute Force

#### Derivation

The most direct simulation mirrors how a student actually clears a degree: keep taking any course whose prerequisites are already finished, and repeat until no new course can be taken. If every course eventually gets taken, the schedule is feasible; if a round ever passes without taking anything while courses remain, the leftovers depend on one another in a cycle:

1. For each course, record the list of prerequisites it still needs in
   `remaining`.
2. Sweep over every untaken course. If all of its prerequisites are already
   `taken`, take it and mark that `progress` was made this round.
3. Repeat the full sweep as long as any course was taken during it.
4. When a sweep makes no progress, stop and compare `taken_count` against
   `numCourses`.

A course stuck forever is one whose prerequisites can never all be satisfied, which is exactly a cycle. The loop terminates because each sweep either takes at least one new course or ends the process.

#### Walkthrough

Trace the Brute Force on Example 1: `numCourses = 2`, `prerequisites = [[1,0]]`. The pair `[1, 0]` means course `1` needs course `0` first.

First, build `remaining` so each entry lists the prerequisites that course still needs:

- `remaining[0] = []`: course `0` has no prerequisites.
- `remaining[1] = [0]`: course `1` needs course `0`.

Start with `taken = [False, False]` and `taken_count = 0`. Now sweep, taking any untaken course whose prerequisites are all taken. Each row below is one course check inside a sweep:

| Sweep | course | `remaining[course]` | All prereqs taken? | Action | `taken` | `taken_count` |
|-------|--------|---------------------|--------------------|--------|---------|---------------|
| 1 | `0` | `[]` | yes (none needed) | take `0` | `[True, False]` | `1` |
| 1 | `1` | `[0]` | yes (`0` is taken) | take `1` | `[True, True]` | `2` |
| 2 | `0`, `1` | either | already taken: skip | none | `[True, True]` | `2` |

Sweep `1` took both courses, so `progress` stayed `True` and one more sweep ran. Sweep `2` took nothing, so `progress` became `False` and the loop stopped.

Finally, compare `taken_count == numCourses`: `2 == 2` is `True`, so the function returns `True`, matching the expected Output for Example 1. On Example 2's cycle `[[1,0],[0,1]]`, the first sweep places nothing, `progress` dies immediately, and `0 == 2` fails, so the function returns `False`.

#### Solution

The code is the walkthrough's sweep loop: keep taking courses until a round takes nothing.

```python
from typing import List


class Solution:
    def solve(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        """Return True when every course can be completed, False on a cycle.

        Time:  O(V^2 + V * E): up to V sweeps, each re-checking every course's
            outstanding prerequisite list.
        Space: O(V + E) for the remaining lists and the taken flags.
        """
        remaining: List[List[int]] = [[] for _ in range(num_courses)]
        for course, prerequisite in prerequisites:
            remaining[course].append(prerequisite)

        taken = [False] * num_courses
        taken_count = 0

        progress = True
        while progress:
            progress = False
            for course in range(num_courses):
                if taken[course]:
                    continue
                if all(taken[prerequisite] for prerequisite in remaining[course]):
                    taken[course] = True
                    taken_count += 1
                    progress = True

        return taken_count == num_courses
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V^2 + V * E)`

Each sweep is `O(V + E)` because it re-checks every course's full prerequisite list, and in the worst case only one course is taken per sweep, forcing up to `V` sweeps. That gives `O(V^2 + V * E)` overall: the same prerequisites are re-examined every round.

##### Space Complexity: `O(V + E)`

The `remaining` lists store all `E` prerequisite edges, and the `taken` array uses `O(V)`.

#### Key Insights

- This is pure simulation: no graph vocabulary is needed, only the rule "take a course once its prerequisites are done."
- The wasted work is re-scanning every course's prerequisites on every sweep, even courses and prerequisites that have not changed.
- The next solutions remove that waste either by following edges directly (DFS) or by counting prerequisites once and only revisiting a course when one of its prerequisites is taken (Kahn's Algorithm).

### DFS Three-Color

#### Derivation

The brute force re-checks unchanged prerequisites every sweep because it never follows the dependency structure; it only polls it. Model the courses as a directed graph instead: each course is a vertex, and a prerequisite pair `[course, prerequisite]` becomes an edge from `prerequisite` to `course`. Every course can be finished if and only if this graph has no cycle, so the polling loop can be replaced by one walk of the graph that looks for a cycle directly.

The subtlety is that a plain visited flag cannot recognize a cycle in a directed graph: reaching an already-visited vertex is harmless when it was finished by an earlier branch, and fatal only when it is an ancestor still on the current recursion path. A [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) with three states per vertex captures that distinction:

1. Build the adjacency list `adjacency`, pointing each prerequisite at the
   courses that depend on it.
2. Mark every vertex `WHITE` (unvisited) in `color`.
3. Run `has_cycle` from each `WHITE` vertex. On entry, paint the vertex `GRAY`
   to mark it as part of the active recursion path.
4. If the search reaches a `GRAY` vertex, that is a back edge to an ancestor in
   the current path, which proves a cycle exists, so return `False`.
5. After exploring all of a vertex's neighbors, paint it `BLACK` to record that
   it is fully processed and can never participate in a cycle reached later.

If no search ever revisits a `GRAY` vertex, the graph is acyclic and every course can be finished.

#### Walkthrough

Example 2 is the one with a cycle, so it exercises the back-edge detection: `numCourses = 2`, `prerequisites = [[1,0],[0,1]]`. Building the adjacency list gives `adjacency[0] = [1]` and `adjacency[1] = [0]` (each prerequisite points at the course depending on it), with `color = [WHITE, WHITE]`.

The outer loop starts at vertex `0`, and the trace indents one level per recursive call:

```text
has_cycle(0)     color[0] = GRAY               path: 0
  has_cycle(1)   color[1] = GRAY               path: 0 -> 1
    has_cycle(0) color[0] is GRAY -> back edge -> return True
  has_cycle(1)   -> True
has_cycle(0)     -> True
```

Following the edge `0 -> 1` and then `1 -> 0` lands the search on vertex `0` while it is still `GRAY`, meaning still on the active path: the recursion has looped back onto its own ancestor, which is the cycle `0 -> 1 -> 0`. The `True` bubbles up, the outer loop sees the cycle, and the function returns `False`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's colored search: `GRAY` on entry, `BLACK` on exit, cycle on meeting `GRAY`.

```python
from typing import List


class Solution:
    def solve(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        """Return True when every course can be completed, False on a cycle.

        Time:  O(V + E): each course is colored once and each prerequisite
            edge is followed at most once.
        Space: O(V + E) for the adjacency list, colors, and recursion stack.
        """
        white, gray, black = 0, 1, 2

        adjacency: List[List[int]] = [[] for _ in range(num_courses)]
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)

        color = [white] * num_courses

        def has_cycle(course: int) -> bool:
            if color[course] == gray:
                return True
            if color[course] == black:
                return False

            color[course] = gray
            for next_course in adjacency[course]:
                if has_cycle(next_course):
                    return True
            color[course] = black
            return False

        for course in range(num_courses):
            if color[course] == white and has_cycle(course):
                return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Where `V` is `numCourses` and `E` is the number of prerequisite pairs. Building the graph touches each edge once, and the three-color DFS visits each vertex and traverses each edge at most once.

##### Space Complexity: `O(V + E)`

The adjacency list stores all `E` edges, the color array uses `O(V)`, and the recursion stack reaches depth `O(V)` in the worst case.

#### Key Insights

- A simple binary visited flag is not enough for a directed graph; the distinct `GRAY` state is what distinguishes a back edge (cycle) from a cross or forward edge into an already finished branch.
- Painting a vertex `BLACK` lets later searches skip work that is known to be cycle-free, which keeps the traversal linear.
- The outer loop starting a DFS from every still-`WHITE` vertex is what covers disconnected prerequisite graphs.

### DFS with Visited and Path Sets

#### Derivation

The three-color search packs two different facts into one array: "this vertex is on the active path" and "this vertex is fully done". Splitting them into two explicit sets states each fact by name, which some find clearer to reason about than color codes. This variant also orients the graph the other way, from each course to its prerequisites, so the recursion walks dependencies before the course that needs them; the cycle test is unaffected by the direction:

1. Build the adjacency list `adjacency` mapping each course to the courses it
   requires.
2. Keep a `visited` set of fully processed courses and a `path` set of courses
   currently on the recursion stack.
3. For each unvisited course, run
   [DFS](https://en.wikipedia.org/wiki/Depth-first_search) via `has_cycle`.
   Add the course to both sets on entry.
4. If the search reaches a course already in `path`, the recursion has looped
   back on itself, so a cycle exists and the answer is `False`.
5. After exploring a course's prerequisites, remove it from `path` (backtrack)
   while leaving it in `visited`, so future searches skip it.

#### Walkthrough

Example 1 is acyclic, which is the case that exercises both the backtrack and the `visited` skip: `numCourses = 2`, `prerequisites = [[1,0]]`. With this orientation the adjacency list maps each course to its prerequisites: `adjacency[0] = []` and `adjacency[1] = [0]`. Both sets start empty.

```text
course 0: has_cycle(0)    path = {0}, visited = {0}
  adjacency[0] is empty   no prerequisites to follow
  backtrack 0             path = {}, return False
course 1: has_cycle(1)    path = {1}, visited = {0, 1}
  has_cycle(0)            0 in visited -> False, no re-exploration
  backtrack 1             path = {}, return False
no cycle found -> return True
```

Course `0` enters and leaves the path without finding a loop, staying in `visited`. When course `1` follows its prerequisite edge to `0`, the `visited` check answers immediately: `0` is done and cycle-free, and crucially it is no longer in `path`, so it is not mistaken for a cycle. Both calls return `False`, so the function returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's search with the two sets: `path` for the active branch, `visited` for finished courses.

```python
from typing import List


class Solution:
    def solve(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        """Return True when every course can be completed, False on a cycle.

        Time:  O(V + E): each course and prerequisite edge is processed at
            most once across the whole traversal.
        Space: O(V + E) for the adjacency list, both sets, and the recursion
            stack.
        """
        adjacency: List[List[int]] = [[] for _ in range(num_courses)]
        for course, prerequisite in prerequisites:
            adjacency[course].append(prerequisite)

        visited = set()  # Courses fully proven cycle-free.
        path = set()  # Courses on the active recursion path.

        def has_cycle(course: int) -> bool:
            if course in path:
                return True
            if course in visited:
                return False

            path.add(course)
            visited.add(course)
            for prerequisite in adjacency[course]:
                if has_cycle(prerequisite):
                    return True
            path.remove(course)
            return False

        for course in range(num_courses):
            if course not in visited and has_cycle(course):
                return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Each course and prerequisite edge is processed at most once across the whole traversal.

##### Space Complexity: `O(V + E)`

The adjacency list holds `O(V + E)`, the `visited` and `path` sets each hold up to `O(V)` entries, and the recursion stack reaches `O(V)` depth.

#### Key Insights

- The `path` set is the set-based equivalent of the `GRAY` color: membership in it means the vertex is an ancestor on the current recursion path.
- Removing a course from `path` on the way out is essential; without the backtrack, sibling branches would falsely look like cycles.
- Keeping `visited` separate from `path` avoids re-exploring shared subgraphs, preserving the linear time bound.

### Kahn's Algorithm

#### Derivation

The DFS solutions fix the brute force by following edges, but there is a second repair: fix the counting. The brute force re-derives "are all prerequisites taken?" from scratch each sweep; instead, count each course's outstanding prerequisites once, and update that count only when one of its prerequisites actually completes. This is [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm), a [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) performed with BFS. The key observation is that in an acyclic dependency graph there is always at least one course with no remaining prerequisites, so courses can be finished one in-degree-zero layer at a time:

1. Build the adjacency list `adjacency` and an `in_degree` array counting how
   many prerequisites each course still needs.
2. Seed a `queue` with every course whose in-degree is `0`.
3. Pop a course, count it in `completed`, and decrement the in-degree of each
   course that depended on it. Whenever a dependent course drops to in-degree
   `0`, enqueue it.
4. Continue until the queue empties, then return `completed == numCourses`.

If every course was completed, a full topological order exists and the graph is acyclic. If some courses never reached in-degree `0`, they are trapped in a cycle, so return `False`.

#### Termination Condition

The in-degree of a course counts its outstanding prerequisites:

$$ \deg^{-}(v) = \bigl|\{\, (u \to v) \in E \,\}\bigr| $$

```text
in_degree[v] = number of prerequisite edges u -> v into course v
```

A course is takeable once that count reaches zero, the queue holds exactly the currently takeable set, and removing a course decrements the in-degree of everything depending on it, peeling the graph one layer at a time.

The correctness rests on a property of finite directed graphs:

$$ G \text{ is acyclic} \iff \text{every non-empty subgraph of } G \text{ has a vertex with } \deg^{-} = 0 $$

```text
graph is acyclic  if and only if  every non-empty subgraph of it
                                  has a vertex with in_degree == 0
```

Forward: a DAG has a topological order, whose first vertex has no incoming edges. Backward: if some subgraph had no such vertex, every vertex would have a predecessor, and walking backwards through a finite graph must eventually revisit a vertex, which is a cycle.

So the queue empties early precisely when a non-empty set of courses remains in which every course still waits on another, which is a cycle. That makes the final check a cycle test rather than mere bookkeeping: each vertex enters the queue at most once (only on the decrement that brings it to zero) and each edge is relaxed exactly once.

#### Walkthrough

Trace the peeling on Example 1: `numCourses = 2`, `prerequisites = [[1,0]]`. Building the structures gives `adjacency[0] = [1]` (course `1` depends on `0`) and `in_degree = [0, 1]`. Course `0` starts takeable, so the queue is seeded with it:

```text
setup    adjacency[0] = [1]    in_degree = [0, 1]      queue = [0]   completed = 0
pop 0    completed = 1         in_degree[1]: 1 -> 0    enqueue 1  -> queue = [1]
pop 1    completed = 2         no dependents           queue = []
queue empty -> completed == numCourses is 2 == 2 -> return True
```

Taking course `0` removes the only outstanding prerequisite of course `1`, whose in-degree drops to `0` at that exact moment, so it enters the queue and is taken next. Both courses complete, so the function returns `True`, matching the expected Output for Example 1. On Example 2 both in-degrees start at `1`, the queue seeds empty, `completed` stays `0`, and `0 == 2` fails, so the function returns `False` there.

#### Solution

The code is the walkthrough's peel: pop a takeable course, decrement its dependents, enqueue any that hit zero.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        """Return True when every course can be completed, False on a cycle.

        Time:  O(V + E): each course is dequeued once and each prerequisite
            edge is relaxed once.
        Space: O(V + E) for the adjacency list, in-degree array, and queue.
        """
        adjacency: List[List[int]] = [[] for _ in range(num_courses)]
        in_degree = [0] * num_courses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            in_degree[course] += 1

        queue = deque(
            course for course in range(num_courses) if in_degree[course] == 0
        )
        completed = 0

        while queue:
            ready_course = queue.popleft()
            completed += 1
            for next_course in adjacency[ready_course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)

        return completed == num_courses
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Building the graph is `O(E)`, and the BFS dequeues each course once and relaxes each edge once, for `O(V + E)` overall.

##### Space Complexity: `O(V + E)`

The adjacency list uses `O(V + E)`, while the in-degree array and the queue each use `O(V)`.

#### Key Insights

- The number of completed courses is the cycle test: any shortfall against `numCourses` means at least one course never lost all its prerequisites.
- The algorithm is iterative, so it avoids the deep recursion that DFS can hit on long dependency chains near the constraint limit.
- The processing order is itself a valid course schedule, which is useful when the problem later asks for the order rather than a yes/no answer.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(V^2 + V * E)` - re-scans every course's prerequisites each sweep, and may need up to `V` sweeps.
- **DFS Three-Color**: `O(V + E)` - visits each vertex and edge at most once.
- **DFS with Visited and Path Sets**: `O(V + E)` - identical traversal, tracked with sets instead of a color array.
- **Kahn's Algorithm**: `O(V + E)` - dequeues each course once and relaxes each edge once.

### Space Complexity

- **Brute Force**: `O(V + E)` - stores all prerequisite edges plus the `taken` flags.
- **DFS Three-Color**: `O(V + E)` - adjacency list plus the color array and recursion stack.
- **DFS with Visited and Path Sets**: `O(V + E)` - adjacency list plus the `visited` and `path` sets and recursion stack.
- **Kahn's Algorithm**: `O(V + E)` - adjacency list plus the in-degree array and BFS queue.

### Trade-offs

- **Brute Force**: simplest to derive (just simulate taking courses), but wastes time re-checking unchanged prerequisites every sweep.
- **DFS Three-Color**: direct and compact cycle detection, but it relies on recursion that can be deep on long chains.
- **DFS with Visited and Path Sets**: set-based state can read more clearly than color codes, at the cost of higher constant factors than an integer array.
- **Kahn's Algorithm**: iterative and produces a usable topological order as a byproduct, at the cost of a slightly more involved in-degree setup.

### When to Use Each

- **Brute Force**: as a first intuition or sanity check; too slow for the upper constraints but easy to reason about.
- **DFS Three-Color** (Recommended): best for interviews; it states the core idea of finding a back edge in a directed graph as directly as possible.
- **DFS with Visited and Path Sets**: when explicit `visited`/`path` sets are clearer to the reader than a numeric color state.
- **Kahn's Algorithm**: when you prefer an iterative solution that avoids deep recursion on large graphs, or when the follow-up asks for the concrete order.

### Optimization Notes

- The brute-force simulation's waste is re-scanning prerequisites that have not changed; Kahn's Algorithm fixes this by counting prerequisites once and only revisiting a course when one of its prerequisites is taken.
- The three-state coloring is essential: a vertex found in the `GRAY` state signals a cycle, whereas a plain visited flag would mistake a finished branch for a back edge in a directed graph.
- Union-Find is not appropriate here: it detects cycles in undirected graphs, and a directed prerequisite cycle can hide between two branches it would merge.
