# [Swim In Rising Water](https://leetcode.com/problems/swim-in-rising-water/)

**Hard** | **40 minutes** | **Array, Binary Search, Depth-First Search, Breadth-First Search, Union Find, Heap (Priority Queue), Matrix**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md), [Shortest Path](../patterns/shortest_path/intuition.md), [Union-Find](../patterns/union_find/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) · [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) · [Disjoint-set (Union-Find)](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)

**Practice:** [`practice/swim_in_rising_water/solution.py`](../../practice/swim_in_rising_water/solution.py)

You are given a square 2-D matrix of distinct integers `grid` where each integer `grid[i][j]` represents the elevation at position `(i, j)`.

Rain starts to fall at time = `0`, which causes the water level to rise. At time `t`, the water level across the entire grid is `t`.

You may swim either horizontally or vertically in the grid between two adjacent squares if the original elevation of both squares is less than or equal to the water level at time `t`.

Starting from the top left square `(0, 0)`, return the minimum amount of time it will take until it is possible to reach the bottom right square `(n - 1, n - 1)`.

## Examples

### Example 1

**Input:** `grid = [[0,1],[2,3]]`

**Output:** `3`

**Explanation:** For a path to exist to the bottom right square `grid[1][1]` the water elevation must be at least `3`. At time `t = 3`, the water level is `3`.

### Example 2

**Input:**

```text
grid = [
  [0,1,2,10],
  [9,14,4,13],
  [12,3,8,15],
  [11,5,7,6]
]
```

**Output:**

```text
8
```

**Explanation:** The water level must be at least `8` to reach the bottom right square. The path is `[0, 1, 2, 4, 8, 7, 6]`.

## Constraints

- `grid.length == grid[i].length`
- `1 <= grid.length <= 50`
- `0 <= grid[i][j] < n^2`

## Deriving the Solution

A swim is possible at level `t` exactly when a path from corner to corner exists whose every cell elevation is `<= t`, so the answer is the path minimizing its own maximum elevation. Every solution below searches for that min-max path; they differ in whether they search one level at a time or one cell at a time.

1. **Start literal.** Simulate the rain: for each candidate level `t` in
   increasing order, flood fill from the top-left through cells with elevation `<= t` and stop at the first level that reaches the bottom-right. Correct, `O(n^3)` on a grid of `n^2` cells when each restart rescans the grid: see [Level-by-Level Flood Fill](#level-by-level-flood-fill).
2. **Search the level, not the rain.** The feasibility predicate is monotone: if level `t` connects the corners, so does `t + 1`. Binary search on the level collapses the simulation loop to `O(log m)` fills, each `O(n^2)`: see [Binary Search on the Answer](#binary-search-on-the-answer).
3. **Search the cells instead.** Modified Dijkstra flips the search inside out: grow the reachable region from the start, always extending through the cell whose required level is smallest, carrying path cost `max(level so far, cell elevation)` instead of a sum. The first arrival at the far corner is optimal: see [Modified Dijkstra's Algorithm](#modified-dijkstras-algorithm).
4. **Merge cells directly.** Union-Find sees the same process as edge insertion: sort cells by elevation, add them one by one, and stop at the elevation that first connects both corners. The answer is simply that cell's elevation: see [Union-Find by Elevation](#union-find-by-elevation).

## Solutions

### Level-by-Level Flood Fill

#### Derivation

The rain metaphor translates directly: try `t = grid[0][0]`, `t + 1`, ... and after each increment test whether the bottom-right is reachable. The reachability test is a flood fill over cells whose elevation is at most `t`. Restarting the fill from scratch each level keeps the logic honest and simple; the inefficiency of rescanning is what the later solutions remove:

1. Set `level = grid[0][0]` (the water cannot be lower than the start cell).
2. Flood fill from `(0, 0)` through cells with elevation `<= level`.
3. If the fill reached `(n - 1, n - 1)`, return `level`; otherwise increment
   `level` and fill again.

#### Walkthrough

Let us run the levels on Example 2: `grid = [[0,1,2,10],[9,14,4,13],[12,3,8,15],[11,5,7,6]]`:

```text
level 0..2   fill reaches (0,0), (0,1), (0,2): the top row alone
level 3..7   (1,2) joins at 4; the pocket at (2,1) stays sealed off
level 8      (2,1), (2,2), (3,1), (3,2), (3,3) all join: corner reached -> return 8
```

The corridor opens gradually: level `3` admits the isolated pocket at `(2,1)` but cannot connect it onward, level `4` extends the fill through `(1,2)`, and level `8` is the first level that chains through `(2,2)` into the bottom row, where `(3,3)` waits. The first successful level is `8`, matching the expected Output for Example 2.

#### Solution

The code is the incrementing level with a from-scratch fill per attempt.

```python
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        size = len(grid)
        level = grid[0][0]
        while True:
            visited = [[False] * size for _ in range(size)]
            if self._reaches(grid, level, visited):
                return level
            level += 1

    def _reaches(self, grid: List[List[int]], level: int, visited: List[List[bool]]) -> bool:
        size = len(grid)

        def dfs(row: int, col: int) -> bool:
            if grid[row][col] > level or visited[row][col]:
                return False
            visited[row][col] = True
            if (row, col) == (size - 1, size - 1):
                return True
            return (
                (row > 0 and dfs(row - 1, col))
                or (row < size - 1 and dfs(row + 1, col))
                or (col > 0 and dfs(row, col - 1))
                or (col < size - 1 and dfs(row, col + 1))
            )

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³)` up to elevation bounds

Up to `n²` distinct levels are tried (the answer is bounded by the largest elevation), and each attempt fills the `n²` grid once.

##### Space Complexity: `O(n²)`

The visited grid per attempt and the recursion stack of depth up to `n²`.

#### Key Insights

- The start cell's elevation is the floor of the search: swimming before the water covers `(0, 0)` is impossible.
- Restarting the fill per level wastes work on cells already known reachable, which is precisely the waste the flood fill's own memory could carry forward.
- The recursion's short-circuit `or` chain stops at the first success, keeping typical fills cheaper than the full-grid worst case.

### Binary Search on the Answer

#### Derivation

The level loop scans every level one by one, but the predicate "level `t` connects the corners" never flips back: it is false up to some threshold and true after. Monotone predicates are binary-search territory: halve the level range instead of stepping it. Each probe is one `O(n²)` reachability fill, and `O(log(max elevation))` probes replace up to `n²` of them:

1. Set `low = grid[0][0]` and `high = max` elevation over the grid.
2. While `low < high`: probe `mid = (low + high) // 2` with a BFS over cells
   of elevation `<= mid`.
3. If the BFS reaches the bottom-right, `high = mid`; otherwise `low = mid + 1`.
4. Return `low`, the minimal connecting level.

#### Walkthrough

Let us bisect on Example 2, with `low = grid[0][0] = 0` and `high = 15`, the largest elevation. Each row is one probe and the bound it moves:

```text
probe 7    no path yet    -> low = 8
probe 11   path exists    -> high = 11
probe 9    path exists    -> high = 9
probe 8    path exists    -> high = 8
low == high == 8 -> return 8
```

The first probe fails because level `7` only opens the top row and the `(2,1)` pocket, leaving the bottom row sealed; every later probe succeeds and walks the corridor through `(1,2)` at `4`, `(2,2)` at `8`, and the bottom row's `5, 7, 6`. Each failure raises `low` past a provably insufficient level and each success lowers `high` onto a known-sufficient one, so the bounds close in on the minimal connecting level. The loop ends with `low == high == 8`, matching the expected Output for Example 2.

#### Solution

The code is the monotone bisection with a BFS probe.

```python
from collections import deque
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        size = len(grid)

        def reaches(level: int) -> bool:
            if grid[0][0] > level:
                return False
            visited = {(0, 0)}
            queue = deque([(0, 0)])
            while queue:
                row, col = queue.popleft()
                if (row, col) == (size - 1, size - 1):
                    return True
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    next_row, next_col = row + dr, col + dc
                    if (
                        0 <= next_row < size
                        and 0 <= next_col < size
                        and (next_row, next_col) not in visited
                        and grid[next_row][next_col] <= level
                    ):
                        visited.add((next_row, next_col))
                        queue.append((next_row, next_col))
            return False

        low, high = grid[0][0], max(max(row) for row in grid)
        while low < high:
            mid = (low + high) // 2
            if reaches(mid):
                high = mid
            else:
                low = mid + 1
        return low
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² * log m)`

Each of the `O(log m)` probes runs one grid-wide BFS, where `m` is the elevation range; the distinct elevations bound the useful range further.

##### Space Complexity: `O(n²)`

The BFS visited set and queue per probe.

#### Key Insights

- Binary search applies off the shelf because feasibility is monotone in the level; recognizing monotone predicates generalizes far past this problem.
- The search converges on the minimal sufficient level even though probes only ever answer yes or no: failures raise the floor, successes lower the ceiling.
- The probe count is independent of how far apart the levels are, which is what defeats the level-by-level scan's worst case.

### Modified Dijkstra's Algorithm

#### Derivation

Both fills answer "is level `t` enough?" for whole levels; the per-cell question is sharper: what is the smallest level at which each cell becomes reachable? That per-cell minimum is exactly a shortest path where path cost is the maximum elevation along the path instead of a sum, and [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) survives the change: all elevations are non-negative and `max` is monotone, so expanding always through the reachable cell with the smallest bottleneck settles cells in nondecreasing order of their final level. The start cell contributes `grid[0][0]`, not `0`:

1. Seed the heap with `(grid[0][0], 0, 0)` and `best[0][0] = grid[0][0]`.
2. Pop the smallest `(level, row, col)`; if it is the far corner, return
   `level` immediately.
3. Skip stale entries where `level > best[row][col]`.
4. For each in-bounds neighbor, compute `candidate = max(level, elevation)`
   and adopt it when it beats `best[neighbor]`, pushing the new entry.
5. The far corner is always reachable on a connected grid, so the heap empties
   only after returning.

#### Walkthrough

Let us run the heap on Example 2: `grid = [[0,1,2,10],[9,14,4,13],[12,3,8,15],[11,5,7,6]]`. The frontier spreads by smallest bottleneck; each row is one productive pop:

```text
pop (0, (0,0))   best (1,0)=9   best (0,1)=1
pop (1, (0,1))   best (1,1)=14  best (0,2)=2
pop (2, (0,2))   best (1,2)=4   best (0,3)=10
pop (4, (1,2))   best (2,2)=8   best (1,3)=13
pop (8, (2,2))   best (3,2)=8   best (2,3)=15   best (2,1)=8
pop (8, (2,1))   best (3,1)=8   best (2,0)=12
pop (8, (3,1))   best (3,0)=11
pop (8, (3,2))   best (3,3)=8
pop (8, (3,3))   -> return 8
```

Level `8` is the workhorse: popped at four different cells in a row, it floods the entire low basin (bottom three rows' cheap cells) at once, and `(3,3)` adopts `8` from `(3,2)`. The return happens on the pop, before the pricier entries at `9` through `15` are ever touched, and `8` matches the expected Output for Example 2. This particular run pushes each cell exactly once, because every relaxation improves a `None` best; on grids where a cell is re-offered at a strictly better level, the outdated entry pops later and the `level > best` guard skips it as stale.

#### Solution

The code is the max-relaxed Dijkstra with an early return at the corner.

```python
import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        size = len(grid)
        best = [[None] * size for _ in range(size)]
        best[0][0] = grid[0][0]
        heap = [(grid[0][0], 0, 0)]
        while heap:
            level, row, col = heapq.heappop(heap)
            if (row, col) == (size - 1, size - 1):
                return level
            if level > best[row][col]:
                continue
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row, next_col = row + dr, col + dc
                if not (0 <= next_row < size and 0 <= next_col < size):
                    continue
                candidate = max(level, grid[next_row][next_col])
                if (
                    best[next_row][next_col] is None
                    or candidate < best[next_row][next_col]
                ):
                    best[next_row][next_col] = candidate
                    heapq.heappush(heap, (candidate, next_row, next_col))
        raise AssertionError("bottom-right cell is always reachable on a square grid")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² * log n)`

Each cell may be pushed once per improving relaxation, `O(1)` neighbors each, so the heap holds `O(n²)` entries with `O(log n²) = O(log n)` costs; every cell is settled once.

##### Space Complexity: `O(n²)`

The `best` grid and the heap.

#### Key Insights

- Replacing Dijkstra's `distance + weight` with `max(distance, weight)` is the entire modification; the greedy correctness argument carries over because `max` is monotone under extension.
- The early return at the corner is safe for the same reason as in ordinary Dijkstra: the smallest bottleneck is popped first, so the first corner pop is final.
- Seeding with `grid[0][0]` rather than `0` quietly encodes the rule that the start cell must be covered before any swim begins.

### Union-Find by Elevation

#### Derivation

The rain process has a batch view: raise the water until cells submerge one by one, cheapest first, and the answer is the elevation of the cell whose submersion first joins the two corners into one component. Sorting cells by elevation and adding them to a union-find in that order reproduces the flood without simulating levels; after each addition, one component test answers "connected yet?":

1. Order the cells by elevation (a flat list sorted by value; the input's
   distinct integers make the order total).
2. Initialize union-find over cell indices.
3. Add cells in order, unioning each with its already-added neighbors.
4. When `(0, 0)` and `(n - 1, n - 1)` first share a root, return the current
   cell's elevation.

#### Walkthrough

Let us add cells on Example 1: `grid = [[0,1],[2,3]]`, sorted order `0, 1, 2, 3`:

```text
add (0,0) elevation 0   no added neighbors        roots: {(0,0)}
add (0,1) elevation 1   union with (0,0)          components: {(0,0),(0,1)}
add (1,0) elevation 2   union with (0,0)          components: one, size 3
                        corners still separate
add (1,1) elevation 3   union with (0,1) and (1,0)
                        corners share a root -> return 3
```

Cells `(0,1)` and `(1,0)` are both adjacent to the growing component and merge in; the final cell `(1,1)` touches `(0,1)` and `(1,0)`, so its union fuses everything and the corner test fires at elevation `3`, matching the expected Output for Example 1.

#### Solution

The code is the sorted insertion loop with the corner test after each union.

```python
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        size = len(grid)
        order = sorted(
            (grid[row][col], row, col)
            for row in range(size)
            for col in range(size)
        )
        parent = list(range(size * size))

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        added = [[False] * size for _ in range(size)]
        for elevation, row, col in order:
            added[row][col] = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row, next_col = row + dr, col + dc
                if (
                    0 <= next_row < size
                    and 0 <= next_col < size
                    and added[next_row][next_col]
                ):
                    root_a = find(row * size + col)
                    root_b = find(next_row * size + next_col)
                    if root_a != root_b:
                        parent[root_b] = root_a
            if find(0) == find(size * size - 1):
                return elevation
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² * log n)`

Sorting the `n²` cells dominates; each cell then unions with at most four neighbors at inverse-Ackermann amortized cost, and the corner test is two finds.

##### Space Complexity: `O(n²)`

The sorted cell list, the parent array, and the added grid.

#### Key Insights

- The answer is a cell elevation, not an accumulated cost: the sort directly orders the candidate answers, and the first connecting one is exact.
- Adding only already-submerged neighbors is what makes each union a true "level reached" event rather than a forward reference.
- The per-addition corner test costs two finds and can be dropped to once-per-component-merge, but the simple form is already inside the sort's log factor.

## Comparison of Solutions

### Time Complexity

- **Level-by-Level Flood Fill**: `O(n³)` up to elevation bounds - one full fill per candidate level.
- **Binary Search on the Answer**: `O(n² * log m)` - logarithmically many full-grid BFS probes.
- **Modified Dijkstra's Algorithm**: `O(n² * log n)` - one settling pass with heap-ordered expansion.
- **Union-Find by Elevation**: `O(n² * log n)` - one sort plus near-constant merges.

### Space Complexity

- **Level-by-Level Flood Fill**: `O(n²)` - the visited grid per attempt.
- **Binary Search on the Answer**: `O(n²)` - the probe's visited set and queue.
- **Modified Dijkstra's Algorithm**: `O(n²)` - the best grid and the heap.
- **Union-Find by Elevation**: `O(n²)` - the sorted list, parent array, and added grid.

### Trade-offs

- The two level-driven solutions keep the rain metaphor and reuse a plain flood fill; the cell-driven solutions pay for a heap or a sort but touch each cell a bounded number of times.
- Binary search is the least code from the monotonicity observation; Dijkstra and Union-Find are restructurings that also survive when the question changes (per-cell arrival times, dynamic water levels).
- None of the four needs the `grid` values to be a permutation; only the elevation ordering matters, which keeps all of them correct on general height maps.

### When to Use Each

- **Level-by-Level Flood Fill**: as the executable definition of the answer on tiny grids.
- **Binary Search on the Answer**: when a monotone feasibility check is already available and code economy matters.
- **Modified Dijkstra's Algorithm**: the interview default here; it also answers richer queries (the min-max level to every cell) for free (recommended here).
- **Union-Find by Elevation**: when the problem extends to dynamic merging or offline batched queries, or when a union-find is already in play.

### Optimization Notes

- Because the values are a permutation of `0..n²-1`, binary search can probe over exactly the present elevations; the `while low < high` form already exploits that implicitly.
- Dijkstra's early return makes its cost output-sensitive: pops stop at the answer's level, often well before the heap empties.
- Union-Find can hoist the corner test to fire only when a merge actually connects the two roots, avoiding two finds per addition on large grids.

