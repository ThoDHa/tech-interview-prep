# [Max Area of Island](https://www.fastprep.io/problems/amazon-max-area-of-island)

**Medium** | **NN minutes** | **Matrix, Graph, Depth First Search, Breadth First Search**

Given a binary matrix grid, return the maximum area of an island.

## Examples

### Example 1

**Input:** `grid = [[0,0,1,0],[1,1,1,0],[0,1,0,1]]`

**Output:** `5`

**Explanation:** The center component has five orthogonally connected land cells. The lower-right cell is separate.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-max-area-of-island; fill them in. -->

## Solutions

### Recursive DFS with Grid Modification

#### Derivation

The literal question is "how big is the biggest connected patch of `1` cells?", and the direct way to answer it is to measure each patch and keep the maximum. Reading the matrix as an implicit graph, where each `1` cell is a node and orthogonally adjacent `1` cells share an edge, every patch is a connected component, and [DFS](https://en.wikipedia.org/wiki/Depth-first_search) visits exactly one component per start cell, counting the cells it sinks along the way. Sinking each visited cell to `0` turns the grid itself into the visited marker, so the fill both measures and erases the component:

1. Scan every cell with a double loop over `rows` and `cols`.
2. When `grid[row][col] == 1`, a not-yet-counted island starts there: call
   `dfs(row, col)` and compare its returned cell count with `largest_area`.
3. `dfs` returns `0` when the cell is out of bounds or already `0`; otherwise it
   sinks the cell (`grid[row][col] = 0`) and returns `1` plus the four recursive
   results over the neighbors from `directions` (right, down, left, up).
4. After the scan completes, return `largest_area`.

#### Walkthrough

The single island in Example 1 spans five cells, and tracing all of them would be long, so we use a smaller tailored grid with one large and one small island:

```text
grid = [
  [1, 1, 0],
  [1, 0, 1],
]
```

The main loop scans in row-major order and starts a fill at every `1` it finds; the fill sinks each visited cell so no cell is measured twice:

```text
scan (0,0)  '1' -> dfs(0,0) sinks (0,0),(0,1),(1,0), returns 3   largest_area = 3
scan (0,1)   0  -> sunk by the fill, skip
scan (0,2)   0  -> water, skip
scan (1,0)   0  -> sunk by the fill, skip
scan (1,1)   0  -> water, skip
scan (1,2)  '1' -> dfs(1,2) sinks (1,2), returns 1               largest_area stays 3
```

Inside `dfs(0, 0)` the recursion explores neighbors in the order right, down, left, up: `(0,1)` sinks first, then `(1,0)` from its downward branch, and each call contributes `1` to its parent's sum, so `dfs(0,0)` returns `1 + (1 + 0 + 0 + 0) + (1 + 0 + 0 + 0) = 3`. The scan ends with `largest_area = 3`, the larger island's size.

The same procedure on Example 1 returns `5`: the center component contributes five cells and the lone lower-right cell contributes one, matching the expected Output of `5`.

#### Solution

The code is the walkthrough's scan and counting fill: the main loop seeds each island and `dfs` returns the number of cells it sinks.

```python
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        largest_area = 0

        def dfs(row: int, col: int) -> int:
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                grid[row][col] == 0):
                return 0

            grid[row][col] = 0

            area = 1
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for row_offset, col_offset in directions:
                area += dfs(row + row_offset, col + col_offset)
            return area

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    island_area = dfs(row, col)
                    if island_area > largest_area:
                        largest_area = island_area

        return largest_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Each cell is sunk at most once, so the total work across all fills is one visit per cell plus the constant-time scan around it.

##### Space Complexity: `O(rows × cols)`

The recursion can descend once per cell of a snake-shaped island, so the call stack may hold all cells in the worst case.

#### Key Insights

- Counting during the fill turns the island-numbering pattern into an area measure: the only change from a flood fill is the return value `1 + sum of neighbors`.
- Sinking visited cells to `0` doubles as the visited marker, so no extra matrix is needed.
- A lone cell is still an island of area `1`, which is why the lower-right cell in Example 1 cannot lower the answer even though the center component dominates.

### BFS with Grid Modification

#### Derivation

The recursive fill's memory is the call stack, and on a snake-shaped island it can grow to the full cell count, deep enough to threaten the interpreter's recursion limit. The repair changes the exploration order rather than the algorithm: expand the island as a widening frontier with a [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) queue, which holds only the current wavefront, and count the cells as they are enqueued. The queue needs an explicit area accumulator because, unlike the recursion, it returns no per-cell sums:

1. The main scan is unchanged: every `1` starts one fill, now `bfs(row, col)`.
2. `bfs` sinks the seed, enqueues it, and sets `area = 0`.
3. While the queue is non-empty, `popleft` a cell, add `1` to `area`, and enqueue
   every in-bounds neighbor still holding `1`, sinking it at enqueue time.
4. Return `area` and keep the maximum in `largest_area`.

Sinking at enqueue time guarantees no cell enters the queue twice, so `area` counts each cell exactly once.

#### Walkthrough

Let us measure the center island of Example 1 by hand. The grid is `[[0,0,1,0],[1,1,1,0],[0,1,0,1]]`; the scan starts at `(0, 2)` and each line is one queue event, with neighbors checked in the order right, down, left, up:

```text
seed (0,2)    sink, queue = [(0,2)], area = 0
pop (0,2)     area = 1   right (0,3) water; down (1,2) '1' -> sink+enqueue
              left (0,1) water; up out of bounds       queue = [(1,2)]
pop (1,2)     area = 2   right (1,3) water; down (2,2) water
              left (1,1) '1' -> sink+enqueue; up (0,2) sunk
              queue = [(1,1)]
pop (1,1)     area = 3   right (1,2) sunk; down (2,1) '1' -> sink+enqueue
              left (1,0) '1' -> sink+enqueue; up (0,1) water
              queue = [(2,1), (1,0)]
pop (2,1)     area = 4   all neighbors water, sunk, or out of bounds
              queue = [(1,0)]
pop (1,0)     area = 5   right (1,1) sunk; down (2,0) water
              left out of bounds; up (0,0) water
              queue = []  -> bfs returns 5
```

The fill sinks exactly the five orthogonally connected cells `(0,2), (1,2), (1,1), (2,1), (1,0)` and returns `5`. The scan then finds `(2, 3)`, whose fill returns `1`, so `largest_area` stays `5`, matching the expected Output for Example 1.

#### Solution

The code is the queue discipline from the walkthrough: sink at enqueue time, count at dequeue time.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        largest_area = 0

        def bfs(start_row: int, start_col: int) -> int:
            queue = deque([(start_row, start_col)])
            grid[start_row][start_col] = 0
            area = 0

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            while queue:
                row, col = queue.popleft()
                area += 1

                for row_offset, col_offset in directions:
                    new_row, new_col = row + row_offset, col + col_offset
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                        grid[new_row][new_col] == 1):
                        grid[new_row][new_col] = 0
                        queue.append((new_row, new_col))

            return area

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    island_area = bfs(row, col)
                    if island_area > largest_area:
                        largest_area = island_area

        return largest_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Each cell is enqueued at most once because it is sunk before entering the queue, so the fills touch every cell a constant number of times.

##### Space Complexity: `O(min(rows, cols))`

The queue holds one wavefront of the island at a time, and a rectangular wavefront never exceeds the shorter grid dimension.

#### Key Insights

- Sinking at enqueue time, not dequeue time, is what keeps `area` honest: a cell cannot be counted or enqueued twice.
- The explicit accumulator replaces the recursion's return-value plumbing, and the answer comes from counting dequeues rather than summing returns.
- Bounding memory by the wavefront instead of the longest path sidesteps the recursion limit on large grids.

### Iterative DFS with Explicit Stack

#### Derivation

The BFS queue fixes the recursion-depth risk by changing the container, and the same fix works while keeping the depth-first order: DFS needs *some* to-do list of cells, and an explicit list used as a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) is one the interpreter's recursion limit cannot touch. Pushing all four neighbors and validating them on pop keeps the inner loop minimal, at the cost of stacking cells that later get discarded:

1. `iterative_dfs` seeds `stack` with the starting cell and starts `area = 0`.
2. While the stack is non-empty, `pop` a cell and skip it when it is out of
   bounds or `0` (water or already sunk).
3. Otherwise add `1` to `area`, sink the cell, and push all four neighbors
   unconditionally.
4. The main scan compares each fill's `area` with `largest_area` as before.

#### Walkthrough

We reuse the tailored two-island grid from the recursive walkthrough, `grid = [[1,1,0],[1,0,1]]`, so the pop order can be compared with the recursion on the same input. The scan starts at `(0, 0)`; each line is one pop:

```text
seed (0,0)    area = 0, stack = [(0,0)]
pop (0,0)     '1' -> area = 1, sink, push   stack = [(0,1), (1,0), (0,-1), (-1,0)]
pop (-1,0)    out of bounds -> skip
pop (0,-1)    out of bounds -> skip
pop (1,0)     '1' -> area = 2, sink, push   stack = [(0,1), (1,1), (2,0), (1,-1), (0,0)]
pop (0,0)     already 0 -> skip             (duplicate entry, guard rejects it)
pop (1,-1)    out of bounds -> skip
pop (2,0)     out of bounds -> skip
pop (1,1)     water -> skip
pop (0,1)     '1' -> area = 3, sink, push   stack = [(0,2), (1,1), (0,0), (-1,1)]
pop (-1,1)    out of bounds -> skip
pop (0,0)     already 0 -> skip
pop (1,1)     water -> skip
pop (0,2)     water -> skip                 stack = [] -> fill returns 3
```

Because the stack is LIFO and neighbors are pushed right, down, left, up, the sink order is `(0,0), (1,0), (0,1)`, different from the recursive order `(0,0), (0,1), (1,0)`, which changes nothing about the count: `area` is `3` either way. The scan then finds `(1, 2)`, whose fill returns `1`, and the function returns `largest_area = 3`.

#### Solution

The code is the pop, guard, count, push loop from the walkthrough, wrapped in the usual scan.

```python
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        largest_area = 0

        def iterative_dfs(start_row: int, start_col: int) -> int:
            stack = [(start_row, start_col)]
            area = 0

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            while stack:
                row, col = stack.pop()

                if (row < 0 or row >= rows or
                    col < 0 or col >= cols or
                    grid[row][col] == 0):
                    continue

                area += 1
                grid[row][col] = 0

                for row_offset, col_offset in directions:
                    stack.append((row + row_offset, col + col_offset))

            return area

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    island_area = iterative_dfs(row, col)
                    if island_area > largest_area:
                        largest_area = island_area

        return largest_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Each land cell is counted exactly once, and the duplicate stack entries it generates are discarded by the guard in constant time.

##### Space Complexity: `O(rows × cols)`

The explicit stack can hold every cell of a snake-shaped island, duplicated entries included.

#### Key Insights

- The explicit stack replaces the interpreter's call stack, so the fill cannot hit the recursion limit on a large grid.
- Counting at pop time (after the guard) is what keeps `area` exact despite cells entering the stack multiple times.
- Pushing invalid neighbors and filtering them on pop trades a wider stack for a simpler inner loop; pre-validating each push would shrink the stack at the cost of a longer push condition.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS with Grid Modification**: `O(rows × cols)` - each cell is sunk at most once across the scan and the fills.
- **BFS with Grid Modification**: `O(rows × cols)` - sinking at enqueue time caps each cell at one queue entry.
- **Iterative DFS with Explicit Stack**: `O(rows × cols)` - each land cell is counted once and duplicate pops are discarded in constant time.

### Space Complexity

- **Recursive DFS with Grid Modification**: `O(rows × cols)` - the call stack can descend once per cell of a snake-shaped island.
- **BFS with Grid Modification**: `O(min(rows, cols))` - the queue holds a single wavefront, bounded by the shorter grid dimension.
- **Iterative DFS with Explicit Stack**: `O(rows × cols)` - the explicit stack can hold every cell, duplicated entries included.

### Trade-offs

- Recursive DFS with Grid Modification is the shortest to write and carries no auxiliary structure, but it mutates the grid and its depth is bounded only by the interpreter's recursion limit.
- BFS with Grid Modification bounds peak memory by the wavefront and removes the recursion risk, at the cost of an explicit accumulator and queue management.
- Iterative DFS with Explicit Stack keeps the depth-first order without any recursion, paying for it with duplicate stack entries and a pop-time guard.

### When to Use Each

- **Recursive DFS with Grid Modification (Recommended)**: The interview default: it is optimal in time, brief, and easy to explain.
- **BFS with Grid Modification**: When the grid is large enough that recursion depth is a real hazard, or when level-by-level expansion is useful for extensions such as distance queries.
- **Iterative DFS with Explicit Stack**: When the depth-first order itself matters and the recursion limit rules out the recursive form.

### Optimization Notes

- The recursion's `1 + sum of recursive results` counts cells on the way back up, while the queue and stack versions count with a local `area`; both produce the same total because each cell is admitted exactly once.
- The grid sink is the visited marker in all three fills; when the caller needs the grid intact, move the marks into a parallel boolean matrix at `O(rows × cols)` extra space.
- A common pitfall is counting at enqueue time in the BFS while also counting at dequeue time; sink at enqueue, but count at dequeue, or count only where the guard has admitted the cell.
