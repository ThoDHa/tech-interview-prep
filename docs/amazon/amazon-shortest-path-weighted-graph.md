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

## Deriving the Solution

Nonnegative weights buy the one property everything else builds on: settling vertices in increasing distance order is safe, because any path leaving the settled frontier can only get more expensive. [Network Delay Time](../leetcode/network_delay_time.md) shares the nonnegative weights and the Dijkstra core, then answers a different question: it collapses the distances into one number, the moment the last node on a directed graph receives the signal, where this statement returns every vertex's distance in order on an undirected graph. The task then reduces to "hand me the not-yet-settled vertex with the smallest tentative distance, fast", and the two solutions below differ only in how literally they answer that request.

1. **Start literal.** Relax every edge over and over; a pass that changes nothing means every shortest distance has settled: correct, `O(V * E)`: see [Bellman-Ford Relaxation](#bellman-ford-relaxation).
2. **Spot the waste.** A full sweep touches every edge even though each round only the frontier's cheapest vertex can improve anything; most relaxations are re-checks of vertices whose distance stopped changing long ago.
3. **Fix it with a heap.** Keep only the frontier in a min-heap keyed by tentative distance, pop the true nearest vertex each step, and ignore stale entries: `O(E log V)`: see [Dijkstra with a Min-Heap](#dijkstra-with-a-min-heap).

## Solutions

### Bellman-Ford Relaxation

#### Derivation

The statement's most literal reading asks for the shortest distance to every vertex, so propagate what is known until nothing improves:

1. Keep `distances`, one slot per vertex, starting at "unreached"; the source starts at `0`.
2. Sweep every undirected edge `[u, v, w]` in both directions: if `distances[u] + w` beats `distances[v]`, lower it, and symmetrically for `v`.
3. Repeat the sweep until a full pass makes no change.
4. Translate the final table: an unreached vertex reports `-1`, everything else its distance.

This never orders the work: it just keeps relaxing, which makes it the independent oracle the heap version is checked against.

#### Walkthrough

Example 1 (`vertexCount = 5`, `source = 0`), the distance table pass by pass:

```text
            dist[0..4]
initial     [0, inf, inf, inf, inf]
pass 1      [0, 3, 1, 4, inf]   0-1 relaxed 4->3 through 2; 1-3 settles 4; 2-3 relaxes to 6, no change
pass 2      no change: done
answer      [0, 3, 1, 4, -1]
```

Matching the expected Output; vertex 4 was never touched, so it reports `-1`.

#### Solution

```python
from typing import List


class Solution:
    def shortestUndirectedDistances(self, vertexCount: int, edges: List[List[int]], source: int) -> List[int]:
        unreached = float("inf")
        distances = [unreached] * vertexCount
        distances[source] = 0
        changed = True
        while changed:
            changed = False
            for u, v, w in edges:
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    changed = True
                if distances[v] + w < distances[u]:
                    distances[u] = distances[v] + w
                    changed = True
        return [distance if distance != unreached else -1 for distance in distances]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V * E)`

Up to one sweep per vertex of the path's length in the worst case, each sweep touching both orientations of every edge; the early exit stops at the diameter.

##### Space Complexity: `O(V)`

The distance table; the edge list is the input.

#### Key Insights

- Repeating full sweeps needs no ordering argument at all: the loop condition itself certifies that every distance is final.
- Undirected edges relax twice per sweep; missing the reverse orientation silently computes a directed graph.
- The unreached sentinel exists only to be translated at the end; arithmetic never mixes it with real distances because a relaxation through `inf` can never win.

### Dijkstra with a Min-Heap

#### Derivation

The sweeps waste almost everything: between two improvements only a handful of vertices actually settle. Nonnegative weights let us settle vertices one at a time, cheapest first, and never revisit a settled vertex:

1. Build the undirected adjacency list, appending both orientations of every edge; parallel edges and self-loops just become extra list entries.
2. Seed a min-heap with `(0, source)`; keep `distances` initialized to unreached, with `distances[source] = 0`.
3. Pop the cheapest frontier entry; if it is a stale duplicate (its recorded distance beats the current best), discard it. Otherwise the vertex is settled: its distance can no longer improve, because any other route would have to leave the frontier through an entry that is already no cheaper.
4. Relax its edges: an improvement lowers the slot and pushes a new heap entry.
5. After the heap empties, translate unreached slots to `-1` and return the table.

#### Recurrence

Let `dist[v]` be the best known distance to `v` and `(u, v, w)` any edge:

$$ \text{dist}[v] = \min(\text{dist}[v],\ \text{dist}[u] + w) $$

applied in nondecreasing `\text{dist}[u]` order; slots never relaxed stay unreached and report `-1`.

#### Walkthrough

Example 1 (`vertexCount = 5`, `source = 0`), the heap's life:

```text
push (0,0)
pop 0  settle d=0    push (4,1) via 0-1, push (1,2) via 0-2
pop 2  settle d=1    push (3,1) via 2-1, push (6,3) via 2-3
pop 1  settle d=3    push (4,3) via 1-3
pop 4  stale: recorded d(1)=4 beats current 3, discard
pop 3  settle d=4    edges relax, no improvement
pop 6  stale: recorded d(3)=6 beats current 4, discard
heap empty: [0, 3, 1, 4, -1]
```

Matching the expected Output, with each vertex settled exactly once and
two stale pops discarded.

#### Solution

```python
import heapq
from typing import List


class Solution:
    def shortestUndirectedDistances(self, vertexCount: int, edges: List[List[int]], source: int) -> List[int]:
        adjacency = [[] for _ in range(vertexCount)]
        for u, v, w in edges:
            adjacency[u].append((v, w))
            adjacency[v].append((u, w))

        unreached = -1
        distances = [unreached] * vertexCount
        distances[source] = 0
        frontier = [(0, source)]
        while frontier:
            distance, vertex = heapq.heappop(frontier)
            if distance > distances[vertex]:
                continue
            for next_vertex, weight in adjacency[vertex]:
                arrival = distance + weight
                if distances[next_vertex] == unreached or arrival < distances[next_vertex]:
                    distances[next_vertex] = arrival
                    heapq.heappush(frontier, (arrival, next_vertex))
        return distances
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(E log V)`

Each edge pushes at most one entry and the heap holds `O(E)` of them; every pop costs `O(log E) = O(log V)`.

##### Space Complexity: `O(V + E)`

The adjacency list, the distance table, and the frontier.

#### Key Insights

- The stale-entry check is the whole implementation discipline: the heap is allowed to hold outdated records because re-pushing an improvement is cheaper than DecreaseKey.
- Settling in nondecreasing distance order is exactly what nonnegative weights buy; one negative edge would break the first-settlement-is-final argument and hand the problem back to Bellman-Ford.
- Distances reach `(V - 1) * max_weight ~ 10^14`, far past 32 bits, which is why the statement pins 64-bit arithmetic and Python's integers simply comply.
- `distances[source] = 0` before the loop both seeds the answer and, combined with the improvement test, ignores any cycle back into the source.

## Comparison of Solutions

### Time Complexity

- **Bellman-Ford Relaxation**: `O(V * E)` - full sweeps until nothing changes.
- **Dijkstra with a Min-Heap**: `O(E log V)` - each edge relaxes once from its settled endpoint.

### Space Complexity

- **Bellman-Ford Relaxation**: `O(V)` - the distance table.
- **Dijkstra with a Min-Heap**: `O(V + E)` - adjacency list, distance table, frontier.

### Trade-offs

- **Bellman-Ford Relaxation**: no data structure and no ordering invariant, so it is the independent checker; at `10^5` vertices and `2 * 10^5` edges it is two orders of magnitude too slow.
- **Dijkstra with a Min-Heap (Recommended)**: the standard shortest-path tool for nonnegative weights, and the only one of the two that meets the constraints' scale.

### When to Use Each

- **Bellman-Ford Relaxation**: small graphs, teaching the relaxation rule, and always as the oracle validating Dijkstra's answers in tests.
- **Dijkstra with a Min-Heap (Recommended)**: the interview answer: adjacency list, lazy-deletion heap, one settlement per vertex.

### Optimization Notes

- **Dijkstra with a Min-Heap** is the recommended choice: `O(E log V)` against the sweeps' `O(V * E)` is the difference between meeting and missing the constraints.
- Python lacks a DecreaseKey, so the lazy pattern (push, skip on pop) is the idiomatic form here; the heap grows to `O(E)` but every pop still pays only a logarithm.
- The unreached `-1` translation lives at the boundary: keeping `inf`-style sentinels inside the loop and converting once at return keeps every relaxation a plain integer comparison.
