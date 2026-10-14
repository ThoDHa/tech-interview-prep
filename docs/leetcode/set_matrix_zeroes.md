# [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

**Medium** | **25 minutes** | **Array, Hash Table, Matrix**

**Pattern:** [Simulation](../patterns/simulation/intuition.md), [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [In-place algorithm](https://en.wikipedia.org/wiki/In-place_algorithm) · [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Matrix](https://en.wikipedia.org/wiki/Matrix_(mathematics))

**Practice:** [`practice/set_matrix_zeroes/solution.py`](../../practice/set_matrix_zeroes/solution.py)

Given an `m x n` matrix of integers `matrix`, if an element is `0`, set its entire row and column to `0`'s.

You must update the matrix *in-place*.

## Examples

### Example 1

**Input:**

```text
matrix = [
  [0,1],
  [1,0]
]
```

**Output:**

```text
[
  [0,0],
  [0,0]
]
```

### Example 2

**Input:**

```text
matrix = [
  [1,2,3],
  [4,0,5],
  [6,7,8]
]
```

**Output:**

```text
[
  [1,0,3],
  [0,0,0],
  [6,0,8]
]
```

## Constraints

- `m == matrix.length`
- `n == matrix[0].length`
- `1 <= m, n <= 200`
- `-2^31 <= matrix[i][j] <= (2^31) - 1`

## Follow-up

Could you solve it using `O(1)` space?

## Deriving the Solution

Zeroing is destructive twice over: a `0` at `(i, j)` zeroes row `i` and column `j`, and once those writes land, the matrix no longer records which zeros were original. Every cell of row `i` and column `j` must be decided from the pre-pass state, so each approach is a scheme for remembering the zero set while overwriting as little extra space as possible, ending inside the matrix itself.

1. **Start literal.** Scan the matrix, collect the coordinates of every
   original `0` into two sets, then re-scan and zero every cell whose row or
   column appears in the sets. Correct, but it allocates `O(m + n)` space:
   see [Extra Row and Column Sets](#extra-row-and-column-sets).
2. **Drop the row set.** Rows can be remembered inside the matrix: the first
   cell of a row, `matrix[i][0]`, is free flag storage. Column `0` then needs
   its own single variable, since its flag cell is also its data: see
   [First-Cell Flags](#first-cell-flags).
3. **Shrink to two booleans.** The same flag idea applied to the first row and
   first column leaves two booleans for the borders and an in-matrix grid for
   the interior, `O(1)` space total: see
   [First Row and Column as Flags](#first-row-and-column-as-flags).

## Solutions

### Extra Row and Column Sets

#### Derivation

The literal reading treats zeroing as two phases: record, then apply. The trap the recording avoids is invisible until stated: a `0` written at `(0, 1)` during a naive single pass would later be read as an original zero and wrongly zero column `1`. Separating the phases makes every decision from the pre-pass state:

1. Walk the matrix once, collecting `rows`, the set of row indices holding an
   original `0`, and `cols`, the same for columns.
2. Walk the matrix again: any cell whose row index is in `rows` or whose
   column index is in `cols` becomes `0`.
3. Both passes read only the original state in phase one and write only in
   phase two, so no order dependence can arise.

#### Walkthrough

Record then apply on Example 2: `matrix = [[1,2,3], [4,0,5], [6,7,8]]`. The recording pass finds exactly one original zero, at `(1, 1)`:

```text
record    scan (0,0)..(2,2):  matrix[1][1] == 0
          rows = {1}   cols = {1}
apply     row 1 in rows -> zero every cell of row 1
          col 1 in cols -> zero every cell of column 1
result    [1,0,3]
          [0,0,0]
          [6,0,8]
```

Cell `(0, 1)` is zeroed because its column is marked, and cell `(1, 0)` because its row is; the rest keep their values, producing `[[1,0,3], [0,0,0], [6,0,8]]`, which matches the expected Output for Example 2.

#### Solution

The code is the two passes of the walkthrough: one set-building scan, one zeroing scan.

```python
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        rows = set()
        cols = set()
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    rows.add(i)
                    cols.add(j)
        for i in range(m):
            for j in range(n):
                if i in rows or j in cols:
                    matrix[i][j] = 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

Two full scans of the grid, constant work per cell; the second pass is unavoidable since every cell's fate must be settled.

##### Space Complexity: `O(m + n)`

Each set holds at most one entry per row and one per column, the minimal index-level memory of the zero positions.

#### Key Insights

- The two-phase split is the whole correctness argument: nothing is written until every original zero is known, so no written zero can masquerade as an original one.
- The sets are pure index bookkeeping: a cell's fate depends only on its row and column appearing, never on where in the row or column the zero sat.
- This is the version to reach for first and the oracle for the in-place variants below.

### First-Cell Flags

#### Derivation

The row set stores one bit per row, which is small enough to live inside the matrix: `matrix[i][0]`, the first cell of row `i`, can carry row `i`'s zero flag instead of a set entry. Column `0` cannot host its own flag the same way, because `matrix[i][0]` is doing double duty as row `i`'s flag cell: a genuine zero at `(2, 0)` and a flag written for row `2` would be indistinguishable. One boolean, `first_col_has_zero`, remembers column `0` separately:

1. Record `first_col_has_zero` by scanning column `0` for any `0`.
2. Walk the interior (`j` from `1`): when `matrix[i][j] == 0`, write the flag
   `matrix[i][0] = 0` and `matrix[0][j] = 0`. Row flags live in column `0`,
   column flags in row `0`.
3. Sweep rows `1..m - 1`: when `matrix[i][0] == 0`, zero the row; when
   `matrix[0][j] == 0`, zero the column `j` cell of that row.
4. Zero row `0`'s interior when `matrix[0][0] == 0`: the flag sweep above
   starts at row `1`, so row `0`'s own flag needs this dedicated step, and it
   runs only after the sweep has consumed the column flags stored in row `0`.
5. Finally apply the column `0` verdict from `first_col_has_zero` to the whole
   first column.

#### Invariant

After the interior scan, for every row `i` and interior column `j >= 1`, the border cells hold exactly the original-zero verdicts:

```text
matrix[i][0] == 0   iff   row i contains an original 0, either an interior
                          one (some j >= 1) or at (i, 0) itself
matrix[0][j] == 0   iff   column j contains an original 0 at some i >= 1
first_col_has_zero  iff   column 0 contains an original 0
```

The first line earns its "or at `(i, 0)` itself" clause honestly: the scan never writes column `0` for `i >= 1`, so an original zero there survives untouched, and reading it as a row flag is correct because a zero at `(i, 0)` demands row `i` zeroed anyway. Column `0`'s own verdict is partitioned off into `first_col_has_zero`, read before any flag write muddies it. The application order preserves the invariant's consumption: interior cells read both flags while they are intact, row `0`'s interior is zeroed only after the column flags stored in row `0` have been read, and column `0` is applied last from the boolean. Every zeroing decision reads pre-pass truth, the two-phase guarantee of the sets version, achieved with no container.

#### Walkthrough

Run the flag scheme on Example 2: `matrix = [[1,2,3], [4,0,5], [6,7,8]]`. Column `0` holds no zero, so `first_col_has_zero` is `False`; the interior scan finds the single zero at `(1, 1)` and writes two flags:

```text
record    first_col_has_zero = False
          matrix[1][1] == 0 -> matrix[1][0] = 0   (row 1 flagged)
                            -> matrix[0][1] = 0   (col 1 flagged)
state     [1,0,3]
          [0,0,5]
          [6,7,8]
apply     row 1: matrix[1][0] == 0 -> zero the row
          col 1: matrix[0][1] == 0 -> zero (1,1), (2,1)
          row 0: matrix[0][0] == 1 -> interior stays
          col 0: first_col_has_zero = False -> stays
final     [1,0,3]
          [0,0,0]
          [6,0,8]
```

The flag writes destroyed the values `4` at `(1, 0)` and `2` at `(0, 1)`, but both were already destined to become `0` (row `1` and column `1` are both marked), so no information is lost. The final grid matches the expected Output for Example 2.

#### Solution

The code is the walkthrough's three movements: record the column-zero verdict, write interior flags into the borders, then apply flags row by row and finish the first column.

```python
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])

        # Column 0's own verdict, read before any flag write muddies it
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

        for i in range(m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    # Row i's flag lives in matrix[i][0], column j's in row 0
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # Row 0's flag is consumed last: the sweep above had to read the
        # column flags parked in row 0 first
        if matrix[0][0] == 0:
            for j in range(1, n):
                matrix[0][j] = 0

        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

A recording scan of the interior, an application sweep of the interior, and at most two linear passes over column `0`: each cell is touched a constant number of times.

##### Space Complexity: `O(1)`

One boolean; the flag storage is reclaimed from the matrix's own first row and column.

#### Key Insights

- The double-duty problem is the crux: column `0` cannot both hold row flags and remember its own zeros, and splitting those two roles is what turns `O(m + n)` space into `O(1)`.
- Reading `first_col_has_zero` before any flag writes is not caution but necessity: a zero at `(2, 0)` would be overwritten by row `2`'s flag if the verdict were deferred.
- Row `0` needs its own application step because the flag sweep starts at row `1`, and that step must wait until the column flags parked in row `0` have been read; zeroing row `0` first would flood every column flag to `0` and wrongly zero unmarked columns.

### First Row and Column as Flags

#### Derivation

The First-Cell Flags version leans on one boolean because column `0` is both data and flag storage, and row `0` quietly plays the same double role there. Make the double role explicit instead of splitting it: reserve `matrix[0][j]` as the flag for column `j` and `matrix[i][0]` as the flag for row `i`, exactly as before, and keep the two border originals out of the flag business entirely, each summarized by its own boolean verdict read up front. The structure is now symmetric and self-documenting: the interior flags live in the matrix's own borders, which act as the row and column sets of the first solution:

1. Read the border verdicts before anything is written: `first_row_has_zero`
   scans row `0` for any `0`, and `first_col_has_zero` scans column `0`. Both
   must be settled first because the interior scan writes flags into the
   borders and would bury the original zeros it is about to summarize.
2. Interior scan (`i >= 1`, `j >= 1`): a `0` at `(i, j)` sets
   `matrix[i][0] = 0` and `matrix[0][j] = 0`.
3. Sweep the interior using the flags.
4. Apply the two border verdicts: zero row `0` when `first_row_has_zero`, and
   zero column `0` when `first_col_has_zero`. `(0, 0)` sits in both ranges,
   which is exactly what an original zero there demands.

#### Walkthrough

Run the symmetric scheme on Example 1: `matrix = [[0,1], [1,0]]`, where every zero sits on a border, the case that distinguishes this version's bookkeeping:

```text
record    row 0 scan: 0 at (0,0)    -> first_row_has_zero = True
          column 0 scan: 0 at (0,0) -> first_col_has_zero = True
          interior: 0 at (1,1)      -> matrix[1][0] = 0, matrix[0][1] = 0
state     [0,0]   the flag writes consumed the 1s at (0,1) and (1,0),
          [0,0]   both already destined for 0 (row 1 and col 1 flagged)
apply     interior: row 1 and col 1 flagged -> (1,1) stays 0
          first_row_has_zero  -> zero row 0 (already 0)
          first_col_has_zero  -> zero column 0 (already 0)
final     [0,0]
          [0,0]
```

The border zero at `(0, 0)` was consumed as two verdicts rather than flags, and both rulings fire. The interior zero at `(1, 1)` wrote its two flags over the `1`s at `(1, 0)` and `(0, 1)`, a safe destruction because row `1` and column `1` are flagged, so both cells were headed for `0`. The matrix ends at `[[0,0], [0,0]]`, matching the expected Output for Example 1.

#### Solution

The code is the symmetric flag scheme: two border verdicts, an interior flag scan, and a three-part application.

```python
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])

        # Both verdicts read before any flag write buries the originals
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    # Row i's flag in column 0, column j's flag in row 0
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0
        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

Interior record and apply sweeps plus three linear border passes; constant work per cell.

##### Space Complexity: `O(1)`

Two booleans; the flags occupy the matrix's own first row and column.

#### Key Insights

- Both border verdicts are whole-border scans, not single-cell reads: a zero at `(0, 2)` must zero row `0` just as much as a zero at `(0, 0)`, and collapsing the verdict to `matrix[0][0]` would miss it.
- `(0, 0)` belongs to both borders, which is why the symmetry is imperfect in what it costs (two booleans) but perfect in what it says: an original zero there demands both borders zeroed, and both verdicts fire.
- The verdicts must be read before the interior scan runs: an interior zero writes flags into the borders and would corrupt verdicts read afterward.
- This is the form to reconstruct in an interview: one story, "the borders are the sets", covers the recording, the application, and the corner case.

## Comparison of Solutions

The practice harness's `practice/set_matrix_zeroes/reference.py` implements the **First Row and Column as Flags** solution.

### Time Complexity

- **Extra Row and Column Sets**: `O(m * n)` - two full scans, one recording and one applying.
- **First-Cell Flags**: `O(m * n)` - interior scans plus two column-zero passes.
- **First Row and Column as Flags**: `O(m * n)` - interior scans plus three border passes.

### Space Complexity

- **Extra Row and Column Sets**: `O(m + n)` - one set entry per marked row and column.
- **First-Cell Flags**: `O(1)` - a single boolean; row and column flags live in the matrix.
- **First Row and Column as Flags**: `O(1)` - two border booleans; all other flags live in the matrix.

### Trade-offs

- **Extra Row and Column Sets**: The transparent two-phase design that is easiest to trust and extend, at the cost of index-level auxiliary memory.
- **First-Cell Flags**: One boolean shy of full symmetry, with the column-zero case handled out of band; slightly trickier than the symmetric version for the same asymptotics.
- **First Row and Column as Flags**: The same `O(1)` space in one coherent scheme, at the price of ordering rules (verdicts before flags) that must be honored exactly.

### When to Use Each

- **Extra Row and Column Sets**: First implementation and the test oracle; also right when auxiliary space is unconstrained and review clarity dominates.
- **First-Cell Flags**: When the `O(1)` space is required and the row-flag-first framing feels more natural than the symmetric borders story.
- **First Row and Column as Flags** (recommended): The default under the follow-up's `O(1)` constraint; one mental model, the borders are the sets, drives every line.

### Optimization Notes

- All three versions are `O(m * n)` time; the optimization axis is space only, from `O(m + n)` down to `O(1)`, and the ladder runs exactly through the solutions above.
- The verdict-before-flags ordering is the one landmine: reading `matrix[0][0]` or scanning column `0` after the interior scan would mistake a freshly written flag for an original zero and over-zero a border.
- The Follow-up's tighter `O(1)` variants that flag rows and columns with sentinel values during a single scan trade clarity for one fewer pass and are easy to get subtly wrong; the two-phase shape is the reliable core.

