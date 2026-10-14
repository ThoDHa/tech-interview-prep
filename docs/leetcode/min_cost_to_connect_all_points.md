# [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/)

**Medium** | **25 minutes** | **Array, Union Find, Graph Theory, Minimum Spanning Tree**

**Pattern:** [Greedy](../patterns/greedy_core/intuition.md), [Union-Find](../patterns/union_find/intuition.md)

**Algorithm:** [Minimum spanning tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree) · [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm) · [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm) · [Disjoint-set (Union-Find)](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)

**Practice:** [`practice/min_cost_to_connect_all_points/solution.py`](../../practice/min_cost_to_connect_all_points/solution.py)

You are given a 2-D integer array `points`, where `points[i] = [xi, yi]`. Each `points[i]` represents a distinct point on a 2-D plane.

The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the **manhattan distance** between the two points, i.e. `|xi - xj| + |yi - yj|`.

Return the minimum cost to connect all points together, such that there exists exactly one path between each pair of points.

## Examples

### Example 1

**Input:** `points = [[0,0],[2,2],[3,3],[2,4],[4,2]]`

**Output:** `10`

## Constraints

- `1 <= points.length <= 1000`
- `-1,000,000 <= xi, yi <= 1,000,000`
- All pairs `(xi, yi)` are distinct.

## Deriving the Solution

The points and Manhattan distances are a complete weighted graph: every pair of points is an edge whose weight is `|xi - xj| + |yi - yj|`, and a cheapest way to connect all points is a [minimum spanning tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree) of that graph. Every solution below builds a spanning structure; they differ in how much of the complete graph they examine.

1. **Start literal.** Enumerate every subset of edges that connects all
   `n` points, keep the ones forming a tree, and take the cheapest. Combinatorial and hopeless at `n = 1000`, but it states the target: see [Brute Force Spanning Tree Enumeration](#brute-force-spanning-tree-enumeration).
2. **Grow a tree one edge at a time.** Prim's algorithm starts from one point
   and repeatedly adds the cheapest edge leaving the tree grown so far. The cut property guarantees each such edge belongs to some minimum spanning tree, so the greedy result is optimal: see [Prim's Algorithm](#prims-algorithm).
3. **Sort the edges instead.** Kruskal's algorithm takes the same greedy view
   from the global side: consider all edges cheapest-first and keep any that joins two different components. On a complete graph with `n(n-1)/2` edges the sort dominates, which is why Prim's lazy-heap variant wins here: see [Kruskal's Algorithm with Union-Find](#kruskals-algorithm-with-union-find).

## Solutions

### Brute Force Spanning Tree Enumeration

#### Derivation

The most literal reading of "exactly one simple path between any two points" is a tree, and the cheapest such tree is the minimum over all spanning trees. Enumerating trees directly means choosing `n - 1` edges out of the `n(n-1)/2` possible pairs, checking connectivity, and taking the minimum total weight. A tractable small-scale version enumerates edge subsets through recursion: for each candidate edge, either include it (if it does not close a cycle) or skip it, and record the cost whenever the included edges form a spanning tree:

1. List all pairs `(i, j)` with their Manhattan weights.
2. Recursively decide each pair in order, tracking the included set, its
   total weight, and a union-find over included edges.
3. When the included edges connect all `n` points with exactly `n - 1` of
   them, compare the total against the best found.
4. Return the best total.

#### Walkthrough

The explosion is visible on the smallest interesting input, three collinear points `[0,0], [1,0], [2,0]`. The three pair weights are `0-1: 1`, `1-2: 1`, `0-2: 2`, and the subsets that span:

```text
edges {0-1, 0-2}   weight 1 + 2 = 3   spans, a tree   best = 3
edges {0-1, 1-2}   weight 1 + 1 = 2   spans, a tree   best = 2
edges {0-2, 1-2}   weight 1 + 2 = 3   spans, a tree   best stays 2
edges {0-1}        1 edge for 3 points                 not spanning
edges {0-1, 1-2, 0-2}   3 edges close a cycle          not a tree
```

The include branch runs before the skip branch, so the first spanning subset found is `{0-1, 0-2}` at weight `3`; backtracking then swaps in the cheaper `1-2` edge, dropping `best` to `2`, and the last subset cannot improve it. The minimum over spanning trees is `2`, which is the answer this enumeration returns and the correct output for the tailored input. The same procedure on Example 1's five points already weighs `10 choose 4 = 210` edge subsets, and at `n = 1000` the subsets outnumber atoms, which is exactly the wall the next solutions climb over.

#### Solution

The code is the recursive include-or-skip enumeration, kept honest by union-find cycle checks.

```python
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        count = len(points)
        pairs = [
            (abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
            for i in range(count)
            for j in range(i + 1, count)
        ]

        parent = list(range(count))

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        best = [None]

        def enumerate_edges(index: int, used: int, total: int) -> None:
            if used == count - 1:
                if best[0] is None or total < best[0]:
                    best[0] = total
                return
            if index == len(pairs):
                return
            weight, a, b = pairs[index]
            root_a, root_b = find(a), find(b)
            if root_a != root_b:
                parent[root_b] = root_a
                enumerate_edges(index + 1, used + 1, total + weight)
                parent[root_b] = root_b
            enumerate_edges(index + 1, used, total)

        enumerate_edges(0, 0, 0)
        return best[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^m * α(n))` with `m = n(n-1)/2`

Every pair is included or skipped, so the recursion visits `2^m` states, each paying near-constant union-find work; viable only for a handful of points.

##### Space Complexity: `O(n + m)`

The pair list is `O(m)` (it can be streamed to `O(n)`), and the recursion depth is `O(m)`.

#### Key Insights

- This solution is the specification: "cheapest set of edges forming a spanning tree", executed literally.
- The union-find check inside the recursion prunes subsets containing cycles early, but the exponential core remains.
- The jump from here to Prim's is one observation: the cheapest edge crossing any cut is always safe, so the choices never need revisiting.

### Prim's Algorithm

#### Derivation

The enumeration re-decides overlapping subproblems because it never asks what makes an edge safe. The [cut property](https://en.wikipedia.org/wiki/Minimum_spanning_tree#Cut_property) answers: for any partition of the points into tree and non-tree, the cheapest edge crossing the partition belongs to some minimum spanning tree. So grow one tree from point `0`, and at every step take the cheapest edge from a connected point to an unconnected one; the process cannot leave the optimal tree. A min-heap holds `(cost, point)` entries for reaching unconnected points, seeded with `(0, 0)`, and a boolean array claims points:

1. Seed the heap with `(0, 0)`: reaching point `0` costs nothing.
2. Pop the cheapest `(cost, index)`. If its point is already connected, the
   entry is stale: skip it.
3. Otherwise connect the point, adding `cost` to `total`.
4. Push its Manhattan distance to every unconnected point.
5. Stop when all `n` points are connected; return `total`.

#### Walkthrough

Let us grow the tree on Example 1: `points = [[0,0],[2,2],[3,3],[2,4],[4,2]]`. Each row shows a pop, its effect, and the pushes; the heap contents after each claim are abbreviated to the entries that matter:

```text
pop (0, 0)  claim point 0 (0,0)    total = 0   push (4,1) (6,2) (6,3) (6,4)
pop (4, 1)  claim point 1 (2,2)    total = 4   push (2,2) (2,3) (2,4)
pop (2, 2)  claim point 2 (3,3)    total = 6   push (2,3) (2,4)
pop (2, 3)  claim point 3 (2,4)    total = 8   push (4,4)
pop (2, 3)  stale, point 3 already connected
pop (2, 4)  claim point 4 (4,2)    total = 10
```

Point `3` generates two heap entries: it was offered at cost `2` by point `1` and again at cost `2` by point `2`; the first pop claims it and the duplicate is skipped as stale. Four claims later every point is connected and `total = 10`, matching the expected Output for Example 1. The final tree joins point `0` to point `1` and hubs the rest through point `1`, exactly the MST the sorted edge list confirms.

#### Solution

The code is the lazy-heap growth: pop, stale-skip, claim, push.

```python
import heapq
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        total = 0
        connected = 0
        in_tree = [False] * len(points)
        heap = [(0, 0)]
        while connected < len(points):
            cost, index = heapq.heappop(heap)
            if in_tree[index]:
                continue
            in_tree[index] = True
            connected += 1
            total += cost
            x, y = points[index]
            for other in range(len(points)):
                if not in_tree[other]:
                    other_x, other_y = points[other]
                    distance = abs(x - other_x) + abs(y - other_y)
                    heapq.heappush(heap, (distance, other))
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² * log n)`

Each of the `n` claims scans all `n` points and may push one entry per pair, so the heap holds `O(n²)` entries with `O(log n²) = O(log n)` costs; the complete graph makes this the right trade against Kruskal's global sort.

##### Space Complexity: `O(n²)`

The heap's worst case holds one entry per pair of points; the `in_tree` array is `O(n)`.

#### Key Insights

- The cut property converts an exponential choice problem into a greedy one: the cheapest frontier edge is always safe, so nothing is ever reconsidered.
- Lazy deletion (stale entries skipped at pop time) avoids hunting the heap for decreasing keys, which Python's `heapq` cannot do anyway.
- The complete graph is never materialized: distances are computed on demand from coordinates, which is what keeps the space bounded by the heap rather than an adjacency matrix.

### Kruskal's Algorithm with Union-Find

#### Derivation

Prim's grows locally; [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm) takes the global view: sort every edge by weight and sweep cheapest-first, keeping an edge exactly when its endpoints are in different components. Union-find makes the component test near-constant, and the sweep stops after `n - 1` acceptances. On this problem's complete graph the sort sees all `n(n-1)/2` edges, which costs more than Prim's lazy heap at `n = 1000`, but the structure shines when edges are sparse or pre-sorted:

1. Build all pair edges `(weight, i, j)` and sort by weight.
2. Initialize union-find over the `n` points.
3. Sweep the sorted edges: when `find(i) != find(j)`, union the components
   and add the weight to `total`; stop after `n - 1` unions.
4. Return `total`.

#### Walkthrough

Let us sweep the edges on Example 1: `points = [[0,0],[2,2],[3,3],[2,4],[4,2]]`. The sorted pairs begin `1-2: 2`, `1-3: 2`, `1-4: 2`, `2-3: 2`, `2-4: 2`, `0-1: 4`, ... (all five pairs among points `1..4` weigh `2`, and every pair touching point `0` weighs `4` or more):

```text
edge 1-2 (w=2)  roots 1, 2  union -> {1,2}          total = 2
edge 1-3 (w=2)  roots 1, 3  union -> {1,2,3}        total = 4
edge 1-4 (w=2)  roots 1, 4  union -> {1,2,3,4}      total = 6
edge 2-3 (w=2)  roots equal  cycle, skip
edge 2-4 (w=2)  roots equal  cycle, skip
edge 0-1 (w=4)  roots 0, 1  union -> {0,1,2,3,4}    total = 10
four unions on five points -> stop
```

The first three weight-`2` edges merge points `1..4` into one component (the tie order among equal weights is arbitrary but immaterial: any spanning choice of them weighs the same), the remaining weight-`2` pairs are rejected by the shared root, and edge `0-1` joins the last isolated point. After four unions the sweep stops with `total = 10`, matching the expected Output for Example 1.

#### Solution

The code is the sorted sweep with union-find cycle rejection and an early stop.

```python
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        count = len(points)
        edges = sorted(
            (abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
            for i in range(count)
            for j in range(i + 1, count)
        )
        parent = list(range(count))
        rank = [0] * count

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        total = 0
        unions = 0
        for weight, a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                continue
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
            total += weight
            unions += 1
            if unions == count - 1:
                break
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² * log n)`

The `n(n-1)/2` edges are sorted, dominating the near-constant-amortized union-find sweep; asymptotically tied with Prim's here, with a larger constant from materializing every pair.

##### Space Complexity: `O(n²)`

The edge list holds one entry per pair before sorting; the union-find arrays are `O(n)`.

#### Key Insights

- Sorting once replaces all priority bookkeeping: after the sort, the sweep is branch-free apart from the union test.
- The `n - 1` union cap lets the sweep abandon the tail of the sorted list, which is where the heaviest edges live.
- On a complete geometric graph this pays for edges Prim's never looks at; on a sparse graph the roles reverse, and Kruskal's is the leaner method.

## Comparison of Solutions

### Time Complexity

- **Brute Force Spanning Tree Enumeration**: `O(2^m * α(n))`, `m = n(n-1)/2` - every edge subset decided recursively.
- **Prim's Algorithm**: `O(n² * log n)` - `n` claims, each pushing up to `n` heap entries.
- **Kruskal's Algorithm with Union-Find**: `O(n² * log n)` - sorting all `m` pairs dominates the linear sweep.

### Space Complexity

- **Brute Force Spanning Tree Enumeration**: `O(n + m)` - the pair list and recursion stack.
- **Prim's Algorithm**: `O(n²)` - the lazy heap in the worst case; no edge list is ever stored.
- **Kruskal's Algorithm with Union-Find**: `O(n²)` - the materialized, sorted edge list.

### Trade-offs

- The brute force defines optimality without greedy reasoning and cannot run past toy sizes.
- Prim's never materializes the complete graph, computing distances on demand; Kruskal's pays memory for a simpler, sort-driven loop.
- Both greedy algorithms are optimal by the cut property; the choice between them on a complete graph is a constant-factor contest that Prim's lazy heap wins.

### When to Use Each

- **Brute Force Spanning Tree Enumeration**: validating the greedy methods on tiny inputs, or when the connectivity requirement deviates from a plain tree.
- **Prim's Algorithm**: dense or complete graphs, this problem's geometry included; also the natural choice when points stream in (recommended here).
- **Kruskal's Algorithm with Union-Find**: sparse graphs with a known edge list, and any problem that reuses the components afterward.

### Optimization Notes

- An `O(n²)` Prim's without a heap (array-scan for the minimum frontier distance) beats the lazy heap's log factor on dense graphs and is worth reaching for at the constraint ceiling.
- Manhattan distance decomposes by sign pattern (`±x ± y` maxima), which yields an `O(n)` Borůvka-style improvement; beyond this problem's scope but the known follow-up.
- Both greedy solutions accept any tie order among equal weights: every tie-breaking choice yields a minimum spanning tree, though possibly a different one.

