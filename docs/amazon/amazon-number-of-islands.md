# [Number of Islands](https://www.fastprep.io/problems/amazon-number-of-islands)

**Medium** | **NN minutes** | **Matrix, Graph, Depth First Search, Breadth First Search**

Given an array of equal-length strings grid, where '1' represents land and '0' represents water, return the number of islands.

## Examples

### Example 1

**Input:** `grid = ["11110","11010","11000","00000"]`

**Output:** `1`

**Explanation:** All land cells belong to one orthogonally connected component.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-number-of-islands; fill them in. -->

## Solutions

### DFS with Grid Modification

#### Derivation

The question to ask first is the literal one: how many times does a scan of the grid step onto land that belongs to no island counted so far? Each such cell is the seed of exactly one new island, so the problem reduces to two duties: detect a fresh land cell, then mark the rest of its island as seen before the scan continues.

The marking duty is a flood fill over an implicit graph in which each land cell is a node and horizontally or vertically adjacent land cells share an edge. [DFS](https://en.wikipedia.org/wiki/Depth-first-search) naturally explores an entire connected component before returning, and sinking every visited cell to `'0'` turns the copy of the grid into the visited marker. Because the rows arrive as strings, which Python does not allow code to mutate, the fill first copies the grid into lists of characters, and the copy is what makes the sink legal:

1. Copy the string rows into `cells`, a list of lists of characters.
2. Scan every cell of `cells` with a double loop over `rows` and `cols`.
3. When `cells[row][col] == '1'`, a new island starts: increment `islands` and
   call `dfs(row, col)`.
4. `dfs` returns immediately when the cell is out of bounds or `'0'`; otherwise
   it sinks the cell (`cells[row][col] = '0'`) and recurses into the four neighbors from `directions` (right, down, left, up).
5. After the scan completes, return `islands`.

#### Walkthrough

Example 1 is a 4 × 5 grid whose single island spans nine cells, so to keep the trace short we use a smaller tailored grid with two islands:

```text
grid = [
  "110",
  "100",
  "001"
]
```

The main loop scans cells in row-major order (left to right, top to bottom). It only starts work when it finds a `'1'`, and the flood fill sinks every connected land cell to `'0'` so the same island is never counted twice:

| Cell `(row, col)` | `cells[row][col]` | Action | `islands` |
| --- | --- | --- | --- |
| `(0, 0)` | `'1'` | new island: increment, then `dfs(0, 0)` sinks the top-left island | `1` |
| `(0, 1)` | `'0'` | already sunk by the first `dfs`, skip | `1` |
| `(0, 2)`, `(1, 1)`, `(1, 2)`, `(2, 0)`, `(2, 1)` | `'0'` | water, skip | `1` |
| `(2, 2)` | `'1'` | new island: increment, then `dfs(2, 2)` sinks the lone cell | `2` |

**Inside `dfs(0, 0)`** (the first island), the recursion explores neighbors in the order right, down, left, up. Each call either sinks a land cell to `'0'` and recurses, or returns immediately when it hits water, an already-sunk cell, or the grid edge:

```text
dfs(0,0): cells[0][0]='1' -> sink to '0', explore neighbors
  dfs(0,1): cells[0][1]='1' -> sink to '0', explore neighbors
    dfs(0,2): water -> return
    dfs(1,1): water -> return
    dfs(0,0): already '0' -> return
    dfs(-1,1): out of bounds -> return
  dfs(1,0): cells[1][0]='1' -> sink to '0', explore neighbors
    dfs(1,1): water -> return
    dfs(2,0): water -> return
    dfs(1,-1): out of bounds -> return
    dfs(0,0): already '0' -> return
  dfs(0,-1): out of bounds -> return
  dfs(-1,0): out of bounds -> return
```

After this call returns, cells `(0,0)`, `(0,1)`, and `(1,0)` are all `'0'`: the entire top-left island has been sunk in one flood fill. The second `dfs(2, 2)` sinks the single bottom-right cell and finds no land neighbors. When the main loop finishes, `islands` is `2`, which is the returned value. (For Example 1, the same process returns `1`, matching its expected Output of `1`.)

#### Solution

The code is the walkthrough's scan and flood fill: the main loop seeds each island and `dfs` sinks it.

```python
from typing import List


class Solution:
    def solve(self, grid: List[str]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        cells = [list(row) for row in grid]
        islands = 0

        def dfs(row: int, col: int) -> None:
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                    cells[row][col] == '0'):
                return

            cells[row][col] = '0'

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(row + dr, col + dc)

        for row in range(rows):
            for col in range(cols):
                if cells[row][col] == '1':
                    islands += 1
                    dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Every cell is copied once and then visited at most once across the main loop and the flood fill.

##### Space Complexity: `O(m × n)`

The character copy of the grid plus the recursion stack, which can hold all cells of a snake-shaped island.

#### Key Insights

- Each unvisited `'1'` is the seed of exactly one island; the flood fill guarantees the rest of that island is sunk before the main loop advances.
- Sinking visited land to `'0'` doubles as the visited marker inside the copy, so no separate bookkeeping structure is needed.
- String rows are immutable in Python, so the "modify the grid" trick requires copying the rows into lists first; the copy is one `O(m × n)` pass and does not change the asymptotics.
- The four-direction fill matches the adjacency rule (horizontal and vertical only), so diagonally touching cells stay separate islands.

### BFS with Grid Modification

#### Derivation

The recursive fill has one weakness: its memory is the call stack. On a snake-shaped island the recursion descends once per cell, so the stack can grow to `m × n` frames, deep enough to threaten the interpreter's recursion limit. The repair is to change the exploration order: instead of following one path as deep as it goes, expand the island as a widening frontier. [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) holds only the current wavefront in a queue, and the wavefront of a grid fill never exceeds `O(min(m, n))` cells:

1. The main scan is unchanged: every unvisited `'1'` increments `islands` and
   starts a fill, now `bfs(row, col)`.
2. `bfs` seeds a `queue` with `(start_row, start_col)` and sinks that cell to
   `'0'` in `cells` immediately.
3. While the queue is non-empty, `popleft` a cell and inspect its four
   neighbors; every in-bounds neighbor still holding `'1'` is sunk and appended.
4. Sinking at enqueue time (not at dequeue time) guarantees no cell enters the
   queue twice.

#### Walkthrough

Let us sink the island of Example 1 by hand. The scan reaches `(0, 0)`, finds `'1'`, sets `islands = 1`, and calls `bfs(0, 0)`, which sinks the seed and enqueues it. Each line below is one queue event; neighbors are checked in the order right, down, left, up:

```text
seed (0,0)   sink, queue = [(0,0)]
pop (0,0)    right (0,1)='1' -> sink+enqueue; down (1,0)='1' -> sink+enqueue
             queue = [(0,1), (1,0)]
pop (0,1)    right (0,2)='1' -> sink+enqueue; down (1,1)='1' -> sink+enqueue
             queue = [(1,0), (0,2), (1,1)]
pop (1,0)    right (1,1) already sunk; down (2,0)='1' -> sink+enqueue
             queue = [(0,2), (1,1), (2,0)]
pop (0,2)    right (0,3)='1' -> sink+enqueue; down (1,2) water
             queue = [(1,1), (2,0), (0,3)]
pop (1,1)    right (1,2) water; down (2,1)='1' -> sink+enqueue
             queue = [(2,0), (0,3), (2,1)]
pop (2,0)    right (2,1) already sunk; down (3,0) water
             queue = [(0,3), (2,1)]
pop (0,3)    right (0,4) water; down (1,3)='1' -> sink+enqueue
             queue = [(2,1), (1,3)]
pop (2,1)    right (2,2) water; down (3,1) water
             queue = [(1,3)]
pop (1,3)    right (1,4) water; down (2,3) water; left (1,2) water
             queue = []  -> bfs returns
```

All nine land cells, including the eastern arm `(0,3)` and `(1,3)`, were sunk in expanding rings around the seed, and the queue never held more than three cells. The scan then finds no remaining `'1'` and the function returns `1`, matching the expected Output for Example 1.

#### Solution

The code is the queue discipline from the walkthrough: sink at enqueue time, expand at dequeue time.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[str]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        cells = [list(row) for row in grid]
        islands = 0

        def bfs(start_row: int, start_col: int) -> None:
            queue = deque([(start_row, start_col)])
            cells[start_row][start_col] = '0'

            while queue:
                row, col = queue.popleft()
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                            cells[new_row][new_col] == '1'):
                        cells[new_row][new_col] = '0'
                        queue.append((new_row, new_col))

        for row in range(rows):
            for col in range(cols):
                if cells[row][col] == '1':
                    islands += 1
                    bfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Every cell is copied once and enqueued at most once across the whole run.

##### Space Complexity: `O(m × n)`

The character copy of the grid dominates; the queue itself never holds more than `O(min(m, n))` wavefront cells.

#### Key Insights

- Marking a cell visited at enqueue time (rather than dequeue time) prevents the same cell from being added to the queue twice.
- Replacing the call stack with a queue removes the recursion-depth hazard; on a mutable grid the wavefront bound would also cap the fill's memory at `O(min(m, n))`.
- The traversal order does not affect the island count, so BFS and DFS are interchangeable for correctness here.

### DFS with Separate Visited Array

#### Derivation

The previous fill copies the whole grid only because it wants to write into it. But reading strings is legal, and the only duty that needs a write is "remember that this cell is counted". Separating those two roles keeps `grid` as pure input and records the counted state in a parallel boolean matrix `visited`, so no character copy is needed at all. The traversal is otherwise identical to [DFS with Grid Modification](#dfs-with-grid-modification):

1. Allocate `visited`, an `m × n` matrix of `False`.
2. The scan counts a new island at every cell where `grid[row][col] == '1'`
   and `visited[row][col]` is still `False`.
3. `dfs` returns when the cell is out of bounds, already visited, or water;
   otherwise it sets `visited[row][col] = True` and recurses into the four neighbors.
4. The string rows are never written, so no copy is made.

#### Walkthrough

We reuse the tailored two-island grid from the [DFS with Grid Modification](#dfs-with-grid-modification) walkthrough, chosen so the identical traversal is easy to compare with the sinking version: `grid = ["110", "100", "001"]`. This time nothing is copied or sunk; each line shows the cells of `visited` holding `True` after the event:

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

The visit order `(0,0)`, `(0,1)`, `(1,0)` matches the sinking DFS exactly; only the marker moved. The decisive beat is the scan reaching `(0, 1)`: the string still reads `'1'`, and only the `visited[0][1]` check stops it from being counted as a second island. The loop ends with `islands = 2`.

#### Solution

The code is the same flood fill with every visited mark redirected from the grid copy into `visited`.

```python
from typing import List


class Solution:
    def solve(self, grid: List[str]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        islands = 0

        def dfs(row: int, col: int) -> None:
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                visited[row][col] or
                    grid[row][col] == '0'):
                return

            visited[row][col] = True

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(row + dr, col + dc)

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1' and not visited[row][col]:
                    islands += 1
                    dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Same traversal pattern as the sinking DFS; each cell is visited at most once.

##### Space Complexity: `O(m × n)`

The visited matrix plus the recursion stack, which can hold all cells of a snake-shaped island.

#### Key Insights

- Reading the string rows directly removes the character copy the sinking variants needed; the visited matrix carries the mutation instead.
- Decoupling the counted state from the input also keeps the caller's grid intact, which matters when the grid is read-only or reused afterward.
- Marking a cell visited before recursing into its neighbors is what stops adjacent land cells from bouncing the recursion back and forth forever.

### Iterative DFS with Stack

#### Derivation

The recursive fills all inherit the interpreter's recursion limit: a snake island threading a 300 × 300 grid is 90,000 calls deep, far beyond Python's default limit of 1,000. The observation that removes the risk is that the call stack contributes nothing but a to-do list of cells, so DFS only needs *some* stack, not the interpreter's. Replace it with an explicit list used as a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)):

1. `iterative_dfs` seeds `stack` with the starting cell.
2. Loop while the stack is non-empty: `pop` a cell, and skip it when it is out
   of bounds or `'0'` (water or already sunk).
3. Otherwise sink it in `cells` and push all four neighbors unconditionally;
   invalid ones are filtered when they are popped.
4. The main scan is unchanged: each unvisited `'1'` increments `islands` and
   runs one fill.

#### Walkthrough

We reuse the tailored two-island grid `grid = ["110", "100", "001"]` so the stack's visit order can be compared with the recursive DFS on the same input. The scan finds `(0, 0)`, sets `islands = 1`, and starts the fill. Each line is one pop:

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

Because the stack is LIFO and neighbors are pushed right, down, left, up, the last push is examined first: the sink order is `(0,0)`, `(1,0)`, `(0,1)`, different from the recursive order `(0,0)`, `(0,1)`, `(1,0)`, which changes nothing about the count. The scan then finds `(2, 2)`, whose fill sinks the lone cell and skips its four pushed neighbors, and the function returns `islands = 2`.

#### Solution

The code is the pop, guard, sink, push loop from the walkthrough, wrapped in the usual scan.

```python
from typing import List


class Solution:
    def solve(self, grid: List[str]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        cells = [list(row) for row in grid]
        islands = 0

        def iterative_dfs(start_row: int, start_col: int) -> None:
            stack = [(start_row, start_col)]
            while stack:
                row, col = stack.pop()
                if (row < 0 or row >= rows or
                    col < 0 or col >= cols or
                        cells[row][col] == '0'):
                    continue

                cells[row][col] = '0'

                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    stack.append((row + dr, col + dc))

        for row in range(rows):
            for col in range(cols):
                if cells[row][col] == '1':
                    islands += 1
                    iterative_dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each cell is copied once and processed at most a constant number of times (a cell can sit on the stack once per sunk neighbor).

##### Space Complexity: `O(m × n)`

The character copy of the grid plus the explicit stack, which may hold all cells for a snake-like island.

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
   `uf.components - water_cells` is the island count.

#### Walkthrough

The tailored two-island grid from the earlier walkthroughs, `grid = ["110", "100", "001"]`, keeps the component arithmetic small: 9 cells indexed `0` to `8` by `get_index(row, col) = row * 3 + col`, with land at indices `0`, `1`, `3`, `8`. `components` starts at `9`, and the scan visits cells in row-major order:

```text
(0,0) idx 0   land: right (0,1) land -> union(0, 1), components 9 -> 8
              down (1,0) land -> union(0, 3), components 8 -> 7
(0,1) idx 1   land: right (0,2) water, down (1,1) water -> no unions
(0,2)         water, water_cells = 1
(1,0) idx 3   land: right (1,1) water, down (2,0) water -> no unions
(1,1)..(2,1)  water, water_cells = 2, 3, 4, 5
(2,2) idx 8   land: right and down out of bounds -> no unions
```

Inside the first union, `find(0)` and `find(1)` return distinct roots of equal rank, so `parent[1] = 0` and `rank[0]` rises to `1`; the second union then hangs index `3` under the higher-ranked root `0`. After the scan, the surviving components are `{0, 1, 3}` (the merged top-left island), `{8}` (the lone corner), and five water singletons: `7` components in all. Returning `uf.components - water_cells = 7 - 5 = 2` counts exactly the two islands. (For Example 1, the same process returns `1`, matching its expected Output.)

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
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x, root_y = self.find(x), self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            self.components -= 1


class Solution:
    def solve(self, grid: List[str]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        water_cells = 0
        uf = UnionFind(rows * cols)

        def get_index(row: int, col: int) -> int:
            return row * cols + col

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '0':
                    water_cells += 1
                    continue

                current_idx = get_index(row, col)
                for dr, dc in [(0, 1), (1, 0)]:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                            grid[new_row][new_col] == '1'):
                        neighbor_idx = get_index(new_row, new_col)
                        uf.union(current_idx, neighbor_idx)

        return uf.components - water_cells
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × α(m × n))`

Where `a` is the inverse Ackermann function (practically constant): each cell is processed once, and each union/find operation takes nearly constant time with path compression and union by rank.

##### Space Complexity: `O(m × n)`

The parent and rank arrays in the Union-Find structure.

#### Key Insights

- Unioning only the right and down neighbors covers every adjacency exactly once, avoiding redundant union calls.
- Subtracting the water-cell count from the total component count yields the island count without copying or sinking anything, so the string rows are read in place.
- Path compression plus union by rank keep each operation effectively constant, which is what makes the structure competitive with linear traversal.

## Comparison of Solutions

### Time Complexity

- **DFS with Grid Modification**: `O(m × n)` - each cell is copied once and visited at most once across the main loop and DFS traversal.
- **BFS with Grid Modification**: `O(m × n)` - each cell is copied once and enqueued at most once.
- **DFS with Separate Visited Array**: `O(m × n)` - identical traversal pattern with no copy, each cell visited once.
- **Iterative DFS with Stack**: `O(m × n)` - each cell is processed a constant number of times across stack operations.
- **Union-Find**: `O(m × n × α(m × n))` - one pass over the cells with nearly constant inverse-Ackermann union/find operations.

### Space Complexity

- **DFS with Grid Modification**: `O(m × n)` - character copy plus a recursion stack that can grow to the cell count for a snake-like island.
- **BFS with Grid Modification**: `O(m × n)` - the character copy dominates; the queue itself stays within the `O(min(m, n))` wavefront.
- **DFS with Separate Visited Array**: `O(m × n)` - the visited matrix plus recursion stack, with no character copy.
- **Iterative DFS with Stack**: `O(m × n)` - character copy plus an explicit stack that may hold all cells.
- **Union-Find**: `O(m × n)` - parent and rank arrays for every cell, with no copy.

### Trade-offs

- **DFS with Grid Modification**: the shortest expression of the idea and optimal in time, but it needs the character copy to mutate anything.
- **BFS with Grid Modification**: removes the recursion-depth hazard and keeps memory to the wavefront during the fill, at the cost of queue bookkeeping.
- **DFS with Separate Visited Array**: reads the immutable strings directly with no copy, and preserves the input, but pays for an explicit visited matrix.
- **Iterative DFS with Stack**: avoids recursion depth limits, but requires explicit stack management.
- **Union-Find**: no traversal and no input mutation, and it extends naturally to dynamic grids, but its implementation is the most involved.

### When to Use Each

- **DFS with Grid Modification (Recommended)**: best for interviews: simple, optimal, and demonstrates core graph traversal concepts.
- **BFS**: when memory during the fill matters or level-order exploration is needed.
- **DFS with Separate Visited Array**: when the input must be preserved or when avoiding the copy is worth the visited matrix.
- **Iterative DFS**: when dealing with very large grids where recursion depth might be an issue.
- **Union-Find**: for advanced scenarios with dynamic grid updates or connectivity queries.

### Optimization Notes

- DFS with Grid Modification is the recommended interview choice: it is optimal in time, simple to implement, and demonstrates core graph traversal cleanly.
- The immutable string rows force a design decision the classic list-of-lists version never faces: either copy the rows once (`cells`) or keep the mutation in a visited matrix. Both cost `O(m × n)` space, so the choice is about intent, not asymptotics.
- For very large grids, prefer BFS or Iterative DFS with Stack to avoid Python's recursion depth limit causing a stack overflow.
- A common pitfall is missing bounds checks before indexing neighbors; the direction array `[(0,1),(1,0),(0,-1),(-1,0)]` with explicit `0 <= row < rows` guards keeps the traversal safe.
