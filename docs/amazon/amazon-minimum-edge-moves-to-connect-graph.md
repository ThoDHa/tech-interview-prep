# [Minimum Edge Moves to Connect a Network](https://www.fastprep.io/problems/amazon-minimum-edge-moves-to-connect-graph)

**Medium** | **NN minutes** | **Graph, Union Find**

You manage an undirected network with nodes 0 through n - 1. In one move, you may remove one existing cable and reconnect that cable between any two nodes.

Return the minimum number of cable moves needed to make every node connected. Return -1 when the network does not contain enough cables to connect all nodes.

## Examples

### Example 1

**Input:** `n = 4`, `edges = [[0,1],[0,2],[1,2]]`

**Output:** `1`

**Explanation:** One cycle edge can be moved to attach the isolated node.

### Example 2

**Input:** `n = 6`, `edges = [[0,1],[0,2],[0,3],[1,2]]`

**Output:** `-1`

**Explanation:** Four cables cannot connect six nodes.

## Constraints

- `1 <= n <= 100000.`
- `Every edge has two valid node IDs.`
- `Self-loops and parallel edges are allowed and still count as available cables.`

## Solutions

### DFS with Visited Set

#### Derivation

A move relocates one cable but never creates or destroys one, so the total cable count is fixed. That observation splits the problem in two. Feasibility first: a connected network on `n` nodes needs at least `n - 1` cables, so anything fewer is hopeless and the answer is -1. The minimum number of moves second: one well-placed cable per gap, and the gaps are exactly the connections missing between the network's connected components, of which there is always one fewer than the number of components. Counting those components is therefore the whole job, and a traversal per component does it:

1. Return -1 immediately when `len(edges) < n - 1`.
2. Build `neighbors`, an adjacency list, from the edge list.
3. Scan nodes `0` through `n - 1`. Each still-unvisited node starts a new component:
   increment `components` and run `dfs(node)`.
4. `dfs` marks the node in `visited` and recurses into every unvisited neighbor.
5. Return `components - 1`.

#### Walkthrough

Example 1, `n = 4` with `edges = [[0,1],[0,2],[1,2]]`, passes the feasibility gate (`3` cables against the required `3`). The adjacency list reads `0: [1, 2]`, `1: [0, 2]`, `2: [0, 1]`, `3: []`, and the scan runs:

```text
scan 0   unvisited -> components = 1
  dfs(0)     visit 0
    dfs(1)   visit 1
      dfs(0) visited, dfs(2) visit 2 -> dfs(0), dfs(1) both visited
scan 1   visited -> skip
scan 2   visited -> skip
scan 3   unvisited -> components = 2, dfs(3) visits the lone node
```

The first component is the triangle `0, 1, 2` (its third edge is the redundant, movable cable) and node `3` stands alone: `components = 2`, and the function returns `2 - 1 = 1`, the expected Output. Example 2 never reaches the scan: `4` cables cannot cover the required `5`, so it returns -1 at the gate.

#### Solution

The code is the gate plus the per-component scan from the walkthrough.

```python
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        if len(edges) < n - 1:
            return -1

        neighbors: List[List[int]] = [[] for _ in range(n)]
        for node_a, node_b in edges:
            neighbors[node_a].append(node_b)
            neighbors[node_b].append(node_a)

        visited = [False] * n
        components = 0

        def dfs(node: int) -> None:
            visited[node] = True
            for neighbor in neighbors[node]:
                if not visited[neighbor]:
                    dfs(neighbor)

        for node in range(n):
            if not visited[node]:
                components += 1
                dfs(node)

        return components - 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e)`

Every node and every edge endpoint is touched once while building the adjacency list, and the traversal visits each node once with each edge examined from both ends.

##### Space Complexity: `O(n + e)`

The adjacency list holds every edge in both directions, on top of the `visited` array and the recursion stack, which a chain-shaped component drives to `O(n)` frames.

#### Key Insights

- The cable count is invariant under moves, which makes `len(edges) >= n - 1` a complete feasibility test before any traversal runs.
- `components - 1` is both necessary and sufficient: merging two components takes exactly one cable, and a component always holds a spare one while any gap remains.
- Self-loops and parallel edges never change the component count, yet they still count toward feasibility: a self-loop is a cable sitting idle in its component, ready to be moved.
- With `n` up to 100000, a chain-shaped input drives the recursion one frame per node, far past Python's default recursion limit.

### BFS with Visited Set

#### Derivation

The DFS count has one flaw worth repairing: its memory is the call stack, so a long chain of nodes recurses once per node and can overflow. The component count itself does not care about exploration order, so swapping depth for breadth loses nothing: [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) expands a component outward from its seed using an explicit queue, whose depth is bounded by the queue and not by the interpreter:

1. The feasibility gate and the adjacency build are unchanged.
2. The scan seeds a queue with each unvisited node, marking it visited at enqueue
   time.
3. Each dequeue reads `neighbors[node]` and enqueues every unvisited neighbor,
   marking it visited as it is enqueued.
4. Every seed incremented one component; return `components - 1`.

#### Walkthrough

Example 1 again, `n = 4` with `edges = [[0,1],[0,2],[1,2]]`. The gate passes, the adjacency list is the same, and the scan starts at node `0` with `components = 1`. Each line is one queue event; marking happens at enqueue time:

```text
seed 0      mark, queue = [0]
pop 0       neighbors 1, 2 unvisited -> mark+enqueue   queue = [1, 2]
pop 1       neighbor 0 visited; 2 unvisited -> mark+enqueue
            queue = [2]
pop 2       neighbors 0, 1 visited                     queue = []
scan 3      unvisited -> components = 2, seed+mark, queue = [3]
pop 3       no neighbors                               queue = []
```

The triangle drained in three pops and the lone node needed one: `components = 2` and the function returns `1`, matching the expected Output. The queue never held more than two nodes; on a 100000-node chain it would stay near a single node while a call stack would have grown to 100000 frames.

#### Solution

The code is the queue discipline from the walkthrough, wrapped in the same gate and scan.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        if len(edges) < n - 1:
            return -1

        neighbors: List[List[int]] = [[] for _ in range(n)]
        for node_a, node_b in edges:
            neighbors[node_a].append(node_b)
            neighbors[node_b].append(node_a)

        visited = [False] * n
        components = 0

        for start_node in range(n):
            if visited[start_node]:
                continue
            components += 1
            queue = deque([start_node])
            visited[start_node] = True
            while queue:
                node = queue.popleft()
                for neighbor in neighbors[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

        return components - 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e)`

Same touch count as the depth-first count: each node is enqueued once and each edge endpoint read once.

##### Space Complexity: `O(n + e)`

The adjacency list dominates; the queue holds at most the current frontier and `visited` holds one flag per node.

#### Key Insights

- Marking at enqueue time, not dequeue time, is what keeps every node out of the queue twice.
- Traversal order is irrelevant to a component count, so the BFS form is a drop-in replacement that removes the recursion-depth hazard.
- The price is structural: BFS needs the whole adjacency list materialized before it starts, where the streaming approach below never builds one.

### Union-Find

#### Derivation

Both traversals answer "how many components?" by walking each one, after paying to build an adjacency list. [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) asks the cheaper question: starting from `n` singleton components, how many merges do the edges actually perform? Each edge that joins two different components drops the count by one; an edge whose endpoints already share a root is redundant, and redundancy is exactly what a movable cable is. No adjacency list is built and the edge list is consumed as a stream:

1. Return -1 immediately when `len(edges) < n - 1`.
2. Initialize `uf` over `n` nodes, with `components = n`.
3. For each edge, union its endpoints; `union` does nothing when both endpoints
   already share a root, and otherwise merges by rank with path compression in
   `find` and decrements `components`.
4. Return `uf.components - 1`.

#### Walkthrough

Example 1, `n = 4`, runs three unions over the edges in order; `components` starts at `4`:

```text
union(0, 1)   roots 0 and 1 differ -> merge, components 4 -> 3
union(0, 2)   roots 0 and 2 differ -> merge, components 3 -> 2
union(1, 2)   find(1) = find(2) = 0 -> redundant edge, no merge
```

The third edge is the cycle edge the example's Explanation calls the movable cable: it joins two nodes the first two edges already connected, so the union ignores it, but it still counted toward the feasibility gate. With `components = 2` the function returns `2 - 1 = 1`, the expected Output.

#### Solution

The code is the edge stream from the walkthrough, with the `UnionFind` helper carrying the component count.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node_a: int, node_b: int) -> None:
        root_a, root_b = self.find(node_a), self.find(node_b)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        self.components -= 1


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        if len(edges) < n - 1:
            return -1
        uf = UnionFind(n)
        for node_a, node_b in edges:
            uf.union(node_a, node_b)
        return uf.components - 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e × α(n))`

One pass over the edges, where `α` is the inverse Ackermann function (practically constant): path compression and union by rank keep every find and union nearly constant.

##### Space Complexity: `O(n)`

The `parent` and `rank` arrays hold one entry per node; no adjacency structure is ever built.

#### Key Insights

- A redundant edge, one whose endpoints already share a root, is precisely a cable free to move; the union skip and the move count are the same fact seen twice.
- Streaming the edges removes the adjacency list entirely, which is where the approach beats the traversals in both time and space constants.
- `components` is maintained incrementally by `union`, so the answer needs no second pass.
- The feasibility gate still runs first: union-find cannot detect a cable shortage, because a shortage shows up as "too few edges", not as any property of the components.

## Comparison of Solutions

### Time Complexity

- **DFS with Visited Set**: `O(n + e)` - one adjacency build plus one traversal touch per node and edge endpoint.
- **BFS with Visited Set**: `O(n + e)` - the identical touch count with a queue instead of the call stack.
- **Union-Find**: `O(n + e × α(n))` - one streaming pass with nearly constant union and find operations.

### Space Complexity

- **DFS with Visited Set**: `O(n + e)` - adjacency list plus visited flags plus recursion that can reach `n` frames.
- **BFS with Visited Set**: `O(n + e)` - adjacency list plus visited flags plus a bounded frontier queue.
- **Union-Find**: `O(n)` - two arrays over the nodes, with no adjacency structure at all.

### Trade-offs

- **DFS with Visited Set**: the most familiar formulation, but it carries the full adjacency list and the recursion-depth hazard of a 100000-node chain.
- **BFS with Visited Set**: keeps the traversal formulation while removing the overflow risk, at the cost of building the same adjacency list.
- **Union-Find**: the leanest on every resource and the only one that consumes edges as a stream, with the most specialized implementation to write correctly.

### When to Use Each

- **Union-Find (Recommended)**: the default here: the gate, one loop, and `O(n)` auxiliary space fit the constraint sizes best.
- **BFS with Visited Set**: when a traversal is easier to defend in an interview or the adjacency list is needed for follow-up questions.
- **DFS with Visited Set**: when the input is known to be shallow, or as the first formulation to reach before trading the call stack away.

### Optimization Notes

- Every version returns -1 before doing any other work; ordering the gate first makes the -1 case cost `O(1)`.
- The feasibility test is `len(edges) < n - 1` on the raw edge count, self-loops and parallel edges included, because a move relocates any cable regardless of what it currently connects.
- Path compression in `find` plus union by rank is what holds the streaming pass at inverse-Ackermann cost; dropping either keeps the same asymptotics here but weakens the worst-case guarantee.
- The answer is `components - 1` even when the network is already connected: one component yields `0` moves, so no special case is needed.
