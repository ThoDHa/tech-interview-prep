# [Dijkstra Shortest Paths in a Weighted Undirected Graph](https://www.fastprep.io/problems/amazon-shortest-path-weighted-graph)

**Medium** | **NN minutes** | **Graph, Shortest Path, Heap**

You are given vertexCount vertices numbered from 0 to vertexCount - 1, an array of undirected weighted edges, and a source vertex. Each edge is [u, v, weight] with a nonnegative weight.

Return the shortest distance from source to every vertex in vertex order. Return -1 for an unreachable vertex. Parallel edges and self-loops are allowed, and all distance arithmetic must use signed 64-bit values.

## Examples

### Example 1

**Input:** `vertexCount = 5`, `edges = [[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,3,5]]`, `source = 0`

**Output:** `[0,3,1,4,-1]`

**Explanation:** Vertex 1 is reached more cheaply through vertex 2, vertex 3 then follows through vertex 1, and vertex 4 is disconnected.

### Example 2

**Input:** `vertexCount = 1`, `edges = []`, `source = 0`

**Output:** `[0]`

**Explanation:** The source has distance zero from itself.

### Example 3

**Input:** `vertexCount = 4`, `edges = [[0,1,10],[0,1,3],[1,2,0],[2,3,7],[0,3,20]]`, `source = 0`

**Output:** `[0,3,3,10]`

**Explanation:** The lighter parallel edge reaches vertex 1, the zero-weight edge reaches vertex 2 at the same distance, and the best route to vertex 3 costs 10.

## Constraints

- `1 <= vertexCount <= 100000.`
- `0 <= edges.length <= 200000.`
- `Every edge has valid endpoints and a weight in [0, 1000000000].`
- `0 <= source < vertexCount.`
- `Every reachable shortest distance fits a signed 64-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
