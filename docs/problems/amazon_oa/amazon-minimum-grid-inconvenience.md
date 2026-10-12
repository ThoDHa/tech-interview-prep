# [Minimum Grid Inconvenience](https://www.fastprep.io/problems/amazon-minimum-grid-inconvenience)

**Hard** | **NN minutes** | **Matrix, Breadth First Search, Binary Search**

A city is represented by a binary grid. A cell marked 1 is a delivery center, and a cell marked 0 is any other place.

The distance between two cells is the maximum of the absolute row-coordinate difference and the absolute column-coordinate difference. The inconvenience of the grid is the maximum, over every 0 cell, of its distance to the nearest delivery center.

Amazon may open one new delivery center by converting at most one 0 cell into 1. Return the minimum possible inconvenience after this conversion.

## Examples

### Example 1

**Input:** `grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]`

**Output:** `2`

**Explanation:** With no existing delivery center, it is optimal to convert the center cell (1,1) to 1. The farthest cells then have distance 2.

### Example 2

**Input:** `grid = [[0]]`

**Output:** `0`

**Explanation:** Convert the only cell to a delivery center, leaving no 0 cell with positive distance.

## Constraints

- `1 <= n, m <= 500`
- `0 <= grid[i][j] <= 1`

## Solutions

### BFS Distance Field with Conversion Trials

#### Derivation

The inconvenience is a max over 0 cells of a distance to the nearest delivery center, so the natural first question is: what is that distance for every cell at once? A [multi-source BFS](https://en.wikipedia.org/wiki/Breadth-first_search) seeded with all existing centers answers it in one sweep. One detail decides the move set: the distance here is the maximum of the absolute row difference and the absolute column difference, which is the [Chebyshev distance](https://en.wikipedia.org/wiki/Chebyshev_distance), not the rook-move distance a four-neighbor BFS would count. A king that may step to all eight neighbors needs exactly `max(|row_a - row_b|, |col_a - col_b|)` moves between two cells, so an eight-direction BFS counts the right quantity.

With the distance field in hand, the conversion itself is tried honestly: convert each 0 cell in turn, rescan the grid, and keep the best result. Cells with no center at all fit the same machinery by seeding the field with a sentinel larger than any possible distance:

1. Seed a multi-source king-move BFS from every `grid[row][col] == 1` cell at
   distance `0`; unreached cells keep the sentinel `unreached = rows + cols`.
2. The do-nothing baseline is the max of `distance` over all 0 cells (`0` when
   there are none).
3. For each candidate 0 cell `(cell_row, cell_col)`, scan every other 0 cell
   and compute `min(distance[row][col], max(|row - cell_row|,
   |col - cell_col|))`: the distance after the conversion. The candidate cell
   itself is skipped because it becomes a center.
4. The trial's value is the max of that expression over all other 0 cells;
   return the minimum over all trials and the do-nothing baseline.

#### Walkthrough

Example 1, `grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]`, has no existing center, so the field stays at the sentinel `rows + cols = 7` everywhere and every conversion is judged purely on Chebyshev spread. The do-nothing baseline is the sentinel, and the trials decide:

| Candidate | Farthest other cell | Chebyshev distance | Trial value |
| --- | --- | --- | --- |
| `(0, 0)` | `(2, 3)` | `max(2, 3)` | `3` |
| `(0, 1)` | `(2, 3)` | `max(2, 2)` | `2` |
| `(1, 1)` | `(0, 3)` or `(2, 3)` | `max(1, 2)` | `2` |
| `(1, 2)` | `(0, 0)` or `(2, 0)` | `max(1, 2)` | `2` |

No placement beats distance `2`: a single center in a 3 × 4 grid is always at least `2` king-moves from some corner. The minimum trial value is `2`, which is the returned answer and matches the expected Output. On Example 2, `grid = [[0]]`, the only candidate is the only cell, the trial scan skips it and finds no other 0 cells, so the trial value is `0` and the answer is `0`.

#### Solution

The code is the field sweep followed by the trial loop: `inconvenience_with_new_center` is the rescan of step 3.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        unreached = rows + cols

        distance = [[unreached] * cols for _ in range(rows)]
        queue = deque()
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    distance[row][col] = 0
                    queue.append((row, col))

        king_directions = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)]
        while queue:
            row, col = queue.popleft()
            for row_step, col_step in king_directions:
                next_row, next_col = row + row_step, col + col_step
                if (0 <= next_row < rows and 0 <= next_col < cols
                        and distance[next_row][next_col] == unreached):
                    distance[next_row][next_col] = distance[row][col] + 1
                    queue.append((next_row, next_col))

        def inconvenience_with_new_center(cell_row: int,
                                          cell_col: int) -> int:
            farthest = 0
            for row in range(rows):
                for col in range(cols):
                    if row == cell_row and col == cell_col:
                        continue
                    to_new_center = max(abs(row - cell_row),
                                        abs(col - cell_col))
                    farthest = max(farthest,
                                   min(distance[row][col], to_new_center))
            return farthest

        best = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    best = max(best, distance[row][col])

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    best = min(best,
                               inconvenience_with_new_center(row, col))
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m × n)^2)`

The BFS builds the field in `O(m × n)`, and each of the up to `m × n` conversion trials rescans all `m × n` cells.

##### Space Complexity: `O(m × n)`

The distance field plus the BFS queue.

#### Key Insights

- The distance in this problem is Chebyshev, so the BFS must move like a chess king: four-neighbor BFS silently computes a different metric and wrong answers.
- Seeding the field with a sentinel instead of special-casing "no centers" lets one trial loop serve both the all-zero grid and grids with existing centers.
- Skipping the candidate cell in the rescan encodes "the converted cell is no longer a 0 cell"; forgetting that skip overcounts by the candidate's own distance.

### Binary Search on the Answer

#### Derivation

The trials repeat one expensive question per candidate: how far does this conversion's benefit reach? Flip the question. Instead of asking what a chosen center achieves, ask what a target inconvenience `limit` demands: which placements make every 0 cell sit within `limit` of some center? A cell whose field distance already satisfies `distance[row][col] <= limit` is covered no matter where the new center goes. Every remaining cell forces the new center into its Chebyshev ball of radius `limit`, and a Chebyshev ball is an axis-aligned square, `rows` in `[row - limit, row + limit]` and `cols` in `[col - limit, col + limit]`. The intersection of axis-aligned squares is computed from running bounds: `row_low = max(row - limit)`, `row_high = min(row + limit)`, and the same for `cols`. A placement exists exactly when `row_low <= row_high` and `col_low <= col_high`.

Feasibility is monotone: a `limit` that works for one placement works for `limit + 1` with the same placement, because raising `limit` only shrinks the violated set and widens every square. That monotonicity is a binary search invitation. The search bounds run from `0` to the sentinel, which no answer can reach on a non-empty grid:

1. Build the same king-move BFS distance field.
2. `conversion_covers_all(limit)` intersects the radius-`limit` squares of all
   cells with `distance > limit`, starting the bounds at the full grid, and
   reports whether the intersection is non-empty.
3. Binary search the smallest feasible `limit` over `[0, unreached]` and return
   it.

#### Walkthrough

Example 1 again, the 3 × 4 all-zero grid where every cell keeps the sentinel distance. The search runs `low = 0`, `high = 7`:

```text
middle = 3   violated: all cells   row_low = max(0,-3,-2,-1) = 0  row_high = min(2,3,4,5) = 2
                                   col_low = max(0,-3,-2,-1) = 0  col_high = min(3,3,4,5) = 3
                                   0 <= 2 and 0 <= 3 -> feasible        high = 3
middle = 1   violated: all cells   row_low = max(0,-1, 0, 1) = 1  row_high = min(2,1,2,3) = 1
                                   col_low = max(0,-1, 0, 1) = 2  col_high = min(3,1,2,3) = 1
                                   2 > 1 -> no square remains           low  = 2
middle = 2   violated: all cells   row_low = max(0,-2,-1, 0) = 0  row_high = min(2,2,3,4) = 2
                                   col_low = max(0,-2,-1, 0) = 1  col_high = min(3,2,3,4) = 2
                                   0 <= 2 and 1 <= 2 -> feasible        high = 2
low == high == 2 -> return 2
```

The `middle = 1` step is the telling one: the corner cells `(0, 0)` and `(2, 3)` alone already conflict, because the first confines the center to columns at most `0 + 1 = 1` while the second demands columns at least `3 - 1 = 2`, so no cell can serve both corners within distance `1`. At `middle = 2` the square `[1, 2] × [0, 2]` survives, and the center `(1, 1)` or `(1, 2)` inside it reproduces the walkthrough of the trial approach. On Example 2, `grid = [[0]]`, the first probe `middle = 3` clamps all four bounds to the single cell and is feasible, then `middle = 1`, `middle = 0` also come out feasible, and the search returns `0`.

#### Solution

The code is the same field sweep with the trial loop replaced by the feasibility probe and the binary search over it.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        unreached = rows + cols

        distance = [[unreached] * cols for _ in range(rows)]
        queue = deque()
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    distance[row][col] = 0
                    queue.append((row, col))

        king_directions = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)]
        while queue:
            row, col = queue.popleft()
            for row_step, col_step in king_directions:
                next_row, next_col = row + row_step, col + col_step
                if (0 <= next_row < rows and 0 <= next_col < cols
                        and distance[next_row][next_col] == unreached):
                    distance[next_row][next_col] = distance[row][col] + 1
                    queue.append((next_row, next_col))

        def conversion_covers_all(limit: int) -> bool:
            row_low, row_high = 0, rows - 1
            col_low, col_high = 0, cols - 1
            for row in range(rows):
                for col in range(cols):
                    if distance[row][col] <= limit:
                        continue
                    row_low = max(row_low, row - limit)
                    row_high = min(row_high, row + limit)
                    col_low = max(col_low, col - limit)
                    col_high = min(col_high, col + limit)
            return row_low <= row_high and col_low <= col_high

        low, high = 0, unreached
        while low < high:
            middle = (low + high) // 2
            if conversion_covers_all(middle):
                high = middle
            else:
                low = middle + 1
        return low
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × log(m × n))`

The field costs `O(m × n)`, and the binary search performs `O(log(m × n))` feasibility probes, each an `O(m × n)` scan of the field.

##### Space Complexity: `O(m × n)`

The distance field plus the BFS queue; the feasibility probe keeps only four running bounds.

#### Key Insights

- Inverting "pick a center" into "test a target" converts a quadratic enumeration into a logarithmic search over a monotone predicate.
- A Chebyshev ball is an axis-aligned square, so intersecting every violated cell's requirement is four running bounds, not a geometric construction.
- A non-empty intersection square always contains a real grid cell: `row_low <= rows - 1` because the largest violated row minus `limit` never passes the last row, and `row_high >= 0` for the mirror reason, so the clamped bounds stay ordered whenever the raw ones are.
- The sentinel `rows + cols` exceeds every true distance (`max(rows - 1, cols - 1)`) and every feasible `limit` the search probes, so unseeded grids need no special case.

## Comparison of Solutions

### Time Complexity

- **BFS Distance Field with Conversion Trials**: `O((m × n)^2)` - one full-grid rescan per conversion candidate on top of one `O(m × n)` field sweep.
- **Binary Search on the Answer**: `O(m × n × log(m × n))` - one full-grid scan per feasibility probe, `O(log(m × n))` probes.

### Space Complexity

- **BFS Distance Field with Conversion Trials**: `O(m × n)` - the distance field dominates.
- **Binary Search on the Answer**: `O(m × n)` - the same field, with only four scalar bounds per probe.

### Trade-offs

- The trial scan states the optimization directly and needs no insight beyond the metric, but its cost squares the cell count and gives up at `500 × 500` grids.
- The binary search adds one layer of indirection (the feasibility predicate) and pays for it with a logarithmic factor instead of a linear one: roughly 18 scans of the grid instead of 250,000 at the constraint ceiling.

### When to Use Each

- **BFS Distance Field with Conversion Trials**: as the interview baseline, or on tiny grids where the constant of the search machinery is not worth it.
- **Binary Search on the Answer (Recommended)**: whenever the grid can be large; the predicate is simple enough to state and the asymptotics win decisively.

### Optimization Notes

- Both solutions share the same king-move field; write it once and re-derive the second solution from the first in an interview.
- The feasibility probe scans every cell each time; it could instead walk only cells with `distance` above a threshold if the field were bucketed by distance, but the plain scan is already fast enough for the stated bounds.
- The column of the optimal placement is never materialized: the bounds prove existence, and recovering a concrete `(row, col)` would take one more pass inside the final feasible square.

