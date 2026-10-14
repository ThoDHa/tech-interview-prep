# [Number of Islands](https://leetcode.com/problems/number-of-islands/)

**Medium** | **25 minutes** | **Array, DFS, BFS, Union Find, Matrix**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Disjoint-set / Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)

**Practice:** [`practice/number_of_islands/solution.py`](../../practice/number_of_islands/solution.py)

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

## Examples

### Example 1

**Input:**

```text
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
```

**Output:** `1`

### Example 2

**Input:**

```text
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
```

**Output:** `3`

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`.

## Deriving the Solution

Reading "island" as a graph term does all the work: every land cell is a node, horizontally or vertically adjacent land cells share an edge, and an island is a connected component of that implicit graph. Every solution below counts connected components; they differ only in how a component is traversed and how visited land is remembered.

1. **Start literal.** Scan the grid cell by cell. Every `'1'` not yet visited is
   the first cell of a brand-new island, so count it, then flood fill outward to mark the rest of its component before scanning on. Sinking visited land to `'0'` makes the grid itself the visited marker, and recursive DFS is the shortest way to write the fill: see [DFS with Grid Modification](#dfs-with-grid-modification).
2. **Bound the memory.** The recursion descends once per cell of a snake-shaped
   island, so the call stack can hold all `m × n` cells. Exploring the component as an expanding frontier with a queue caps the extra memory at the wavefront, `O(min(m, n))`: see [BFS with Grid Modification](#bfs-with-grid-modification).
3. **Stop mutating the input.** Both fills destroy the grid. When the caller
   needs it intact, move the visited marker into a separate boolean matrix and leave the grid read-only, paying `O(m × n)` extra space: see [DFS with Separate Visited Array](#dfs-with-separate-visited-array).
4. **Drop the recursion, keep the order.** Python's recursion limit is a real
   hazard at `300 × 300`. Replacing the call stack with an explicit list keeps the depth-first fill without any recursion at all: see [Iterative DFS with Stack](#iterative-dfs-with-stack).
5. **Count components without traversing.** Connectivity can also be computed
   algebraically: start with every cell as its own component, merge each land cell with its land neighbors, and subtract the water cells from the final component count. This pays off when the grid changes dynamically: see [Union-Find](#union-find).

## Solutions

### DFS with Grid Modification

#### Derivation

The question to ask first is the literal one: how many times does a scan of the grid step onto land that belongs to no island counted so far? Each such cell is the seed of exactly one new island, so the whole problem reduces to two duties: detect a fresh land cell, then mark the rest of its island as seen before the scan continues.

The marking duty is a flood fill over an implicit graph in which each land cell is a node, adjacent land cells (horizontally and vertically) are connected by edges, and each connected component is one island. [DFS](https://en.wikipedia.org/wiki/Depth-first_search) naturally explores an entire connected component before returning, and sinking every visited cell to `'0'` turns the grid itself into the visited marker, so no extra bookkeeping structure is needed:

1. Scan every cell with a double loop over `rows` and `cols`.
2. When `grid[row][col] == '1'`, a new island starts: increment `islands` and
   call `dfs(row, col)`.
3. `dfs` returns immediately when the cell is out of bounds or `'0'`; otherwise
   it sinks the cell (`grid[row][col] = '0'`) and recurses into all four neighbors from `directions` (right, down, left, up).
4. After the scan completes, return `islands`.

#### Walkthrough

Example 1 is a 4×5 grid whose single island spans many cells, so to keep the trace short we use a smaller tailored grid with two islands:

```text
grid = [
  ["1","1","0"],
  ["1","0","0"],
  ["0","0","1"]
]
```

The main loop scans cells in row-major order (left to right, top to bottom). It only starts work when it finds a `'1'`, and the flood fill sinks every connected land cell to `'0'` so the same island is never counted twice.

**Main loop scan:**

| Cell `(row, col)` | `grid[row][col]` | Action | `islands` |
| --- | --- | --- | --- |
| `(0, 0)` | `'1'` | new island: increment, then `dfs(0, 0)` sinks the top-left island | `1` |
| `(0, 1)` | `'0'` | already sunk by the first `dfs`, skip | `1` |
| `(0, 2)` | `'0'` | water, skip | `1` |
| `(1, 0)` | `'0'` | already sunk, skip | `1` |
| `(1, 1)`, `(1, 2)`, `(2, 0)`, `(2, 1)` | `'0'` | water, skip | `1` |
| `(2, 2)` | `'1'` | new island: increment, then `dfs(2, 2)` sinks the lone cell | `2` |

**Inside `dfs(0, 0)`** (the first island), the recursion explores neighbors in the order right, down, left, up. Each call either sinks a land cell to `'0'` and recurses, or returns immediately when it hits water, an already-sunk cell, or the grid edge:

```text
dfs(0,0): grid[0][0]='1' -> sink to '0', explore neighbors
  dfs(0,1): grid[0][1]='1' -> sink to '0', explore neighbors
    dfs(0,2): water -> return
    dfs(1,1): water -> return
    dfs(0,0): already '0' -> return
    dfs(-1,1): out of bounds -> return
  dfs(1,0): grid[1][0]='1' -> sink to '0', explore neighbors
    dfs(1,1): water -> return
    dfs(2,0): water -> return
    dfs(1,-1): out of bounds -> return
    dfs(0,0): already '0' -> return
  dfs(0,-1): out of bounds -> return
  dfs(-1,0): out of bounds -> return
```

After this call returns, cells `(0,0)`, `(0,1)`, and `(1,0)` are all `'0'`: the entire top-left island has been sunk in one flood fill.

The second `dfs(2, 2)` sinks the single bottom-right cell and finds no land neighbors, so it returns immediately.

When the main loop finishes, `islands` is `2`, which is the returned value. (For the doc's Example 1, the same process returns `1`, matching its expected Output of `1`.)

#### Solution

The code is the walkthrough's scan and flood fill: the main loop seeds each island and `dfs` sinks it.

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def dfs(row: int, col: int) -> None:
            # Base cases: out of bounds or already visited/water
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                grid[row][col] == '0'):
                return

            # Mark current cell as visited by changing it to '0'
            grid[row][col] = '0'

            # Recursively explore all 4 adjacent directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
            for dr, dc in directions:
                dfs(row + dr, col + dc)

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1':
                    islands += 1
                    # Use DFS to mark all connected land cells as visited
                    dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

In the worst case (all land), we visit each cell exactly once: once in the main loop and potentially once during DFS traversal.

##### Space Complexity: `O(m × n)`

In the worst case (single snake-like island), the recursion stack can be as deep as the total number of cells. The algorithm modifies the input grid in-place.

#### Key Insights

- Each unvisited `'1'` is the seed of exactly one island; the flood fill guarantees the rest of that island is sunk before the main loop advances.
- Sinking visited land to `'0'` doubles as the visited marker, so no extra bookkeeping structure is needed.
- The four-direction flood fill matches the adjacency rule (horizontal and vertical only), so diagonally touching cells stay separate islands.

### BFS with Grid Modification

#### Derivation

The recursive fill has one weakness: its memory is the call stack. On a snake-shaped island the recursion descends once per cell, so the stack can grow to `m × n` frames, deep enough to threaten the interpreter's recursion limit. The fix is to change the exploration order: instead of following one path as deep as it goes, expand the island as a widening frontier. A [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) queue holds only the current wavefront, which stays within `O(min(m, n))` cells, and its distance-ordered exploration also serves extensions such as shortest paths within a component:

1. The main scan is unchanged: every unvisited `'1'` increments `islands` and
   starts a fill, now `bfs(row, col)`.
2. `bfs` seeds a `queue` with `(start_row, start_col)` and sinks that cell to
   `'0'` immediately.
3. While the queue is non-empty, `popleft` a cell and inspect its four
   neighbors; every in-bounds neighbor still holding `'1'` is sunk and appended.
4. Sinking at enqueue time (not at dequeue time) guarantees no cell enters the
   queue twice.

#### Walkthrough

Let us sink the first island of Example 2 by hand. The scan reaches `(0, 0)`, finds `'1'`, sets `islands = 1`, and calls `bfs(0, 0)`, which sinks the seed and enqueues it. Each line below is one queue event; neighbors are checked in the order right, down, left, up:

```text
seed (0,0)   sink, queue = [(0,0)]
pop (0,0)    right (0,1)='1' -> sink+enqueue; down (1,0)='1' -> sink+enqueue
             queue = [(0,1), (1,0)]
pop (0,1)    right (0,2) water; down (1,1)='1' -> sink+enqueue; left (0,0) sunk
             queue = [(1,0), (1,1)]
pop (1,0)    right (1,1) already sunk; down (2,0) water; up (0,0) sunk
             queue = [(1,1)]
pop (1,1)    all four neighbors water, sunk, or out of bounds
             queue = []  -> bfs returns
```

The 2 × 2 block in the top-left corner is now entirely `'0'`, sunk in expanding rings around the seed rather than along one deep path. The scan continues, finds `'1'` at `(2, 2)` (`islands = 2`, a lone cell whose fill enqueues no neighbors), and then `'1'` at `(3, 3)` (`islands = 3`, whose fill sinks `(3, 4)` the same way). The function returns `3`, matching the expected Output for Example 2.

#### Solution

The code is the queue discipline from the walkthrough: sink at enqueue time, expand at dequeue time.

```python
from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def bfs(start_row: int, start_col: int) -> None:
            queue = deque([(start_row, start_col)])
            grid[start_row][start_col] = '0'  # Mark as visited immediately

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                row, col = queue.popleft()

                # Check all 4 adjacent directions
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc

                    # If adjacent cell is valid land, add to queue and mark as visited
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                        grid[new_row][new_col] == '1'):

                        grid[new_row][new_col] = '0'  # Mark as visited
                        queue.append((new_row, new_col))

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1':
                    islands += 1
                    # Use BFS to mark all connected land cells as visited
                    bfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Same as DFS: each cell is visited at most once during the entire algorithm.

##### Space Complexity: `O(min(m, n))`

In the worst case (rectangle-shaped island), the BFS queue contains at most `O(min(m, n))` cells, which occurs when the wavefront forms a diagonal. This can be more space-efficient than DFS for certain grid shapes.

#### Key Insights

- Marking a cell visited at enqueue time (rather than dequeue time) prevents the same cell from being added to the queue twice.
- BFS bounds peak memory by the frontier size rather than the longest path, so it sidesteps the deep recursion that can crash DFS on huge grids.
- The traversal order does not affect the island count, so BFS and DFS are interchangeable for correctness here.

### DFS with Separate Visited Array

#### Derivation

Both previous fills share a side effect: they destroy the input. Sinking land to `'0'` is elegant, but the caller may need the grid afterward, or the grid may be read-only. The repair is to separate the two roles the grid was playing: keep `grid` as pure input and record "already counted" in a parallel boolean matrix `visited`. The traversal is otherwise identical to [DFS with Grid Modification](#dfs-with-grid-modification):

1. Allocate `visited`, an `m × n` matrix of `False`.
2. The scan counts a new island at every cell where `grid[row][col] == '1'`
   and `visited[row][col]` is still `False`.
3. `dfs` returns when the cell is out of bounds, already visited, or water;
   otherwise it sets `visited[row][col] = True` and recurses into the four neighbors.
4. The grid is never written, so it survives the call unchanged.

#### Walkthrough

We reuse the tailored two-island grid from the [DFS with Grid Modification](#dfs-with-grid-modification) walkthrough, chosen so the identical traversal is easy to compare with the sinking version: `grid = [["1","1","0"], ["1","0","0"], ["0","0","1"]]`. This time the grid never changes; each line shows the cells of `visited` holding `True` after the event:

```text
scan (0,0)   grid '1', not visited -> islands = 1, dfs(0, 0)
  dfs(0,0)   visited = {(0,0)}             recurse right first
  dfs(0,1)   visited = {(0,0), (0,1)}      right/down water, left visited, up out
  dfs(1,0)   visited = {(0,0), (0,1), (1,0)}   every neighbor water/visited/out
scan (0,1)   grid '1' but visited -> skip, no new island
scan (0,2) .. (2,1)   water or visited -> skip
scan (2,2)   grid '1', not visited -> islands = 2, dfs(2, 2)
  dfs(2,2)   visited = {(0,0), (0,1), (1,0), (2,2)}
```

The visit order `(0,0)`, `(0,1)`, `(1,0)` matches the sinking DFS exactly; only the marker moved. The decisive beat is the scan reaching `(0, 1)`: the cell still reads `'1'` in the untouched grid, and only the `visited[0][1]` check stops it from being counted as a second island. The loop ends with `islands = 2` while `grid` still holds its original characters.

#### Solution

The code is the same flood fill with every visited mark redirected from `grid` into `visited`.

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        islands = 0

        def dfs(row: int, col: int) -> None:
            # Base cases: out of bounds, already visited, or water
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                visited[row][col] or
                grid[row][col] == '0'):
                return

            # Mark current cell as visited
            visited[row][col] = True

            # Recursively explore all 4 adjacent directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                dfs(row + dr, col + dc)

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1' and not visited[row][col]:
                    islands += 1
                    # Use DFS to mark all connected land cells as visited
                    dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Same traversal pattern as previous solutions.

##### Space Complexity: `O(m × n)`

Requires additional space for the visited matrix plus recursion stack space.

#### Key Insights

- Decoupling the visited state from the grid keeps the caller's input intact, which matters when the grid is read-only or reused afterward.
- The cost is an explicit `O(m × n)` boolean matrix, the price of not mutating the input.
- Marking a cell visited before recursing into its neighbors is what stops adjacent land cells from bouncing the recursion back and forth forever; the relative order of the visited and water checks in the guard does not affect correctness.

### Iterative DFS with Stack

#### Derivation

The recursive fills all inherit the interpreter's recursion limit: a snake island threading a `300 × 300` grid is 90,000 calls deep, far beyond Python's default limit of 1,000. The observation that removes the risk is that the call stack contributes nothing but a to-do list of cells, so DFS only needs *some* stack, not the interpreter's. Replace it with an explicit list used as a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)):

1. `iterative_dfs` seeds `stack` with the starting cell.
2. Loop while the stack is non-empty: `pop` a cell, and skip it when it is out
   of bounds or `'0'` (water or already sunk).
3. Otherwise sink it and push all four neighbors unconditionally; invalid ones
   are filtered when they are popped.
4. The main scan is unchanged: each unvisited `'1'` increments `islands` and
   runs one fill.

#### Walkthrough

We reuse the tailored two-island grid `grid = [["1","1","0"], ["1","0","0"], ["0","0","1"]]` so the stack's visit order can be compared with the recursive DFS on the same input. The scan finds `(0, 0)`, sets `islands = 1`, and starts the fill. Each line is one pop:

```text
seed (0,0)    stack = [(0,0)]
pop (0,0)     '1' -> sink, push neighbors   stack = [(0,1), (1,0), (0,-1), (-1,0)]
pop (-1,0)    out of bounds -> skip
pop (0,-1)    out of bounds -> skip
pop (1,0)     '1' -> sink, push neighbors   stack = [(0,1), (1,1), (2,0), (1,-1), (0,0)]
pop (0,0)     already '0' -> skip           (duplicate entry, guard rejects it)
pop (1,-1)    out of bounds -> skip
pop (2,0)     water -> skip
pop (1,1)     water -> skip
pop (0,1)     '1' -> sink, push neighbors   stack = [(0,2), (1,1), (0,0), (-1,1)]
pop (-1,1)    out of bounds -> skip
pop (0,0)     already '0' -> skip
pop (1,1)     water -> skip
pop (0,2)     water -> skip                 stack = [] -> fill done
```

Because the stack is LIFO and neighbors are pushed right, down, left, up, the last push is examined first: the sink order is `(0,0)`, `(1,0)`, `(0,1)`, different from the recursive order `(0,0)`, `(0,1)`, `(1,0)`, which changes nothing about the count. Note `(0, 0)` re-enters the stack twice and is discarded by the guard both times. The scan then finds `(2, 2)`, whose fill sinks the lone cell and skips its four pushed neighbors, and the function returns `islands = 2`.

#### Solution

The code is the pop, guard, sink, push loop from the walkthrough, wrapped in the usual scan.

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def iterative_dfs(start_row: int, start_col: int) -> None:
            stack = [(start_row, start_col)]
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while stack:
                row, col = stack.pop()

                # Skip if out of bounds or water/visited
                if (row < 0 or row >= rows or
                    col < 0 or col >= cols or
                    grid[row][col] == '0'):
                    continue

                # Mark as visited
                grid[row][col] = '0'

                # Add all valid neighbors to stack
                for dr, dc in directions:
                    stack.append((row + dr, col + dc))

        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # If we find an unvisited land cell, it's a new island
                if grid[row][col] == '1':
                    islands += 1
                    # Use iterative DFS to mark all connected land cells
                    iterative_dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each cell is processed at most once.

##### Space Complexity: `O(m × n)`

In the worst case, the explicit stack might contain all cells (for a snake-like island).

#### Key Insights

- The explicit stack replaces Python's call stack, so the traversal cannot hit the interpreter recursion limit on a 300 × 300 grid.
- Pushing neighbors first and validating them on pop keeps the inner loop simple, at the cost of occasionally stacking already-sunk cells that are then skipped.
- A cell can appear multiple times on the stack, so the bounds-and-water guard on pop is what guarantees each cell is sunk exactly once.

### Union-Find

#### Derivation

Every approach so far answers "how many islands?" by walking each island. [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) asks a different question: if every cell starts as its own component, how many components remain after gluing all adjacent land together? Merging components is exactly what a disjoint-set structure does in near-constant time, and it keeps working when the grid is built dynamically or when connectivity between arbitrary cells must be queried, which a one-shot traversal cannot support without re-running:

1. Build `uf = UnionFind(rows * cols)` over all cells, flattening coordinates
   with `get_index(row, col) = row * cols + col`; `components` starts at the total cell count.
2. Scan the grid. Count each `'0'` in `water_cells`; for each `'1'`, union it
   with its right and down land neighbors only, so every adjacent pair is processed exactly once.
3. Each `union` of two different roots decrements `components`; `find` applies
   path compression and `union` applies union by rank to keep both operations nearly constant.
4. Water cells never union with anything, so each stays a singleton component;
   subtracting them, `uf.get_components() - water_cells` is the island count.

#### Walkthrough

The tailored two-island grid from the earlier walkthroughs, `grid = [["1","1","0"], ["1","0","0"], ["0","0","1"]]`, keeps the component arithmetic small: 9 cells indexed `0` to `8` by `get_index(row, col) = row * 3 + col`, with land at indices `0`, `1`, `3`, `8`. `components` starts at `9`, and the scan visits cells in row-major order:

```text
(0,0) idx 0   land: right (0,1) land -> union(0, 1), components 9 -> 8
              down (1,0) land -> union(0, 3), components 8 -> 7
(0,1) idx 1   land: right (0,2) water, down (1,1) water -> no unions
(0,2)         water, water_cells = 1
(1,0) idx 3   land: right (1,1) water, down (2,0) water -> no unions
(1,1)..(2,1)  water, water_cells = 2, 3, 4, 5
(2,2) idx 8   land: right and down out of bounds -> no unions
```

Inside the first union, `find(0)` and `find(1)` return distinct roots of equal rank, so `parent[1] = 0` and `rank[0]` rises to `1`; the second union then hangs index `3` under the higher-ranked root `0`. After the scan, the surviving components are `{0, 1, 3}` (the merged top-left island), `{8}` (the lone corner), and five water singletons: `7` components in all. Returning `uf.get_components() - water_cells = 7 - 5 = 2` counts exactly the two islands, matching the DFS result on the same grid.

#### Solution

The code is the single scan from the walkthrough, with the `UnionFind` helper carrying the component count.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, x: int) -> int:
        # Path compression optimization
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x, root_y = self.find(x), self.find(y)

        if root_x != root_y:
            # Union by rank optimization
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

            self.components -= 1

    def get_components(self) -> int:
        return self.components


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])

        # Count water cells to subtract from total components later
        water_cells = 0

        # Create Union-Find structure for all cells
        uf = UnionFind(rows * cols)

        # Check right and down neighbors only (to avoid double processing)
        directions = [(0, 1), (1, 0)]

        def get_index(row: int, col: int) -> int:
            """Convert 2D coordinates to 1D index"""
            return row * cols + col

        # Process each cell and union with adjacent land cells
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '0':
                    water_cells += 1
                else:  # Land cell
                    current_idx = get_index(row, col)

                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc

                        # If neighbor is valid land, union them
                        if (0 <= new_row < rows and
                            0 <= new_col < cols and
                            grid[new_row][new_col] == '1'):

                            neighbor_idx = get_index(new_row, new_col)
                            uf.union(current_idx, neighbor_idx)

        # Total islands = total components - water cells
        return uf.get_components() - water_cells
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × α(m × n))`

Where α is the inverse Ackermann function (practically constant). Each cell is processed once, and each union/find operation takes nearly constant time with path compression and union by rank.

##### Space Complexity: `O(m × n)`

Space for the parent and rank arrays in the Union-Find structure.

#### Key Insights

- Unioning only the right and down neighbors covers every adjacency exactly once, avoiding redundant union calls.
- Subtracting the water-cell count from the total component count yields the island count without ever sinking land, so the input grid is preserved.
- Path compression plus union by rank keep each operation effectively constant, which is what makes the structure competitive with linear traversal.

## Comparison of Solutions

### Time Complexity

- **DFS with Grid Modification**: `O(m × n)` - Each cell is visited at most once across the main loop and DFS traversal.
- **BFS with Grid Modification**: `O(m × n)` - Same as DFS, each cell is processed at most once.
- **DFS with Separate Visited Array**: `O(m × n)` - Identical traversal pattern, each cell visited once.
- **Iterative DFS with Stack**: `O(m × n)` - Each cell is processed at most once.
- **Union-Find**: `O(m × n × α(m × n))` - Each cell is processed once, with each union/find operation taking nearly constant inverse-Ackermann time.

### Space Complexity

- **DFS with Grid Modification**: `O(m × n)` - Recursion stack can grow as deep as the cell count for a snake-like island.
- **BFS with Grid Modification**: `O(min(m, n))` - The BFS queue holds at most a diagonal wavefront, which is more space-efficient for wide grids.
- **DFS with Separate Visited Array**: `O(m × n)` - Requires the visited matrix plus recursion stack space.
- **Iterative DFS with Stack**: `O(m × n)` - The explicit stack may contain all cells for a snake-like island.
- **Union-Find**: `O(m × n)` - Parent and rank arrays for every cell.

### Trade-offs

- **DFS with Grid Modification**: Simple, space-efficient, and optimal, but it modifies the input grid.
- **BFS with Grid Modification**: Offers better space usage on wide grids, at the cost of a more complex implementation.
- **DFS with Separate Visited Array**: Preserves the input grid, but requires extra space for the visited matrix.
- **Iterative DFS with Stack**: Avoids recursion depth limits, but requires explicit stack management.
- **Union-Find**: Handles dynamic connectivity scenarios well, but the implementation is complex.

### When to Use Each

- **DFS with Grid Modification (Recommended)**: Best for interviews: simple, optimal, and demonstrates core graph traversal concepts.
- **BFS**: When you need level-order exploration or have memory constraints with deep grids.
- **DFS with Separate Visited**: When input grid must be preserved or is read-only.
- **Iterative DFS**: When dealing with very large grids where recursion depth might be an issue.
- **Union-Find**: For advanced scenarios with dynamic grid updates or connectivity queries.

### Optimization Notes

- DFS with Grid Modification is the recommended interview choice: it is optimal in time, simple to implement, and demonstrates core graph traversal cleanly.
- When the input grid must remain intact, switch to the DFS with Separate Visited Array approach's separate visited array; the only cost is the extra `O(m × n)` matrix.
- For very large grids, prefer BFS or Iterative DFS with Stack to avoid Python's recursion depth limit causing a stack overflow.
- A common pitfall is missing bounds checks before indexing neighbors; the direction array `[(0,1),(1,0),(0,-1),(-1,0)]` with explicit `0 <= r < rows` guards keeps the traversal safe.
