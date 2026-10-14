# [Max Area of Island](https://leetcode.com/problems/max-area-of-island/)

**Medium** | **25 minutes** | **Array, Depth-First Search, Breadth-First Search, Union Find, Matrix**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md)

**Algorithm:** [Flood fill](https://en.wikipedia.org/wiki/Flood_fill) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/max_area_of_island/solution.py`](../../practice/max_area_of_island/solution.py)

You are given a matrix `grid` where `grid[i]` is either a `0` (representing water) or `1` (representing land).

An island is defined as a group of `1`'s connected horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

The **area** of an island is defined as the number of cells within the island.

Return the maximum **area** of an island in `grid`. If no island exists, return `0`.

## Examples

### Example 1

**Input:**

```text
grid = [
  [0,1,1,0,1],
  [1,0,1,0,1],
  [0,1,1,0,1],
  [0,1,0,0,1]
]
```

**Output:**

```text
6
```

**Explanation:** `1`'s cannot be connected diagonally, so the maximum area of the island is `6`.

## Constraints

- `1 <= grid.length, grid[i].length <= 50`

## Deriving the Solution

Each island is a connected component of the grid's land cells under 4-directional adjacency, so the problem is "measure every component, return the biggest measurement." Every solution below walks each component once and tracks the largest count; they differ in how the walk is driven and where the "already counted" information lives.

1. **Start literal.** Walk every land cell, carrying a separate `visited`
   grid, and count each component with a recursive flood fill: see
   [Recursive DFS](#recursive-dfs).
2. **Drop the ledger.** Marking a counted island by sinking its cells to
   water erases the bookkeeping: the grid itself records what was visited,
   no extra structure needed: see [Iterative BFS](#iterative-bfs).

## Solutions

### Recursive DFS

#### Derivation

The most direct reading asks, for each land cell not yet counted, "how big is the island here?" A flood fill answers it: one cell's island is that cell plus the fills of its land neighbors. Two mechanisms make the recursion total and terminating: a boundary/land check returns 0 for anything that is not an uncounted land cell, and every counted cell is sunk to `0` before recursing, so each cell contributes to exactly one fill. The outer scan tries a fill from every cell and keeps the maximum:

1. Scan all `(row, column)`; skip cells that are not `1`.
2. From a `1` cell, recurse: return 0 off-board or on water; otherwise set
   the cell to `0` and return `1 +` the sum of the four recursive calls.
3. Compare the fill's area against the running maximum.
4. Return the maximum after the scan.

Because sinking is destructive, the caller's grid is consumed; a non-destructive variant adds a `visited` grid and checks it alongside `grid[row][column] == 1`.

#### Walkthrough

Trace Example 1: `grid` has a six-cell island, `(0,1)`, `(0,2)`, `(1,2)`, `(2,1)`, `(2,2)`, `(3,1)`, a four-cell island down column 4, and the single cell `(1,0)`. The scan enters land first at `(0,1)`:

```text
fill(0,1)  1 -> 0   (1,1) is water, off-board up
  fill(0,2)  1 -> 0
    fill(1,2)  1 -> 0
      fill(2,2)  1 -> 0
        fill(2,1)  1 -> 0
          fill(3,1)  1 -> 0
            neighbors: (4,1) off-board, (2,1) sunk, (3,0)=0, (3,2)=0 -> stop
```

The deepest call returns first and the `1 +` sums unwind back up the chain, giving the fill `6`; no other island (the column-4 strip is size 4, `(1,0)` stands alone) exceeds it, so the answer is `6`, matching the expected Output.

#### Solution

The code is the scan driving the sinking fill.

```python
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        rows, columns = len(grid), len(grid[0])

        def sink_island(row: int, column: int) -> int:
            if not (0 <= row < rows and 0 <= column < columns):
                return 0
            if grid[row][column] != 1:
                return 0
            grid[row][column] = 0
            return (
                1
                + sink_island(row + 1, column)
                + sink_island(row - 1, column)
                + sink_island(row, column + 1)
                + sink_island(row, column - 1)
            )

        largest = 0
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == 1:
                    largest = max(largest, sink_island(row, column))
        return largest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * columns)`

Every cell is sunk at most once and the scan touches each cell once; each cell therefore does constant work across both passes.

##### Space Complexity: `O(rows * columns)`

The recursion depth is bounded by the largest island's size; a snake-shaped island filling the grid gives the worst case.

#### Key Insights

- Sinking turns the grid into its own `visited` set: a cell reads `1` if
  and only if it is uncounted land.
- The fill's guard order matters: bounds first, then land, then sink,
  or the recursion re-enters and overcounts.
- The `1 +` sum shape counts on the way out; an accumulating counter
  variable works identically.

### Iterative BFS

#### Derivation

The recursive fill spends its space budget on call frames, one per island cell. An explicit [queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) holds the same "cells of this island still to process" state on the heap, which survives a snake island that would exhaust Python's recursion limit; the algorithm is otherwise the sinking flood fill. This is [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search), but for counting purposes the frontier's order is irrelevant:

1. Scan for an unsunk `1` cell.
2. Sink it, put it on the `queue`, and start an `area` counter at 0.
3. Pop cells until the queue empties, adding 1 per pop and pushing each
   in-bounds, unsunk land neighbor (sunk at push time).
4. Fold `area` into the maximum and continue the scan.

Sinking at push time rather than pop time is what keeps a cell from
entering the queue twice.

#### Walkthrough

Trace the BFS on the six-cell island of Example 1, starting when the scan reaches `(0,1)`:

```text
dequeue (0,1)  area 1   push (0,2)            (1,1) is water, (0,0)=0
dequeue (0,2)  area 2   push (1,2)            (0,1) sunk, (0,3)=0
dequeue (1,2)  area 3   push (2,2)            (1,1)=0, (1,3)=0, (0,2) sunk
dequeue (2,2)  area 4   push (2,1)            (3,2)=0, (1,2) sunk, (2,3)=0
dequeue (2,1)  area 5   push (3,1)            (1,1)=0, (2,0)=0, (2,2) sunk
dequeue (3,1)  area 6   nothing               (4,1) off-board, (3,0)=0, (3,2)=0, (2,1) sunk
queue empty -> island area 6
```

The maximum over all islands stays `6`, matching the expected Output. Each cell was enqueued exactly once, at its first discovery.

#### Solution

The code is the scan driving the queue-based fill; `deque` makes the pops `O(1)`.

```python
from collections import deque
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        rows, columns = len(grid), len(grid[0])
        largest = 0
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] != 1:
                    continue
                grid[row][column] = 0
                queue = deque([(row, column)])
                area = 0
                while queue:
                    current_row, current_column = queue.popleft()
                    area += 1
                    for next_row, next_column in (
                        (current_row + 1, current_column),
                        (current_row - 1, current_column),
                        (current_row, current_column + 1),
                        (current_row, current_column - 1),
                    ):
                        if (
                            0 <= next_row < rows
                            and 0 <= next_column < columns
                            and grid[next_row][next_column] == 1
                        ):
                            grid[next_row][next_column] = 0
                            queue.append((next_row, next_column))
                largest = max(largest, area)
        return largest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * columns)`

Each cell is sunk and enqueued at most once, and the scan visits every cell once.

##### Space Complexity: `O(rows * columns)`

The queue holds one frontier wave; a spiral island one cell wide keeps the wave near the grid's smaller dimension, while a compact blob's frontier spans its full width. The safe general bound is linear in the island's size (a measured 50 x 50 spiral peaks at a 50-entry queue; other shapes peak higher, never past the island's cell count).

#### Key Insights

- The queue swaps recursion depth for heap memory: same visit order
  guarantees, no recursion-limit risk on deep islands.
- Sink-on-push is the duplicate guard; sinking on pop would let a cell
  with two discovered neighbors enqueue twice and double-count. (Sinking
  is one-way here: the grid is consumed, not restored.)
- For counting areas the BFS/DFS distinction changes only the frontier
  order, never the total.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(rows * columns)` - every cell is processed a constant number of times.
- **Iterative BFS**: `O(rows * columns)` - same visit guarantee with an explicit queue.

### Space Complexity

- **Recursive DFS**: `O(rows * columns)` - recursion depth up to the largest island's area.
- **Iterative BFS**: `O(rows * columns)` - the frontier queue, bounded by the island's cell count.

### Trade-offs

- The recursive DFS is the shortest and clearest; it dies to Python's
  recursion limit (default 1000) on islands larger than that.
- The iterative BFS handles any island size and, because each island is
  fully sunk before the scan moves on, keeps the per-island counting
  logic in one flat loop instead of nested recursion; it costs the
  deque import and the frontier loop. Its peak queue can exceed the
  DFS's average stack depth on blob-shaped islands, but it never hits
  a hard limit.

### When to Use Each

- **Recursive DFS**: boards at these constraints (at most 50 x 50 = 2500
  cells fit the recursion limit with headroom) and interview sketches
  (recommended here).
- **Iterative BFS**: production grids of unbounded size, and any language
  or setting where deep recursion is a hazard.

### Optimization Notes

- The sinking variants destroy the input; pass a copy when the caller
  needs the grid back.
- A union-find variant processes the grid edge by edge without any
  frontier at all, at the price of far more code for the same bounds.
- Counting on the way out (`return 1 + ...`) versus accumulating in an
  outer variable is purely stylistic; both visit identically.
