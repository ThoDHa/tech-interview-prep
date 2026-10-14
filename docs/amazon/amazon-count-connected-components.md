# [Count Connected Components](https://www.fastprep.io/problems/amazon-count-connected-components)

**Easy** | **NN minutes** | **Graph, Union Find, Depth First Search**

You are given an undirected graph with n nodes and a list of edges. Each edge connects two nodes in the graph.

Return the number of connected components in the graph. A connected component is a maximal group of nodes where every pair of nodes is connected by some path.

Function Description Complete the function countConnectedComponents in the editor.

countConnectedComponents has the following parameters:

int n: the number of nodes, labeled from 0 to n - 1int edges[][]: an array where each element [u, v] represents an undirected edge between nodes u and vReturns int: the number of connected components in the graph

## Examples

### Example 1

**Input:** `n = 5`, `edges = [[0, 1], [1, 2], [3, 4]]`

**Output:** `2`

**Explanation:** Nodes 0, 1, and 2 form one connected component. Nodes 3 and 4 form another connected component. Therefore, there are 2 connected components.

### Example 2

**Input:** `n = 5`, `edges = [[0, 1], [1, 2], [2, 0], [3, 4]]`

**Output:** `2`

**Explanation:** The cycle among nodes 0, 1, and 2 is still one connected component. Nodes 3 and 4 form the second component.

### Example 3

**Input:** `n = 4`, `edges = []`

**Output:** `4`

**Explanation:** With no edges, every node is isolated, so each node is its own connected component.

## Constraints

- `Nodes are labeled from 0 to n - 1.`
- `The graph is undirected.`
- `The input edges are valid node pairs.`

## Solutions

Throughout, `n` is the node count and `e` is the edge count. The approaches mirror the unified-track page [Number of Connected Components in an Undirected Graph](../leetcode/number_of_connected_components_in_an_undirected_graph.md), which solves the same problem on LeetCode's adjacency-list input.

### DFS with Visited Set

#### Derivation

The literal reading turns the count into a scan: a node belongs to some component, and the first of its component to come under inspection must be recognized as new. A `visited` set records everything already claimed by an earlier component, so an unvisited node at scan time is provably a component nobody has counted yet. What remains is marking the rest of that component before the scan continues, which is a flood fill over the graph, and [DFS](https://en.wikipedia.org/wiki/Depth-first_search) expresses it in the fewest lines:

1. Build `adjacency`, a list of neighbor lists, appending each undirected edge
   in both directions.
2. Scan nodes `0` through `n - 1` in order, keeping `components`.
3. When a node is not in `visited`, increment `components` and run a recursive
   `dfs` that adds each reached node to `visited` and recurses into unvisited
   neighbors.
4. Return `components` after the scan.

#### Walkthrough

Let us run the scan and fill by hand on Example 1: `n = 5`, `edges = [[0, 1], [1, 2], [3, 4]]`. The adjacency lists come out as `0: [1]`, `1: [0, 2]`, `2: [1]`, `3: [4]`, `4: [3]`. Each row shows the scan position, the action taken, and the state after it:

```text
scan 0   unvisited -> components = 1, dfs(0) marks {0, 1, 2}   visited = {0, 1, 2}
scan 1   visited, skip
scan 2   visited, skip
scan 3   unvisited -> components = 2, dfs(3) marks {3, 4}      visited = {0, 1, 2, 3, 4}
scan 4   visited, skip
```

Inside `dfs(0)` the fill reaches node `1` and from it node `2`, and every neighbor it re-meets is already marked, so the fill stops at exactly the component `{0, 1, 2}`. The second fill claims `{3, 4}` the same way. The scan ends with `components = 2`, matching the expected Output for Example 1. On Example 3, `edges = []` leaves every neighbor list empty, so each of the four scan positions starts a fill of one node and the function returns `4`.

#### Solution

The code is the walkthrough's scan-and-fill: the loop seeds each component and `dfs` claims it.

```python
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        adjacency: List[List[int]] = [[] for _ in range(n)]
        for node_a, node_b in edges:
            adjacency[node_a].append(node_b)
            adjacency[node_b].append(node_a)

        visited: set[int] = set()
        components = 0

        def dfs(node: int) -> None:
            visited.add(node)
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        for node in range(n):
            if node not in visited:
                components += 1
                dfs(node)
        return components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e)`

Building the adjacency lists touches each edge twice, and the fill visits each node once while scanning each edge from both ends: every node and edge participates in constant work overall.

##### Space Complexity: `O(n)`

The adjacency lists and the visited set are linear, and the recursion stack reaches depth `n` on a path-shaped graph.

#### Key Insights

- The scan order does the component bookkeeping: an unvisited node at scan time is exactly a new component, because every earlier fill marked its whole component.
- Node labels being `0` through `n - 1` lets the scan be a plain `range(n)`; arbitrary labels would need an explicit iteration order over the node set.
- The fill never revisits: each node enters `visited` once, which is what keeps the traversal linear even with cycles (Example 2's triangle just re-meets marked nodes).

### BFS with Visited Set

#### Derivation

The DFS version's memory is the call stack, which on a path-shaped graph descends once per node and runs into Python's recursion limit. The flood fill is indifferent to exploration order, so the frontier can move into an explicit [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) queue with the scan-and-count loop unchanged; the only care point is marking nodes visited at enqueue time so no node enters the queue once per incoming edge:

1. Build `adjacency` as before.
2. Scan nodes `0` through `n - 1`, keeping `components`.
3. When a node is not in `visited`, increment `components`, mark it visited,
   and seed a `queue` with it.
4. While the queue is non-empty, `popleft` a node and enqueue each unvisited
   neighbor, marking it visited at enqueue time.
5. Return `components`.

#### Walkthrough

Let us drain the queue on Example 1: `n = 5`, `edges = [[0, 1], [1, 2], [3, 4]]`, same adjacency lists as before:

```text
scan 0  new component -> components = 1
  pop 0   visit 1   visited = {0, 1}     queue = [1]
  pop 1   visit 2   visited = {0, 1, 2}  queue = [2]
  pop 2   none new  visited = {0, 1, 2}  queue = []
scan 1, 2   visited, skip
scan 3   unvisited -> components = 2
  pop 3   visit 4   visited = {0, 1, 2, 3, 4}  queue = [4]
  pop 4   none new  visited = {0, 1, 2, 3, 4}  queue = []
scan 4   visited, skip
```

The first component drains fully before the scan moves on, and the second fill starts only because node `3` was never reached. The final count is `components = 2`, matching the expected Output for Example 1.

#### Solution

The code is the scan-and-count loop with the recursive fill replaced by the queue loop.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        adjacency: List[List[int]] = [[] for _ in range(n)]
        for node_a, node_b in edges:
            adjacency[node_a].append(node_b)
            adjacency[node_b].append(node_a)

        visited: set[int] = set()
        components = 0
        for node in range(n):
            if node in visited:
                continue
            components += 1
            visited.add(node)
            queue = deque([node])
            while queue:
                current_node = queue.popleft()
                for neighbor in adjacency[current_node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        return components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e)`

Each node is enqueued once and each edge is scanned from both ends; the scan and adjacency build add the same linear work as before.

##### Space Complexity: `O(n)`

The adjacency lists, the visited set, and the queue are linear. The queue holds one wavefront at a time, which on a balanced graph is far smaller than the DFS stack's worst case; the asymptotic bound is unchanged.

#### Key Insights

- Same count, same complexity, different frontier: the choice between DFS and BFS here is about memory shape and recursion safety, not speed.
- Marking visited at enqueue time is the duplicate guard; marking at dequeue would let one node enter the queue once per incoming edge.
- The queue dies with each component, so the memory between components is just the adjacency lists and the visited set.

### Union-Find

#### Derivation

Both fills compute reachability the expensive way, by walking the graph. The count itself is cheaper to maintain algebraically: begin with `components = n`, every node its own component, and process edges one at a time. An edge between two different components merges them and lowers the count by one; an edge inside one component is redundant and lowers nothing. `find` with path halving locates each endpoint's component root, and union by rank keeps the trees flat. Example 2's triangle is the case this handles for free: its third edge `[2, 0]` finds equal roots on both sides and skips:

1. Give every node its own entry in `parent` and a `rank` of `0`; set
   `components = n`.
2. For each edge `[u, v]`, find the roots of both endpoints.
3. Equal roots mean the edge is internal to a component: skip it.
4. Otherwise link the lower-rank root under the higher, bumping the rank on a
   tie, and decrement `components`.
5. Return `components` after every edge is processed.

#### Walkthrough

Let us run the merge pass on Example 1: `n = 5`, `edges = [[0, 1], [1, 2], [3, 4]]`. Each row shows the edge, the roots found, and the state after the union:

```text
edge 0-1   roots 0, 1   union   parent = [0, 0, 2, 3, 4]  rank = [1, 0, 0, 0, 0]  components = 4
edge 1-2   roots 0, 2   union   parent = [0, 0, 0, 3, 4]  rank = [1, 0, 0, 0, 0]  components = 3
edge 3-4   roots 3, 4   union   parent = [0, 0, 0, 3, 3]  rank = [1, 0, 0, 1, 0]  components = 2
```

The first two edges each merge a singleton into the growing component rooted at `0`, and the third builds a second component rooted at `3`. No edge ever meets two endpoints with equal roots, so every edge lowers the count, and the final `components = 2` matches the expected Output for Example 1. A redundant edge would behave differently: on Example 2 the extra edge `[2, 0]` arrives with both endpoints already rooted at `0`, so the pass skips it and the count stays at `2`, again matching the expected Output.

#### Solution

The code is the merge pass: two finds per edge, a rank-ordered link, and a counter.

```python
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank = [0] * n

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        components = n
        for edge_start, edge_end in edges:
            root_start, root_end = find(edge_start), find(edge_end)
            if root_start == root_end:
                continue
            if rank[root_start] < rank[root_end]:
                root_start, root_end = root_end, root_start
            parent[root_end] = root_start
            if rank[root_start] == rank[root_end]:
                rank[root_start] += 1
            components -= 1
        return components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e × α(n))`

The `parent` initialization is linear, and each of the `e` edges pays two finds amortized to `α(n)`, the inverse Ackermann function, a constant below `5` for any input that fits in memory.

##### Space Complexity: `O(n)`

The `parent` and `rank` arrays; no adjacency structure is built at all, and the iterative `find` adds no stack.

#### Key Insights

- The count starts at `n` and only successful unions lower it, so redundant edges need no special casing: they simply fail to merge anything.
- No adjacency lists exist in this solution, which is why it dominates when memory is tight or when edges arrive as a stream.
- Union by rank bounds tree height at `O(log n)` and path halving flattens further on every lookup; together they give the inverse-Ackermann amortized cost.

## Comparison of Solutions

### Time Complexity

- **DFS with Visited Set**: `O(n + e)` - one linear adjacency build and one fill visiting every node and edge once.
- **BFS with Visited Set**: `O(n + e)` - identical work with a queue as the frontier.
- **Union-Find**: `O(n + e × α(n))` - two near-constant finds per edge, no traversal of the graph.

### Space Complexity

- **DFS with Visited Set**: `O(n)` - adjacency lists, visited set, and a stack that can reach depth `n`.
- **BFS with Visited Set**: `O(n)` - adjacency lists, visited set, and a queue holding one wavefront.
- **Union-Find**: `O(n)` - two flat arrays, and no adjacency structure at all.

### Trade-offs

- The fills state the definition directly (scan, seed, mark) and generalize to listing the members of each component, at the price of building the full adjacency structure.
- Union-Find never materializes the graph and is the only one of the three that processes edges one at a time without prebuilt neighbor lists, but its counter-based correctness argument is less visual than a fill.

### When to Use Each

- **DFS with Visited Set**: the default interview answer when the graph is given up front and recursion depth is not a concern (recommended here).
- **BFS with Visited Set**: the same answer hardened against deep recursion; prefer it on path-like graphs.
- **Union-Find**: when edges stream in, when memory for adjacency lists is undesirable, or when the problem is a stepping stone to dynamic connectivity.

### Optimization Notes

- Repeated or self-loop edges cost nothing in Union-Find: a same-root union returns before touching any structure, so no deduplication pass is needed.
- Union by rank bounds tree height at `O(log n)` and path halving inside `find` flattens further on every lookup, which together produce the inverse-Ackermann bound without recursion.
- For the follow-up "list the members of each component", keep the DFS fill and collect members into a root-keyed map instead of counting; Union-Find would need the same map bolted on afterward.
