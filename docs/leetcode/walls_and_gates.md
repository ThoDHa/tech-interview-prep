# [Walls And Gates](https://leetcode.com/problems/walls-and-gates/)

**Medium** | **25 minutes** | **Array, Breadth-First Search, Matrix**

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/walls-and-gates/); read it free on [NeetCode](https://neetcode.io/problems/islands-and-treasure).

**Pattern:** [Multi-Source BFS](../patterns/grid_bfs_multi_source/intuition.md)

**Algorithm:** [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Flood fill](https://en.wikipedia.org/wiki/Flood_fill)

**Practice:** [`practice/walls_and_gates/solution.py`](../../practice/walls_and_gates/solution.py)

You are given a $m \times n$ 2D `grid` initialized with these three possible values:

1. `-1` - A water cell that *can not* be traversed.
2. `0` - A treasure chest.
3. `INF` - A land cell that *can* be traversed. We use the integer `2^31 - 1 = 2147483647` to represent `INF`.

Fill each land cell with the distance to its nearest treasure chest. If a land cell cannot reach a treasure chest then the value should remain `INF`.

Assume the grid can only be traversed up, down, left, or right.

Modify the `grid` **in-place**.

## Examples

### Example 1

**Input:**

```text
[
  [2147483647,-1,0,2147483647],
  [2147483647,2147483647,2147483647,-1],
  [2147483647,-1,2147483647,-1],
  [0,-1,2147483647,2147483647]
]
```

**Output:**

```text
[
  [3,-1,0,1],
  [2,2,1,-1],
  [1,-1,2,-1],
  [0,-1,3,4]
]
```

### Example 2

**Input:**

```text
[
  [0,-1],
  [2147483647,2147483647]
]
```

**Output:**

```text
[
  [0,-1],
  [1,2]
]
```

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 100`
- `grid[i][j]` is one of `{-1, 0, 2147483647}`

## Deriving the Solution

Each land cell needs the length of its shortest wall-avoiding walk to any chest, which is a shortest-path question on an unweighted grid: [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) territory. The design choices are where the search starts (one chest at a time, or all chests together) and what stops it (a visited set, or the `INF` value itself). Every solution below runs BFS along 4-directional steps; they differ in how many searches run and how much bookkeeping each carries.

1. **Start literal.** For each chest, BFS over the whole grid recording
   steps, and keep the minimum per cell: see
   [Per-Chest BFS](#per-chest-bfs).
2. **Spot the waste.** A cell near several chests is visited once per
   chest, and a chest whose wave cannot help anyone still floods the map.
3. **Start all chests at once.** One BFS seeded with every chest expands a
   single combined wavefront; the first wave to reach a land cell
   necessarily carries its nearest-chest distance, so a cell is written at
   most once and the `INF` value itself is the visited test: see
   [Multi-Source BFS](#multi-source-bfs).

## Solutions

### Per-Chest BFS

#### Derivation

The most literal reading computes, for each chest, the full distance map from that chest, then takes an element-wise minimum over the maps. Each map is a textbook BFS: step count 0 at the chest, +1 per 4-directional move, walls impassable:

1. Collect `chests`, the positions of every `0` cell.
2. For each chest, run a BFS carrying a fresh `dist` grid (`None` meaning
   unreached), stepping only through cells that are not walls.
3. Merge each finished map into the answer: for land cells
   (`grid[row][column] == INF`), keep the smallest distance seen; cells no
   chest reached stay `INF`.

#### Walkthrough

Trace Example 2: `grid = [[0, -1], [INF, INF]]`, one chest at `(0,0)`. Its BFS wavefront expands:

```text
dist start          [(0), None]      chest (0,0) at step 0
step 1              [(0), wall]      neighbors of (0,0): (1,0) reaches at 1, (0,1) is a wall
step 2              [(0), wall]      neighbors of (1,0): (1,1) reaches at 2, rest seen/wall
```

The merged map assigns `(1,0) = 1` and `(1,1) = 2`, giving `[[0, -1], [1, 2]]`, Example 2's expected Output. On Example 1 the two chest maps along column 0's rows 0-2 read `[4, 3, 4]` from chest `(0,2)` and `[3, 2, 1]` from chest `(3,0)`; cell `(1,1)` reads 2 from `(0,2)`'s map against 3 from `(3,0)`'s map, and the merge keeps 2, which is what the expected output shows.

#### Solution

The code is one BFS per chest plus the element-wise minimum merge.

```python
from collections import deque
from typing import List, Optional, Tuple

INF = 2147483647


class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        if not grid:
            return
        rows, columns = len(grid), len(grid[0])
        chests = [
            (row, column)
            for row in range(rows)
            for column in range(columns)
            if grid[row][column] == 0
        ]
        land = [
            (row, column)
            for row in range(rows)
            for column in range(columns)
            if grid[row][column] == INF
        ]

        def chest_distances(start: Tuple[int, int]) -> List[List[Optional[int]]]:
            dist = [[None] * columns for _ in range(rows)]
            dist[start[0]][start[1]] = 0
            queue = deque([start])
            while queue:
                row, column = queue.popleft()
                for next_row, next_column in (
                    (row + 1, column),
                    (row - 1, column),
                    (row, column + 1),
                    (row, column - 1),
                ):
                    if (
                        0 <= next_row < rows
                        and 0 <= next_column < columns
                        and dist[next_row][next_column] is None
                        and grid[next_row][next_column] != -1
                    ):
                        dist[next_row][next_column] = (
                            dist[row][column] + 1
                        )
                        queue.append((next_row, next_column))
            return dist

        for row, column in chests:
            dist = chest_distances((row, column))
            for r, c in land:
                if dist[r][c] is not None:
                    grid[r][c] = min(grid[r][c], dist[r][c])
```

The merge iterates a `land` list captured before any chest runs: testing `grid[r][c] == INF` during the loop instead would stop merging after the first chest writes a cell, and a nearer chest processed later could never lower the value.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(chests * rows * columns)`

Each chest's BFS floods up to the whole grid, and the merge is another full pass per chest.

##### Space Complexity: `O(rows * columns)`

One `dist` grid per BFS at a time (plus the queue).

#### Key Insights

- Correctness needs no cleverness: per-chest distances are independent and
  the minimum is taken explicitly.
- The waste is structural: a land cell between two chests is reached by
  both searches, and cells only near one chest still pay for every other
  chest's flood.

### Multi-Source BFS

#### Derivation

The per-chest version runs one search per chest and takes minima afterward. But the minimum over per-chest distances is exactly what a single BFS from all chests simultaneously computes: seed the queue with every chest at distance 0, and the wavefront advances one ring per step across the whole grid. The first wave to arrive at a land cell has traveled the shortest wall-avoiding path from its nearest chest, so the cell is written once and never revisited. Even better, the grid itself is the visited record: only cells still reading `INF` may be written, walls are never `INF`, and chest cells are never `INF`:

1. Enqueue every `0` cell (the chest cells) as the BFS's sources.
2. Pop a cell; for each neighbor still reading `INF`, write
   `grid[row][column] + 1` and enqueue it.
3. Stop when the queue drains; unreachable cells were never written and
   remain `INF`.

#### Walkthrough

Trace the merged wavefront on Example 2: `grid = [[0, -1], [INF, INF]]`. The queue starts with the single chest:

```text
seed     queue [(0,0)]                 grid [[0, -1], [INF, INF]]
pop (0,0)  d=0  neighbors: (1,0) is INF -> write 1, queue [(1,0)]
                (0,1) is -1, (-1,0) off-board, (0,-1) off-board
pop (1,0)  d=1  neighbors: (1,1) is INF -> write 2, queue [(1,1)]
                (0,0) is 0, (2,0) off-board
pop (1,1)  d=2  neighbors: (1,0) is 1, (0,1) is -1, rest off-board
queue empty
```

The grid reads `[[0, -1], [1, 2]]`, Example 2's expected Output. The "first wave wins" property is visible on Example 1's cell `(1,1)`: it sits at BFS distance 2 from `(0,2)` and 3 from `(3,0)`, so the `(0,2)`-side wave arrives first, writes 2, and the later wave reads a non-`INF` cell and moves on.

#### Solution

The code is the seeded queue and the `INF`-only write guard.

```python
from collections import deque
from typing import List

INF = 2147483647


class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        if not grid:
            return
        rows, columns = len(grid), len(grid[0])
        queue = deque()
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == 0:
                    queue.append((row, column))
        while queue:
            row, column = queue.popleft()
            for next_row, next_column in (
                (row + 1, column),
                (row - 1, column),
                (row, column + 1),
                (row, column - 1),
            ):
                if (
                    0 <= next_row < rows
                    and 0 <= next_column < columns
                    and grid[next_row][next_column] == INF
                ):
                    grid[next_row][next_column] = grid[row][column] + 1
                    queue.append((next_row, next_column))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * columns)`

Every cell enters the queue at most once (each write happens exactly once per cell), and each entry does constant work.

##### Space Complexity: `O(rows * columns)`

The queue holds one wavefront; on a fully open grid the wavefront is a diagonal ring at most `min(rows, columns) + 1` cells wide, and adversarial layouts push the peak toward the whole grid. The simple honest bound is linear in the grid's cells.

#### Key Insights

- Multi-source BFS computes "distance to the nearest source" in one pass:
  seeding all sources at distance 0 makes the wavefront itself do the
  minimization.
- The `INF` value doubles as the visited set; no auxiliary grid and no
  explicit distance array are needed, because distance is written exactly
  when the cell is first claimed.
- Unreachable land stays `INF` for free: nothing ever writes it.

## Comparison of Solutions

### Time Complexity

- **Per-Chest BFS**: `O(chests * rows * columns)` - one full flood per chest.
- **Multi-Source BFS**: `O(rows * columns)` - one combined flood.

### Space Complexity

- **Per-Chest BFS**: `O(rows * columns)` - one `dist` grid per BFS.
- **Multi-Source BFS**: `O(rows * columns)` - one wavefront queue.

### Trade-offs

- The per-chest scan re-writes cells and re-walks edges once per chest;
  with many chests it multiplies work that the multi-source version does
  once.
- The multi-source version needs the "all sources at once" insight but is
  the shorter code: no merge step, no auxiliary grid.

### When to Use Each

- **Per-Chest BFS**: when distances from one specific source are needed
  (queries like "how far from THIS chest?"), the per-source map is the
  reusable artifact.
- **Multi-Source BFS**: the intended solution whenever the answer is a
  nearest-source field; the same pattern solves rotting oranges and fire
  spread (recommended here).

### Optimization Notes

- The `INF`-only write guard also rejects walls (`-1`) and chests (`0`)
  without a separate wall test, which is why the code has no explicit
  `grid != -1` check.
- Chest cells are never re-enqueued: they read `0`, not `INF`, when the
  wavefront reaches them.
- The same idea floods inward from the border in
  [Surrounded Regions](surrounded_regions.md); here the wavefront carries
  distance, there it only carries reachability.
