# [Shortest Grid Path With One Wall Break](https://www.fastprep.io/problems/amazon-shortest-grid-path-with-one-wall-break)

**Medium** | **NN minutes** | **Matrix, Breadth First Search, Shortest Path**

Given a rectangular binary matrix grid, a cell containing 1 is open and a cell containing 0 is a wall.

Start at the top-left cell and move to the bottom-right cell. Each move goes one cell up, down, left, or right. During the route, you may break and enter at most one wall.

Return the minimum number of moves needed to reach the destination, or -1 when no valid route exists.

## Examples

### Example 1

**Input:** `grid = [[1,0,1],[0,0,1],[1,1,1]]`

**Output:** `4`

**Explanation:** Break the wall at (0,1), then move through (0,2) and (1,2) to reach (2,2) in four moves.

### Example 2

**Input:** `grid = [[1,0,1],[0,0,0],[1,0,1]]`

**Output:** `-1`

**Explanation:** Every route from the start to the destination would enter at least two wall cells, so one wall break is insufficient.

### Example 3

**Input:** `grid = [[1]]`

**Output:** `0`

**Explanation:** The start is already the destination, so no move is needed.

## Constraints

- `1 <= grid.length <= 200`
- `1 <= grid[i].length <= 200`
- `Every row has the same length.`
- `grid[i][j] is either 0 or 1.`
- `The top-left and bottom-right cells contain 1.`

## Solutions

### Break One Wall, Then Plain BFS

#### Derivation

"The route may break at most one wall" reads most literally as: pick the wall to break (or none), then solve the ordinary shortest path on the opened grid. With walls enumerated, each attempt is a plain breadth-first search where the chosen wall cell behaves as open:

1. Run plain BFS with no break; keep the distance.
2. For every wall cell, run plain BFS treating that cell as open.
3. Return the smallest distance found, or `-1` when every attempt fails.

#### Walkthrough

Example 1, `grid = [[1,0,1],[0,0,1],[1,1,1]]`: with no break, the start `(0,0)` is enclosed by walls at `(0,1)` and `(1,0)`, unreachable. Breaking `(0,1)` opens the route `(0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)`: four moves, the expected output. Breaking `(1,0)` instead reaches `(2,0) -> (2,1) -> (2,2)` in five, so the best break wins with `4`. Example 2's grid separates every corner region by two or more wall entries from the destination, so all attempts fail and the answer is `-1`; Example 3 starts on the destination with zero moves.

#### Solution

```python
from collections import deque
from typing import List, Optional, Tuple


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        """Return the shortest start-to-end moves with at most one wall break.

        Time:  O(w * n * m) with w the wall count; worst case O((n * m)^2).
        Space: O(n * m) per BFS.
        """
        rows, columns = len(grid), len(grid[0])

        def bfs(broken: Optional[Tuple[int, int]]) -> int:
            distance = {(0, 0): 0}
            frontier = deque([(0, 0)])
            while frontier:
                row, column = frontier.popleft()
                if (row, column) == (rows - 1, columns - 1):
                    return distance[(row, column)]
                for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    next_row, next_column = row + row_step, column + column_step
                    if (
                        0 <= next_row < rows
                        and 0 <= next_column < columns
                        and (next_row, next_column) not in distance
                        and (
                            grid[next_row][next_column] == 1
                            or (next_row, next_column) == broken
                        )
                    ):
                        distance[(next_row, next_column)] = distance[(row, column)] + 1
                        frontier.append((next_row, next_column))
            return -1

        best = bfs(None)
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == 0:
                    attempt = bfs((row, column))
                    if attempt != -1:
                        best = attempt if best == -1 else min(best, attempt)
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(w * n * m)`

One BFS per wall (plus one unbroken), each `O(n * m)`.

##### Space Complexity: `O(n * m)`

One distance map per attempt.

#### Key Insights

- Enumerating the break externalizes the decision, leaving each attempt a textbook BFS.
- The wall count can approach `n * m`, which is what motivates folding the choice into the state.

### One BFS With a Broken-Flag State

#### Derivation

The wasted work above is recomputing everything per candidate wall. The alternative carries the choice inside the search state: `(row, column, used)` where `used` records whether the single break is already spent. Entering an open cell keeps `used` unchanged; entering a wall cell is allowed exactly once, from `used = 0`, and flips it to `1`. The state graph has `2 * n * m` nodes, BFS on it is optimal per state, and the first arrival at the destination in either flag is the answer:

1. Seed the queue with `(0, 0, used)` where `used` is `1` exactly when the start itself is a wall (entering it spends the break).
2. Expand neighbors: open cells inherit the flag; wall cells are entered only from `used = 0` and set it to `1`.
3. The first pop at the destination cell returns its distance.

#### Walkthrough

Example 1 again: the seed is `(0,0,0)` since the start is open. The first level reaches `(0,1)` and `(1,0)`, both walls, both entered with the flag flipping to `1`: states `(0,1,1)` and `(1,0,1)` at distance 1. From `(0,1,1)`, the open cells `(0,2)` and `(1,1)` follow at distance 2, then `(1,2)` at 3, then the destination `(2,2)` at 4, matching the expected output. No second break exists anywhere in the state space, which is exactly Example 2's obstruction: every route to the corner requires two wall entries, and the state graph has no path.

#### Solution

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        """Return the shortest start-to-end moves with at most one wall break.

        Time:  O(n * m): each of the 2 * n * m states expands once.
        Space: O(n * m): the visited map over states.
        """
        rows, columns = len(grid), len(grid[0])
        start_used = 0 if grid[0][0] == 1 else 1
        distance = {(0, 0, start_used): 0}
        frontier = deque([(0, 0, start_used)])
        while frontier:
            row, column, used = frontier.popleft()
            if (row, column) == (rows - 1, columns - 1):
                return distance[(row, column, used)]
            for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row, next_column = row + row_step, column + column_step
                if not (0 <= next_row < rows and 0 <= next_column < columns):
                    continue
                if grid[next_row][next_column] == 1:
                    state = (next_row, next_column, used)
                elif used == 0:
                    state = (next_row, next_column, 1)
                else:
                    continue
                if state not in distance:
                    distance[state] = distance[(row, column, used)] + 1
                    frontier.append(state)
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * m)`

The state graph doubles the node count and keeps unit-weight BFS optimal.

##### Space Complexity: `O(n * m)`

The visited map holds at most `2 * n * m` states.

#### Key Insights

- A budgeted one-shot ability becomes one boolean in the state; the search never re-derives which wall to break.
- Seeding the start with `used = 1` when the start is a wall is the single edge case; the destination being a wall is handled by the same transition rule.
- The unbroken BFS of the first rung is exactly the `used = 0` half of this state space.

## Comparison of Solutions

### Time Complexity

- **Break One Wall, Then Plain BFS**: `O(w * n * m)` - up to `4 * 10^8` cell visits at the constraint ceiling.
- **One BFS With a Broken-Flag State**: `O(n * m)`.

### Space Complexity

- **Break One Wall, Then Plain BFS**: `O(n * m)` per attempt.
- **One BFS With a Broken-Flag State**: `O(n * m)` once.

### Trade-offs

- The enumeration is self-evidently correct and reuses plain BFS untouched.
- The state-space rung needs the flag discipline but pays for it with a linear pass.

### When to Use Each

- **Break One Wall, Then Plain BFS**: sparse small grids, or as the oracle for randomized cross-checks.
- **One BFS With a Broken-Flag State**: the stated `200 x 200` ceiling and beyond.

### Optimization Notes

- Bidirectional BFS or A* with the Manhattan lower bound would trim explored states but change nothing asymptotic.
- The same boolean-state idea generalizes to "at most k breaks" with a `k + 1`-sized flag dimension.
