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

The problem statement fixes both halves of the output before any approach is chosen: `order` must be the lexicographically smallest topological order, and `cycle` must be the first cycle a deterministic left-to-right search closes. Every solution below pairs one way of picking the next course with the same deterministic cycle search, so the approaches differ only in how efficiently they find the smallest ready course and how the search itself is driven.

### Repeated Min-Scan

#### Derivation

The most literal reading of "lexicographically smallest topological order" is the greedy rule itself: among the courses whose prerequisites are all met, always take the smallest-numbered one, and write the taken courses down in the order taken. Executed with no cleverness, the rule means a fresh scan for the smallest untaken zero-prerequisite course every round:

1. Build `adjacency` (prerequisite to dependent courses) and `indegree` (remaining prerequisite counts) from `prerequisites`.
2. Repeat `numCourses` rounds: scan courses `0` through `numCourses - 1` for the first untaken course whose `indegree` is `0`.
3. Take it: record it in `order`, mark it in `taken`, and decrement the `indegree` of each dependent course.
4. A round that finds no candidate means the remaining courses form a cycle, and the DFS below exhibits one.

#### Walkthrough

Example 1, `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`. The edges run `0 -> 1`, `0 -> 2`, `1 -> 3`, `2 -> 3`, so `indegree` starts as `[0, 1, 1, 2]`; each round lists the scan verdict:

```text
round 1   scan 0..3: course 0 has indegree 0    take 0, order = [0]
          indegree[1] 1->0, indegree[2] 1->0
round 2   scan 0..3: 0 taken, course 1 next     take 1, order = [0, 1]
          indegree[3] 2->1
round 3   scan 0..3: course 2 has indegree 0    take 2, order = [0, 1, 2]
          indegree[3] 1->0
round 4   scan 0..3: course 3 has indegree 0    take 3, order = [0, 1, 2, 3]
```

The scan always stops at the smallest available course, which is what makes the order lexicographically smallest. The function returns `[[0, 1, 2, 3], []]`, matching the expected Output. On Example 2, `prerequisites = [[1,0],[2,1],[0,2]]` give every course `indegree` `1`, so round 1's scan finds no candidate at all and the cycle search below returns `[[0, 1, 2]]`.

#### Solution

The code is the walkthrough's round loop: scan, take, relax:

```python
from typing import List


class Solution:
    def analyzeCourses(self, numCourses: int, prerequisites: List[List[int]]) -> List[List[int]]:
        """Return [topological_order, []] or [[], first_cycle].

        Time:  O(V^2 + E): up to V rounds, each rescanning all V courses,
            plus one pass over the edges.
        Space: O(V + E) for the adjacency list, indegrees, and markers.
        """
        adjacency: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            indegree[course] += 1

        order: List[int] = []
        taken = [False] * numCourses
        for _ in range(numCourses):
            smallest_available = -1
            for course in range(numCourses):
                if not taken[course] and indegree[course] == 0:
                    smallest_available = course
                    break
            if smallest_available == -1:
                return [[], self.find_cycle(numCourses, adjacency)]
            taken[smallest_available] = True
            order.append(smallest_available)
            for next_course in adjacency[smallest_available]:
                indegree[next_course] -= 1
        return [order, []]

    def find_cycle(self, numCourses: int, adjacency: List[List[int]]) -> List[int]:
        """Return the first directed cycle a left-to-right DFS closes.

        Time:  O(V + E): each course is entered at most once.
        Space: O(V + E) for the three state arrays and recursion stack.
        """
        states = [0] * numCourses
        parent = [-1] * numCourses
        cycle = None

        def dfs(course: int) -> None:
            nonlocal cycle
            if cycle is not None:
                return
            states[course] = 1
            for next_course in adjacency[course]:
                if cycle is not None:
                    return
                if states[next_course] == 0:
                    parent[next_course] = course
                    dfs(next_course)
                elif states[next_course] == 1:
                    cycle = [course]
                    walk = course
                    while walk != next_course:
                        walk = parent[walk]
                        cycle.append(walk)
                    cycle.reverse()
            states[course] = 2

        for start in range(numCourses):
            if states[start] == 0:
                dfs(start)
        return cycle
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V^2 + E)` for the order, `O(V + E)` for the cycle

Each of up to `V` rounds rescans all `V` courses; every edge is relaxed exactly once; the cycle pass is linear.

##### Space Complexity: `O(V + E)`

The adjacency list holds every edge; the indegree and marker arrays hold one entry per course.

#### Key Insights

- The greedy rule "smallest ready course first" is the entire lexicographic argument; the later solutions change only how the smallest ready course is found.
- The quadratic cost is invisible on toy inputs and fatal at `numCourses = 10^5`: around `10^10` scan steps.
- The shortfall signal ("no candidate this round") is already a complete cycle proof, so the same shared search serves every variant on the page.

### Min-Heap Kahn's Algorithm

#### Derivation

The repeated scan is correct but pays `O(V)` per round to rediscover a pool that changed only incrementally. [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm) maintains the candidate pool directly: every course whose remaining prerequisite count reaches zero joins the pool, and each round selects one. A [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) keeps the pool ordered, so the smallest ready course is a single pop:

1. Build `adjacency` (prerequisite to dependent courses) and `indegree` (remaining prerequisite counts) from `prerequisites`.
2. Seed `available` with every course whose `indegree` is `0`.
3. While `available` is non-empty, pop the smallest course, append it to `order`, decrement the `indegree` of each dependent course, and push every dependent whose `indegree` hits `0`.
4. If `order` holds all `numCourses` courses, return `[order, []]`. Otherwise a cycle exists and the DFS below finds it.

#### Walkthrough

Example 1, `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`. The edges run `0 -> 1`, `0 -> 2`, `1 -> 3`, `2 -> 3`, so `indegree` starts as `[0, 1, 1, 2]`:

```text
available = [0]          order = []
pop 0    order = [0]      indegree[1] 1->0, indegree[2] 1->0
         available = [1, 2]
pop 1    order = [0,1]    indegree[3] 2->1
         available = [2]
pop 2    order = [0,1,2]  indegree[3] 1->0
         available = [3]
pop 3    order = [0,1,2,3]
         available = []   -> order complete, cycle = []
```

Course `1` is popped before course `2` because the heap pops the minimum, which is what makes the order lexicographically smallest. The function returns `[[0, 1, 2, 3], []]`, matching the expected Output. Example 2 ends with `order = [0]` (course `2` keeps course `0` waiting forever, and course `0` keeps course `1` waiting), so the ordering pass reports a cycle and the search below returns `[[0, 1, 2]]`.

#### Solution

The code is the walkthrough's seed, pop, and decrement loop:

```python
import heapq
from typing import List


class Solution:
    def analyzeCourses(self, numCourses: int, prerequisites: List[List[int]]) -> List[List[int]]:
        """Return [topological_order, []] or [[], first_cycle].

        Time:  O(V + E log V): every course enters the heap once and each
            edge triggers one push or pop.
        Space: O(V + E) for the adjacency list, indegrees, and heap.
        """
        adjacency: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            indegree[course] += 1

        available = [course for course in range(numCourses) if indegree[course] == 0]
        heapq.heapify(available)
        order: List[int] = []
        while available:
            course = heapq.heappop(available)
            order.append(course)
            for next_course in adjacency[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    heapq.heappush(available, next_course)

        if len(order) == numCourses:
            return [order, []]
        return [[], self.find_cycle(numCourses, adjacency)]

    def find_cycle(self, numCourses: int, adjacency: List[List[int]]) -> List[int]:
        """Return the first directed cycle a left-to-right DFS closes.

        Time:  O(V + E): each course is entered at most once.
        Space: O(V + E) for the three state arrays and recursion stack.
        """
        states = [0] * numCourses
        parent = [-1] * numCourses
        cycle = None

        def dfs(course: int) -> None:
            nonlocal cycle
            if cycle is not None:
                return
            states[course] = 1
            for next_course in adjacency[course]:
                if cycle is not None:
                    return
                if states[next_course] == 0:
                    parent[next_course] = course
                    dfs(next_course)
                elif states[next_course] == 1:
                    cycle = [course]
                    walk = course
                    while walk != next_course:
                        walk = parent[walk]
                        cycle.append(walk)
                    cycle.reverse()
            states[course] = 2

        for start in range(numCourses):
            if states[start] == 0:
                dfs(start)
        return cycle
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E log V)` for the order, `O(V + E)` for the cycle

Each course enters and leaves the heap exactly once, and each edge triggers at most one push; the cycle search visits each course and edge at most once.

##### Space Complexity: `O(V + E)`

The adjacency list holds every edge, and the indegree array, heap, and DFS state arrays hold at most one entry per course.

#### Key Insights

- A heap-fed Kahn's algorithm turns "lexicographically smallest" from an afterthought into a one-line property: the pool is always sorted, so the smallest available course is chosen first. The heap also repairs the repeated scan's weakness, since a course joins the pool once instead of being re-found by every later round.
- Kahn's algorithm doubles as a cycle detector: the leftover courses (those never reaching `indegree` zero) prove a cycle exists, and the DFS below only has to exhibit one.
- The cycle search follows the statement's determinism rules literally: starts ascend, neighbors ascend, and the first edge into an in-progress course closes the reported cycle.

### Iterative Kahn's Algorithm with Explicit Cycle Search

#### Derivation

The recursive DFS inherits the interpreter's recursion limit: with `numCourses` up to `10^5`, a chain-shaped graph drives the recursion `10^5` frames deep, past Python's default limit of 1,000. The order half of the problem is already loop-shaped (Kahn's main loop), so only the cycle search needs restructuring: an explicit stack replaces the call stack, and the three-color state marks are rewritten as a course list per state so the iterative version can reconstruct the active path without `parent` array gymnastics:

1. Run the heap-fed Kahn's loop unchanged to produce `order` or detect shortfall.
2. On shortfall, iterate starts `0` through `numCourses - 1`; skip courses already marked done.
3. Pop a course from `stack`, walk its neighbors in ascending order, and push unvisited ones after marking them in-progress.
4. The first neighbor found in-progress closes a cycle: rebuild it by walking `path` back to that neighbor, then return the reversed segment.

#### Walkthrough

The cycle half on Example 2, `numCourses = 3`, `prerequisites = [[1,0],[2,1],[0,2]]`, with edges `0 -> 1`, `1 -> 2`, `2 -> 0`. The Kahn loop leaves `order = [0]` short, so the search starts:

```text
start 0   stack = [0]                in_progress = [0]
pop 0     neighbors [1]              push 1
          stack = [1]                in_progress = [0, 1]
pop 1     neighbors [2]              push 2
          stack = [2]                in_progress = [0, 1, 2]
pop 2     neighbors [0]
          0 is in_progress           path = [0, 1, 2]
          cycle = path[0:] = [0, 1, 2]
```

The back edge `2 -> 0` points at the bottom of the current path, so the segment `path[0:]` is the whole path. Reversed, it reads `[0, 1, 2]`, which matches Example 2's expected cycle. The start courses were inspected in increasing order (`start 0` first) and each course's neighbors in increasing order, exactly as the statement requires.

#### Solution

The code is the heap-fed ordering loop plus the stack-driven cycle search from the walkthrough:

```python
import heapq
from typing import List


class Solution:
    def analyzeCourses(self, numCourses: int, prerequisites: List[List[int]]) -> List[List[int]]:
        """Return [topological_order, []] or [[], first_cycle], recursion-free.

        Time:  O(V + E log V) for the order, O(V + E) for the cycle.
        Space: O(V + E) for the adjacency list, heap, and state lists.
        """
        adjacency: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            indegree[course] += 1

        available = [course for course in range(numCourses) if indegree[course] == 0]
        heapq.heapify(available)
        order: List[int] = []
        while available:
            course = heapq.heappop(available)
            order.append(course)
            for next_course in adjacency[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    heapq.heappush(available, next_course)

        if len(order) == numCourses:
            return [order, []]
        return [[], self.find_cycle(numCourses, adjacency)]

    def find_cycle(self, numCourses: int, adjacency: List[List[int]]) -> List[int]:
        """Return the first directed cycle a left-to-right iterative DFS closes.

        Time:  O(V + E): each course and edge is processed at most once.
        Space: O(V + E) for the state lists and the explicit stack.
        """
        unvisited, in_progress, done = 0, 1, 2
        states = [unvisited] * numCourses
        for start in range(numCourses):
            if states[start] != unvisited:
                continue
            path: List[int] = []
            stack = [(start, iter(adjacency[start]))]
            states[start] = in_progress
            path.append(start)
            while stack:
                course, neighbors = stack[-1]
                advanced = False
                for next_course in neighbors:
                    if states[next_course] == unvisited:
                        states[next_course] = in_progress
                        path.append(next_course)
                        stack.append((next_course, iter(adjacency[next_course])))
                        advanced = True
                        break
                    if states[next_course] == in_progress:
                        joined = path.index(next_course)
                        return path[joined:]
                if not advanced:
                    states[course] = done
                    stack.pop()
                    path.pop()
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E log V)` for the order, `O(V + E)` for the cycle

The heap loop is unchanged from the first variant. In the cycle search, each course is pushed and popped once and each `adjacency` iterator is consumed once; `path.index` runs only once, on the closing edge, so it adds a single `O(V)` term.

##### Space Complexity: `O(V + E)`

The adjacency list and heap, plus the explicit stack and path, which hold at most one entry per course.

#### Key Insights

- The recursion-depth hazard comes only from the cycle search; Kahn's ordering loop is naturally iterative, so the page's fast path never risks the stack.
- Carrying `(course, neighbors_iterator)` frames on the stack preserves the statement's "outgoing neighbors in increasing order" rule without re-sorting.
- Recording the active path as a list makes the closed cycle a slice `path[joined:]`, replacing parent-pointer backtracking with one index lookup.

## Comparison of Solutions

### Time Complexity

- **Repeated Min-Scan**: `O(V^2 + E)` for the order plus `O(V + E)` for the cycle; each of up to `V` rounds rescans all `V` courses.
- **Min-Heap Kahn's Algorithm**: `O(V + E log V)` plus `O(V + E)`; every course passes through the heap once.
- **Iterative Kahn's Algorithm with Explicit Cycle Search**: `O(V + E log V)` plus `O(V + E)`, with one added `O(V)` index lookup on the closing edge.

### Space Complexity

- **Repeated Min-Scan**: `O(V + E)` for the adjacency list, indegrees, and taken markers.
- **Min-Heap Kahn's Algorithm**: `O(V + E)` for the adjacency list, indegrees, heap, and DFS arrays.
- **Iterative Kahn's Algorithm with Explicit Cycle Search**: `O(V + E)`, swapping the recursion stack for an explicit one of the same bound.

### Trade-offs

- **Repeated Min-Scan**: the greedy rule stated as directly as possible, but the per-round rescan is quadratic and unusable at `10^5` courses.
- **Min-Heap Kahn's Algorithm**: optimal enough for the constraints and the clearest statement of both halves, but its recursive cycle search can exceed Python's recursion limit on chain-shaped graphs.
- **Iterative Kahn's Algorithm with Explicit Cycle Search**: removes the recursion-depth failure mode entirely, at the cost of trickier frame bookkeeping in the cycle search.

### When to Use Each

- **Min-Heap Kahn's Algorithm (Recommended)**: the default interview answer: it derives the lexicographic order, detects the cycle, and reads cleanly.
- **Repeated Min-Scan**: as the spoken baseline, or when `numCourses` is tiny and code size matters more than asymptotics.
- **Iterative Kahn's Algorithm with Explicit Cycle Search**: when constraints approach `10^5` courses in a chain shape and recursion depth is a real risk.

### Optimization Notes

- The two outputs share one property worth stating in an interview: the leftover courses after Kahn's loop are exactly the courses on or downstream of a cycle, which is why shortfall is a sound trigger for the cycle search.
- The cycle search's determinism contract (ascending starts, ascending neighbors, first back edge) must be preserved by any rewrite; the iterative variant carries neighbor iterators precisely to keep that contract.
- `heapq` pops `O(log V)` per course, so the lexicographic requirement costs `O(E log V)`; plain queue Kahn's gives an `O(V + E)` order but not the smallest one.
