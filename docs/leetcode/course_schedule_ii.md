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

## Deriving the Solution

Each pair `[a, b]` is an ordering constraint, and a full schedule consistent with every constraint is a [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) of the graph having one edge `b -> a` per pair. Two classic families produce such an order: repeatedly removing courses with no unmet prerequisites, and finishing subtrees of a depth-first search before their parents. Both also have to detect the cycle case, where no valid order exists. Every solution below works on the same graph; they differ in which end of the ordering they build from and how the cycle shows itself.

1. **Start literal.** Scan for a course whose prerequisites are all placed,
   place it, repeat. Every round rescans every course and re-tests its
   whole prerequisite list: see
   [Repeated Course Selection](#repeated-course-selection).
2. **Track the count, not the set.** A course becomes takeable the moment
   its unmet-prerequisite count hits 0; decrementing counters and a queue
   of ready courses replace the rescans: see [Kahn's Algorithm](#kahns-algorithm).
3. **Build from the far end.** A DFS postorder emits each course after
   everything that depends on it; reversing that postorder is a valid
   order, and a course revisited mid-DFS exposes the cycle: see
   [DFS Postorder](#dfs-postorder).

## Solutions

### Repeated Course Selection

#### Derivation

The most literal reading of "schedule without violating prerequisites" keeps a `placed` set and repeats: find any course whose prerequisites are all in `placed`, add it. Each round is a fresh scan over all courses, so a long chain walks the course list once per course:

1. Build `prereqs`, a map from each course to its prerequisite courses.
2. While `order` holds fewer than `numCourses` courses:
3. scan for a course not yet placed whose every prerequisite is placed;
4. if none exists, the remaining courses are in a cycle: return `[]`.
5. Otherwise place the first such course and rescan.

#### Walkthrough

Trace the selection on Example 1: `numCourses = 3`, `prerequisites = [[1, 0]]`, so course 1 needs course 0:

```text
round 1  scan 0 (no prereqs, place)                                     order [0]
round 2  scan 0 placed, 1 (needs 0: met, place)                         order [0, 1]
round 3  scan 0 placed, 1 placed, 2 (no prereqs, place)                 order [0, 1, 2]
```

Each round places at most one course (the scan breaks after the first placement), so this input takes three rounds to give `[0, 1, 2]`, one of the accepted answers for Example 1 (any order with `0` before `1` is valid). On Example 2's cycle `[[0,1], [1,2], [2,0]]`, round 1 runs the full scan without placing anything (each course needs another) and the `else` fires, returning `[]`, matching the expected output.

#### Solution

The code is the rescan loop with the `placed` set.

```python
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        prereqs = {course: [] for course in range(numCourses)}
        for course, prerequisite in prerequisites:
            prereqs[course].append(prerequisite)

        placed = set()
        order = []
        while len(order) < numCourses:
            for course in range(numCourses):
                if course not in placed and all(
                    prerequisite in placed for prerequisite in prereqs[course]
                ):
                    placed.add(course)
                    order.append(course)
                    break
            else:
                return []
        return order
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V * (V + E))`

Each round appends at most one course, so up to `V` rounds; every round scans all `V` courses and re-runs the `all` prerequisite check over each course's list (up to `E` entries overall) until the placement is found. One round therefore costs `O(V + E)`, giving the `O(V * (V + E))` bound; the looser `O(V² * E)` treats the prerequisite re-check as a full `E` sweep per scanned course rather than per round.

##### Space Complexity: `O(V + E)`

The prerequisite map, the placed set, and the order.

#### Key Insights

- Termination is guaranteed on acyclic graphs (some course becomes takeable
  each round); a full round with no placement proves a cycle.
- The repeated rescans are the entire cost problem: nothing remembers how
  close a course is to becoming takeable, so every round re-tests every
  unplaced course's full prerequisite list.

### Kahn's Algorithm

#### Derivation

The rescan loop re-asks "is this course ready?" for every course every round. Readiness is a countdown: a course's `pending` count starts at its number of prerequisites and every placed prerequisite decrements it, so the moment a count hits 0 the course is ready and needs no further polling. Seeding a queue with the initially-ready courses (no prerequisites) and processing ready courses first-in-first-out turns the repeated scan into one pass over courses and edges. If the queue drains before all courses are placed, the unplaced courses form a cycle and the answer is `[]`:

1. Build `adjacency` (`prerequisite -> courses it unlocks`) and `pending`
   counts from the pairs.
2. Seed the queue with every course whose `pending` count is 0.
3. Pop a course, append it to `order`, and decrement `pending` for each
   course it unlocks; enqueue any course whose count reaches 0.
4. Return `order` when it holds all `numCourses` courses, else `[]`.

#### Walkthrough

Trace Example 1: `pending = [0, 1, 0]` (course 1 waits on one prerequisite) and `adjacency = [[1], [], []]`:

```text
seed     queue [0, 2]        order []
take 0   pending 1 -> 0      order [0]    queue [2, 1]
take 2   nothing unlocked    order [0, 2] queue [1]
take 1   nothing unlocked    order [0, 2, 1]  queue []
```

The result `[0, 2, 1]` is a valid ordering for Example 1: course 0 precedes course 1, and the problem accepts any such order. On Example 2's cycle, `pending` starts `[1, 1, 1]` with no ready course, the queue seeds empty, and `order` never grows past `[]`, so the answer is `[]`. The four-course diamond `[[1,0], [2,0], [3,1], [3,2]]` shows the countdown at work: `pending = [0, 1, 1, 2]`, taking 0 drops courses 1 and 2 to ready, and 3's count falls to 0 only after both are placed, yielding `[0, 1, 2, 3]`.

#### Solution

The code is the countdown graph and the ready queue.

```python
from collections import deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjacency = [[] for _ in range(numCourses)]
        pending = [0] * numCourses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            pending[course] += 1

        queue = deque(
            course for course in range(numCourses) if pending[course] == 0
        )
        order = []
        while queue:
            course = queue.popleft()
            order.append(course)
            for next_course in adjacency[course]:
                pending[next_course] -= 1
                if pending[next_course] == 0:
                    queue.append(next_course)
        return order if len(order) == numCourses else []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Building the graph is one pass over the pairs; each course is enqueued and dequeued at most once, and each edge decrements a counter exactly once.

##### Space Complexity: `O(V + E)`

The adjacency list, the count array, the queue, and the order.

#### Key Insights

- The `pending` array is the rescan loop's memory: each edge is consulted
  once, when its source course is placed.
- The cycle never needs special detection code: courses inside a cycle
  never reach `pending == 0`, so a short `order` is the whole proof.
- Every course with no prerequisites enters the initial queue, so all
  independent chains grow in interleaved rounds rather than one at a time.

### DFS Postorder

#### Derivation

Kahn's builds the order from the front (courses with nothing left to wait for). A depth-first search builds it from the back: explore each course's full downstream chain, and only when every course depending on `course` is finished append `course` to `postorder`. The postorder of a directed acyclic graph has each course before everything that depends on it, which is backwards, so reversing it yields a valid schedule. Cycles surface as a course reached again while its visit is still in progress, which a three-color `state` mark (unvisited / in progress / done) detects exactly:

1. Build `adjacency` (`course -> courses that depend on it`).
2. Run `visit(course)` from every course: mark in progress, visit each
   dependent, then mark done and append to `postorder`.
3. Hitting an in-progress course is a cycle: unwind with a `[]` result.
4. Return the reversed `postorder` (or `[]`).

#### Walkthrough

Trace the DFS from course 0 on the diamond `numCourses = 4`, `prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]`, whose edges run `0 -> 1`, `0 -> 2`, `1 -> 3`, `2 -> 3`:

```text
visit 0  state 0 = in-progress
  visit 1  state 1 = in-progress
    visit 3  state 3 = in-progress   no dependents -> done, postorder [3]
  state 1 = done                     postorder [3, 1]
  visit 2  state 2 = in-progress
    visit 3  state 3 = done          already finished, skip
  state 2 = done                     postorder [3, 1, 2]
state 0 = done                       postorder [3, 1, 2, 0]
reversed -> [0, 2, 1, 3]
```

Course 3 is appended first (nothing depends on it) and course 0 last, so the reversal puts prerequisites first: `[0, 2, 1, 3]` is valid (0 before 1 and 2, 1 and 2 before 3). On Example 2's cycle, `visit(0)` marks 0 in progress, descends `0 -> 1 -> 2 -> 0`, reads 0's in-progress mark, and the answer collapses to `[]`.

#### Solution

The code is the three-color DFS with the reversed postorder.

```python
from typing import List

UNVISITED, IN_PROGRESS, DONE = 0, 1, 2


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjacency = [[] for _ in range(numCourses)]
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)

        state = [UNVISITED] * numCourses
        postorder = []

        def visit(course: int) -> bool:
            if state[course] == IN_PROGRESS:
                return False
            if state[course] == DONE:
                return True
            state[course] = IN_PROGRESS
            for next_course in adjacency[course]:
                if not visit(next_course):
                    return False
            state[course] = DONE
            postorder.append(course)
            return True

        for course in range(numCourses):
            if not visit(course):
                return []
        return postorder[::-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Each course is visited once; each edge is followed once; everything else is constant per course.

##### Space Complexity: `O(V + E)`

The adjacency list, the state array, the postorder, and the recursion stack (up to `V` on a chain).

#### Key Insights

- The postorder is the order of completion, and completion order is the
  reverse of schedulability order; no separate readiness concept exists.
- The in-progress mark is the minimum cycle detector: done courses are
  safe to reuse, in-progress ones are the current path.
- Kahn's handles giant graphs without recursion-limit worries; the DFS
  form is the more common interview sketch.

## Comparison of Solutions

### Time Complexity

- **Repeated Course Selection**: `O(V * (V + E))`, coarsely `O(V² * E)` - a full rescan per placed course.
- **Kahn's Algorithm**: `O(V + E)` - one pass over courses and edges.
- **DFS Postorder**: `O(V + E)` - one visit per course, one walk per edge.

### Space Complexity

- **Repeated Course Selection**: `O(V + E)` - prerequisite map plus placed set.
- **Kahn's Algorithm**: `O(V + E)` - adjacency, counts, queue.
- **DFS Postorder**: `O(V + E)` - adjacency, states, postorder, recursion.

### Trade-offs

- The selection loop is the problem statement in code; the rescans are the
  price of remembering nothing between rounds.
- Kahn's and the DFS postorder share asymptotics; Kahn's is iterative with
  a naturally early cycle check (queue drains early), the DFS exposes the
  path structure and adapts to "any course before its dependents" variants
  with a one-line reversal removal.
- Both fast versions answer "order or cycle" with no extra pass.

### When to Use Each

- **Repeated Course Selection**: tiny inputs and as the transliteration
  baseline; it also cross-checks the others.
- **Kahn's Algorithm**: the default: iterative, linear, and the pattern
  reused by every "process in dependency order" pipeline (recommended here).
- **DFS Postorder**: when the problem hands you dependencies as edges you
  would naturally recurse over, or when cycle *location* (not just
  existence) matters.

### Optimization Notes

- The iteration order inside Kahn's queue decides which valid order comes
  out; a heap instead of a deque gives the lexicographically smallest
  order (the related "schedule with smallest course number first" variant)
  at an `O(log V)` per-pop cost.
- Seeding the queue in one comprehension over `pending` keeps the initial
  pass branch-free; courses added later always arrive via a decrement.
- For huge graphs, the iterative Kahn's avoids Python's recursion limit
  that the DFS postorder must respect or convert to an explicit stack.
