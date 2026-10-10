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

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
