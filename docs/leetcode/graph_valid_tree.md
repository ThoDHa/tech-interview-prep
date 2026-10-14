# [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/)

**Medium** | **25 minutes** | **Depth-First Search, Breadth-First Search, Union Find, Graph**

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/graph-valid-tree/); read it free on [NeetCode](https://neetcode.io/problems/valid-tree).

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md), [Union-Find](../patterns/union_find/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Disjoint-set (Union-Find)](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)

**Practice:** [`practice/graph_valid_tree/solution.py`](../../practice/graph_valid_tree/solution.py)

Given `n` nodes labeled from `0` to `n - 1` and a list of **undirected** edges (each edge is a pair of nodes), write a function to check whether these edges make up a valid tree.

## Examples

### Example 1

**Input:** `n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]`

**Output:** `true`

### Example 2

**Input:** `n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]`

**Output:** `false`

## Constraints

- `1 <= n <= 2000`
- `0 <= edges.length <= 5000`
- `edges[i].length == 2`
- `0 <= a_i, b_i < n`
- `a_i != b_i`
- There are no self-loops or repeated edges.

## Deriving the Solution

A tree is the graph that is connected, acyclic, and holds exactly `n - 1` edges, and these three properties are redundant in pairs: `n - 1` acyclic edges on `n` nodes already connect the graph, and `n - 1` connected edges on `n` nodes already forbid cycles. Every solution below exploits that redundancy by checking two properties cheaply and letting the third follow.

1. **Start literal.** A flood fill from node `0` settles connectivity: walk the
   graph through an adjacency list, remember every reached node in a `visited` set, and require the set to hold all `n` nodes. Paired with the edge-count gate `len(edges) == n - 1`, the fill answers the whole question. Recursive DFS is the shortest way to write it: see [DFS with Visited Set](#dfs-with-visited-set).
2. **Spot the hazard.** The recursion descends once per node of a path-shaped
   graph, so the call stack can reach depth `n`, deep enough to threaten Python's recursion limit at `n = 2000`. The same flood fill run from an explicit queue keeps the exploration iterative: see [BFS with Visited Set](#bfs-with-visited-set).
3. **Drop the graph entirely.** Connectivity can also be computed algebraically:
   start with every node as its own component and let each edge merge two components. An edge whose endpoints already share a component closes a cycle, so the merge pass itself detects acyclicity, and the edge-count gate does the rest: see [Union-Find](#union-find).

## Solutions

### DFS with Visited Set

#### Derivation

The literal reading asks two yes/no questions: do the edges connect all `n` nodes, and do they contain a cycle? The edge-count gate collapses the second question into the first. A connected graph on `n` nodes needs at least `n - 1` edges; with exactly `n - 1` edges it is a tree and therefore acyclic, while any extra edge forces a cycle. So the only thing the flood fill must establish is reachability of every node from node `0`:

1. Reject immediately unless `len(edges) == n - 1`.
2. Build `adjacency`, one neighbor list per node, appending each undirected
   edge in both directions.
3. Flood fill from `0` with a recursive `dfs` that adds each reached node to
   `visited` and recurses into neighbors not yet visited.
4. Return `len(visited) == n`.

#### Walkthrough

Let us run the fill by hand on Example 1: `n = 5`, `edges = [[0,1],[0,2],[0,3],[1,4]]`. The gate passes (`4 == 5 - 1`) and the adjacency lists come out as `0: [1, 2, 3]`, `1: [0, 4]`, `2: [0]`, `3: [0]`, `4: [1]`. The trace shows each `dfs` entry, the neighbors it visits in list order, and the growing `visited` set:

```text
dfs(0)   visited = {0}        neighbors 1, 2, 3
  dfs(1)   visited = {0, 1}     neighbors 0 (visited), 4
    dfs(4)   visited = {0, 1, 4}   neighbors 1 (visited)
  dfs(2)   visited = {0, 1, 4, 2}   neighbors 0 (visited)
  dfs(3)   visited = {0, 1, 4, 2, 3}   neighbors 0 (visited)
```

The recursion order follows adjacency list order: node `1` explores before `2` and `3`, and inside `dfs(1)` the already-visited `0` is skipped before `4` is reached. The final `visited` holds `5` of `5` nodes, so the function returns `True`, matching the expected Output for Example 1. On Example 2 the gate rejects before any traversal: `len(edges) = 5` against `n - 1 = 4`, an extra edge that must close a cycle.

#### Solution

The code is the walkthrough's gate, adjacency build, and flood fill.

```python
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        adjacency = [[] for _ in range(n)]
        for a, b in edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        visited = set()

        def dfs(node: int) -> None:
            visited.add(node)
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(0)
        return len(visited) == n
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The gate rejects in constant time. With exactly `n - 1` edges, building the adjacency lists touches each edge twice, and the fill visits each node once and scans each edge twice: `O(n + e)` reduced to `O(n)` by the gate.

##### Space Complexity: `O(n)`

The adjacency lists, the visited set, and the recursion stack (depth up to `n` on a path-shaped graph) are all linear.

#### Key Insights

- The edge-count gate is what lets connectivity stand in for acyclicity: `n - 1` connecting edges cannot cycle.
- The visited set of a fill from `0` is the connected component of `0`; comparing its size with `n` is the whole connectivity test.
- Without the gate the fill alone is wrong: a connected graph with one extra edge also reaches all `n` nodes, and only `len(edges) == n - 1` separates that case from a tree.

### BFS with Visited Set

#### Derivation

The DFS version's memory is the call stack, which descends once per node of a path-shaped graph and hits Python's recursion limit around depth `1000`. The flood fill itself is order-agnostic: any discipline that reaches every connected node works. Moving the frontier into an explicit queue turns the fill into an iterative [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) whose memory is the wavefront, and the gate-and-size test is unchanged:

1. Reject immediately unless `len(edges) == n - 1`.
2. Build `adjacency` as before.
3. Seed `visited` with node `0` and a `queue` with `0`.
4. While the queue is non-empty, `popleft` a node and push every unvisited
   neighbor, adding each to `visited` at push time.
5. Return `len(visited) == n`.

#### Walkthrough

Let us drain the queue by hand on Example 1: `n = 5`, `edges = [[0,1],[0,2],[0,3],[1,4]]`, same adjacency lists as before. Each row shows one `popleft`, the neighbors it pushes, and the state after processing:

```text
pop 0   visit 1, 2, 3   visited = {0, 1, 2, 3}     queue = [1, 2, 3]
pop 1   visit 4         visited = {0, 1, 2, 3, 4}  queue = [2, 3, 4]
pop 2   none new        visited = {0, 1, 2, 3, 4}  queue = [3, 4]
pop 3   none new        visited = {0, 1, 2, 3, 4}  queue = [4]
pop 4   none new        visited = {0, 1, 2, 3, 4}  queue = []
```

Adding to `visited` at push time, not at pop time, is what keeps the wavefront free of duplicates: node `0`'s three neighbors all enter the queue before any of them is popped, and each is enqueued exactly once. The final `visited` holds all `5` nodes, so the function returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the same gate and adjacency build, with the recursion replaced by the queue loop.

```python
from collections import deque
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        adjacency = [[] for _ in range(n)]
        for a, b in edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        visited = {0}
        queue = deque([0])
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) == n
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is enqueued once and every edge is scanned from both ends, and the edge-count gate again bounds `e` at `n - 1`.

##### Space Complexity: `O(n)`

The adjacency lists, the visited set, and the queue are linear. The queue itself can hold an entire wavefront (a star of `n - 1` leaves), so the worst case is unchanged; the constant-factor danger of deep recursion is what disappears.

#### Key Insights

- Same answer, different frontier: the fill discipline does not matter for the count, only for memory shape and recursion safety.
- Marking visited at enqueue time is the duplicate-proofing trick; marking at dequeue would let the same node enter the queue several times.
- On a path graph the BFS queue stays small, which is exactly the shape that breaks the DFS stack.

### Union-Find

#### Derivation

Both fills build the graph and then ask whether it is connected. Connectivity can be computed without ever traversing: treat each node as its own component and let each edge union the two components of its endpoints. The key observation is that unioning exposes cycles for free. When an edge's endpoints already share a component, that edge joins two nodes a path already connects, so it closes a cycle. Together with the edge-count gate, the merge pass answers both remaining questions in one sweep:

1. Reject immediately unless `len(edges) == n - 1`.
2. Give every node its own entry in `parent` and a `rank` of `0`.
3. For each edge `(a, b)`, find the roots of both endpoints. Equal roots mean
   the edge closes a cycle: return `False`.
4. Otherwise link the lower-rank root under the higher, bumping the rank on a
   tie, and continue.
5. Every edge unioned without a collision, so the graph is a forest of exactly
   one tree (the gate plus acyclicity force connectivity): return `True`.

`find` halves each node's hop to its root on every walk (`parent[node] = parent[parent[node]]`), which keeps the near-constant amortized cost in practice; `rank` keeps the trees shallow by attaching smaller to larger.

#### Walkthrough

Let us run the merge pass on a tailored false case, `n = 5`, `edges = [[0,1],[1,2],[2,0],[3,4]]`: the gate passes (`4 == n - 1`) but a triangle hides among the edges. Each row shows the edge, the roots found, and the state after the union:

```text
edge 0-1   roots 0, 1   parent = [0, 0, 2, 3, 4]   rank = [1, 0, 0, 0, 0]
edge 1-2   roots 0, 2   parent = [0, 0, 0, 3, 4]   rank = [1, 0, 0, 0, 0]
edge 2-0   roots 0, 0   cycle! -> return False
```

Edge `0-1` unions two singletons (tie, so `1` attaches under `0` and `rank[0]` rises to `1`). Edge `1-2` finds roots `0` and `2`, and the lower-ranked `2` attaches under `0`. Edge `2-0` then finds the same root `0` on both sides: the triangle is closed, and the function rejects the graph, the expected answer for a graph with a cycle. On Example 1 the same pass unions `1`, `2`, `3`, then `4` under root `0` with no collision and returns `True`.

#### Solution

The code is the gate, the arrays, and the merge pass with inline cycle detection.

```python
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))
        rank = [0] * n

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                return False
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * α(n))`

The gate rejects in constant time; each of the `n - 1` edges then pays two finds. Union by rank with path halving amortizes each find to `α(n)`, the inverse Ackermann function, a constant below `5` for every input that fits in the universe.

##### Space Complexity: `O(n)`

The `parent` and `rank` arrays; the iterative `find` adds no stack.

#### Key Insights

- With the edge-count gate in place, cycle-freedom implies connectivity, so the union pass needs no separate component count: no collision means a tree.
- The union loop detects cycles as a side effect of merging; nothing is ever traversed twice, which is what makes this the go-to structure when edges stream in one at a time.
- Path halving inside `find` flattens the tree during the very lookup that pays for it, so no separate compression pass is needed.

## Comparison of Solutions

The practice harness's `practice/graph_valid_tree/reference.py` implements the **Union-Find** solution.

### Time Complexity

- **DFS with Visited Set**: `O(n)` - gate, adjacency build, and one flood fill over `n - 1` edges.
- **BFS with Visited Set**: `O(n)` - the same work with a queue instead of the call stack.
- **Union-Find**: `O(n * α(n))` - two near-constant finds per edge, no graph traversal.

### Space Complexity

- **DFS with Visited Set**: `O(n)` - adjacency lists, visited set, and a stack that can reach depth `n`.
- **BFS with Visited Set**: `O(n)` - adjacency lists, visited set, and a wavefront queue.
- **Union-Find**: `O(n)` - two flat arrays, no adjacency structure at all.

### Trade-offs

- The flood fills read as the definition of a tree (connectivity plus the gate) and generalize to component listings, but they must build the full adjacency structure first.
- Union-Find never materializes the graph, which makes it the natural choice when edges arrive incrementally, but its correctness argument (gate plus acyclicity implies connectivity) is subtler to state.

### When to Use Each

- **DFS with Visited Set**: the default answer in an interview; shortest correct code when `n` is modest (recommended here).
- **BFS with Visited Set**: the same answer without recursion-limit exposure; prefer it when the graph may be a long path.
- **Union-Find**: when edges stream in, when the problem grows into dynamic connectivity (Redundant Connection, Number of Connected Components), or when several queries share one structure.

### Optimization Notes

- The edge-count gate is doing heavy lifting in all three solutions: rejecting early in constant time, and licensing the two-property check that reaches the third property by implication.
- Path halving (`parent[node] = parent[parent[node]]`) folds path compression into `find` itself; pairing it with union by rank gives the `α(n)` bound without a second pass.
- For a single validity query, DFS and Union-Find tie in practice; for repeated queries over mutating edge sets, only Union-Find survives.

