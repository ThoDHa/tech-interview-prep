# [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)

**Medium** | **25 minutes** | **Array, Hash Table, Matrix**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/valid_sudoku/solution.py`](../../practice/valid_sudoku/solution.py)

You are given a `9 x 9` Sudoku board `board`. A Sudoku board is valid if the following rules are followed:

1. Each row must contain the digits `1-9` without duplicates.
2. Each column must contain the digits `1-9` without duplicates.
3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without duplicates.

Return `true` if the Sudoku board is valid, otherwise return `false`

Note: A board does not need to be full or be solvable to be valid.

## Examples

### Example 1

**Input:**

```text
board =
[["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","8",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]]
```

**Output:**

```text
true
```

### Example 2

**Input:**

```text
board =
[["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","1",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]]
```

**Output:**

```text
false
```

**Explanation:** There are two 1's in the top-left 3x3 sub-box.

## Constraints

- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit `1-9` or `'.'`.

## Deriving the Solution

Validity is a *local* property: each digit must merely be absent from the other members of its own row, its own column, and its own box. Nothing about solving or reachability is asked, so every solution below reduces to one question asked 81 times: has this digit already appeared in any of the three units this cell belongs to?

1. **Start literal.** Check each of the 27 units (9 rows, 9 columns, 9 boxes) independently: collect its digits and test for duplicates. Three nested passes over the board cost a constant multiple of 81 cells, so this is already `O(1)`, but each digit is examined three times: see [Three Passes over Units](#three-passes-over-units).
2. **Spot the waste.** The unit-level passes repeat work only because they are organized around units. One sweep over the cells can serve all three memberships at once: each visited cell is simultaneously a row member, a column member, and a box member.
3. **Fuse into one pass.** Keep, for every row, column, and box, the set of digits already placed there, and test-insert each digit into its three sets as the sweep reaches it. One pass, one lookup each way: see [One Pass with Seen Sets](#one-pass-with-seen-sets).

## Solutions

### Three Passes over Units

#### Derivation

The most literal translation of the three rules walks the board once per rule. Each pass iterates over its nine units, collects the digits that unit holds, and reports failure the moment a digit shows up twice:

1. For each row index `r`, collect `board[r][c]` across `c` and check for a duplicate among the non-empty cells.
2. For each column index `c`, collect `board[r][c]` across `r` and check the same way.
3. For each box, index it by `box_row`, `box_col` in `0..2`, collect the cells at rows `3 * box_row + i` and columns `3 * box_col + j` for `i, j` in `0..2`, and check again.
4. Return `True` only if all 27 checks pass.

A shared helper that answers "does this list of nine cells hold a repeated digit?" keeps the three passes honest and identical in shape.

#### Walkthrough

Trace the duplicate check inside one unit on Example 2's top-left box, the unit that fails. The box spans rows `0..2` and columns `0..2`:

```text
cells:  board[0][0]='1'  board[0][1]='2'  board[0][2]='.'
        board[1][0]='4'  board[1][1]='.'  board[1][2]='.'
        board[2][0]='.'  board[2][1]='9'  board[2][2]='1'

digits  -> ['1', '2', '4', '9', '1']
seen:   '1' yes  '2' no  '4' no  '9' no  '1' yes  -> duplicate found
```

The second `'1'` is already in `seen`, so the box check returns a violation and the whole function returns `False`, matching Example 2's expected Output. On Example 1 the same box holds `['1', '2', '4', '9']` with no repeat, and every other unit checks out, so the function returns `True`.

#### Solution

The code is the three sweeps from the derivation over one shared duplicate test.

```python
from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for row in board:
            if self._has_duplicate(row):
                return False
        for c in range(9):
            if self._has_duplicate([board[r][c] for r in range(9)]):
                return False
        for box_row in range(3):
            for box_col in range(3):
                cells = [
                    board[3 * box_row + i][3 * box_col + j]
                    for i in range(3)
                    for j in range(3)
                ]
                if self._has_duplicate(cells):
                    return False
        return True

    def _has_duplicate(self, cells: List[str]) -> bool:
        seen = set()
        for value in cells:
            if value == ".":
                continue
            if value in seen:
                return True
            seen.add(value)
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

The board size is fixed: 27 units of 9 cells each, so 243 cell visits regardless of content. Generalized to an `n x n` board this is `O(n²)`.

##### Space Complexity: `O(1)`

The duplicate test holds at most one 9-entry set at a time.

#### Key Insights

- Mirrors the rules one-to-one, which makes correctness easy to argue: each rule is checked by its own pass.
- Visits every cell three times, once per membership, though a cell's three answers could share one visit.
- The box index arithmetic (`3 * box_row + i`, `3 * box_col + j`) is the only subtle part; everything else is bookkeeping.

### One Pass with Seen Sets

#### Derivation

The three passes exist because each pass is attached to a *rule* rather than to a *cell*. Flip the organization: sweep the cells once, and treat each filled cell as a simultaneous member of three units, its row `r`, its column `c`, and its box. Every unit keeps a `seen` set; a cell is accepted exactly when its digit is new to all three sets at once:

1. Create `rows`, `columns`, `boxes`, lists of nine empty sets each.
2. Sweep `r` over `0..8` and `c` over `0..8`; skip cells holding `'.'`.
3. Compute the cell's box index as `box = (r // 3) * 3 + c // 3`, flattening the box grid to `0..8`.
4. If the digit already sits in `rows[r]`, `columns[c]`, or `boxes[box]`, return `False`.
5. Otherwise add the digit to all three sets and continue.
6. Surviving the sweep means no unit held a duplicate, so return `True`.

Testing all three sets *before* inserting is what makes the check sound: a digit is compared against everything placed before it, never against itself.

#### Walkthrough

Trace the decisive moment on Example 2. The sweep reaches the conflicting cell at row `2`, column `2` holding `'1'`:

```text
rows[2]    = {'9'}                    '1' not present
columns[2] = {'8'}                    '1' not present
boxes[0]   = {'1', '2', '4', '9'}     '1' present -> return False
```

The row and column checks pass, but `boxes[0]` already holds the `'1'` placed at cell `(0, 0)`, so the sweep stops and returns `False`, matching Example 2's expected Output. The box index arithmetic is what makes this catch possible: `(2 // 3) * 3 + 2 // 3 = 0`, the same box as `(0 // 3) * 3 + 0 // 3 = 0`. On Example 1 no cell ever finds its digit in a seen set, the sweep finishes, and the function returns `True`.

#### Solution

The code is the fused sweep from the walkthrough: one visit, three membership tests, three insertions.

```python
from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        columns = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                value = board[r][c]
                if value == ".":
                    continue
                box = (r // 3) * 3 + c // 3
                if (
                    value in rows[r]
                    or value in columns[c]
                    or value in boxes[box]
                ):
                    return False
                rows[r].add(value)
                columns[c].add(value)
                boxes[box].add(value)
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

Exactly 81 cells are visited once, each doing a constant number of set operations. Generalized to `n x n` this is `O(n²)`, against `O(n²)` for the three-pass version too but with a threefold constant.

##### Space Complexity: `O(1)`

The 27 sets each hold at most 9 digits, so 81 entries at most regardless of content.

#### Key Insights

- One cell visit serves all three memberships: the waste of the three-pass version was organizational, not algorithmic.
- `box = (r // 3) * 3 + c // 3` is the identity worth memorizing: integer division locates the box, the `* 3` flattens the box grid into one index.
- Failing fast stops the sweep at the first conflict; a valid board always pays the full 81 visits.

## Comparison of Solutions

### Time Complexity

- **Three Passes over Units**: `O(1)` - 27 unit scans of 9 cells, about 243 visits.
- **One Pass with Seen Sets**: `O(1)` - a single sweep of 81 cells with three set operations each.

### Space Complexity

- **Three Passes over Units**: `O(1)` - one 9-entry scratch set at a time.
- **One Pass with Seen Sets**: `O(1)` - 27 sets bounded by 9 entries each.

### Trade-offs

- **Three Passes over Units** keeps each rule in its own loop, at the cost of touching every cell three times and writing the box index arithmetic twice (collection and iteration).
- **One Pass with Seen Sets** touches each cell once and carries all bookkeeping in its data layout rather than its loop structure.

### When to Use Each

- **Three Passes over Units**: explaining the rules in an interview, or adapting to settings where only one rule is needed.
- **One Pass with Seen Sets**: the standard implementation (recommended here), and the pattern to reuse for the Sudoku solver variant where the sets become the candidates.

### Optimization Notes

- With the board fixed at 9 x 9, both solutions are constant; asymptotics only distinguish them on a generalized `n x n` board, where the one-pass version wins by its constant factor.
- A common micro-variant packs the three sets into one dictionary keyed by `(kind, index, digit)` tuples; it changes the constant, not the idea.
- Validity is weaker than solvability: an all-empty board is valid, and no solution here ever backtracks, which is what keeps the check linear in the cell count.
