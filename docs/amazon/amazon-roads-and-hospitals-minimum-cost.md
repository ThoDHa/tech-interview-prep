# [Minimum Cost for Roads and Hospitals](https://www.fastprep.io/problems/amazon-roads-and-hospitals-minimum-cost)

**Medium** | **NN minutes** | **Graph, Union Find, Greedy**

Cities are labeled from 0 to cityCount - 1. A hospital can be built in any city for hospitalCost, and any listed undirected road can be built for roadCost.

Choose hospitals and roads at minimum total cost so every city can reach a hospital.

## Examples

### Example 1

**Input:** `cityCount = 3`, `possibleRoads = [[0,1],[1,2]]`, `hospitalCost = 3`, `roadCost = 2`

**Output:** `7`

**Explanation:** Case 1 exercises the documented deterministic contract.

### Example 2

**Input:** `cityCount = 3`, `possibleRoads = [[0,1]]`, `hospitalCost = 2`, `roadCost = 5`

**Output:** `6`

**Explanation:** Case 2 exercises the documented deterministic contract.

### Example 3

**Input:** `cityCount = 5`, `possibleRoads = [[0,1],[2,3]]`, `hospitalCost = 6`, `roadCost = 1`

**Output:** `20`

**Explanation:** Case 3 exercises the documented deterministic contract.

## Constraints

- `1 <= cityCount <= 200000.`
- `0 <= possibleRoads.length <= 200000.`
- `Costs are positive and the answer fits a signed 32-bit integer.`

## Solutions

### Kruskal's Algorithm with a Virtual Hospital Node

#### Derivation

The goal "every city can reach a hospital" mixes two kinds of purchases, but both are just connections. Introduce a virtual hospital node `H` and re-express each purchase as an edge: building a hospital in city `c` is the edge `(c, H)` priced at `hospitalCost`, and building a listed road is its edge priced at `roadCost`. A choice of purchases lets every city reach a hospital exactly when the chosen edges connect all `cityCount + 1` nodes, and any connecting set contains a spanning tree costing no more (cycle edges are pure waste). So the answer is the minimum spanning tree of the augmented graph.

Kruskal's algorithm computes it by scanning all edges cheapest-first and taking any edge that joins two different components:

1. Build the edge list: `[hospitalCost, city, cityCount]` for every city, where the
   node `cityCount` plays `H`, plus `[roadCost, city_one, city_two]` for every listed road.
2. Sort the edges by weight ascending.
3. Sweep the sorted edges with a union-find over `cityCount + 1` nodes, taking an
   edge exactly when `union` reports that it merged two different components.
4. Stop after `cityCount` edges are taken (a spanning tree of `cityCount + 1` nodes
   has exactly that many edges) and return the accumulated weight.

#### Walkthrough

Example 1 (`cityCount = 3`, `possibleRoads = [[0,1],[1,2]]`, `hospitalCost = 3`, `roadCost = 2`) augments to three hospital edges of weight `3` and two road edges of weight `2`. Sorted, the roads come first:

```text
edge 0-1 (2)   components {0,1} {2} {H}    total_cost = 2
edge 1-2 (2)   components {0,1,2} {H}      total_cost = 4
edge 0-H (3)   components {0,1,2,H}        total_cost = 7
               3 edges taken = cityCount -> stop
```

The two remaining hospital edges would each form a cycle with `H` and are skipped. Every city reaches a hospital: cities `0` and `2` over roads, city `1` through its own hospital. The total `7` matches the expected Output.

#### Solution

The code is the sorted sweep from the walkthrough, with a union-find carrying path compression and union by rank.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node_one: int, node_two: int) -> bool:
        root_one, root_two = self.find(node_one), self.find(node_two)
        if root_one == root_two:
            return False
        if self.rank[root_one] < self.rank[root_two]:
            root_one, root_two = root_two, root_one
        self.parent[root_two] = root_one
        if self.rank[root_one] == self.rank[root_two]:
            self.rank[root_one] += 1
        return True


class Solution:
    def minimumInfrastructureCost(self, cityCount: int, possibleRoads: List[List[int]], hospitalCost: int, roadCost: int) -> int:
        hospital_node = cityCount
        edges: List[List[int]] = []
        for city in range(cityCount):
            edges.append([hospitalCost, city, hospital_node])
        for city_one, city_two in possibleRoads:
            edges.append([roadCost, city_one, city_two])
        edges.sort()

        total_cost = 0
        edges_taken = 0
        components = UnionFind(cityCount + 1)
        for weight, city_one, city_two in edges:
            if components.union(city_one, city_two):
                total_cost += weight
                edges_taken += 1
                if edges_taken == cityCount:
                    break
        return total_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(E log E)`

The `E = cityCount + len(possibleRoads)` edges are sorted; the union-find sweep costs near-constant amortized time per edge with path compression and union by rank.

##### Space Complexity: `O(E)`

The edge list plus the parent and rank arrays for `cityCount + 1` nodes.

#### Key Insights

- The virtual hospital node converts a two-currency design problem into plain MST; no special casing of "which city gets the hospital" survives into the code.
- Hospital edges guarantee the augmented graph is connected even with zero roads, so a spanning tree always exists.
- Exactly `cityCount` edges are needed, so the sweep can stop early instead of scanning the rest of the sorted list.
- Redundant listed roads (duplicates, or edges inside an already-joined component) are rejected by the `union` check without any preprocessing.

### Prim's Algorithm with a Min-Heap

#### Derivation

Kruskal sorts every edge up front, including all `cityCount` hospital edges, even though a hospital edge is never interesting once a city has a cheaper road. Prim's algorithm grows one tree, always committing to the cheapest connection into it next, and here the virtual node dissolves into the initialization: because a hospital can be built in every city, each city's connection cost starts at `hospitalCost`, and listed roads can only try to lower it:

1. Initialize `connect_cost[city] = hospitalCost` for every city and seed a
   min-heap with `(hospitalCost, city)` for all cities.
2. Repeatedly pop the cheapest entry; skip it when its city already joined the
   tree (a stale entry). Otherwise add its cost to `total_cost` and mark the city.
3. For each listed road out of the newly added city, when the road is cheaper
   than the neighbor's current `connect_cost`, update the key and push the neighbor.
4. When every city has joined the tree, return `total_cost`.

#### Walkthrough

Example 3 (`cityCount = 5`, `possibleRoads = [[0,1],[2,3]]`, `hospitalCost = 6`, `roadCost = 1`): all five cities start with key `6`, and each listed road offers a connection at `1`. The heap pops cities in this order:

```text
pop (6, 0)   total_cost = 6;   road 0-1 offers 1 < 6 -> key[1] = 1, push (1, 1)
pop (1, 1)   total_cost = 7
pop (6, 2)   total_cost = 13;  road 2-3 offers 1 < 6 -> key[3] = 1, push (1, 3)
pop (1, 3)   total_cost = 14
pop (6, 4)   total_cost = 20   heap empty, all cities in the tree
```

Cities `1` and `3` piggyback on cheap roads; cities `0`, `2`, and `4` each pay for their own hospital. The total `20` matches the expected Output.

#### Solution

The code is the pop, mark, relax loop from the walkthrough; the hospital option lives in the initialization of `connect_cost` and the heap seed.

```python
import heapq
from typing import List, Tuple


class Solution:
    def minimumInfrastructureCost(self, cityCount: int, possibleRoads: List[List[int]], hospitalCost: int, roadCost: int) -> int:
        adjacency: List[List[Tuple[int, int]]] = [[] for _ in range(cityCount)]
        for city_one, city_two in possibleRoads:
            adjacency[city_one].append((city_two, roadCost))
            adjacency[city_two].append((city_one, roadCost))

        connect_cost = [hospitalCost] * cityCount
        in_tree = [False] * cityCount
        heap: List[Tuple[int, int]] = [(hospitalCost, city) for city in range(cityCount)]
        heapq.heapify(heap)

        total_cost = 0
        while heap:
            cost, city = heapq.heappop(heap)
            if in_tree[city]:
                continue
            in_tree[city] = True
            total_cost += cost
            for neighbor_city, neighbor_cost in adjacency[city]:
                if (not in_tree[neighbor_city]
                        and neighbor_cost < connect_cost[neighbor_city]):
                    connect_cost[neighbor_city] = neighbor_cost
                    heapq.heappush(heap, (neighbor_cost, neighbor_city))
        return total_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(E log E)`

Each road relaxation pushes at most one heap entry, so heap operations are bounded by `E` at `O(log E)` each; no global sort is needed.

##### Space Complexity: `O(E)`

The adjacency lists plus the heap of pending connection offers.

#### Key Insights

- Starting every key at `hospitalCost` is the whole trick: Prim never materializes the virtual node, yet the hospital option stays on the table for every city.
- Stale entries are inevitable (a city can be pushed by several roads over time); the `in_tree` check on pop makes them harmless.
- With zero roads the loop degenerates into buying `cityCount` hospitals, which is exactly the right fallback.

## Comparison of Solutions

### Time Complexity

- **Kruskal's Algorithm with a Virtual Hospital Node**: `O(E log E)` - sorting the edge list dominates the union-find sweep.
- **Prim's Algorithm with a Min-Heap**: `O(E log E)` - heap operations replace the sort at the same asymptotic bound.

### Space Complexity

- **Kruskal's Algorithm with a Virtual Hospital Node**: `O(E)` - the explicit edge list plus union-find arrays.
- **Prim's Algorithm with a Min-Heap**: `O(E)` - adjacency lists plus the heap of pending offers.

### Trade-offs

- **Kruskal's Algorithm with a Virtual Hospital Node**: a flat sorted edge list and a small disjoint-set helper; easy to interrupt early once `cityCount` edges are taken, and it never builds adjacency structure.
- **Prim's Algorithm with a Min-Heap**: no sort and no materialized virtual node, at the price of adjacency lists and stale-entry management on pop.

### When to Use Each

- **Kruskal's Algorithm with a Virtual Hospital Node (Recommended)**: the default interview answer: the virtual-node reduction plus Kruskal is the shortest path from statement to correct code.
- **Prim's Algorithm with a Min-Heap**: when the graph already lives in adjacency lists, or when edges stream in and a global sort is awkward.

### Optimization Notes

- The two approaches tie at `O(E log E)`; the practical difference is constants and which input representation is at hand.
- Kruskal's early stop after `cityCount` accepted edges skips the tail of the sorted scan when the road list is long.
- Prim's `connect_cost` array doubles as the "already offered cheaper" guard, keeping the heap from bloating with duplicate offers.
