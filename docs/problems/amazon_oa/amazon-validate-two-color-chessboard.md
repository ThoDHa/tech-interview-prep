# [Validate a Two-Color Chessboard](https://www.fastprep.io/problems/amazon-validate-two-color-chessboard)

**Easy** | **NN minutes** | **Matrix, Array**

You are given a nonempty rectangular integer matrix board. Every cell is one of two colors, encoded as 0 or 1.

Return true if board is a valid chessboard pattern: every pair of horizontally adjacent cells has different colors, and every pair of vertically adjacent cells has different colors. Otherwise, return false.

## Examples

### Example 1

**Input:** `board = [[0,1,0],[1,0,1]]`

**Output:** `true`

**Explanation:** Every horizontal and vertical neighbor has the opposite color.

### Example 2

**Input:** `board = [[0,1],[1,1]]`

**Output:** `false`

**Explanation:** The two cells in the bottom row have the same color, so the pattern is invalid.

## Constraints

- `1 <= board.length <= 100`
- `1 <= board[i].length <= 100`
- `Every row has the same length.`
- `board[i][j] is either 0 or 1.`

## Solutions

### Full Adjacent-Pair Scan

#### Derivation

The most literal reading of the validity rule is to test it pair by pair: every horizontally adjacent pair must hold different colors, and every vertically adjacent pair must hold different colors. A double loop over the cells covers both families at once, because the pair to the right of a cell and the pair below a cell are exactly the pairs whose left or upper member is that cell. Out-of-bounds neighbors simply do not exist, so the two comparisons are guarded rather than assumed:

1. Read `rows` and `cols` from `board`.
2. Scan every cell `(row, col)`.
3. When `col + 1 < cols`, require `board[row][col] != board[row][col + 1]`.
4. When `row + 1 < rows`, require `board[row][col] != board[row + 1][col]`.
5. Return `False` on the first equal pair; return `True` after every pair has passed.

#### Walkthrough

Example 2, `board = [[0,1],[1,1]]`, whose expected Output is `false`. The scan walks the four cells in row-major order, and each line shows the guarded comparisons for one cell:

```text
(0,0) color 0   right (0,1) color 1   differ   continue
                down  (1,0) color 1   differ   continue
(0,1) color 1   right                 out of bounds
                down  (1,1) color 1   equal    -> return False
```

The first violation found is the vertical pair `(0,1)` over `(1,1)`, both color `1`; the equal horizontal pair of the bottom row that the Explanation names is the same failure seen one comparison later. The function returns `False`, matching the expected Output.

#### Solution

The code is the guarded right and down comparisons from the walkthrough:

```python
from typing import List


class Solution:
    def isValidChessboard(self, board: List[List[int]]) -> bool:
        """Return True when every horizontal and vertical neighbor pair differs.

        Time:  O(m * n): each cell is compared with its right and down neighbor.
        Space: O(1): only loop indices and the pair being compared.
        """
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if col + 1 < cols and board[row][col] == board[row][col + 1]:
                    return False
                if row + 1 < rows and board[row][col] == board[row + 1][col]:
                    return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each of the `m × n` cells triggers at most two constant-time comparisons; an invalid board usually returns much earlier, and the full scan is the worst case.

##### Space Complexity: `O(1)`

Only the loop indices are held; the checks read the board in place.

#### Key Insights

- The definition translates to code almost verbatim, and each adjacent pair is tested exactly once, by its left or upper member.
- The early return makes invalid boards cheap; the linear bound only binds on valid boards, where every pair must be checked before the verdict.
- Bounds guards make degenerate shapes work for free: a single-row board has no vertical pairs, and a single-column board no horizontal ones.

### Position-Parity Formula

#### Derivation

The pair scan compares neighbors, yet the comparison is redundant: fix `board[0][0]` and every other color is forced. Each step right or down must flip the color, so reaching cell `(row, col)` from the top-left corner takes `row + col` flips, and a binary color flipped `row + col` times is an addition modulo 2. That collapses the web of neighbor comparisons into one closed-form condition each cell can check about itself, with no neighbor reads at all:

1. Read `first_color = board[0][0]`.
2. Scan every cell `(row, col)`.
3. Compute `expected = (row + col + first_color) % 2` and require the cell to equal it.
4. Return `False` on the first mismatch; return `True` after every cell matches.

#### Formula

Cell `(row, col)` is legal exactly when its color equals the corner color flipped once per step of distance from the corner:

$$ \text{board[row][col]} = (\text{row} + \text{col} + \text{board[0][0]}) \bmod 2 $$

```text
board[row][col] == (row + col + board[0][0]) % 2
```

The condition holds for the corner itself (`row + col = 0`), and any two horizontally or vertically adjacent cells have `row + col` values of different parity, so two cells satisfying the formula are always neighbors of different colors. That makes "every adjacent pair differs" equivalent to "every cell satisfies the formula".

#### Walkthrough

Example 1, `board = [[0,1,0],[1,0,1]]`, with `first_color = 0`. Each cell is checked against `(row + col) % 2`:

```text
(0,0)  expected (0+0)%2 = 0   board 0   match
(0,1)  expected (0+1)%2 = 1   board 1   match
(0,2)  expected (0+2)%2 = 0   board 0   match
(1,0)  expected (1+0)%2 = 1   board 1   match
(1,1)  expected (1+1)%2 = 0   board 0   match
(1,2)  expected (1+2)%2 = 1   board 1   match
```

Every cell satisfies the formula, so the function returns `True`, matching the expected Output for Example 1. Example 2 (`board = [[0,1],[1,1]]`) fails at cell `(1, 1)`: the formula expects `(1 + 1) % 2 = 0` while the cell holds `1`.

#### Solution

The code is the per-cell formula check from the walkthrough:

```python
from typing import List


class Solution:
    def isValidChessboard(self, board: List[List[int]]) -> bool:
        """Return True when every cell matches the parity pattern it must follow.

        Time:  O(m * n): one formula evaluation per cell.
        Space: O(1): the expected color is recomputed per cell.
        """
        rows, cols = len(board), len(board[0])
        first_color = board[0][0]
        for row in range(rows):
            for col in range(cols):
                if board[row][col] != (row + col + first_color) % 2:
                    return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Every cell is visited once and checked with one constant-time arithmetic condition.

##### Space Complexity: `O(1)`

Only `first_color` and the loop indices are held.

#### Key Insights

- Two cells are horizontal or vertical neighbors exactly when the parities of their `row + col` values differ, so "all neighbors differ" is the same fact as "color depends only on the parity of `row + col`".
- The formula performs about half the comparisons of the pair scan and never indexes a neighbor, but both approaches are `O(m × n)`; the gain is constant-factor and conceptual, not asymptotic.
- This is the rule real chessboards follow: a square's color is the parity of its file plus its rank.

## Comparison of Solutions

### Time Complexity

- **Full Adjacent-Pair Scan**: `O(m × n)` - up to two neighbor comparisons per cell.
- **Position-Parity Formula**: `O(m × n)` - one arithmetic condition per cell.

### Space Complexity

- **Full Adjacent-Pair Scan**: `O(1)` - loop indices only.
- **Position-Parity Formula**: `O(1)` - the corner color and loop indices only.

### Trade-offs

- **Full Adjacent-Pair Scan**: restates the definition, so it is hard to get wrong, but every comparison re-derives what the pattern already determines.
- **Position-Parity Formula**: the fewest operations per cell and a sharper reading of the structure, at the cost of needing the parity argument justified before the code is trusted.

### When to Use Each

- **Full Adjacent-Pair Scan (Recommended)**: the default interview answer: direct from the statement, trivially correct, and easy to extend to more than two colors or to diagonal adjacency rules.
- **Position-Parity Formula**: when the two-color structure is worth exploiting, or when the follow-up asks why a chessboard is colored the way it is.

### Optimization Notes

- Both approaches are asymptotically optimal: any correct algorithm must at least read every cell, which is already `O(m × n)`.
- Both scans early-exit on invalid boards after a handful of cells; neither can beat linear time on valid input.
- The pair scan survives rule changes the parity argument does not: a third color, or diagonal neighbors required to differ, still reduce to guarded pair comparisons, while the formula depends on two colors and axis-aligned adjacency.
- A common micro-variant folds the two comparisons into one loop over the offset pairs `[(0, 1), (1, 0)]`; the bound is unchanged.
