# [Course Schedule II](https://www.fastprep.io/problems/amazon-course-schedule-ii)

**Medium** | **NN minutes** | **Graph, Heap, Breadth First Search, Topological Sort**

There are numCourses courses labeled from 0 to numCourses - 1. Each pair [course, prerequisite] means the prerequisite must be completed before the course.

Return the lexicographically smallest course ordering that satisfies every prerequisite. If no valid ordering exists, return an empty array.

## Examples

### Example 1

**Input:** `numCourses = 2`, `prerequisites = [[1,0]]`

**Output:** `[0,1]`

**Explanation:** Course 0 must appear before course 1.

### Example 2

**Input:** `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`

**Output:** `[0,1,2,3]`

**Explanation:** After course 0, courses 1 and 2 are both available, so lexicographic order chooses 1.

### Example 3

**Input:** `numCourses = 2`, `prerequisites = [[1,0],[0,1]]`

**Output:** `[]`

**Explanation:** The two courses form a cycle, so no complete ordering exists.

## Constraints

- `1 <= numCourses <= 2000.`
- `0 <= prerequisites.length <= 5000.`
- `prerequisites[i].length == 2.`
- `0 <= course, prerequisite < numCourses.`
- `Every prerequisite pair is unique, and a course is never its own prerequisite.`

## Solutions

### Repeated Course Selection

#### Derivation

The most literal reading of "lexicographically smallest ordering that satisfies every prerequisite" is a greedy replay of the sentence: at every step, look at the courses not yet scheduled, find those whose prerequisites are all already scheduled, and schedule the smallest-labeled one. Scheduling a course can only unlock further courses and never blocks any, so taking the smallest takeable course immediately is always safe. The exchange argument makes the lexicographic claim precise: let any valid order disagree with the greedy at some position, and let `course` be the greedy's pick there, the smallest takeable label. Move `course` up to the disagreement slot: it still sits after its prerequisites (they are inside the shared prefix), and shifting the displaced courses one slot later cannot break any prerequisite pair, since nothing moves before its own prerequisites. The rewritten order is valid, matches the greedy on one more position, and is lexicographically smaller, so no valid order beats the greedy's pick at any position:

1. Build `prereqs`, mapping each course to the courses that must come before it.
2. While `order` holds fewer than `numCourses` courses:
3. scan courses in ascending label order for the first untaken course whose
   every prerequisite is already in `placed`;
4. if a full scan places nothing, the remaining courses depend on one another
   in a cycle: return `[]`.
5. Otherwise place that course, append it to `order`, and rescan.

#### Walkthrough

Trace the selection on Example 2: `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`, the diamond where courses 1 and 2 both wait on course 0 and course 3 waits on both:

```text
round 1  scan: course 0 takeable (no prerequisites)             order [0]
round 2  scan: 0 placed, course 1 takeable (0 is placed)        order [0, 1]
round 3  scan: 0, 1 placed, course 2 takeable (0 is placed)     order [0, 1, 2]
round 4  scan: 0..2 placed, course 3 takeable (1, 2 placed)     order [0, 1, 2, 3]
```

Each round places exactly one course, always the smallest label whose prerequisites are met, so the loop yields `[0, 1, 2, 3]`, matching the expected Output for Example 2. On Example 3's cycle `[[1,0],[0,1]]`, the first scan finds both courses waiting on each other, places nothing, and the `else` branch returns `[]`.

#### Solution

The code is the rescan loop with the `placed` flags and the ascending scan.

```python
from typing import List


class Solution:
    def solve(self, num_courses: int, prerequisites: List[List[int]]) -> List[int]:
        """Return the lexicographically smallest valid course order, [] on a cycle.

        Time:  O(V * (V + E)): at most V rounds, each rescanning every course
            and its prerequisite list.
        Space: O(V + E) for the prerequisite lists, placed flags, and order.
        """
        prereqs: List[List[int]] = [[] for _ in range(num_courses)]
        for course, prerequisite in prerequisites:
            prereqs[course].append(prerequisite)

        placed = [False] * num_courses
        order: List[int] = []
        while len(order) < num_courses:
            for course in range(num_courses):
                if not placed[course] and all(
                    placed[prerequisite] for prerequisite in prereqs[course]
                ):
                    placed[course] = True
                    order.append(course)
                    break
            else:
                return []
        return order
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V * (V + E))`

Each round appends at most one course, so there are up to `V` rounds; a round scans all `V` courses and re-runs the prerequisite check over the edge list until it finds the placement, costing `O(V + E)`.

##### Space Complexity: `O(V + E)`

The prerequisite lists store all `E` pairs, and the placed flags plus `order` use `O(V)`.

#### Key Insights

- The ascending scan is the whole lexicographic trick: placing *any* takeable course yields a valid order, but scanning from label `0` upward yields the smallest one.
- The greedy never needs retraction: scheduling a course early only removes constraints, which is why the exchange argument goes through without case analysis.
- A scan that places nothing is a cycle proof: every remaining course waits on another remaining course.

### Kahn's Algorithm with Min-Heap

#### Derivation

The selection loop re-asks "is this course ready?" for every course on every round. Readiness is a countdown: a course's `pending` count starts at its prerequisite total, and each placed prerequisite decrements it once, so a count reaching `0` is the only moment a course becomes takeable. Tracking those events turns the rescan into [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm) with one change for this problem's tie-break: the ready courses wait in a [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) instead of a FIFO queue, so every pop hands over the smallest currently takeable label. The substitution preserves the greedy invariant from the selection loop, because the heap always holds exactly the set of takeable courses the ascending scan would have found:

1. Build `adjacency` (prerequisite -> courses it unlocks) and the `pending` counts.
2. Heapify `ready` with every course whose `pending` count is `0`.
3. Pop the smallest course, append it to `order`, and decrement the `pending`
   count of each course it unlocks, pushing any that reach `0`.
4. Return `order` when it holds all `numCourses` courses, else `[]`.

#### Walkthrough

Trace the heap on Example 2: `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]` gives `pending = [0, 1, 1, 2]`:

```text
setup    pending = [0, 1, 1, 2]    ready = [0]              order []
pop 0    pending[1] 1 -> 0: push   pending[2] 1 -> 0: push
         ready = [1, 2]            order [0]
pop 1    pending[3] 2 -> 1         ready = [2]              order [0, 1]
pop 2    pending[3] 1 -> 0: push   ready = [3]              order [0, 1, 2]
pop 3    nothing unlocked          ready = []               order [0, 1, 2, 3]
```

Course `3` enters `ready` only after both `1` and `2` have been popped, which is exactly the moment its last pending prerequisite completes. The heap drains with all four courses placed, so the function returns `[0, 1, 2, 3]`, matching the expected Output. On Example 3's cycle, both counts start at `1`, `ready` heapifies empty, `order` never grows, and the length check returns `[]`.

#### Solution

The code is the countdown graph with the min-heap as the ready set.

```python
import heapq
from typing import List


class Solution:
    def solve(self, num_courses: int, prerequisites: List[List[int]]) -> List[int]:
        """Return the lexicographically smallest valid course order, [] on a cycle.

        Time:  O(V log V + E): heapify costs O(V), each course is pushed and
            popped once at O(log V), and each edge is relaxed once.
        Space: O(V + E) for the adjacency list, pending counts, heap, and order.
        """
        adjacency: List[List[int]] = [[] for _ in range(num_courses)]
        pending = [0] * num_courses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            pending[course] += 1

        ready = [course for course in range(num_courses) if pending[course] == 0]
        heapq.heapify(ready)
        order: List[int] = []
        while ready:
            course = heapq.heappop(ready)
            order.append(course)
            for next_course in adjacency[course]:
                pending[next_course] -= 1
                if pending[next_course] == 0:
                    heapq.heappush(ready, next_course)
        return order if len(order) == num_courses else []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V log V + E)`

Building the graph is one pass over the `E` pairs; the initial `heapify` costs `O(V)`, each of the `V` courses is popped once at `O(log V)` and pushed at most once, and each edge is decremented exactly once.

##### Space Complexity: `O(V + E)`

The adjacency list stores all edges; the `pending` array, heap, and `order` each hold `O(V)` entries.

#### Key Insights

- The min-heap is the rescan loop's memory, refined for ties: it holds exactly the takeable set, and `heappop` performs the smallest-label search the scan did by hand.
- Cycle detection needs no extra code: courses inside a cycle never reach `pending == 0`, so a short `order` is the entire proof.
- With a FIFO queue the same loop is `O(V + E)` but returns *some* valid order; the heap upgrade costs `O(log V)` per course and is what the lexicographic requirement buys.

## Comparison of Solutions

### Time Complexity

- **Repeated Course Selection**: `O(V * (V + E))` - up to `V` rounds of full rescans over courses and prerequisites.
- **Kahn's Algorithm with Min-Heap**: `O(V log V + E)` - one push and pop per course, one decrement per edge.

### Space Complexity

- **Repeated Course Selection**: `O(V + E)` - prerequisite lists plus placed flags and order.
- **Kahn's Algorithm with Min-Heap**: `O(V + E)` - adjacency list plus pending counts, heap, and order.

### Trade-offs

- **Repeated Course Selection**: the problem statement in code and the clearest statement of the greedy; it pays by re-testing every unplaced course every round.
- **Kahn's Algorithm with Min-Heap**: near-linear and event-driven, at the cost of heap discipline and the in-degree setup.

### When to Use Each

- **Repeated Course Selection**: tiny inputs, or as the spoken first step that derives the greedy before optimizing it.
- **Kahn's Algorithm with Min-Heap** (Recommended): the interview default: it scales to the constraint limits and keeps the lexicographic guarantee with one heap substitution.

### Optimization Notes

- Replacing the heap with a plain `deque` restores `O(V + E)` but loses the tie-break: the queue emits a valid order, not the smallest one. The same objection removes the DFS postorder from this variant's toolbox, since it orders by completion time and ignores labels entirely.
- The greedy argument applies only to the lexicographic objective: any other goal (shortest total time, fewest restarts) needs a different formulation, not a topological sort.
- Heapify the initially takeable courses in one pass rather than pushing them one by one: same asymptotics, but no `O(log V)` factor per seed course.
