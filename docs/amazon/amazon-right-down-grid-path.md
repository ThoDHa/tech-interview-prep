# [Path Through an O/X Grid Using Only Right and Down](https://www.fastprep.io/problems/amazon-right-down-grid-path)

**Medium** | **NN minutes** | **Array, Matrix, Dynamic Programming, Breadth First Search**

Given a rectangular array of strings grid, a zero-based coordinate source = [row, col], and a zero-based coordinate destination = [row, col], return whether the destination is reachable.

The character O is open and X is blocked. From an open cell you may move exactly one cell right or one cell down. A blocked endpoint is unreachable, and a destination above or left of the source is also unreachable.

## Examples

### Example 1

**Input:** `grid = ["OOO","OXO","OOO"]`, `source = [0,0]`, `destination = [2,2]`

**Output:** `true`

**Explanation:** Move right twice and then down twice while avoiding the center obstacle.

### Example 2

**Input:** `grid = ["OX","XO"]`, `source = [0,0]`, `destination = [1,1]`

**Output:** `false`

**Explanation:** Both first moves enter blocked cells.

### Example 3

**Input:** `grid = ["OOO"]`, `source = [0,2]`, `destination = [0,0]`

**Output:** `false`

**Explanation:** Reaching the destination would require moving left.

## Constraints

- `1 <= grid.length, grid[i].length <= 500.`
- `Every row has the same length, and the grid has at most 250000 cells.`
- `Every cell is O or X.`
- `source and destination each contain exactly two valid grid coordinates.`

## Solutions

### BFS from the Source

#### Derivation

The statement dresses the grid as a maze, so the most intuitive reading treats it as one:
the open cells are nodes, each open cell has directed edges to its right and down
neighbors, and the question is plain reachability. [Breadth-first
search](https://en.wikipedia.org/wiki/Breadth-first_search) answers reachability on any
graph without needing any property of the move set, which makes it the natural baseline;
the same framing drives the flood fills of
[Number of Islands](../leetcode/number_of_islands.md):

1. Read `start_row, start_col` from `source` and `target_row, target_col` from
   `destination`; return `False` immediately when either endpoint is blocked (`'X'`).
2. Mark the source cell in `visited` and seed `queue` with it.
3. Pop a cell; return `True` when it is the destination.
4. Otherwise inspect the two successors `next_row, next_col` (right, then down): enqueue
   each one that stays inside the grid, is open, and is unvisited, marking it visited at
   enqueue time.
5. When the queue drains without reaching the destination, return `False`.

Because moves only ever increase the row or the column, the search cannot cycle, and the
visited matrix only trims duplicate arrivals at the same cell.

#### Walkthrough

Trace the search on Example 1: `grid = ["OOO","OXO","OOO"]`, `source = [0,0]`,
`destination = [2,2]`. Each line is one dequeue, the successors that survive the filters,
and the queue that remains:

```text
seed (0,0)   visited = {(0,0)}                      queue = [(0,0)]
pop (0,0)    right (0,1) open, down (1,0) open      queue = [(0,1), (1,0)]
pop (0,1)    right (0,2) open, down (1,1) blocked   queue = [(1,0), (0,2)]
pop (1,0)    right (1,1) blocked, down (2,0) open   queue = [(0,2), (2,0)]
pop (0,2)    right out of grid, down (1,2) open     queue = [(2,0), (1,2)]
pop (2,0)    right (2,1) open, down out of grid     queue = [(1,2), (2,1)]
pop (1,2)    right out of grid, down (2,2) open     queue = [(2,1), (2,2)]
pop (2,1)    right (2,2) already visited            queue = [(2,2)]
pop (2,2)    equals the destination                 return True
```

The blocked center `(1,1)` deflects both frontier arms around it, and the destination
enters the queue from above via `(1,2)`. The dequeue of `(2,2)` returns `True`, matching
the expected Output; the path baked into that arrival is right, right, down, down, exactly
the route the example's explanation describes.

#### Solution

The code is the walkthrough's queue loop: seed the source, expand right and down, and
test the destination on dequeue.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[str], source: List[int], destination: List[int]) -> bool:
        rows, cols = len(grid), len(grid[0])
        start_row, start_col = source
        target_row, target_col = destination
        if grid[start_row][start_col] == 'X' or grid[target_row][target_col] == 'X':
            return False

        visited = [[False] * cols for _ in range(rows)]
        visited[start_row][start_col] = True
        queue = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            if (row, col) == (target_row, target_col):
                return True
            for next_row, next_col in ((row, col + 1), (row + 1, col)):
                if (next_row < rows and next_col < cols
                        and grid[next_row][next_col] == 'O'
                        and not visited[next_row][next_col]):
                    visited[next_row][next_col] = True
                    queue.append((next_row, next_col))

        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Every cell enters the queue at most once and does constant work when dequeued; the worst
case sweeps all `250000` cells the constraints allow.

##### Space Complexity: `O(rows × cols)`

The `visited` matrix holds one flag per cell, and the queue can hold a whole frontier of
open cells.

#### Key Insights

- Reachability needs no shortest-path bookkeeping: cells carry no distances, so a plain
  visited matrix suffices and the queue could even be a stack (DFS) without changing the
  answer.
- Directional moves buy cycle-freedom for free: no cell can revisit an ancestor of the
  current path, so the visited matrix only prevents duplicate queue entries.
- The baseline never uses the fact that both moves point the same general way; the next
  solution cashes that fact in.

### Dynamic Programming Sweep

#### Derivation

The queue treats the grid as a general graph, but right-and-down moves have a stronger
consequence than "no cycles": every path from the source stays inside the rectangle whose
opposite corners are the source and the destination, and inside that rectangle row-major
order agrees with move order. A cell is reachable exactly when it is open and at least one
of its two possible predecessors (the cell above, the cell to the left) is reachable, so
one ordered sweep computes reachability for the whole rectangle with no queue and no
recursion. The same one-directional transition underlies
[Unique Paths](../leetcode/unique_paths.md), which counts these paths instead of deciding
reachability:

1. Return `False` when the destination sits above or left of the source (outside the
   rectangle, so no path can exist) or when either endpoint is blocked.
2. Allocate `reachable`, a rolling row of `target_col + 1` booleans; it holds the
   previous sweep row's results and is updated in place.
3. Sweep `row` from `start_row` through `target_row` and `col` from `start_col` through
   `target_col`: set `reachable[col]` to true exactly when `grid[row][col] == 'O'` and
   (`is_source`, or `from_above` = `reachable[col]` before the update, or `from_left` =
   `reachable[col - 1]` after it).
4. After the sweep reaches `target_row`, return `reachable[target_col]`.

The in-place update works because the sweep reads `reachable[col]` (the cell above, from
the previous row) before writing it, and `reachable[col - 1]` (the cell to the left, from
the current row) after writing it.

#### Walkthrough

Trace the sweep on Example 1: `grid = ["OOO","OXO","OOO"]`, `source = [0,0]`,
`destination = [2,2]`. The rectangle is the whole grid; each line shows one sweep row and
the `reachable` row it leaves behind (`T` true, `F` false):

```text
row 0   (0,0) source, open      -> T   (0,1) from left  -> T   (0,2) from left  -> T   reachable = [T, T, T]
row 1   (1,0) from above, open  -> T   (1,1) blocked    -> F   (1,2) from above -> T   reachable = [T, F, T]
row 2   (2,0) from above, open  -> T   (2,1) from left  -> T   (2,2) from above -> T   reachable = [T, T, T]
```

Row 1 is the decisive one: the blocked center kills `(1,1)`, but `(1,2)` survives on its
above-neighbor `(0,2)` without needing the dead cell to its left, and row 2 then
re-enters column 1 through `(2,1)`'s left-neighbor `(2,0)`. After the last row,
`reachable[2]` is `True`, matching the expected Output. On Example 2 the same sweep ends
with `reachable = [F, F]` (both second-column routes hit an `X`), returning `False`, and
on Example 3 the destination-above-source guard returns `False` before any sweep.

#### Solution

The code is the rectangle sweep from the walkthrough: the rolling `reachable` row, the
three-way transition, and the final lookup.

```python
from typing import List


class Solution:
    def solve(self, grid: List[str], source: List[int], destination: List[int]) -> bool:
        start_row, start_col = source
        target_row, target_col = destination
        if (target_row < start_row or target_col < start_col
                or grid[start_row][start_col] == 'X'
                or grid[target_row][target_col] == 'X'):
            return False

        reachable = [False] * (target_col + 1)
        for row in range(start_row, target_row + 1):
            for col in range(start_col, target_col + 1):
                is_source = row == start_row and col == start_col
                from_above = row > start_row and reachable[col]
                from_left = col > start_col and reachable[col - 1]
                reachable[col] = grid[row][col] == 'O' and (is_source or from_above or from_left)
        return reachable[target_col]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

The sweep touches each cell of the source-to-destination rectangle once with constant
work; the rectangle is the full grid at worst, the same `250000`-cell bound.

##### Space Complexity: `O(cols)`

One boolean per swept column: the rolling row replaces the visited matrix and the queue
entirely.

#### Key Insights

- Right-and-down moves make row-major order a valid processing order, which converts
  reachability from a graph search into a single sweep; the queue disappears because the
  sweep order already respects every dependency.
- The rolling row is the payoff of processing order: only the previous row's results are
  ever read, so the `O(rows × cols)` visited matrix shrinks to one row.
- The sweep covers only the rectangle between source and destination, so a destination
  above or left of the source is rejected by the bounds guard instead of discovered
  absent the slow way.
- Reachability composes through OR (`from_above or from_left`) where path counting would
  add; the transition skeleton is shared with [Unique Paths](../leetcode/unique_paths.md).

## Comparison of Solutions

### Time Complexity

- **BFS from the Source**: `O(rows × cols)` - each cell is enqueued at most once and does
  constant work per dequeue.
- **Dynamic Programming Sweep**: `O(rows × cols)` - one constant-time transition per cell
  of the source-to-destination rectangle.

### Space Complexity

- **BFS from the Source**: `O(rows × cols)` - the visited matrix plus a queue of frontier
  cells.
- **Dynamic Programming Sweep**: `O(cols)` - one rolling boolean row.

### Trade-offs

- **BFS from the Source**: works for any move set (including up and left) without
  rederiving anything, but pays for a full visited matrix and queue bookkeeping.
- **Dynamic Programming Sweep**: exploits the one-directional move set to drop the queue
  and most of the bookkeeping, but the transition argument (row-major order respects move
  order) must be re-derived if the moves ever change.

### When to Use Each

- **BFS from the Source**: when the move set is richer than right-and-down, or as the
  first framing to confirm reachability is the right question.
- **Dynamic Programming Sweep (Recommended)**: for this problem as stated; it is the
  simplest correct code on the page and holds the smallest memory footprint.

### Optimization Notes

- The sweep reads each cell's above-neighbor before overwriting it and its left-neighbor
  after, which is what lets one row carry two rows' worth of state; getting that read
  order backwards silently corrupts the transition.
- The BFS dequeues the destination to recognize arrival; testing successors at enqueue
  time would return one level earlier at the cost of a duplicated check.
- Both solutions reject blocked endpoints up front; only the sweep needs the
  destination-above-source guard, because its rectangle argument requires the
  destination to be reachable in principle.
