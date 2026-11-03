# [Search a Row and Column Sorted Matrix](https://www.fastprep.io/problems/amazon-search-row-column-sorted-matrix)

**Medium** | **NN minutes** | **Matrix, Binary Search**

Given a nonempty rectangular integer matrix matrix and an integer target, return true if the target occurs anywhere in the matrix, or false otherwise.

Each row is sorted in nondecreasing order from left to right. Each column is sorted in nondecreasing order from top to bottom. Duplicate values are allowed. The first value of a row need not be greater than the last value of the preceding row: the matrix is not necessarily sorted in row-major order.

## Examples

### Example 1

**Input:** `matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 6`

**Output:** `true`

**Explanation:** The target 6 is in the third row and second column (using one-based positions).

### Example 2

**Input:** `matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 8`

**Output:** `false`

**Explanation:** The matrix values are 1, 4, 7, 2, 5, 9, 3, 6, 12. None equals 8.

## Constraints

- `1 <= matrix.length <= 300.`
- `1 <= matrix[i].length <= 300.`
- `-1000000000 <= matrix[i][j] <= 1000000000.`
- `-1000000000 <= target <= 1000000000.`
- `The matrix is rectangular.`
- `Each row is nondecreasing from left to right, and each column is nondecreasing from top to bottom.`

## Deriving the Solution

Two sort orders cross in one grid, and neither alone is a row-major sort: every row ascends and every column ascends, but a row may start below the previous row's end. Any cell therefore partitions the matrix into four regions relative to its value, and one comparison against `target` can eliminate a whole region. The ladder sharpens which cells get compared:

1. **Start literal.** Compare every cell until `target` appears: correct, and it touches all `m * n` cells: see [Scan Every Cell](#scan-every-cell).
2. **Sort a row, then search it.** Each row is sorted, so a binary search answers "is `target` in this row" in logarithmic time, one row at a time: see [Binary Search Each Row](#binary-search-each-row).
3. **Use both orders at once.** Standing at the top-right corner, one comparison discards either the whole column (everything below is at least as large) or the whole row (everything left is at most as small), so the search walks a staircase of at most `m + n` cells: see [Staircase Search from the Top-Right Corner](#staircase-search-from-the-top-right-corner).
4. **Hand the row search to the library.** The per-row binary search of rung two is one `bisect` call away: see [Tidied with bisect](#tidied-with-bisect).

## Solutions

### Scan Every Cell

#### Derivation

The statement's most literal reading: membership over a grid, so visit every cell until the value turns up:

1. Iterate over every row, then every column.
2. Return `True` the moment a cell equals `target`.
3. Return `False` after the full scan finds nothing.

#### Walkthrough

Example 2 (`matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 8`), the comparisons in order:

```text
1  4  7        none equals 8
2  5  9        none equals 8
3  6  12       none equals 8
```

All nine cells disagree with `8`, so the scan returns `False`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            for value in row:
                if value == target:
                    return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

Every cell of the `m` by `n` grid is compared in the worst case.

##### Space Complexity: `O(1)`

The loop carries no state beyond the iterators.

#### Key Insights

- The full scan is the definition of the answer, which makes it the oracle every other approach is checked against.
- The scan ignores both sort orders completely; the information sits unused in the input, and the ladder spends it.
- Duplicates never complicate the scan: it asks only whether the value exists, not where.

### Binary Search Each Row

#### Derivation

Each row is sorted, which is exactly the precondition a binary search needs. Searching row by row answers the membership question once per row instead of once per cell:

1. For each row: keep `low` and `high` on its column indices.
2. While `low <= high`: compare the middle value to `target`; equal returns `True`, smaller moves `low` up, larger moves `high` down.
3. Return `False` after every row misses.

#### Walkthrough

Example 1 (`matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 6`), rows searched in order:

```text
row [1, 4, 7]:    low 0 high 2, mid 4 < 6; mid 7 > 6; low passes high: miss
row [2, 5, 9]:    low 0 high 2, mid 5 < 6; mid 9 > 6; low passes high: miss
row [3, 6, 12]:   low 0 high 2, mid 6 == 6                -> True
```

The third row's middle cell holds `6`, so the search returns `True`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            low, high = 0, len(row) - 1
            while low <= high:
                middle = (low + high) // 2
                if row[middle] == target:
                    return True
                if row[middle] < target:
                    low = middle + 1
                else:
                    high = middle - 1
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * log n)`

One binary search over `n` columns for each of the `m` rows.

##### Space Complexity: `O(1)`

Two indices per search, reused.

#### Key Insights

- The column order is left completely on the table: this approach treats the matrix as `m` independent sorted lists.
- Rows may start below the previous row's end, so no cross-row shortcut exists at this rung; the searches are genuinely separate.
- The hand-rolled loop is the reference form for the tidy-up that follows: the same three comparisons, one library call apart.

### Staircase Search from the Top-Right Corner

#### Derivation

The top-right cell is the only one that is the largest of its row and the smallest of its column. Comparing it to `target` therefore splits the remaining matrix in two: if the cell is too small, every cell above it in the column is smaller too, so the column is done; if the cell is too large, every cell left of it in the row is smaller too, so the row is done. One comparison kills one full line of the grid, and the surviving submatrix keeps the same two sort orders, so the argument repeats at its new top-right corner:

1. Start at `row = 0`, `column = len(matrix[0]) - 1`, the top-right corner.
2. While the position is inside the grid: compare `matrix[row][column]` to `target`; equal returns `True`.
3. If the cell is smaller than `target`, move down (`row += 1`); if it is larger, move left (`column -= 1`).
4. Leaving the grid means the value is absent: return `False`.

#### Walkthrough

Example 1 (`matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 6`), the staircase:

```text
(0, 2) = 7    7 > 6    move left
(0, 1) = 4    4 < 6    move down
(1, 1) = 5    5 < 6    move down
(2, 1) = 6    6 == 6   -> True
```

Four comparisons land on `6`, matching the expected Output.

Example 2 (`target = 8`) on the same matrix:

```text
(0, 2) = 7    7 < 8    move down
(1, 2) = 9    9 > 8    move left
(1, 1) = 5    5 < 8    move down
(2, 1) = 6    6 < 8    move down: row 3 is outside the grid
```

Four comparisons exhaust the grid without meeting `8`, so the search returns `False`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row, column = 0, len(matrix[0]) - 1
        while row < len(matrix) and column >= 0:
            candidate = matrix[row][column]
            if candidate == target:
                return True
            if candidate < target:
                row += 1
            else:
                column -= 1
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

Every step moves one line in, so the walk takes at most `m + n - 1` steps before it leaves the grid.

##### Space Complexity: `O(1)`

Two indices.

#### Key Insights

- The corner is the mechanism: only a cell that is maximal in one direction and minimal in the other lets a single comparison discard a whole line.
- The walk is deterministic and never revisits a cell, so the bound `m + n` needs no amortization argument.
- Duplicates cost nothing: the walk stops at the first copy it meets, and the region-elimination argument never depends on values being distinct.
- Starting bottom-left works symmetrically (move up on too-large, right on too-small); starting top-left does not work at all, because that corner is extreme in the same direction for both orders.

### Tidied with bisect

#### Derivation

The per-row binary search of rung two is three lines of index bookkeeping around one comparison, which is the exact shape of `bisect.bisect_left`: it returns where `target` would sit in the row, and the value at that position, if any, decides membership:

1. For each row: `position = bisect_left(row, target)`.
2. The row contains `target` exactly when `position < len(row)` and `row[position] == target`.
3. Return `True` on the first hit, `False` after every row misses.

#### Walkthrough

Example 1 (`matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 6`) again:

```text
row [1, 4, 7]:   bisect_left -> 2, row[2] = 7   not 6: miss
row [2, 5, 9]:   bisect_left -> 2, row[2] = 9   not 6: miss
row [3, 6, 12]:  bisect_left -> 1, row[1] = 6   hit -> True
```

The third row's insertion point holds `6`, so the search returns `True`, matching the expected Output.

#### Solution

```python
from bisect import bisect_left
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            position = bisect_left(row, target)
            if position < len(row) and row[position] == target:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * log n)`

The same row searches as the hand-rolled version, one library call each.

##### Space Complexity: `O(1)`

One position per row, reused.

#### Key Insights

- `bisect_left` returns the leftmost insertion point, which is exactly where a duplicate would start; the follow-up equality check decides membership.
- The boundary check `position < len(row)` is the whole subtlety: a target larger than every row value lands at `len(row)` and must not be indexed.
- The staircase still wins on this statement: `m + n` beats `m * log n` on square inputs, and the library does not change that balance.

## Comparison of Solutions

### Time Complexity

- **Scan Every Cell**: `O(m * n)` - every cell compared.
- **Binary Search Each Row**: `O(m * log n)` - one binary search per row.
- **Staircase Search from the Top-Right Corner**: `O(m + n)` - at most `m + n - 1` steps.
- **Tidied with bisect**: `O(m * log n)` - the row searches, one call each.

### Space Complexity

- **Scan Every Cell**: `O(1)` - nothing stored.
- **Binary Search Each Row**: `O(1)` - two indices.
- **Staircase Search from the Top-Right Corner**: `O(1)` - two indices.
- **Tidied with bisect**: `O(1)` - one position.

### Trade-offs

- **Scan Every Cell**: the definition, usable as the oracle; `300 * 300` cells are still cheap, but the approach reads none of the structure.
- **Binary Search Each Row**: uses half the structure (row order only); predictable and easy to verify.
- **Staircase Search from the Top-Right Corner**: uses both orders at once and is linear in the grid's perimeter; the elimination argument is the one to say out loud in an interview.
- **Tidied with bisect**: the row search with its bookkeeping removed; shortest correct code, same bounds as the hand-rolled row search.

### When to Use Each

- **Scan Every Cell**: for tiny grids, and always as the independent checker for the other three.
- **Binary Search Each Row**: when the column order is in doubt or the interviewer asks for a first improvement over the scan.
- **Staircase Search from the Top-Right Corner (Recommended)**: the interview default on this statement: `m + n` steps, two indices, one elimination argument.
- **Tidied with bisect**: when the code must be shortest and the log factor is acceptable; also the natural form if the rows arrive as an opaque sorted collection.

### Optimization Notes

- **Staircase Search from the Top-Right Corner** is the recommended choice: at the statement's bounds (`m, n <= 300`) it is at most 599 comparisons against up to 90000 for the scan.
- Values span the full `[-10^9, 10^9]` range and duplicates are allowed; no comparison in the walk depends on distinctness or on fits beyond the platform integer.
- The matrix is rectangular by the statement, so `len(matrix[0])` is a valid column bound; a ragged input would need per-row widths and would break the region-elimination argument.
- The row-major-sorted variant of this problem, [Search a 2D Matrix](../leetcode/search_a_2d_matrix.md), admits a single flat binary search in `O(log(m * n))`; this statement's weaker guarantee (rows and columns sorted independently, rows not concatenated) is exactly what rules that out and makes the staircase the fast lane.
