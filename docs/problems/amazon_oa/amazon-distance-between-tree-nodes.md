# [Distance Between Two Tree Nodes](https://www.fastprep.io/problems/amazon-distance-between-tree-nodes)

**Medium** | **NN minutes** | **Tree, Breadth First Search, Graph**

You are given a rooted tree whose nodes are numbered from 1 through treeNodes. The arrays treeFrom and treeTo describe the undirected edges of the tree, and root identifies its root.

Given two node IDs source and target, return the number of edges on the unique path between them.

The serialized edge list supplies the tree structure without parent pointers.

## Examples

### Example 1

**Input:** `treeNodes = 7`, `treeFrom = [1,1,2,2,3,3]`, `treeTo = [2,3,4,5,6,7]`, `root = 1`, `source = 4`, `target = 7`

**Output:** `4`

**Explanation:** The unique path is 4 -> 2 -> 1 -> 3 -> 7, which contains 4 edges.

### Example 2

**Input:** `treeNodes = 5`, `treeFrom = [1,1,3,3]`, `treeTo = [2,3,4,5]`, `root = 1`, `source = 3`, `target = 5`

**Output:** `1`

**Explanation:** Node 5 is adjacent to node 3, so their distance is 1.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-distance-between-tree-nodes; fill them in. -->

## Solutions

### BFS from Source Until Target

#### Derivation

The most literal reading of "the number of edges on the unique path" is to walk the path. The tree arrives as a flat edge list with no parent pointers, though, so the first duty is to turn `treeFrom`/`treeTo` into an adjacency structure. With that in hand the path can be found by any graph search, and [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) is the natural pick because its queue processes nodes in nondecreasing distance from `source`, so the first time the search touches `target`, its recorded distance is already the answer. A general graph would also need a visited set to survive cycles, and even though a tree has none, the search still needs one to keep from bouncing back to the parent forever:

1. Build `adjacency`: for each edge `(treeFrom[edge_idx], treeTo[edge_idx])`, add
   each endpoint to the other's neighbor list.
2. Seed a `queue` with `(source, 0)` (node, distance) and a `visited` set holding
   `source`.
3. While the queue is non-empty, pop `(node, distance)`. Return `distance`
   immediately when `node == target`.
4. Otherwise push every `neighbor` in `adjacency[node]` that is not in `visited`,
   each at `distance + 1`.
5. A tree always connects `source` to `target`, so the loop always returns.

#### Walkthrough

Example 1, `treeNodes = 7`, `treeFrom = [1,1,2,2,3,3]`, `treeTo = [2,3,4,5,6,7]`, `root = 1`, `source = 4`, `target = 7`. The tree hangs node 1 over two subtrees, `1-2-{4,5}` and `1-3-{6,7}`. Each line is one queue event; neighbors are visited in edge order:

```text
seed          queue = [(4, 0)]            visited = {4}
pop (4, 0)    not target; neighbor 2      queue = [(2, 1)]   visited = {4, 2}
pop (2, 1)    not target; neighbors 1, 4  queue = [(1, 2)]   visited = {4, 2, 1}
pop (1, 2)    not target; neighbors 2, 3  queue = [(3, 3)]   visited = {4, 2, 1, 3}
pop (3, 3)    not target; neighbors 1, 6, 7                 visited = {4, 2, 1, 3, 6, 7}
              queue = [(6, 4), (7, 4)]
pop (6, 4)    not target; neighbor 3 already visited
pop (7, 4)    node == target -> return 4
```

The returned `4` counts the edges of the path `4 -> 2 -> 1 -> 3 -> 7`, matching the expected Output. The visited checks are visible in the trace: when `(2, 1)` expands, its neighbor `4` is already visited, so the search never walks the path backward. Example 2 follows the same pattern in one hop: `source = 3` expands `target = 5` at distance `1`, and the second pop returns `1`.

#### Solution

The code is the walkthrough's build-then-search shape: adjacency first, then the seeded queue:

```python
from collections import deque
from typing import Dict, List, Set


class Solution:
    def solve(self, treeNodes: int, treeFrom: List[int], treeTo: List[int],
              root: int, source: int, target: int) -> int:
        """Return the number of edges on the unique path from source to target.

        Time:  O(treeNodes + len(treeFrom)): building adjacency touches every
            edge once, and BFS visits every node at most once.
        Space: O(treeNodes) for the adjacency lists, the visited set, and the
            queue (the tree has treeNodes - 1 edges).
        """
        adjacency: Dict[int, List[int]] = {node: [] for node in range(1, treeNodes + 1)}
        for edge_idx in range(len(treeFrom)):
            adjacency[treeFrom[edge_idx]].append(treeTo[edge_idx])
            adjacency[treeTo[edge_idx]].append(treeFrom[edge_idx])

        queue = deque([(source, 0)])
        visited: Set[int] = {source}
        while queue:
            node, distance = queue.popleft()
            if node == target:
                return distance
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        raise ValueError(f"{target} is unreachable from {source} in the given tree")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(treeNodes + edges)`

Building the adjacency lists reads every edge once; the BFS then visits every node at most once and scans each adjacency list once.

##### Space Complexity: `O(treeNodes)`

The adjacency structure holds `2 × (treeNodes - 1)` directed entries, and the visited set and queue hold at most one entry per node.

#### Key Insights

- A serialized edge list carries no orientation: every edge must be added in both directions, or the search stalls at the first node whose parent link is missing.
- BFS's distance-first order makes the first arrival at `target` optimal by construction, so no relaxation or path storage is needed.
- The visited set does double duty: it would block cycles in a general graph, and here it simply stops the search from revisiting the parent it just came from.
- `root` plays no role in the search; the undirected path between two nodes is the same no matter which node anchors the tree. It matters only for the parent-based approach below.

### Two-Phase Depth Search

#### Derivation

BFS searches outward in all directions, but a tree offers a shortcut no general graph has: every node has exactly one parent, so a node's ancestry is a single chain. Computing each node's parent and depth in one pass over the tree turns the query into an ancestry problem: walk the deeper node up until both nodes sit at the same depth, then walk both up in lockstep until they meet. The number of steps taken across both walks is exactly the path length:

1. Build `adjacency` as before.
2. Compute `parent` and `depth` arrays for all nodes with an iterative DFS or BFS
   from `root`, setting each visited neighbor's parent and depth from its
   discoverer. (The iterative form avoids the recursion limit on chain-shaped
   trees.)
3. To answer `(source, target)`: raise the deeper of the two nodes until
   `depth[source] == depth[target]`, counting the climb steps.
4. Then climb both nodes together until they meet, counting those steps too.
5. Return the total count.

#### Walkthrough

Example 1 again: `root = 1` fixes parent and depth for every node:

```text
node:     1    2    3    4    5    6    7
parent:   -    1    1    2    2    3    3
depth:    0    1    1    2    2    2    2
```

Query `(source = 4, target = 7)`: both sit at depth `2`, so no equalizing climb is needed. The lockstep climb takes over:

```text
step 1   4 -> parent 2,   7 -> parent 3   (no meeting: 2 != 3), count = 2
step 2   2 -> parent 1,   3 -> parent 1   (1 == 1: meet),       count = 4
```

The nodes meet at their lowest common ancestor `1` after `4` climb steps, matching the expected Output. For Example 2, `(source = 3, target = 5)`: `3` sits at depth `1` and `5` at depth `2`, so the equalizing climb raises `5` to `3` (one step) and the nodes meet immediately, for a count of `1`.

#### Solution

The code is the walkthrough's two tables and two climbs:

```python
from collections import deque
from typing import Dict, List


class Solution:
    def solve(self, treeNodes: int, treeFrom: List[int], treeTo: List[int],
              root: int, source: int, target: int) -> int:
        """Return the number of edges on the unique path from source to target.

        Time:  O(treeNodes + edges) to build and root the tree, then O(depth)
            for the two climbs of one query.
        Space: O(treeNodes) for the adjacency lists, parent array, and depth
            array.
        """
        adjacency: Dict[int, List[int]] = {node: [] for node in range(1, treeNodes + 1)}
        for edge_idx in range(len(treeFrom)):
            adjacency[treeFrom[edge_idx]].append(treeTo[edge_idx])
            adjacency[treeTo[edge_idx]].append(treeFrom[edge_idx])

        parent = [0] * (treeNodes + 1)
        depth = [0] * (treeNodes + 1)
        parent[root] = root
        queue = deque([root])
        visited = {root}
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    depth[neighbor] = depth[node] + 1
                    queue.append(neighbor)

        distance = 0
        walk_source, walk_target = source, target
        while depth[walk_source] > depth[walk_target]:
            walk_source = parent[walk_source]
            distance += 1
        while depth[walk_target] > depth[walk_source]:
            walk_target = parent[walk_target]
            distance += 1
        while walk_source != walk_target:
            walk_source = parent[walk_source]
            walk_target = parent[walk_target]
            distance += 2
        return distance
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(treeNodes + edges)`

Rooting the tree reads every edge once. Each climb step is `O(1)`, and both climbs together ascend at most `2 × depth` levels, bounded by the tree height.

##### Space Complexity: `O(treeNodes)`

The adjacency lists plus the `parent` and `depth` arrays; the queue holds at most one level of the tree during rooting.

#### Key Insights

- Rooting the tree once converts every future query into two pointer walks: the parent chain replaces pathfinding.
- The meet point of the lockstep climb is the [lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor), and `depth[source] + depth[target] - 2 × depth[lca]` is exactly the path length, which is why counting climb steps gives the right answer.
- This shape pays off when one rooting serves many queries (the usual Amazon follow-up): the `O(treeNodes + edges)` build amortizes over queries that each cost only the tree height.
- The iterative rooting loop is deliberate: a recursive depth-first pass hits Python's recursion limit on a degenerate chain of `10^5` nodes.

## Comparison of Solutions

### Time Complexity

- **BFS from Source Until Target**: `O(treeNodes + edges)` - one full search from `source`, stopping at the first arrival at `target`.
- **Two-Phase Depth Search**: `O(treeNodes + edges)` to root plus `O(height)` per query - the build dominates for a single query; repeated queries amortize it.

### Space Complexity

- **BFS from Source Until Target**: `O(treeNodes)` - adjacency lists, visited set, and queue.
- **Two-Phase Depth Search**: `O(treeNodes)` - adjacency lists plus `parent` and `depth` arrays.

### Trade-offs

- **BFS from Source Until Target**: no rooting pass and the shortest correct program, but every query pays a fresh full search from `source`.
- **Two-Phase Depth Search**: a one-time rooting pass buys per-query climbs of at most the tree height, and the `parent`/`depth` tables support the natural follow-ups (lowest common ancestor, subtree sizes); it costs two extra arrays and a two-climb loop to write.

### When to Use Each

- **BFS from Source Until Target (Recommended)**: the interview default for a single query: derive it, code it, and state its complexity in under five minutes.
- **Two-Phase Depth Search**: when the interviewer asks for many distance queries on the same tree, or steers the discussion toward lowest common ancestor techniques.

### Optimization Notes

- Both approaches are asymptotically optimal for one query (any method must read the `O(treeNodes)` input), so the comparison is about query amortization, not speed.
- For many queries, the depth-search shape extends further: binary lifting stores `2^j`-level ancestors and answers each lowest-common-ancestor step in `O(log treeNodes)`, and a Euler tour plus a sparse table answers it in `O(1)` after `O(treeNodes log treeNodes)` preprocessing.
- A common pitfall is allocating the `parent`/`depth` arrays as `[0] * treeNodes` instead of `[0] * (treeNodes + 1)`: node IDs run from `1` through `treeNodes`, so index `treeNodes` must exist.
