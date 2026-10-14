# [Redundant Connection](https://leetcode.com/problems/redundant-connection/)

**Medium** | **25 minutes** | **Depth-First Search, Breadth-First Search, Union Find, Graph Theory**

**Pattern:** [Union-Find](../patterns/union_find/intuition.md)

**Algorithm:** [Disjoint-set (Union-Find)](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)

**Practice:** [`practice/redundant_connection/solution.py`](../../practice/redundant_connection/solution.py)

You are given a connected **undirected graph** with `n` nodes labeled from `1` to `n`. Initially, it contained no cycles and consisted of `n-1` edges.

We have now added one additional edge to the graph. The edge has two **different** vertices chosen from `1` to `n`, and was not an edge that previously existed in the graph.

The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` represents an edge between nodes `ai` and `bi` in the graph.

Return an edge that can be removed so that the graph is still a connected non-cyclical graph. If there are multiple answers, return the edge that appears last in the input `edges`.

## Examples

### Example 1

**Input:** `edges = [[1,2],[1,3],[3,4],[2,4]]`

**Output:** `[2,4]`

### Example 2

**Input:** `edges = [[1,2],[1,3],[1,4],[3,4],[4,5]]`

**Output:** `[3,4]`

## Constraints

- `n == edges.length`
- `3 <= n <= 1000`
- `1 <= edges[i][0] < edges[i][1] <= edges.length`
- There are no repeated edges and no self-loops in the input.

## Deriving the Solution

The graph is a tree plus exactly one extra edge, so the cycle is unique and the redundant edge is an edge of that cycle; the only real question is which edge of the cycle to report, and the tie-break (last in the input) supplies the answer's shape: process edges in input order and return the first one that closes a cycle. Every solution below detects that closing moment, differing only in how the "already connected?" question is answered.

1. **Start literal.** Take the definition at face value: for each edge, ask
   whether removing it leaves the graph a connected tree on `n` nodes, and return the last edge for which it does. Each trial pays a full connectivity check, `O(n²)` overall: see [Brute Force Edge Removal](#brute-force-edge-removal).
2. **Spot the repetition.** Every trial rebuilds the same adjacency structure
   and rescans the same graph. Reading the edges in input order and asking a different question inverts the work: an edge is redundant exactly when its endpoints are already joined by the edges listed before it, so one pass with a connectivity structure answers everything.
3. **Answer "already connected?" in near-constant time.** A disjoint-set
   structure maintains the components of the growing forest: each edge unions its endpoints, and the first edge whose endpoints share a component is the answer: see [Union-Find with Early Exit](#union-find-with-early-exit).

## Solutions

### Brute Force Edge Removal

#### Derivation

The most literal reading of "return an edge that can be removed so the graph is still connected and acyclic" tries each removal and tests the remainder. The test itself reduces to two checks: the remainder holds `n - 1` edges (it does by construction, since `n` edges minus one is `n - 1`), and it connects all `n` nodes; with the edge count fixed, connectivity alone certifies a tree. Trying edges from last to first makes the first success the last-listed removable edge, honoring the tie-break:

1. Scan `edges` from the last entry to the first, keeping the candidate
   `(a, b)` under trial.
2. Build the adjacency lists of every edge except the candidate.
3. Flood fill from node `a` with a recursive `dfs` over the `visited` set.
4. If `len(visited) == n`, the remainder is a tree: return the candidate.
5. Otherwise move to the next earlier edge.

#### Walkthrough

Let us run the removal loop on Example 1: `edges = [[1,2],[1,3],[3,4],[2,4]]`, `n = 4`. Each row shows the candidate removed, the remaining edges, and whether the fill from the candidate's first endpoint reaches all `4` nodes:

```text
remove [2,4]   edges [1-2, 1-3, 3-4]   dfs from 2 reaches {2, 1, 3, 4}   connected -> return [2, 4]
```

The very first candidate succeeds: dropping edge `[2, 4]` leaves the path `2 - 1 - 3 - 4`, which spans all `n = 4` nodes with `n - 1 = 3` edges, exactly a tree. The scan returns `[2, 4]`, matching the expected Output for Example 1. The reverse scan is what encodes the tie-break: had an earlier edge also been removable, this candidate order would still have met the last-listed one first. On Example 2 the first candidate `[4, 5]` fails (removing a true tree edge disconnects node `5`), and the second candidate `[3, 4]` succeeds.

#### Solution

The code is the reverse scan with the connectivity trial spelled out.

```python
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)

        def connected_without(removed: int) -> bool:
            adjacency = [[] for _ in range(n + 1)]
            for index, (a, b) in enumerate(edges):
                if index == removed:
                    continue
                adjacency[a].append(b)
                adjacency[b].append(a)
            visited = set()

            def dfs(node: int) -> None:
                visited.add(node)
                for neighbor in adjacency[node]:
                    if neighbor not in visited:
                        dfs(neighbor)

            dfs(edges[removed][0])
            return len(visited) == n

        for removed in range(n - 1, -1, -1):
            if connected_without(removed):
                return edges[removed]
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Up to `n` candidates are tried, and each trial rebuilds the adjacency lists and runs a fill over `n - 1` edges: `O(n)` per trial, quadratic overall.

##### Space Complexity: `O(n)`

The per-trial adjacency lists, the visited set, and the recursion stack are linear and rebuilt per candidate.

#### Key Insights

- The reverse scan turns "return the last valid answer" into "return the first hit", so no bookkeeping of alternatives is needed.
- The connectivity trial does double duty as the acyclicity test: `n - 1` edges plus full reachability is precisely a tree.
- Rebuilding everything per candidate is where the quadratic cost lives; nothing learned about one remainder carries to the next.

### Union-Find with Early Exit

#### Derivation

The brute force keeps asking a connectivity question about the graph minus one edge. Invert it: process edges in input order, accumulating a forest, and ask whether this edge joins two nodes that earlier edges already connect. In a tree plus one extra edge, the forest grows cleanly until the extra edge arrives; the path built by the earlier edges is exactly the cycle's other arc, so the first edge whose endpoints share a component is the redundant one, and input order makes it the last-listed removable edge, satisfying the tie-break for free. A [disjoint-set](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) structure answers the shared-component question in amortized near-constant time:

1. Give nodes `0` through `n` their own entries in `parent` and a `rank` of
   `0` (node `0` is padding so labels index directly).
2. For each edge `(a, b)` in input order, find the roots of both endpoints.
3. Equal roots mean earlier edges already connect `a` to `b`: return `[a, b]`.
4. Otherwise link the lower-rank root under the higher, bumping the rank on a
   tie, and continue.
5. The extra edge guarantees the early exit fires before the input runs out.

`find` halves each node's hop to its root on every walk (`parent[node] = parent[parent[node]]`), and union by rank keeps the trees shallow.

#### Walkthrough

Let us run the merge pass on Example 1: `edges = [[1,2],[1,3],[3,4],[2,4]]`. Each row shows the edge, the roots found, and the state after the union:

```text
edge 1-2   roots 1, 2   union   parent = [0, 1, 1, 3, 4]  rank = [0, 1, 0, 0, 0]
edge 1-3   roots 1, 3   union   parent = [0, 1, 1, 1, 4]  rank = [0, 1, 0, 0, 0]
edge 3-4   roots 1, 4   union   parent = [0, 1, 1, 1, 1]  rank = [0, 1, 0, 0, 0]
edge 2-4   roots 1, 1   cycle! -> return [2, 4]
```

The first three edges each merge a new node into the component rooted at `1`, building the path `2 - 1 - 3 - 4` piecewise. Edge `[2, 4]` then finds root `1` on both sides: the earlier edges already connect `2` to `4` through `1` and `3`, so this edge closes the cycle and is returned, matching the expected Output for Example 1. On the tailored case `[[3,4],[1,2],[1,3],[1,4]]` the unions build `{3, 4}` and `{1, 2, 3}` before edge `[1, 4]` finds both endpoints rooted at `1` and returns `[1, 4]`: the same early exit, reached with the components merged in a different order.

#### Solution

The code is the merge pass with the cycle check as the return statement.

```python
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = list(range(n + 1))
        rank = [0] * (n + 1)

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                return [a, b]
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * α(n))`

Each of the `n` edges pays two finds amortized to `α(n)`, the inverse Ackermann function, a constant below `5` for any input that fits in memory; the early exit usually stops well before the last edge.

##### Space Complexity: `O(n)`

The `parent` and `rank` arrays; the iterative `find` adds no stack, and no adjacency structure exists.

#### Key Insights

- Inverting the question is the whole win: "is the graph without this edge connected?" becomes "are these two nodes already connected?", which the running structure answers in near-constant time.
- Input order does the tie-break: the first collision is automatically the last-listed removable edge, so no candidate collection is needed.
- The early exit is structural, not an optimization: the problem guarantees exactly one extra edge, so the loop provably returns inside the pass.

## Comparison of Solutions

### Time Complexity

- **Brute Force Edge Removal**: `O(n²)` - up to `n` trials, each a fresh `O(n)` connectivity check.
- **Union-Find with Early Exit**: `O(n * α(n))` - one pass with two near-constant finds per edge.

### Space Complexity

- **Brute Force Edge Removal**: `O(n)` - adjacency lists, visited set, and recursion stack rebuilt per trial.
- **Union-Find with Early Exit**: `O(n)` - two flat arrays, no adjacency structure.

### Trade-offs

- The brute force reads as the problem statement and needs no data-structure repertoire, but its per-trial rebuild discards everything it learns.
- Union-Find makes one pass and exits on the first collision; the cost is carrying the disjoint-set machinery and trusting that input order encodes the tie-break.

### When to Use Each

- **Brute Force Edge Removal**: to state the specification executable before optimizing, or in a setting where edges arrive with arbitrary deletion semantics.
- **Union-Find with Early Exit**: the interview answer, and the direct ancestor of dynamic-connectivity designs where edges stream in continuously (recommended here).

### Optimization Notes

- The `parent` array is sized `n + 1` because node labels run `1..n`; index `0` is padding so no label translation is needed anywhere.
- Union by rank plus path halving keeps finds effectively constant; on a pure path input the raw chain without them would degrade finds to `O(n)` and the pass to `O(n²)`.
- The tie-break is load-bearing: with "any answer" semantics a plain cycle scan would do, but "last in input" is what makes the single input-order pass provably correct.

