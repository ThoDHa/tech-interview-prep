# [Grid Reachability with a Forbidden Turn](https://www.fastprep.io/problems/amazon-grid-reachability-forbidden-turn)

**Medium** | **NN minutes** | **Breadth First Search, Graph**

Determine whether a destination can be reached on an obstacle grid while respecting movement direction.

For this exercise, assume grid contains 0 for open cells and X for blocked cells. start and destination are zero-based [row, column] coordinates of open cells.

initialHeading is 0 for north, 1 for east, 2 for south, or 3 for west. forbiddenTurn is left or right.

Each move advances exactly one adjacent cell. Relative to the current heading, you may continue straight or turn 90 degrees in the direction that is not forbidden. You cannot reverse direction, enter a blocked cell, or leave the grid. Your heading becomes the direction of the move. Reaching the destination with any heading succeeds. Starting at the destination succeeds with zero moves.

Return whether a valid path exists.

## Examples

### Example 1

**Input:** `grid = ["000","0X0","000"]`, `start = [0,0]`, `destination = [2,2]`, `initialHeading = 1`, `forbiddenTurn = "left"`

**Output:** `true`

**Explanation:** Move east along the top row, turn right, and continue south.

### Example 2

**Input:** `grid = ["000","0X0","000"]`, `start = [0,0]`, `destination = [2,2]`, `initialHeading = 1`, `forbiddenTurn = "right"`

**Output:** `false`

**Explanation:** The only open route from the top-left corner requires a right turn, which is forbidden.

## Constraints

- `For this exercise, assume 1 <= rows, columns <= 500; all rows have equal length.`
- `Every cell is 0 or X.`
- `Start and destination are valid open cells.`
- `0 <= initialHeading <= 3.`
- `forbiddenTurn is left or right.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
