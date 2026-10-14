# [Count the Number of Complete Components](https://www.fastprep.io/problems/amazon-count-complete-components)

**Medium** | **NN minutes** | **Graph, Depth First Search, Breadth First Search, Union Find**

You are given an integer n and an undirected graph whose vertices are numbered from 0 through n - 1. The array edges contains each undirected edge [u, v].

A connected component is complete when every pair of distinct vertices in that component is joined by an edge.

Return the number of complete connected components. A component containing one vertex is complete.

## Examples

### Example 1

**Input:** `n = 6`, `edges = [[0,1],[0,2],[1,2],[3,4]]`

**Output:** `3`

**Explanation:** The components are {0,1,2}, {3,4}, and {5}. Each contains every possible internal edge, so all three are complete.

### Example 2

**Input:** `n = 6`, `edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]`

**Output:** `1`

**Explanation:** The component {0,1,2} is complete. The component {3,4,5} is missing edge [4,5], so it is not complete.

### Example 3

**Input:** `n = 1`, `edges = []`

**Output:** `1`

**Explanation:** The only vertex forms a one-vertex complete component.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-count-complete-components; fill them in. -->

## Solutions

### DFS with Component Census

#### Derivation

The definition of a complete component reduces to an arithmetic identity once a component is isolated: a component with `vertices` vertices is complete exactly when it contains every possible edge among them, and there are `vertices × (vertices - 1) / 2` such pairs. The most literal reading is therefore: find each connected component, count its vertices and its edges, and compare the edge count against the pair formula:

1. Build `adjacency` as a list of neighbor lists, appending both directions of
   every edge.
2. Allocate `visited`, a boolean list over all `n` vertices.
3. For every unvisited vertex, run `dfs` from it and tally while traversing:
   `component_size` counts the vertices reached, `component_edge_count`
   counts every directed hop, so each internal edge is counted twice.
4. A component is complete when
   `component_edge_count == component_size * (component_size - 1)`.
5. Count the components that pass the test and return the total.

#### Walkthrough

Example 1, `n = 6`, `edges = [[0,1],[0,2],[1,2],[3,4]]`. The scan starts at vertex `0` and floods its component; `component_edge_count` doubles each internal edge:

```text
dfs from 0:  visit 0 -> size 1, edges 2   (adjacency[0] = [1, 2])
             visit 1 -> size 2, edges 4   (adjacency[1] = [0, 2])
             visit 2 -> size 3, edges 6   (adjacency[2] = [0, 1])
test: edges 6 == 3 * 2 -> complete, complete_components = 1
dfs from 3:  visit 3 -> size 1, edges 1   (adjacency[3] = [4])
             visit 4 -> size 2, edges 2   (adjacency[4] = [3])
test: edges 2 == 2 * 1 -> complete, complete_components = 2
vertex 5:    unvisited, no edges -> size 1, edges 0
test: edges 0 == 1 * 0 -> complete, complete_components = 3
```

Each visit adds that vertex's adjacency length to `component_edge_count`, so every internal edge lands in the tally once from each endpoint: the triangle `{0,1,2}` accumulates `2 + 2 + 2 = 6` directed hops, the pair `{3,4}` accumulates `1 + 1 = 2`, and the isolated vertex `5` contributes none. All three pass the identity `component_edge_count == component_size × (component_size - 1)`, and the function returns `3`, matching the expected Output.

#### Solution

The code is the census from the walkthrough: `dfs` accumulates `component_size` and `component_edge_count` in an enclosing list so the recursion can update them.

```python
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        adjacency: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            adjacency[u].append(v)
            adjacency[v].append(u)

        visited = [False] * n
        complete_components = 0

        for start in range(n):
            if visited[start]:
                continue
            component_size = 0
            component_edge_count = 0

            def dfs(vertex: int) -> None:
                nonlocal component_size, component_edge_count
                visited[vertex] = True
                component_size += 1
                component_edge_count += len(adjacency[vertex])
                for neighbor in adjacency[vertex]:
                    if not visited[neighbor]:
                        dfs(neighbor)

            dfs(start)
            if component_edge_count == component_size * (component_size - 1):
                complete_components += 1

        return complete_components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e)`

Every vertex enters `dfs` once and every adjacency list is scanned once, where `e = len(edges)`.

##### Space Complexity: `O(n + e)`

The adjacency lists hold both directions of every edge, and the recursion stack can grow to `n` frames on a path-shaped component.

#### Key Insights

- Counting each directed hop turns completeness into a single comparison: every internal edge is seen from both endpoints, so the census total is exactly twice the undirected edge count.
- The identity `component_edge_count == component_size × (component_size - 1)` uses directed hops; the undirected form would need `vertices × (vertices - 1) / 2`.
- Connectivity alone proves nothing: Example 2's `{3,4,5}` is connected but carries only `2` edges where a triangle needs `3`.

### BFS with Component Census

#### Derivation

The census traversal has one weakness inherited from recursion: a single long chain of vertices drives the call stack one frame per vertex, and Python's default recursion limit is 1,000. The traversal order is irrelevant to the census, so DFS can be swapped for an iterative [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) whose queue replaces the call stack; the per-component arithmetic is unchanged:

1. Build `adjacency` and `visited` as before.
2. For each unvisited start, seed a `queue` with it and mark it visited.
3. Pop a vertex, add `1` to `component_size` and `len(adjacency[vertex])` to
   `component_edge_count`, and enqueue each unvisited neighbor after marking
   it visited.
4. Apply the same completeness identity
   `component_edge_count == component_size * (component_size - 1)` when the
   queue drains, and count the components that pass.

#### Walkthrough

Example 2, `n = 6`, `edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]`. The adjacency lists are `0:[1,2]`, `1:[0,2]`, `2:[0,1]`, `3:[4,5]`, `4:[3]`, `5:[3]`. Starting from vertex `0`:

```text
seed 0:   visited = {0}, queue = [0]
pop 0:    size 1, edges 2; enqueue 1, 2        queue = [1, 2]
pop 1:    size 2, edges 4; neighbor 0 visited, neighbor 2 visited
pop 2:    size 3, edges 6; 0 and 1 visited
test: edges 6 == 3 * 2 -> complete, complete_components = 1
seed 3:   visited += {3}, queue = [3]
pop 3:    size 1, edges 2; enqueue 4, 5        queue = [4, 5]
pop 4:    size 2, edges 3; 3 visited
pop 5:    size 3, edges 4; 3 visited
test: edges 4 == 3 * 2? No (4 != 6) -> not complete
scan:     vertices 0..5 all visited -> done
```

Component `{0,1,2}` is a triangle: `3` vertices, `6` hops, and `6 == 3 × 2` passes. Component `{3,4,5}` holds `3` vertices but only `2` edges, `4` hops, and `4 != 3 × 2` fails: it is connected but missing edge `[4,5]`. Every vertex is covered, so the function returns `1`, matching the expected Output.

#### Solution

The code is the same census with the queue discipline from the walkthrough: mark visited at enqueue time so no vertex is counted twice.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        adjacency: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            adjacency[u].append(v)
            adjacency[v].append(u)

        visited = [False] * n
        complete_components = 0

        for start in range(n):
            if visited[start]:
                continue
            component_size = 0
            component_edge_count = 0
            queue = deque([start])
            visited[start] = True

            while queue:
                vertex = queue.popleft()
                component_size += 1
                component_edge_count += len(adjacency[vertex])
                for neighbor in adjacency[vertex]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

            if component_edge_count == component_size * (component_size - 1):
                complete_components += 1

        return complete_components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e)`

Every vertex is enqueued exactly once and every adjacency list scanned once.

##### Space Complexity: `O(n + e)`

The adjacency lists dominate; the queue holds at most one frontier of a component, bounded by `n`.

#### Key Insights

- Marking a neighbor visited at enqueue time, not at pop time, guarantees each vertex contributes its adjacency length exactly once to `component_edge_count`.
- The queue bounds memory by the widest frontier instead of the longest chain, which is what removes the recursion-limit hazard.
- A singleton contributes `0` hops against `1 × 0 = 0`, so isolated vertices pass automatically with no special case.

### Union-Find with Vertex and Edge Tallies

#### Derivation

Both traversals pay a traversal per component. [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) answers the question without ever walking a component: union the endpoints of every edge, then classify the finished groups. The completeness test per root needs two tallies, both computable in one pass after the unions: how many vertices carry that root (`vertex_tally`), and how many edges have both endpoints carrying it (`edge_tally`). A root's group is complete when `edge_tally == vertex_tally × (vertex_tally - 1) / 2`, the undirected pair count:

1. Build `UnionFind(n)` and union `u` with `v` for every edge, skipping
   no-ops where the roots already match.
2. First pass over all vertices: `vertex_tally[find(vertex)] += 1`.
3. Second pass over all edges: `edge_tally[find(u)] += 1`, counting each
   undirected edge exactly once at its shared root.
4. A root is a complete component when
   `edge_tally[root] == vertex_tally[root] * (vertex_tally[root] - 1) // 2`;
   count how many roots satisfy it and return the count.

#### Walkthrough

Example 1, `n = 6`, `edges = [[0,1],[0,2],[1,2],[3,4]]`. After the unions, the roots are `0` for `{0,1,2}`, `3` for `{3,4}`, and `5` for `{5}`:

```text
vertex tallies:  root 0 -> 3      root 3 -> 2      root 5 -> 1
edge tallies:    edge [0,1] -> root 0
                 edge [0,2] -> root 0
                 edge [1,2] -> root 0      root 0 total 3
                 edge [3,4] -> root 3      root 3 total 1
completeness:    root 0: 3 == 3*2/2 = 3 -> complete
                 root 3: 1 == 2*1/2 = 1 -> complete
                 root 5: 0 == 1*0/2 = 0 -> complete
```

Every root's edge tally matches its pair formula, so the function returns `3`, matching the expected Output. For Example 2, the same tables give root `3` (group `{3,4,5}`) an edge tally of `2` against a required `3 * 2 / 2 = 3`, which fails, and only root `0` passes: the return is `1`.

#### Solution

The code is the union pass followed by the two tally passes from the walkthrough, with `UnionFind` carrying the root map.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, vertex: int) -> int:
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, first: int, second: int) -> None:
        first_root, second_root = self.find(first), self.find(second)
        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1


class Solution:
    def solve(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        for u, v in edges:
            uf.union(u, v)

        vertex_tally = [0] * n
        edge_tally = [0] * n
        for vertex in range(n):
            vertex_tally[uf.find(vertex)] += 1
        for u, v in edges:
            edge_tally[uf.find(u)] += 1

        complete_components = 0
        for root in range(n):
            if (vertex_tally[root] > 0
                    and edge_tally[root]
                    == vertex_tally[root] * (vertex_tally[root] - 1) // 2):
                complete_components += 1

        return complete_components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n + e) × α(n))`

`e` unions plus `n + e` find calls, each nearly constant with path compression and union by rank; the tally passes are linear scans.

##### Space Complexity: `O(n)`

The parent and rank arrays plus the two tally arrays, all sized by the vertex count; the edge list itself is input.

#### Key Insights

- Union-Find never materializes adjacency lists: both tallies read the finished root assignments, so the graph is never traversed as a graph.
- The completeness formula flips to the undirected form `vertex_tally × (vertex_tally - 1) / 2` because the edge tally counts each undirected edge once, unlike the traversal census's doubled hops.
- `vertex_tally[root] > 0` filters empty roots: every non-root slot would otherwise trivially satisfy `0 == 0` and corrupt the count.

## Comparison of Solutions

### Time Complexity

- **DFS with Component Census**: `O(n + e)` - one visit per vertex and one scan of each adjacency list.
- **BFS with Component Census**: `O(n + e)` - one enqueue per vertex and one scan of each adjacency list.
- **Union-Find with Vertex and Edge Tallies**: `O((n + e) × α(n))` - near-constant unions and finds, with linear tally passes on top.

### Space Complexity

- **DFS with Component Census**: `O(n + e)` - adjacency lists plus a recursion stack up to `n` deep.
- **BFS with Component Census**: `O(n + e)` - adjacency lists plus a queue bounded by the widest frontier.
- **Union-Find with Vertex and Edge Tallies**: `O(n)` - parent, rank, and tally arrays; no adjacency structure at all.

### Trade-offs

- **DFS with Component Census**: the shortest derivation from the definition, but it inherits the recursion-depth hazard on long, thin components.
- **BFS with Component Census**: same census with the stack swapped for a queue, at the cost of import and enqueue-time visited discipline.
- **Union-Find with Vertex and Edge Tallies**: the only approach that avoids building adjacency lists, but it needs the helper class and a subtler per-root formula.

### When to Use Each

- **BFS with Component Census (Recommended)**: the interview default: linear, iterative, and the doubled-hop census is easy to explain.
- **DFS with Component Census**: when the input is small or components are known to be shallow, or when the interviewer asks for the most direct translation of the definition.
- **Union-Find with Vertex and Edge Tallies**: when the graph arrives as a bare edge list you prefer not to expand, when edges stream in dynamically, or when connectivity queries outlive this single answer.

### Optimization Notes

- The traversal census counts directed hops (`component_edge_count == size × (size - 1)`) while the Union-Find tally counts undirected edges (`edge_tally == size × (size - 1) // 2`); mixing the two formulas is the classic off-by-a-factor-of-two bug on this problem.
- Marking visited at enqueue time (BFS) or on entry (DFS) is what keeps `component_edge_count` exact; a vertex counted twice inflates both tallies and can brand a complete component incomplete, never the reverse (an extra counted degree can no longer fit the pair formula).
- `union` returning early when the roots already match keeps duplicate or redundant edges cheap; a duplicated edge in the input would push `edge_tally` past the pair formula and mark the component incomplete, which is the honest answer for a multi-graph input.
- All three solutions count singleton components for free: `0 == 1 × 0` and `0 == 1 × 0 // 2` both hold, so no special case for `edges == []` is needed (Example 3).
