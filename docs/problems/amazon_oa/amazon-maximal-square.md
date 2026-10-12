# [Maximal Square](https://www.fastprep.io/problems/amazon-maximal-square)

**Medium** | **NN minutes** | **Array, Matrix, Dynamic Programming**

Given a matrix of characters '0' and '1', return the area of the largest square containing only '1' cells.

## Examples

### Example 1

**Input:** `matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]`

**Output:** `4`

**Explanation:** The largest all-one square has side length 2.

### Example 2

**Input:** `matrix = [["0"]]`

**Output:** `0`

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-maximal-square; fill them in. -->

## Solutions

### Brute Force

#### Derivation

The most literal reading of "the largest square of '1' cells" tries squares where they can start: every top-left cell anchors a candidate, and the candidate grows one side at a time until it fails. Growth validates only the newly added border, the new bottom row plus the new right column, because the interior was already validated by the previous, smaller square:

1. Scan every cell as a top-left corner `(top_row, left_col)`; skip it when
   `matrix[top_row][left_col] == '0'`.
2. Start with `side = 1`, which always fits for a `'1'` cell.
3. `can_grow(top_row, left_col, side + 1)` checks the candidate of the next
   side: it returns `False` when the new bottom row or right column leaves the
   grid, then scans the new bottom row (`side + 1` cells) and the new right
   column (`side` cells) for any `'0'`.
4. While `can_grow` holds, increment `side`.
5. Track `largest_side` per anchor and return `largest_side * largest_side`,
   the area.

#### Walkthrough

Example 1's largest square sits mid-grid, so to keep the border checks readable we use a smaller tailored grid:

```text
matrix = [
  ["1", "1", "0"],
  ["1", "1", "1"],
  ["1", "1", "0"]
]
```

The scan tries every cell as a top-left corner; each line shows the growth attempts and the border cells they validate:

```text
(0, 0)  side 1 -> try 2: bottom row (1,0) (1,1) and right col (0,1) all '1' -> side 2
                  try 3: border cell (2,2) is '0' -> stop, side 2
(0, 1)  side 1 -> try 2: border cell (0,2) is '0' -> stop, side 1
(0, 2)  '0' -> skipped
(1, 0)  side 1 -> try 2: bottom row (2,0) (2,1) and right col (1,1) all '1' -> side 2
                  try 3: bottom row row 3 leaves the grid -> stop, side 2
(1, 1)  side 1 -> try 2: border cell (2,2) is '0' -> stop, side 1
(1, 2)  '0' -> skipped
(2, 0)  side 1 -> try 2: bottom row row 3 leaves the grid -> stop, side 1
(2, 1)  side 1 -> try 2: bottom row row 3 leaves the grid -> stop, side 1
(2, 2)  '0' -> skipped
```

The largest confirmed side is `2`, so the function returns `2 * 2 = 4`. (On Example 1 the same growth finds a side-2 square with bottom-right corner `(2, 3)` and returns `4`, matching its expected Output.)

#### Solution

The code is the anchor scan with the incremental border test `can_grow`.

```python
from typing import List


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        rows, cols = len(matrix), len(matrix[0])

        def can_grow(top_row: int, left_col: int, side: int) -> bool:
            bottom_row = top_row + side - 1
            right_col = left_col + side - 1
            if bottom_row >= rows or right_col >= cols:
                return False
            for col in range(left_col, right_col + 1):
                if matrix[bottom_row][col] == '0':
                    return False
            for row in range(top_row, bottom_row):
                if matrix[row][right_col] == '0':
                    return False
            return True

        largest_side = 0
        for top_row in range(rows):
            for left_col in range(cols):
                if matrix[top_row][left_col] == '0':
                    continue
                side = 1
                while can_grow(top_row, left_col, side + 1):
                    side += 1
                largest_side = max(largest_side, side)
        return largest_side * largest_side
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × min(m, n)^2)`

Each of the `m × n` anchors grows through sides `1` up to `min(m, n)`, and growing to side `k` validates the new border of `2k - 1` cells, so one anchor pays `O(min(m, n)^2)` growth work in the worst case.

##### Space Complexity: `O(1)`

Only the running side lengths; no auxiliary structure.

#### Key Insights

- Growing a candidate square only validates the new bottom row and right column: the previous step already proved the interior.
- The worst case is an all-'1' grid, where every anchor grows to the full `min(m, n)` and the quadratic growth term dominates.
- Constant extra space, but the same squares are re-grown at every overlapping anchor, which is the waste the dynamic programming versions remove.

### Bottom-Up 2-D DP

#### Derivation

The brute force re-grows the same squares once per overlapping anchor: the side-2 square ending at `(2, 3)` in Example 1 is validated again, cell by cell, inside growth attempts from other corners. The repair is to invert the question. Instead of asking "how large is the square starting here?", ask "how large is the largest all-'1' square whose bottom-right corner is `(row, col)`?" A square of side `s` with bottom-right corner `(row, col)` exists exactly when the cell holds `'1'` and squares of side at least `s - 1` end above `(row - 1, col)`, to the left `(row, col - 1)`, and diagonally `(row - 1, col - 1)`: those three squares supply the column arm, the row arm, and the interior the new square needs, so the weakest of the three arms limits `s`. Every cell depends only on cells already computed in earlier rows and earlier columns:

1. Allocate `dp` of size `rows × cols`, all zero.
2. Sweep `row` over all rows and `col` over all columns; skip `'0'` cells,
   leaving `dp[row][col]` at `0`.
3. First row or first column: a `'1'` cell anchors only a side-1 square, so
   `dp[row][col] = 1`.
4. Otherwise `dp[row][col] = 1 + min(dp[row - 1][col], dp[row][col - 1], dp[row - 1][col - 1])`.
5. Track `largest_side` across the sweep and return `largest_side * largest_side`.

#### Recurrence

Let `dp[row][col]` be the side of the largest all-'1' square whose bottom-right corner is `(row, col)`:

$$ dp[row][col] = \begin{cases}
0, & matrix[row][col] = '0' \\[4pt]
1, & matrix[row][col] = '1',\ row = 0 \text{ or } col = 0 \\[4pt]
1 + \min(dp[row-1][col],\ dp[row][col-1],\ dp[row-1][col-1]), & matrix[row][col] = '1',\ row, col > 0
\end{cases} $$

```text
dp[row][col] = 0                                    (when matrix[row][col] == '0')
dp[row][col] = 1                                    (first row or column, cell '1')
dp[row][col] = 1 + min(dp[row - 1][col],            (otherwise: column arm)
                       dp[row][col - 1],            (row arm)
                       dp[row - 1][col - 1])        (interior)
```

The zero cells mark positions that end no square at all, and the `min` takes the weakest of the three arms a new square must extend. The answer is the largest value anywhere in the table, squared.

#### Walkthrough

Trace the fill on Example 1: `matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]`. Rows are grid rows, columns grid columns:

```text
        c0  c1  c2  c3  c4
  r0     1   0   1   0   0
  r1     1   0   1   1   1
  r2     1   1   1   2   2
  r3     1   0   0   1   0
```

Cell `(2, 3)` reads its three neighbors, `dp[1][3] = 1`, `dp[2][2] = 1`, and `dp[1][2] = 1`, and reaches `1 + 1 = 2`: a side-2 square ends there. Cell `(2, 4)` then takes `1 + min(dp[1][4] = 1, dp[2][3] = 2, dp[1][3] = 1) = 2`. The largest value in the table is `2`, so the function returns `2 * 2 = 4`, matching the expected Output. Example 2's single `'0'` cell never leaves `0`, and the function returns `0`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
from typing import List


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        dp = [[0] * cols for _ in range(rows)]
        largest_side = 0
        for row in range(rows):
            for col in range(cols):
                if matrix[row][col] == '0':
                    continue
                if row == 0 or col == 0:
                    dp[row][col] = 1
                else:
                    dp[row][col] = 1 + min(dp[row - 1][col],
                                           dp[row][col - 1],
                                           dp[row - 1][col - 1])
                largest_side = max(largest_side, dp[row][col])
        return largest_side * largest_side
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One constant-work cell computation per grid cell.

##### Space Complexity: `O(m × n)`

The full table.

#### Key Insights

- Recomputing per anchor becomes filling one cell from three already-known neighbors: each square is established exactly once.
- The `min` of the three neighbors is the whole trick: a square needs its column arm, row arm, and interior all present at side `s - 1`.
- The table's largest cell, not its bottom-right cell, is the answer: the maximal square can end anywhere.

### Space-Optimized Two-Row DP

#### Derivation

The table fill reads, for cell `(row, col)`, only `dp[row - 1][col]`, `dp[row][col - 1]`, and `dp[row - 1][col - 1]`: the previous row and the cell just built. Rows two and older are dead weight, so the full table collapses to two rows, `previous` for the row above and `current` under construction, with the row rotation (`previous = current`) playing the role the index decrement played in the table version:

1. Initialize `previous` to a row of `cols` zeros.
2. For each `row`, build `current` from `previous` with the same cell rule,
   first column included (`current[0] = 1` for a `'1'` cell).
3. Replace `previous` with `current` after each row.
4. Track `largest_side` while filling and return `largest_side * largest_side`.

#### Walkthrough

Trace the two rolling rows on Example 1:

```text
start       previous = [0, 0, 0, 0, 0]
after row0  current  = [1, 0, 1, 0, 0]
after row1  current  = [1, 0, 1, 1, 1]
after row2  current  = [1, 1, 1, 2, 2]
after row3  current  = [1, 0, 0, 1, 0]
```

Each row equals the corresponding table row from the Bottom-Up 2-D DP walkthrough. Inside row 2, `current[3] = 1 + min(previous[3] = 1, current[2] = 1, previous[2] = 1) = 2` and `current[4] = 1 + min(previous[4] = 1, current[3] = 2, previous[3] = 1) = 2`. The largest value seen across all rows is `2`, so the function returns `4`, matching the expected Output; Example 2 returns `0` because its only cell is `'0'`.

#### Solution

The code is the walkthrough's row loop: build `current` from `previous`, then rotate.

```python
from typing import List


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        previous = [0] * cols
        largest_side = 0
        for row in range(rows):
            current = [0] * cols
            for col in range(cols):
                if matrix[row][col] == '0':
                    continue
                if row == 0 or col == 0:
                    current[col] = 1
                else:
                    current[col] = 1 + min(previous[col],
                                           current[col - 1],
                                           previous[col - 1])
                largest_side = max(largest_side, current[col])
            previous = current
        return largest_side * largest_side
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One comparison per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `cols` cells; the rotated-away row is garbage-collected.

#### Key Insights

- The dependency pattern of a recurrence determines its memory: cells only ever read the previous row and the cell to the left.
- `current` must be a fresh row per grid row; writing into `previous` in place would overwrite the diagonal `previous[col - 1]` before it is read.
- The area return needs only the largest side seen, so no final pass over the last row is required.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(m × n × min(m, n)^2)` - each anchor re-grows squares side by side, validating the new border each time.
- **Bottom-Up 2-D DP**: `O(m × n)` - one constant-work cell computation per grid cell.
- **Space-Optimized Two-Row DP**: `O(m × n)` - the same cells, two rows at a time.

### Space Complexity

- **Brute Force**: `O(1)` - running side lengths only.
- **Bottom-Up 2-D DP**: `O(m × n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.

### Trade-offs

- **Brute Force** is constant-space and needs no recurrence insight, but re-grows the same squares at overlapping anchors and turns quadratic in `min(m, n)` on dense grids.
- **Bottom-Up 2-D DP** removes the re-growth by establishing each square once, at the price of a full table.
- **Space-Optimized Two-Row DP** keeps the same time at linear memory, giving up access to rows older than the previous one.

### When to Use Each

- **Brute Force**: tiny grids, or as the correctness oracle when checking the dynamic programming versions.
- **Bottom-Up 2-D DP**: when the table itself matters, for example to also locate the square by walking back from its bottom-right corner.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated (recommended here).

### Optimization Notes

- On dense grids the two-row version already does the minimum possible work: one comparison per cell, with no auxiliary pass.
- The area is `largest_side * largest_side`, not a sum over squares: the problem asks for one maximal square, not a count.
- A common pitfall is returning the side instead of the area, or reading the bottom-right cell's value instead of tracking the maximum across the whole sweep.
