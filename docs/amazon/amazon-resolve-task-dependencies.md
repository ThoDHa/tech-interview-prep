# [Resolve Task Dependencies](https://www.fastprep.io/problems/amazon-resolve-task-dependencies)

**Hard** | **NN minutes** | **Graph, Topological Sort, Heap**

There are n tasks numbered from 0 through n - 1. A dependency [u, v] means task u must be completed before task v.

The array mandatory contains dependencies that cannot be removed. Each row [u, v, cost] in optional contains a removable dependency u -> v and its cost.

If the graph containing every dependency is acyclic, return its lexicographically smallest topological order without removing anything.If it is cyclic, consider removing exactly one optional dependency. Among the optional dependencies whose removal makes the entire graph acyclic, remove the one with the smallest cost. If costs tie, remove the one appearing earlier in optional. Return the lexicographically smallest topological order of the resulting graph.If no single optional dependency can make the graph acyclic, return an empty array.

## Examples

### Example 1

**Input:** `n = 4`, `mandatory = [[0,1],[2,3]]`, `optional = [[1,2,7]]`

**Output:** `[0,1,2,3]`

**Explanation:** All dependencies are already acyclic, so none is removed. The only valid order is [0,1,2,3].

### Example 2

**Input:** `n = 3`, `mandatory = [[0,1]]`, `optional = [[1,2,5],[2,0,2]]`

**Output:** `[0,1,2]`

**Explanation:** The dependencies form the cycle 0 -> 1 -> 2 -> 0. Removing 2 -> 0 costs 2, which is cheaper than removing 1 -> 2.

### Example 3

**Input:** `n = 2`, `mandatory = [[0,1],[1,0]]`, `optional = []`

**Output:** `[]`

**Explanation:** The mandatory dependencies form a cycle, and there is no optional dependency that can be removed.

## Constraints

- `1 <= n <= 500`
- `0 <= mandatory.length, optional.length`
- `mandatory.length + optional.length <= 2000`
- `Every dependency endpoint is in [0, n - 1], and no dependency is repeated.`
- `0 <= cost <= 1000000000`

## Solutions

### Repeated Smallest-Ready Scan

#### Derivation

The problem is two duties in one, and the first duty hides a classic result. Duty one is deciding acyclicity, and Kahn's peeling argument answers it: a graph is acyclic exactly when tasks can be removed one at a time, each having no unplaced predecessor, and the peeling stalls before all `n` tasks only when the remaining tasks form a cycle. Duty two is the lexicographic tie-break, and among all ready tasks the smallest-numbered one is always safe to place next: placing one ready task never un-readies another, so every ready task stays ready, and exchanging the first two entries of any valid order that starts with a larger ready task yields a valid order that is smaller. The from-scratch version finds each round's smallest ready task by scanning task numbers in ascending order and taking the first with a zero pending count:

1. Build `successors` and `pending_counts` from an edge list.
2. Repeat `n` times: scan task numbers ascending and take the first unplaced
   task with `pending_counts[task] == 0`; finding none proves a cycle and
   returns an empty order.
3. Place the chosen task and decrement each successor's pending count.
4. Run the construction on all dependencies (`mandatory` plus the `optional`
   pairs): if it places all `n` tasks, the graph is acyclic and that order is
   the answer.
5. Otherwise try removing exactly one optional dependency per trial, iterating
   `optional` in stored order. Keep the cheapest removal that yields an
   acyclic graph, replacing the best only on a strictly smaller cost, which
   keeps the earlier slot on ties.
6. No removal works: return an empty array.

#### Walkthrough

Example 1: `n = 4`, `mandatory = [[0,1],[2,3]]`, `optional = [[1,2,7]]`. The full edge list is `0 -> 1`, `2 -> 3`, `1 -> 2`, so `pending_counts = [0, 1, 1, 1]`:

```text
round 1   scan 0..3: task 0 pending 0 -> place 0, order [0]
          release 1: pending [0, 0, 1, 1]
round 2   scan: task 1 pending 0 -> place 1, order [0, 1]
          release 2: pending [0, 0, 0, 1]
round 3   scan: task 2 pending 0 -> place 2, order [0, 1, 2]
          release 3: pending [0, 0, 0, 0]
round 4   scan: task 3 pending 0 -> place 3, order [0, 1, 2, 3]
```

All four tasks placed, so the graph is acyclic, nothing is removed, and `[0, 1, 2, 3]` is returned. Round 2 is the lexicographic beat: tasks 1 and 2 are both ready, and the scan takes 1. Taking 2 first would give the valid but larger order `[0, 2, 1, 3]`.

#### Solution

```python
from typing import List, Optional


class Solution:
    def solve(self, n: int, mandatory: List[List[int]], optional: List[List[int]]) -> List[int]:
        def smallest_topological_order(edges: List[List[int]]) -> List[int]:
            successors: List[List[int]] = [[] for _ in range(n)]
            pending_counts = [0] * n
            for source, target in edges:
                successors[source].append(target)
                pending_counts[target] += 1

            placed = [False] * n
            order: List[int] = []
            for _ in range(n):
                chosen = -1
                for task in range(n):
                    if not placed[task] and pending_counts[task] == 0:
                        chosen = task
                        break
                if chosen == -1:
                    return []
                placed[chosen] = True
                order.append(chosen)
                for next_task in successors[chosen]:
                    pending_counts[next_task] -= 1
            return order

        full_order = smallest_topological_order(
            mandatory + [dependency[:2] for dependency in optional])
        if full_order:
            return full_order

        best_cost: Optional[int] = None
        best_order: List[int] = []
        for removal_position, dependency in enumerate(optional):
            cost = dependency[2]
            remaining = mandatory + [
                other[:2] for position, other in enumerate(optional)
                if position != removal_position]
            candidate_order = smallest_topological_order(remaining)
            if candidate_order and (best_cost is None or cost < best_cost):
                best_cost = cost
                best_order = candidate_order
        return best_order
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((1 + R) × (n² + E))`

Each of the `1 + R` trials (the full graph, then one per optional dependency, `R = optional.length`) builds the graph in `O(E)` and runs `n` selection rounds, each scanning up to `n` task numbers, plus `O(E)` total decrements, where `E = mandatory.length + optional.length`.

##### Space Complexity: `O(n + E)`

The adjacency lists, pending counts, placed marks, and per-trial edge copy are all linear in the input.

#### Key Insights

- A construction that places fewer than `n` tasks is a cycle certificate: every unplaced task still waits on some unplaced predecessor, which is exactly a cycle.
- The lexicographic greedy needs no global sort: scanning task numbers ascending and taking the first ready one is equivalent, and self-evidently correct.
- The tie rule costs nothing: iterating `optional` in stored order and replacing the best only on a strictly smaller cost keeps the earliest slot on ties.
- Scanning up to `n` task numbers for every placement is the cost the next approach removes.

### Min-Heap Kahn's Algorithm

#### Derivation

The scan re-examines every task number at every placement just to learn the smallest ready one, `O(n)` per placement and `O(n²)` per trial. The ready set only ever gains members, and the only query ever asked of it is "smallest", which is exactly what a [min-heap](https://en.wikipedia.org/wiki/Binary_heap) maintains: seed it once with the zero-pending tasks, pop the minimum per placement, and push a task the moment its pending count reaches zero. The selection drops from an `O(n)` rescan to `O(log n)` heap work; the trial loop, the tie rules, and the cycle check are unchanged:

1. Build `successors` and `pending_counts`.
2. Seed `ready` with every task whose pending count is zero and heapify it.
3. Pop the smallest task, append it to `order`, and push each successor whose
   pending count reaches zero.
4. Return `order` when it holds `n` tasks, else an empty order (the cycle case).
5. Run the same `1 + R` trials with the same cheapest-and-earliest bookkeeping
   as before.

#### Walkthrough

Example 2, the cyclic case: `n = 3`, `mandatory = [[0,1]]`, `optional = [[1,2,5],[2,0,2]]`. The full graph has edges `0 -> 1`, `1 -> 2`, `2 -> 0`, so `pending_counts = [1, 1, 1]` and `ready` heapifies to empty: no placement is possible, the graph is cyclic, and the trials begin:

```text
remove optional[0] = 1->2 (cost 5)
  edges 0->1, 2->0          pending [1, 1, 0]
  ready [2]: pop 2, order [2]; release 0
  ready [0]: pop 0, order [2, 0]; release 1
  ready [1]: pop 1, order [2, 0, 1]        valid, best_cost = 5
remove optional[1] = 2->0 (cost 2)
  edges 0->1, 1->2          pending [0, 1, 1]
  ready [0]: pop 0, order [0]; release 1
  ready [1]: pop 1, order [0, 1]; release 2
  ready [2]: pop 2, order [0, 1, 2]        valid, 2 < 5, best_cost = 2
return [0, 1, 2]
```

Both removals repair the graph, and the ascending trial order plus the strict cost comparison keep the cheaper later removal: the answer is `[0, 1, 2]`, matching the expected Output.

#### Solution

```python
import heapq
from typing import List, Optional


class Solution:
    def solve(self, n: int, mandatory: List[List[int]], optional: List[List[int]]) -> List[int]:
        def smallest_topological_order(edges: List[List[int]]) -> List[int]:
            successors: List[List[int]] = [[] for _ in range(n)]
            pending_counts = [0] * n
            for source, target in edges:
                successors[source].append(target)
                pending_counts[target] += 1

            ready = [task for task in range(n) if pending_counts[task] == 0]
            heapq.heapify(ready)
            order: List[int] = []
            while ready:
                task = heapq.heappop(ready)
                order.append(task)
                for next_task in successors[task]:
                    pending_counts[next_task] -= 1
                    if pending_counts[next_task] == 0:
                        heapq.heappush(ready, next_task)
            return order if len(order) == n else []

        full_order = smallest_topological_order(
            mandatory + [dependency[:2] for dependency in optional])
        if full_order:
            return full_order

        best_cost: Optional[int] = None
        best_order: List[int] = []
        for removal_position, dependency in enumerate(optional):
            cost = dependency[2]
            remaining = mandatory + [
                other[:2] for position, other in enumerate(optional)
                if position != removal_position]
            candidate_order = smallest_topological_order(remaining)
            if candidate_order and (best_cost is None or cost < best_cost):
                best_cost = cost
                best_order = candidate_order
        return best_order
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((1 + R) × (n + E) log n)`

Each trial heapifies the `n` seed tasks once and performs one push or pop per task plus one per edge that unblocks a task, each `O(log n)`.

##### Space Complexity: `O(n + E)`

Adjacency lists, pending counts, the heap, and the order are all linear in the input.

#### Key Insights

- The heap holds exactly the ready set, so "smallest ready task" is one pop instead of a scan over all task numbers.
- A cycle announces itself as an empty `ready` heap while `order` is still short; no separate cycle detector is needed.
- Iterating `optional` in stored order with a strict cost comparison implements both selection rules at once: smallest cost wins, earliest slot breaks ties.
- Every trial rebuilds the graph from scratch; sharing work across trials is possible but rarely worth the extra code under OA constraints.

## Comparison of Solutions

### Time Complexity

- **Repeated Smallest-Ready Scan**: `O((1 + R) × (n² + E))` - each placement rescans all task numbers to find the smallest ready one.
- **Min-Heap Kahn's Algorithm**: `O((1 + R) × (n + E) log n)` - heap operations replace the rescans.

### Space Complexity

- **Repeated Smallest-Ready Scan**: `O(n + E)` - adjacency lists, pending counts, placed marks, and the per-trial edge copy.
- **Min-Heap Kahn's Algorithm**: `O(n + E)` - the same structures with a heap instead of placed marks.

### Trade-offs

- **Repeated Smallest-Ready Scan**: imports nothing and is transparent about the greedy rule, but the `n²` selection work per trial dominates once `n` grows (at the stated `n <= 500` with many trials, Python starts to feel it).
- **Min-Heap Kahn's Algorithm**: adds one import and heap bookkeeping, and comfortably fits the constraints: the per-trial cost is near linear in tasks and edges.

### When to Use Each

- **Min-Heap Kahn's Algorithm (Recommended)**: the default in an interview, since it is the standard "lexicographically smallest topological order" construction and its cost model is easy to state.
- **Repeated Smallest-Ready Scan**: for tiny inputs or when explaining the greedy from scratch matters more than the asymptotics.

### Optimization Notes

- The `1 + R` factor comes from rebuilding per trial; an edge lies on some cycle only when `v` reaches `u`, so a pre-pass with reachability from `v` back to `u` can skip hopeless trials, though with `E <= 2000` the simple loop is usually fast enough.
- Costs up to `10^9` fit Python integers natively, so no overflow handling is needed anywhere in the trial loop.
- Ties between equal-cost removals are decided by trial order, not by the resulting orders: the spec fixes the removal first, then asks for the lexicographically smallest order of the graph it produces.
