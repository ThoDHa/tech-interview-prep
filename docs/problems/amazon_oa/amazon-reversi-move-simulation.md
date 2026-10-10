# [Apply a Reversi Move](https://www.fastprep.io/problems/amazon-reversi-move-simulation)

**Medium** | **NN minutes** | **Array, Matrix, Simulation**

Given a Reversi board board, a zero-based target cell row, col, and a player player equal to B or W, apply exactly one move.

A direction captures pieces when one or more consecutive opponent pieces start next to the target and are followed, in that same direction, by one of the current player's pieces. A legal move places the player's piece and flips every captured line in all eight directions.

If the target is occupied or no direction captures an opponent piece, return the original board unchanged. Do not modify the input strings.

## Examples

### Example 1

**Input:** `board = ["....",".WB.","...."]`, `row = 1`, `col = 3`, `player = "W"`

**Output:** `["....",".WWW","...."]`

**Explanation:** The new white piece at column 3 brackets the black piece with the existing white piece at column 1.

### Example 2

**Input:** `board = ["..B..","..W..","BW.WB","..W..","..B.."]`, `row = 2`, `col = 2`, `player = "B"`

**Output:** `["..B..","..B..","BBBBB","..B..","..B.."]`

**Explanation:** The move captures one white piece in each cardinal direction.

### Example 3

**Input:** `board = ["...","...","..."]`, `row = 1`, `col = 1`, `player = "B"`

**Output:** `["...","...","..."]`

**Explanation:** No opponent line is bracketed, so the move is invalid and the board remains unchanged.

## Constraints

- `1 <= board.length, board[i].length <= 50.`
- `Every row has the same length and contains only ., B, or W.`
- `0 <= row < board.length and 0 <= col < board[0].length.`
- `player is B or W.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
