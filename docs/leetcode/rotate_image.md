# [Rotate Image](https://leetcode.com/problems/rotate-image/)

**Medium** | **25 minutes** | **Array, Math, Matrix**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix) · [Transpose](https://en.wikipedia.org/wiki/Transpose) · [In-place algorithm](https://en.wikipedia.org/wiki/In-place_algorithm)

**Practice:** [`practice/rotate_image/solution.py`](../../practice/rotate_image/solution.py)

Given a square `n x n` matrix of integers `matrix`, rotate it by 90 degrees *clockwise*.

You must rotate the matrix *in-place*. Do not allocate another 2D matrix and do the rotation.

## Examples

### Example 1

**Input:**

```text
matrix = [
  [1,2],
  [3,4]
]
```

**Output:**

```text
[
  [3,1],
  [4,2]
]
```

### Example 2

**Input:**

```text
matrix = [
  [1,2,3],
  [4,5,6],
  [7,8,9]
]
```

**Output:**

```text
[
  [7,4,1],
  [8,5,2],
  [9,6,3]
]
```

## Constraints

- `n == matrix.length == matrix[i].length`
- `1 <= n <= 20`
- `-1000 <= matrix[i][j] <= 1000`

## Deriving the Solution

A 90-degree rotation moves every cell to a new address without creating or destroying a value, so the whole problem is bookkeeping: the cell at row `i`, column `j` after the rotation must hold the value that sat at row `n - 1 - j`, column `i` before it. Every approach below is a scheme for readdressing all `n * n` values, and they differ only in how much scratch space they need to avoid overwriting a value before its last read.

1. **Start literal.** Build the rotated grid in scratch: `rotated[i][j]` takes
   `matrix[n - 1 - j][i]`, then copy the grid back into the original object.
   Correct, but it allocates a second `n x n` matrix: see
   [Brute Force with an Extra Matrix](#brute-force-with-an-extra-matrix).
2. **Spot the waste.** The scratch grid exists only so no value is lost
   mid-move. But a rotation moves values in closed four-cell cycles, and four
   cells can trade places using a single temporary, ring by ring: see
   [Layer-by-Layer Four-Way Swap](#layer-by-layer-four-way-swap).
3. **Compose two cheap passes.** A 90-degree clockwise turn is a transpose
   (mirror across the main diagonal) followed by reversing every row; both are
   pure index bookkeeping over the original storage: see
   [Transpose then Reverse Rows](#transpose-then-reverse-rows).
4. **Hand the bookkeeping to the language.** The same read-bottom-up,
   write-as-columns move is one `zip` over the reversed rows, assigned back
   through a slice to keep the mutation in place: see
   [Slice-and-Zip One-Liner](#slice-and-zip-one-liner).

## Solutions

### Brute Force with an Extra Matrix

#### Derivation

The most literal reading rotates the matrix by building its rotated twin: the value that ends up at row `i`, column `j` must come from the cell that the rotation carries there. Reading the examples, row `i` of the result is the input's column `i` read bottom to top, so the source of `rotated[i][j]` is `matrix[n - 1 - j][i]`:

1. Allocate `rotated`, a fresh `n x n` grid.
2. Fill every cell with the index map
   `rotated[i][j] = matrix[n - 1 - j][i]`.
3. Copy `rotated` back into `matrix` through a slice assignment, so the
   caller's object holds the rotation and the method returns nothing.

The scratch grid is what makes the map safe: a single in-place write such as `matrix[0][0] = matrix[n - 1][0]` destroys the value `1` before the map reaches `rotated[2][0]` and needs it. With reads and writes landing in different storage, every cell can be computed in any order and nothing is lost.

#### Walkthrough

Build the rotated grid for Example 2: `matrix = [[1,2,3], [4,5,6], [7,8,9]]`, so `n = 3`. Row by row, `rotated[i][j]` reads `matrix[n - 1 - j][i]`, which walks column `i` of the input from the bottom up:

```text
rotated[0] = [matrix[2][0], matrix[1][0], matrix[0][0]] = [7, 4, 1]
rotated[1] = [matrix[2][1], matrix[1][1], matrix[0][1]] = [8, 5, 2]
rotated[2] = [matrix[2][2], matrix[1][2], matrix[0][2]] = [9, 6, 3]
```

Copying `rotated` back leaves `matrix = [[7,4,1], [8,5,2], [9,6,3]]`, matching the expected Output for Example 2. Each result row is an input column read bottom-up, which is the rotation in one sentence.

#### Solution

The code is the index map written twice: once into the scratch grid, once back.

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        rotated = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                # Column i read bottom-up becomes row i
                rotated[i][j] = matrix[n - 1 - j][i]
        # Slice assignment mutates the caller's matrix in place
        matrix[:] = rotated
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every one of the `n * n` cells is computed once and copied once, constant work each.

##### Space Complexity: `O(n^2)`

The `rotated` grid is a full second copy of the matrix, which the problem statement rules out for the final answer; it serves here as the correctness baseline the later approaches climb down from.

#### Key Insights

- The index map `(i, j) <- (n - 1 - j, i)` is the entire algorithm: everything else in this file computes the same relocation without the scratch grid.
- Copying back through `matrix[:] = rotated` keeps the caller's object identity while replacing its contents, honoring the in-place contract the statement demands.
- The scratch copy is also the cleanest oracle: every later approach is checked against it on small inputs before trusting the in-place arithmetic.

### Layer-by-Layer Four-Way Swap

#### Derivation

The extra grid exists so that no value is overwritten before its last read. Watch what the rotation actually does to a single cell, though: `(i, j)` travels to `(j, n - 1 - i)`, whose occupant travels to `(n - 1 - i, n - 1 - j)`, then to `(n - 1 - j, i)`, and the fourth hop lands back at `(i, j)`. Values move in closed four-cell cycles, and four cells can trade places with one temporary, no grid:

1. Peel the matrix into concentric rings. Ring `first` spans rows and columns
   `first..last` with `last = n - 1 - first`; loop `first` over `0..n // 2 - 1`.
2. Walk the ring's top edge with `offset` from `0` to `last - first - 1`; the
   four cells at the corners of one square are
   `(first, first + offset)`, `(first + offset, last)`,
   `(last, last - offset)`, and `(last - offset, first)`.
3. Cycle them with one `temp`: top takes the left cell's value, left takes
   bottom, bottom takes right, right takes the saved top.
4. Rings overlap only at the center cell for odd `n`, which is a fixed point
   the loops never double-write.

#### Invariant

Write `rot(p)` for the address the rotation assigns to cell `p`: `rot((i, j)) = (j, n - 1 - i)`. The four addresses the swap touches are one orbit of `rot`, cycled so that every cell receives exactly the value `rot` sends it:

$$ (i,\ j)\ \xrightarrow{\ \text{rot}\ }\ (j,\ n{-}1{-}i)\ \xrightarrow{\ \text{rot}\ }\ (n{-}1{-}i,\ n{-}1{-}j)\ \xrightarrow{\ \text{rot}\ }\ (n{-}1{-}j,\ i)\ \xrightarrow{\ \text{rot}\ }\ (i,\ j) $$

```text
top    (i, j)             <- left   (n - 1 - j, i)
left   (n - 1 - j, i)     <- bottom (n - 1 - i, n - 1 - j)
bottom (n - 1 - i, n - 1 - j) <- right (j, n - 1 - i)
right  (j, n - 1 - i)     <- top    (i, j),   saved in temp first
```

Every ring cell belongs to exactly one such orbit and the loop settles each orbit once, so after all rings each cell holds its rotated value; nothing is read after being overwritten because the only value destroyed mid-swap is the one already parked in `temp`.

#### Walkthrough

Rotate Example 2: `matrix = [[1,2,3], [4,5,6], [7,8,9]]`, so `n = 3`, one real ring with `first = 0` and `last = 2`, and the center `5` is a fixed point. Each row below shows the ring after one four-way swap, with `temp` read from the top edge:

```text
start            [1,2,3]     offset 0: temp = m[0][0] = 1
                 [4,5,6]     m[0][0] <- m[2][0] = 7, m[2][0] <- m[2][2] = 9
                 [7,8,9]     m[2][2] <- m[0][2] = 3, m[0][2] <- temp = 1
after offset 0   [7,2,1]
                 [4,5,6]
                 [9,8,3]
after offset 1   [7,4,1]     offset 1: temp = m[0][1] = 2
                 [8,5,2]     m[0][1] <- m[1][0] = 4, m[1][0] <- m[2][1] = 8
                 [9,6,3]     m[2][1] <- m[1][2] = 6, m[1][2] <- temp = 2
```

Both offsets settle, the ring is fully rotated, and the untouched center `5` stays put, leaving `matrix = [[7,4,1], [8,5,2], [9,6,3]]`, matching the expected Output for Example 2. Four swaps moved twelve values with one temporary, and the scratch grid of the Brute Force never appeared.

#### Solution

The code is the walkthrough's ring loop with the four-way swap as its body.

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for first in range(n // 2):
            last = n - 1 - first
            for offset in range(last - first):
                # One temp settles the four-cell cycle losslessly:
                # top <- left <- bottom <- right <- saved top
                temp = matrix[first][first + offset]
                matrix[first][first + offset] = matrix[last - offset][first]
                matrix[last - offset][first] = matrix[last][last - offset]
                matrix[last][last - offset] = matrix[first + offset][last]
                matrix[first + offset][last] = temp
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

There are `n // 2` rings and the ring at depth `first` walks `4 * (n - 1 - 2 * first)` cells, a geometric-style sum that totals one visit per matrix cell.

##### Space Complexity: `O(1)`

One `temp` variable, regardless of `n`; the values circulate through the matrix's own storage.

#### Key Insights

- The four-way swap is the answer to "how do you rotate in place without losing values": rotate in orbits, not cells, and one temporary covers a whole orbit.
- `range(last - first)` on the top edge is the exact cell count that keeps each orbit untouched after it settles; including the corner twice would rotate the corner's orbit two steps at once and corrupt the ring.
- The center cell of an odd-sized matrix never enters a loop: it is the one orbit of size one, which is why the arithmetic needs no special case.

### Transpose then Reverse Rows

#### Derivation

Reading the Brute Force map again, `rot((i, j)) = (j, n - 1 - i)` is a composition of two mirrors. The [transpose](https://en.wikipedia.org/wiki/Transpose) maps `(i, j) -> (j, i)` by swapping across the main diagonal; reversing each row then maps `(j, i) -> (j, n - 1 - i)`. Composed, they are exactly the rotation, and both passes are pure index bookkeeping over the original storage:

1. Transpose in place: for every pair with `j > i`, swap `matrix[i][j]` with
   `matrix[j][i]`. The `j > i` guard swaps each pair once; the diagonal stays.
2. Reverse every row in place with a two-pointer walk, `left` meeting `right`.
3. The matrix is now the 90-degree clockwise rotation; both steps commute with
   the contract because no cell is read after its overwrite inside a pass.

#### Walkthrough

Run the two passes on Example 2: `matrix = [[1,2,3], [4,5,6], [7,8,9]]`. The transpose swaps three off-diagonal pairs, `(0,1) <-> (1,0)`, `(0,2) <-> (2,0)`, and `(1,2) <-> (2,1)`, then each row flips end to end:

```text
start          [1,2,3]    transpose    [1,4,7]    reverse rows    [7,4,1]
               [4,5,6]     swaps       [2,5,8]    (left/right     [8,5,2]
               [7,8,9]    (0,1)(0,2)   [3,6,9]     walks)         [9,6,3]
                          (1,2)
```

The first transposed row `[1, 4, 7]` is the input's first column read top-down, so reversing it lands `7` in the top-left corner where the expected Output puts it. The final grid `[[7,4,1], [8,5,2], [9,6,3]]` matches the expected Output for Example 2.

#### Solution

The code is the two passes of the walkthrough: a guarded pairwise swap, then a two-pointer flip per row.

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                # j > i swaps each off-diagonal pair exactly once
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            left, right = 0, n - 1
            while left < right:
                row[left], row[right] = row[right], row[left]
                left += 1
                right -= 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The transpose performs `n * (n - 1) / 2` swaps and each row reversal does at most `n / 2` swaps, together one constant-time operation per cell.

##### Space Complexity: `O(1)`

Index variables and the swap pairs' tuple handoff only; no auxiliary structure grows with `n`.

#### Key Insights

- Decomposing the rotation into transpose plus row reversal splits one tricky index map into two passes simple enough to write without a scratch grid and without debugging corner cases.
- The `j > i` guard is what makes the transpose single-pass: swapping the full square would undo itself, mirroring every pair twice.
- `row.reverse()` is the idiomatic stand-in for the two-pointer loop and keeps the same in-place guarantee; the hand-written walk is shown once because the reversal is one of the two ideas the whole solution rests on.

### Slice-and-Zip One-Liner

#### Derivation

The Brute Force walkthrough stated the rotation in one sentence: row `i` of the result is column `i` of the input read bottom-up. Reading rows bottom-up is `matrix[::-1]`, and [`zip(*...)`](https://docs.python.org/3/library/functions.html#zip) transposes the resulting rows into columns, so the rotated rows fall out of one expression. Assigning through the slice `matrix[:]` writes the new rows into the caller's list object, keeping the in-place contract:

1. `matrix[::-1]` lists the rows from the last to the first, without copying
   the rows themselves.
2. `zip(*matrix[::-1])` gathers position `i` of every reversed row, which is
   column `i` read bottom-up: the rotated row `i`, as a tuple.
3. `list(row)` materializes each tuple back into a mutable row, and
   `matrix[:] = ...` replaces the contents of the original list in place.

#### Walkthrough

Run the expression on Example 1: `matrix = [[1,2], [3,4]]`.

```text
matrix[::-1]      rows bottom-up:          [3,4], [1,2]
zip(*...)         column 0, column 1:      (3, 1), (4, 2)
list per row      materialized rows:       [3, 1], [4, 2]
matrix[:] = ...   contents replaced:       [[3,1], [4,2]]
```

Column `0` of the reversed listing, `3` above `1`, becomes row `0`, so the grid ends at `[[3,1], [4,2]]`, matching the expected Output for Example 1. The expression is the Brute Force map, with `zip` doing the index arithmetic.

#### Solution

One expression, with the slice assignment carrying the in-place obligation.

```python
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        matrix[:] = [list(row) for row in zip(*matrix[::-1])]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every cell is read once by the `zip` and written once by the slice assignment.

##### Space Complexity: `O(n^2)`

The comprehension materializes all `n` rotated rows before the assignment; this is the Brute Force's scratch grid, compressed into a temporary.

#### Key Insights

- `zip(*rows)` is Python's transpose, and transposing the bottom-up listing is the clockwise rotation: the one-liner is readable precisely because the index map was derived honestly in the Brute Force.
- The slice in `matrix[:] = ...` is not decoration: plain `matrix = ...` would rebind a local name and leave the caller's matrix untouched, failing the in-place contract.
- The new rows are fresh list objects, so aliasing concerns from the original rows disappear, which is a subtle behavior change from the true in-place passes worth knowing when callers hold references to individual rows.

## Comparison of Solutions

The practice harness's `practice/rotate_image/reference.py` implements the **Transpose then Reverse Rows** solution.

### Time Complexity

- **Brute Force with an Extra Matrix**: `O(n^2)` - one map fill plus one copy-back, constant work per cell.
- **Layer-by-Layer Four-Way Swap**: `O(n^2)` - each cell is written exactly once across all rings.
- **Transpose then Reverse Rows**: `O(n^2)` - a triangular transpose sweep plus per-row reversals.
- **Slice-and-Zip One-Liner**: `O(n^2)` - one `zip` read and one slice write over all cells.

### Space Complexity

- **Brute Force with an Extra Matrix**: `O(n^2)` - the full scratch grid.
- **Layer-by-Layer Four-Way Swap**: `O(1)` - one temporary per four-cell orbit.
- **Transpose then Reverse Rows**: `O(1)` - index variables and pairwise swaps only.
- **Slice-and-Zip One-Liner**: `O(n^2)` - the comprehension's row list, freed after the assignment.

### Trade-offs

- **Brute Force with an Extra Matrix**: The trivially correct baseline and a natural oracle, but it spends a full second matrix, which the statement forbids for the real answer.
- **Layer-by-Layer Four-Way Swap**: True constant space in one pass, but the four index expressions are error-prone to reconstruct in an interview and to review afterward.
- **Transpose then Reverse Rows**: Two passes that are each independently checkable, at the cost of touching every cell's swap partner rather than each cell once.
- **Slice-and-Zip One-Liner**: The shortest expression of the map, but it allocates the very scratch structure the statement bans and hides the mechanics behind `zip`.

### When to Use Each

- **Brute Force with an Extra Matrix**: While designing, as the reference the in-place candidates are tested against on small inputs.
- **Layer-by-Layer Four-Way Swap**: When a strict one-pass constant-space requirement is stated and the ring arithmetic can be checked carefully.
- **Transpose then Reverse Rows** (recommended): The default; two memorable primitives, constant space, and each pass is verifiable on its own.
- **Slice-and-Zip One-Liner**: In idiomatic application code, where the in-place constraint does not exist and clarity by brevity wins.

### Optimization Notes

- The two in-place passes do roughly twice the writes of the ring swap's single pass, but both are `O(n^2)`; cache behavior favors the transpose's row-major inner loop over the ring walk's strided corners.
- Counter-clockwise rotation is the family's mirror image: transpose then reverse each column, or equivalently reverse each row first and then transpose; the ring swap flips its cycle direction.
- For an arbitrary `k`-step rotation on a `n x n` matrix, reduce `k` modulo `4` and apply the clockwise passes `k` times, since four quarter-turns compose to the identity.
- `zip(*matrix[::-1])` produces tuples, so rows must be materialized with `list(...)` before assignment; assigning tuples into `matrix[:]` would quietly change the matrix's row types.

