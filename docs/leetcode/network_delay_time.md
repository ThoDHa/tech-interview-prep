# [Network Delay Time](https://leetcode.com/problems/network-delay-time/)

**Medium** | **25 minutes** | **Depth-First Search, Breadth-First Search, Graph, Heap (Priority Queue), Shortest Path**

**Pattern:** [Shortest Path](../patterns/shortest_path/intuition.md)

**Algorithm:** [Bellman-Ford algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm) · [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/network_delay_time/solution.py`](../../practice/network_delay_time/solution.py)

You are given a network of `n` directed nodes, labeled from `1` to `n`. You are also given `times`, a list of directed edges where `times[i] = (ui, vi, ti)`. 

* `ui` is the source node (an integer from `1` to `n`)
* `vi` is the target node (an integer from `1` to `n`)
* `ti` is the time it takes for a signal to travel from the source to the target node (an integer greater than or equal to `0`).

You are also given an integer `k`, representing the node that we will send a signal from.

Return the **minimum** time it takes for all of the `n` nodes to receive the signal. If it is impossible for all the nodes to receive the signal, return `-1` instead.

## Examples

### Example 1

**Input:** `times = [[1,2,1],[2,3,1],[1,4,4],[3,4,1]], n = 4, k = 1`

**Output:** `3`

### Example 2

**Input:** `times = [[1,2,1],[2,3,1]], n = 3, k = 2`

**Output:** `-1`

## Constraints

- `1 <= k <= n <= 100`
- `1 <= times.length <= 1000`

## Deriving the Solution

The signal's arrival time at a node is the total weight of the cheapest path from the source to it, so the problem is single-source shortest paths on a weighted directed graph, finished by taking the maximum over all nodes. Every solution below computes those shortest distances; they differ in how the "not yet final" distances are corrected as better paths are discovered.

1. **Start literal.** Relax edges repeatedly: keep a `distances` array seeded
   with `0` at the source and infinity elsewhere, and sweep every edge, shortening any distance a cheaper path reaches. After enough sweeps the array is exact, and the answer is its maximum, or `-1` where infinity survives: see [Bellman-Ford Relaxation Sweeps](#bellman-ford-relaxation-sweeps).
2. **Spot the waste.** Each sweep rescans all `e` edges even though only the
   nodes whose distance just improved can shorten anything new. Growing the frontier outward from the closest settled node, the way BFS grows by layers, visits an edge only from its most promising endpoint: see [Recursive Relaxation DFS](#recursive-relaxation-dfs).
3. **Order the frontier by distance.** A min-heap holding the candidate
   `(distance, node)` pairs makes "closest unsettled node" a pop instead of a scan. Dijkstra's Algorithm settles each node once with its final distance and relaxes only its outgoing edges, `O(e log e)`: see [Dijkstra's Algorithm](#dijkstras-algorithm).

## Solutions

### Bellman-Ford Relaxation Sweeps

#### Derivation

The most direct implementation of "shortest paths" is corrective: write down the distance estimate every node currently believes in, then sweep the edges, correcting any estimate a cheaper route disproves. A shortest path visits at most `n - 1` edges, so `n - 1` full sweeps suffice for the estimates to stop moving; one sweep per round of improvement is the cost of simplicity:

1. Seed `distances` with `0` at the source `k` and infinity elsewhere, using
   a value larger than any reachable total for infinity.
2. Repeat up to `n - 1` times: sweep every directed edge `(u, v, t)` and, when
   `distances[u] + t` beats `distances[v]`, adopt it.
3. Stop early when a whole sweep corrects nothing.
4. Return the maximum of the `n` distances, or `-1` if any is still infinity.

#### Walkthrough

Let us sweep by hand on Example 1: `times = [[1,2,1],[2,3,1],[1,4,4],[3,4,1]]`, `n = 4`, `k = 1`. The table shows every correction of each sweep; untouched distances are omitted:

```text
seed        distances = [0, inf, inf, inf]
sweep 1     1->2: 0+1=1 < inf   distances = [0, 1, inf, inf]
            2->3: 1+1=2 < inf   distances = [0, 1, 2, inf]
            1->4: 0+4=4 < inf   distances = [0, 1, 2, 4]
            3->4: 2+1=3 < 4     distances = [0, 1, 2, 3]
sweep 2     no corrections -> stop
```

The sweep order matters to the trace but not the result: edge `[3,4,1]` corrects node `4` only because `[2,3,1]` already improved node `3` earlier in the same sweep. A second sweep confirms stability. The maximum distance is `3`, matching the expected Output for Example 1. On Example 2 node `3` is never touched, its distance stays infinite, and the function returns `-1`.

#### Solution

The code is the seeded array and the improvement-guarded sweeps.

```python
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        distances = [None] * (n + 1)
        distances[k] = 0
        for _ in range(n - 1):
            changed = False
            for u, v, t in times:
                if distances[u] is not None and (
                    distances[v] is None or distances[u] + t < distances[v]
                ):
                    distances[v] = distances[u] + t
                    changed = True
            if not changed:
                break
        if any(distances[node] is None for node in range(1, n + 1)):
            return -1
        return max(distances[1:])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * e)`

Up to `n - 1` sweeps over all `e` edges; the early stop bounds the sweeps by the longest improvement chain, but the worst case stands.

##### Space Complexity: `O(n)`

The `distances` array is the only state; no adjacency structure is built, so the input list is scanned directly.

#### Key Insights

- `None` plays infinity: a node with no known path is distinguishable from a node with a `0`-cost path, which matters because `ti` may be `0`.
- The early stop is what saves practical runs: on a graph whose shortest paths are short chains of edges, sweeps halt after a handful of rounds.
- No adjacency list is ever built, which makes this the shortest-path method of choice when the edge list is small or streamed.

### Recursive Relaxation DFS

#### Derivation

The Bellman-Ford sweeps re-relax every edge every round, but an edge can only produce an improvement when its source's distance just changed. Ordering the work by the graph's own structure removes the sweeps: from each node, relax its outgoing edges, and recurse immediately from every neighbor whose distance improved. The recursion spreads improvements outward as they happen, and each node's relaxation re-runs only when a cheaper way to reach it is found later:

1. Build `adjacency`, sorted by neighbor so the traversal order is
   deterministic.
2. Seed `distances` with the source at `0`.
3. `dfs(node)` reads `distances[node]` and, for each neighbor `(v, t)`, adopts
   `distances[node] + t` when it beats `distances[v]`, recursing on `v` after each adoption.
4. After the initial `dfs(k)`, return the maximum distance or `-1` for any
   node left unvisited.

#### Walkthrough

Let us trace the recursion on Example 1: `times = [[1,2,1],[2,3,1],[1,4,4],[3,4,1]]`, `n = 4`, `k = 1`, with adjacency `1: [(2,1), (4,4)]`, `2: [(3,1)]`, `3: [(4,1)]`:

```text
dfs(1): distances = {1: 0}
  1->2: 0+1=1 adopt {1:0, 2:1}    dfs(2)
    2->3: 1+1=2 adopt {1:0, 2:1, 3:2}    dfs(3)
      3->4: 2+1=3 adopt {1:0, 2:1, 3:2, 4:3}    dfs(4) has no edges
  1->4: 0+4=4 not better than 3   no recursion
```

The depth-first path `1 -> 2 -> 3 -> 4` happens to carry improvements the whole way, so the direct edge `1 -> 4` with weight `4` arrives late and loses to the `3` already recorded; the recursion it would have triggered is skipped. The final distances are `{1: 0, 2: 1, 3: 2, 4: 3}` and the maximum is `3`, matching the expected Output for Example 1.

#### Solution

The code is the recursion above with a guard against re-entry on the stack.

```python
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adjacency = {}
        for u, v, t in times:
            adjacency.setdefault(u, []).append((v, t))
        for node in adjacency:
            adjacency[node].sort()

        distances = {k: 0}
        on_stack = {k}

        def dfs(node: int) -> None:
            for neighbor, weight in adjacency.get(node, []):
                candidate = distances[node] + weight
                if neighbor not in distances or candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    if neighbor in on_stack:
                        continue
                    on_stack.add(neighbor)
                    dfs(neighbor)
                    on_stack.discard(neighbor)

        dfs(k)
        if len(distances) < n:
            return -1
        return max(distances.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(e log e + n * e)`

Sorting the adjacency lists costs `O(e log e)`. Each node's `dfs` re-runs once per later improvement to its distance, which is bounded by its in-degree in the worst case, giving the quadratic-flavored `n * e` bound; graphs with few alternative paths finish in near-linear time.

##### Space Complexity: `O(n + e)`

The adjacency lists, distance map, and recursion stack, which reaches depth `n` on a path-shaped graph.

#### Key Insights

- The recursion propagates an improvement the moment it happens instead of waiting for the next sweep, which is why few-sweep graphs finish fast.
- The `on_stack` guard keeps a zero-weight cycle from recursing forever: when an edge improves a node already on the current path, the code adopts the distance and `continue`s without scheduling a re-run; the improvement re-propagates later through the still-active frames' relaxations, which re-read the updated distance as each frame resumes its edge loop.
- Correctness does not come free: unlike the two ordered frontier methods, this variant's termination argument rests on distances strictly decreasing at every adoption, which bounds how often any node's outgoing edges can be re-relaxed.

### Dijkstra's Algorithm

#### Derivation

Both variants pay for correcting mistakes: the sweeps globally, the recursion per node. [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) eliminates corrections by settling nodes in a careful order. All edge weights are non-negative, so the closest unsettled node's tentative distance can never be improved by a detour through any other unsettled node: settling it first is always safe. A min-heap of `(distance, node)` pairs serves the closest candidate in `O(log e)`:

1. Build the adjacency lists.
2. Seed `distances` with `0` at the source and `-1` (unknown) elsewhere, and
   push `(0, k)` into the heap.
3. Pop the smallest `(distance, node)`; skip the entry if it is stale, that is,
   `distance > distances[node]`.
4. Otherwise settle `node` and relax each outgoing edge `(v, t)`: when
   `distance + t` beats `distances[v]`, adopt it and push `(distance + t, v)`.
5. When the heap empties, return `-1` if any node never settled, otherwise the
   maximum over all settled distances.

The stale-entry skip is what keeps the heap linear-sized in spirit: a node may be pushed once per improving relaxation, but only its best entry is ever settled.

#### Walkthrough

Let us run the heap on Example 1: `times = [[1,2,1],[2,3,1],[1,4,4],[3,4,1]]`, `n = 4`, `k = 1`, adjacency `1: [(2,1), (4,4)]`, `2: [(3,1)]`, `3: [(4,1)]`:

```text
pop (0, 1)  settle; relax 1->2: 1, 1->4: 4   heap = [(1,2), (4,4)]   distances = [0, 1, -1, 4]
pop (1, 2)  settle; relax 2->3: 2            heap = [(2,3), (4,4)]   distances = [0, 1, 2, 4]
pop (2, 3)  settle; relax 3->4: 3 < 4        heap = [(3,4), (4,4)]   distances = [0, 1, 2, 3]
pop (3, 4)  settle; no edges                 heap = [(4,4)]
pop (4, 4)  stale: 4 > 3, skip               heap = []
```

Node `4` is pushed twice: the direct edge offers `4` before the cheaper route through nodes `2` and `3` offers `3`. The smaller entry pops first and settles the node; the `4` survives in the heap only to be recognized as stale and skipped. All `4` nodes settled, so the answer is the maximum distance `3`, matching the expected Output for Example 1. On Example 2 node `3` never enters the settled set and the function returns `-1`.

#### Solution

The code is the ordered frontier: seed, pop, stale-skip, settle, relax.

```python
import heapq
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adjacency = [[] for _ in range(n + 1)]
        for u, v, t in times:
            adjacency[u].append((v, t))

        distances = [-1] * (n + 1)
        distances[k] = 0
        heap = [(0, k)]
        settled = 0

        while heap:
            distance, node = heapq.heappop(heap)
            if distance > distances[node]:
                continue
            settled += 1
            for neighbor, weight in adjacency[node]:
                candidate = distance + weight
                if distances[neighbor] == -1 or candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))

        if settled < n:
            return -1
        return max(distances[1:])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + e * log e)`

Each relaxation pushes one heap entry, so the heap holds at most `e` entries and costs `O(log e)` per push or pop; each edge is relaxed from its settled endpoint exactly once.

##### Space Complexity: `O(n + e)`

The adjacency lists and `distances` array are `O(n + e)`, and the heap holds at most one entry per relaxation.

#### Key Insights

- Non-negative weights are the license for the greedy order: a heavier detour can never shorten a closer node's path, so the first pop is final.
- The stale-entry skip keeps a node's outdated heap entries harmless; settling is counted once per node, which is also how reachability is decided (`settled < n` means unreachable).
- `-1` as the unknown marker doubles as the unreachable marker, and the final `max` never sees it because every settled distance is real.

## Comparison of Solutions

### Time Complexity

- **Bellman-Ford Relaxation Sweeps**: `O(n * e)` - up to `n - 1` full sweeps over every edge.
- **Recursive Relaxation DFS**: `O(e log e + n * e)` - improvement-triggered re-relaxations bounded by in-degrees, plus an adjacency sort.
- **Dijkstra's Algorithm**: `O(n + e * log e)` - each edge relaxed once from a settled node, with logarithmic heap costs.

### Space Complexity

- **Bellman-Ford Relaxation Sweeps**: `O(n)` - the distance array, scanned against the raw edge list.
- **Recursive Relaxation DFS**: `O(n + e)` - adjacency lists, distance map, and a recursion stack.
- **Dijkstra's Algorithm**: `O(n + e)` - adjacency lists, distance array, and a heap of at most one entry per relaxation.

### Trade-offs

- Bellman-Ford needs no adjacency structure and no ordering discipline, the shortest correct code, at the price of the quadratic sweep product.
- The recursive DFS trades worst-case predictability for immediate propagation; it shines when few alternative paths exist and pays when the graph offers many.
- Dijkstra pays a logarithmic factor for its heap but settles every node exactly once, making it the only one of the three with a worst-case near-linear bound in `e`.

### When to Use Each

- **Bellman-Ford Relaxation Sweeps**: tiny graphs, a streamed (unsorted, unbuilt) edge list, or as the correctness reference when testing faster methods.
- **Recursive Relaxation DFS**: never the default for weighted shortest paths; it appears here to show what ordering the frontier buys, and its shape is worth knowing because it becomes correct and optimal for DAGs processed in topological order.
- **Dijkstra's Algorithm**: the default for non-negative weighted shortest paths, this problem included (recommended here).

### Optimization Notes

- With `ti >= 0` guaranteed, Dijkstra is safe; the moment negative weights appear, its settle-once guarantee collapses and Bellman-Ford's sweeps are the honest choice.
- Using a `deque` (BFS) instead of the heap would be wrong here: arrival order in an unweighted frontier is not distance order, and node `4` in Example 1 would settle at `4` instead of `3`.
- The settled counter and the `-1` marker overlap in duty; either alone answers reachability, and carrying both keeps the final max free of sentinels.

