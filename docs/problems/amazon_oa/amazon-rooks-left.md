# [Rooks Left](https://www.fastprep.io/problems/amazon-rooks-left)

**Medium** | **NN minutes** | **Matrix, Union Find, Graph**

You are given a 2D grid board that represents a chessboard. The board contains multiple cells, where:


0 indicates an empty cell.1 indicates a cell containing a rook.
A rook can only move vertically or horizontally if there is another rook in its row or column to capture. It cannot move if there are no other rooks in its row or column.



Your task is to determine the minimum number of rooks that can be left on the board in a peaceful state after capturing as many rooks as possible. A peaceful state is defined as a state where no two rooks can capture each other (i.e., no two rooks share the same row or column).



Note:


Rook Movement: A rook can only move if there is another rook in the same row or column to capture. If a rook is alone in its row or column, it cannot move.The goal is to minimize the number of rooks left by capturing as many rooks as possible, while ensuring that the remaining rooks are in a peaceful state.A peaceful state is achieved when no two rooks can capture each other (i.e., no two rooks share the same row or column).

## Examples

### Example 1

**Input:** `board = [[1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 1, 0]]`

**Output:** `1`

**Explanation:** All the rooks are connected either directly or indirectly in the same row or column, forming one single connected group.

### Example 2

**Input:** `board = [[0, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 0, 1], [0, 0, 1, 1, 0]]`

**Output:** `1`

**Explanation:** All the rooks can reach each other, either directly or through a sequence of moves along rows or columns, resulting in one connected component.

### Example 3

**Input:** `board = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]`

**Output:** `3`

**Explanation:** There are 3 rooks, and none of them share the same row or column. Thus, each rook is isolated, resulting in 3 connected components.

### Example 4

**Input:** `board = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]`

**Output:** `1`

**Explanation:** All rooks are connected in both rows and columns, forming one single connected component.

### Example 5

**Input:** `board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]`

**Output:** `0`

**Explanation:** There are no rooks on the board.

### Example 6

**Input:** `board = [[1]]`

**Output:** `1`

**Explanation:** There is single rook, resulting in one connected component.

### Example 7

**Input:** `board = [[1, 0], [1, 0]]`

**Output:** `1`

**Explanation:** The two rooks are in the same row, forming one connected group.

### Example 8

**Input:** `board = [[1, 0, 0], [1, 0, 0], [0, 0, 1]]`

**Output:** `2`

**Explanation:** The two rooks in the first two rows share the sam column, forming one connected component.The rook in the third row is isolated, resulting in a total of two connected components.

## Constraints

- `The dimensions of the board are 1 <= n, m <= 1000.`
- `Each cell contains either 0 or 1.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
