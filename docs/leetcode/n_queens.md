# [N Queens](https://leetcode.com/problems/n-queens/)

**Hard** | **40 minutes** | **Array, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation)

**Practice:** [`practice/n_queens/solution.py`](../../practice/n_queens/solution.py)

The **n-queens** puzzle is the problem of placing `n` queens on an `n x n` chessboard so that no two queens can attack each other.

A **queen** in a chessboard can attack horizontally, vertically, and diagonally.

Given an integer `n`, return all distinct solutions to the **n-queens puzzle**.

Each solution contains a unique board layout where the queen pieces are placed. `'Q'` indicates a queen and `'.'` indicates an empty space.

You may return the answer in **any order**.

## Examples

### Example 1

**Input:** `n = 4`

**Output:** `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`

**Explanation:** There are two different solutions to the 4-queens puzzle.

### Example 2

**Input:** `n = 1`

**Output:** `[["Q"]]`

## Constraints

- `1 <= n <= 8`

## Deriving the Solution

A queen attacks along its row, its column, and both diagonals, so a valid board is exactly one where no two placed queens share any of those lines. That turns "place `n` queens" into "choose one column per row," and every solution below searches those column assignments; they differ in when the attack test runs.

1. **Start literal.** Every row picks any of the `n` columns, and a fully
   built board is validated pairwise. `n^n` boards, each checked in `O(n²)`:
   see [Brute Force](#brute-force).
2. **Spot the waste.** Two queens in one column attack each other just as
   surely as two in one row, so the columns are necessarily all distinct:
   the candidates are the `n!` permutations of the columns, not `n^n`
   assignments: see [Permutations Library](#permutations-library).
3. **Test as you place.** Even a permutation generator completes boards that
   died three rows earlier; checking each queen the moment it is placed and
   abandoning the branch immediately is [backtracking](https://en.wikipedia.org/wiki/Backtracking),
   with three sets answering "is this cell attacked?" in constant time:
   see [Row-by-Row Backtracking](#row-by-row-backtracking).
4. **Squeeze the constants.** The three sets are membership tests over
   `2n + n` lines of the board, a natural fit for bitmasks, where one shift
   per row replaces per-candidate set updates: see
   [Bitmask Backtracking](#bitmask-backtracking).

## Solutions

### Brute Force

#### Derivation

The most literal reading of "place `n` queens so none attack" builds every possible placement and asks of each finished board whether it is valid. Because a queen attacks along its whole row, two queens can never share a row, which fixes the shape of a candidate: one queen per row, `n` rows, each row free to pick any of the `n` columns:

1. Build `queens`, a list where `queens[r]` is the column of the queen in row
   `r`, trying every column for every row.
2. When `row == n`, the board is complete: validate it pairwise.
3. `is_valid` compares every pair of rows `r1`, `r2` and rejects the board
   when `queens[r1] == queens[r2]` (same column) or
   `abs(r1 - r2) == abs(queens[r1] - queens[r2])` (same diagonal).
4. Render each valid board into its `.`/`Q` strings.

#### Walkthrough

Trace the search on Example 1: `n = 4`. The assignment tree holds `4^4 = 256` leaves, and the first leaf to survive `is_valid` is `queens = [1, 3, 0, 2]`; hundreds of earlier leaves die in the pairwise check. Trace that survivor's validation:

```text
queens [1, 3, 0, 2]
  rows 0,1  cols 1,3   column ok   |0-1|=1 vs |1-3|=2  diagonal ok
  rows 0,2  cols 1,0   |0-2|=2 vs |1-0|=1   ok
  rows 0,3  cols 1,2   |0-3|=3 vs |1-2|=1   ok
  rows 1,2  cols 3,0   |1-2|=1 vs |3-0|=3   ok
  rows 1,3  cols 3,2   |1-3|=2 vs |3-2|=1   ok
  rows 2,3  cols 0,2   |2-3|=1 vs |0-2|=2   ok  -> valid
```

Rendering gives `[".Q..", "...Q", "Q...", "..Q."]`, the first of Example 1's two outputs. The second, `queens = [2, 0, 3, 1]`, is found the same way later in the enumeration, and for `n = 4` no third assignment survives. An earlier leaf shows the rejection path: `queens = [0, 2, 3, 1]` fails the moment the pair `(row 1, row 2)` compares `|1 - 2| = 1` against `|2 - 3| = 1`, both queens on one diagonal.

#### Solution

The code is the exhaustive assignment tree with the pairwise check at each leaf.

```python
from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        def is_valid(queens: List[int]) -> bool:
            for r1 in range(n):
                for r2 in range(r1 + 1, n):
                    same_column = queens[r1] == queens[r2]
                    same_diagonal = abs(r1 - r2) == abs(queens[r1] - queens[r2])
                    if same_column or same_diagonal:
                        return False
            return True

        boards: List[List[str]] = []

        def build(row: int, queens: List[int]) -> None:
            if row == n:
                if is_valid(queens):
                    boards.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
                return
            for col in range(n):
                build(row + 1, queens + [col])

        build(0, [])
        return boards
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^n * n²)`

The assignment tree has `n^n` leaves, and each completed board costs a pairwise validation over `O(n²)` row pairs.

##### Space Complexity: `O(n²)`

The recursion holds one `queens` list per depth level (each call builds `queens + [col]`, a copy), so the path retains `1 + 2 + ... + n` entries.

#### Key Insights

- The one-queen-per-row observation is what makes the search a choice of
  columns; without it the candidate space is `n^(n²)`.
- Validation is delayed to the leaf, so the search keeps building boards
  through rows that were already doomed.
- Correct but only usable for tiny `n`: `n = 8` already means 16.7 million
  leaves before validation.

### Permutations Library

#### Derivation

The brute force rejects boards that put two queens in one column, but that outcome was decided the moment the second queen took an occupied column: distinct columns are forced, so the candidates are the permutations of `0..n-1` rather than all `n^n` assignments. Generating permutations by hand is bookkeeping; [`itertools.permutations`](https://docs.python.org/3/library/itertools.html#itertools.permutations) yields each `queens` tuple directly, and only the diagonal test remains:

1. For each `queens` in `permutations(range(n))` (distinct columns by
   construction):
2. reject it when any two rows `a`, `b` satisfy
   `abs(a - b) == abs(queens[a] - queens[b])`;
3. otherwise render and record the board.

#### Walkthrough

`permutations(range(4))` yields the 24 column tuples in lexicographic order; the tuples before the first survivor all die in the diagonal test. Trace that first survivor, `queens = [1, 3, 0, 2]`, through the pairwise test:

```text
a=0 b=1  cols 1,3   |0-1|=1 vs |1-3|=2  ok
a=0 b=2  cols 1,0   |0-2|=2 vs |1-0|=1  ok
a=0 b=3  cols 1,2   |0-3|=3 vs |1-2|=1  ok
a=1 b=2  cols 3,0   |1-2|=1 vs |3-0|=3  ok
a=1 b=3  cols 3,2   |1-3|=2 vs |3-2|=1  ok
a=2 b=3  cols 0,2   |2-3|=1 vs |0-2|=2  ok  -> valid
```

Every pair clears, so the board `[".Q..", "...Q", "Q...", "..Q."]` is recorded, matching the first output of Example 1.

#### Solution

The code is the permutation loop with the pairwise diagonal test folded into one `all`.

```python
from itertools import permutations
from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        boards: List[List[str]] = []
        for queens in permutations(range(n)):
            if all(
                abs(a - b) != abs(queens[a] - queens[b])
                for a in range(n)
                for b in range(a + 1, n)
            ):
                boards.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
        return boards
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! * n²)`

`n!` permutations are generated, each validated over `O(n²)` row pairs.

##### Space Complexity: `O(n)`

One permutation tuple at a time (plus the output).

#### Key Insights

- Distinct columns are a theorem, not a search choice: two queens in one
  column always attack, so permutations cut `n^n` to `n!`.
- The diagonal test is unchanged from the brute force; only the candidate
  generation shrank.
- Still a build-then-validate loop: a permutation that died on row 2 is
  enumerated in full.

### Row-by-Row Backtracking

#### Derivation

The permutation loop's waste is the mirror of the brute force's: it walks every `n!` tuple even when the first two rows already attack. Testing each placement the moment it is made abandons a doomed branch at the row that killed it. The bookkeeping that makes the test constant-time is three sets mirroring the board's lines: `columns` (one per column), `positive_diagonals` (the `/` diagonals, indexed by `row + col`), and `negative_diagonals` (the `\` diagonals, indexed by `row - col`); two cells attack each other exactly when they share an index in one of the three:

1. Recurse row by row, keeping `queens` (the column chosen per row) and the
   three sets.
2. At `row == n`, render the completed `queens` into board strings.
3. Otherwise try each `col` in `range(n)`; skip it when `col in columns`,
   `row + col in positive_diagonals`, or `row - col in negative_diagonals`.
4. On a pass, add the three indices, append `col`, recurse, then undo all
   four changes so the sibling columns see a clean state.

#### Walkthrough

Trace the backtracking on Example 1: `n = 4`, columns tried left to right. Each line shows the candidate and the sets' verdict; `queens` is the current column stack:

```text
row 0  col 0  place  queens [0]
row 1  col 0  column attacked   col 1  diagonal attacked   col 2  place  queens [0, 2]
row 2  col 0..3  all attacked -> dead end, undo row 1
row 1  col 3  place  queens [0, 3]
row 2  col 0  attacked   col 1  place  queens [0, 3, 1]
row 3  col 0..3  all attacked -> undo row 2; col 2, col 3 attacked -> undo row 1; exhausted -> undo row 0
row 0  col 1  place  queens [1]
row 1  col 0, 1, 2  attacked   col 3  place  queens [1, 3]
row 2  col 0  place  queens [1, 3, 0]
row 3  col 0, 1  attacked   col 2  place  queens [1, 3, 0, 2]
row 4 == n -> record [1, 3, 0, 2]
```

The recorded board renders as `[".Q..", "...Q", "Q...", "..Q."]`, Example 1's first output. Continuing the same walk from `row 3 col 3` eventually unwinds to `row 0 col 2` and records `[2, 0, 3, 1]`, the second output; the search then exhausts. Every verdict above falls out of the three indices: for instance `row 1 col 1` under `queens [0]` fails because it shares `row - col = 0` with the queen at `(0, 0)`, while `row 2 col 1` under `queens [0, 3]` passes because the queens hold `row + col` in `{0, 4}`, `row - col` in `{0, -2}`, and column `1` is unclaimed.

#### Solution

The code is the walkthrough's row loop with place-recurse-undo around each candidate.

```python
from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        columns = set()
        positive_diagonals = set()  # row + col indexes the "/" diagonals
        negative_diagonals = set()  # row - col indexes the "\" diagonals
        queens: List[int] = []
        boards: List[List[str]] = []

        def backtrack(row: int) -> None:
            if row == n:
                boards.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
                return
            for col in range(n):
                attacked = (
                    col in columns
                    or row + col in positive_diagonals
                    or row - col in negative_diagonals
                )
                if attacked:
                    continue
                columns.add(col)
                positive_diagonals.add(row + col)
                negative_diagonals.add(row - col)
                queens.append(col)
                backtrack(row + 1)
                columns.remove(col)
                positive_diagonals.remove(row + col)
                negative_diagonals.remove(row - col)
                queens.pop()

        backtrack(0)
        return boards
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n!)`

Row 0 has `n` candidates, a surviving row at most `n - 1`, and so on; the three constant-time set tests per candidate prune the permutation tree without changing its shape. Rendering a found board is `O(n²)` but happens once per solution.

##### Space Complexity: `O(n)`

The recursion depth and the three sets are each bounded by `n` (plus the output).

#### Key Insights

- The diagonal trick: `row + col` is constant along a `/` diagonal and
  `row - col` along a `\`, so three integers per candidate decide attack in
  `O(1)`.
- Undo is what makes shared state safe: the sets are global to the search,
  so every recursive call must restore them.
- This is the canonical n-queens solution; the remaining variants only
  change how the same three tests are stored.

### Bitmask Backtracking

#### Derivation

The set version pays hashing and set updates per candidate. Each set's membership domain is tiny and shifts predictably row by row: the `/` diagonals available in the next row are this row's occupied `/` indices shifted one step left, and the `\` diagonals one step right. Three integers hold all three families (`1 << col` marks column `col`), and the free columns of the current row are the complement of their union, masked to `n` bits:

1. `blocked = columns | positive_diagonals | negative_diagonals`;
   `open_columns = ~blocked & ((1 << n) - 1)` lists the legal columns.
2. Peel the lowest set bit with `col_bit = open_columns & -open_columns`,
   clear it, and recover `col = col_bit.bit_length() - 1`.
3. Recurse with `columns | col_bit`, `(positive_diagonals | col_bit) << 1`,
   and `(negative_diagonals | col_bit) >> 1`: the shifts carry each
   diagonal into its neighbor row's index.
4. At `row == n`, render `queens` as before.

#### Walkthrough

Trace the first path on Example 1: `n = 4`, bit `i` standing for column `i`. Each row's `union` is `columns | positive_diagonals | negative_diagonals`, and `open` is its complement within the low 4 bits; the lowest set bit of `open` always drives the descent:

```text
row 0  union 0b0000   open 0b1111   take col 0   queens [0]
row 1  union 0b0011   open 0b1100   take col 2   queens [0, 2]
row 2  union 0b1111   open 0b0000   dead end, backtrack
row 1  next open bit  take col 3    queens [0, 3]
row 2  union 0b11101  open 0b0010   take col 1   queens [0, 3, 1]
row 3  union 0b101111 open 0b0000   dead end, backtrack past row 1 to row 0
row 0  next open bit  take col 1    queens [1]
row 1  union 0b0111   open 0b1000   take col 3   queens [1, 3]
row 2  union 0b11110  open 0b0001   take col 0   queens [1, 3, 0]
row 3  union 0b111011 open 0b0100   take col 2   queens [1, 3, 0, 2]
row 4 == n -> record [1, 3, 0, 2]
```

The descent order is exactly the set version's: `col 0` dies twice, then `col 1` reaches `row 4` with `[1, 3, 0, 2]`, rendering `[".Q..", "...Q", "Q...", "..Q."]`, Example 1's first output. The shifts are visible in the unions: at `row 2` under `queens [0, 2]` the `positive_diagonals` carry is `(0b0010 | 0b0100) << 1 = 0b1100`, which is what closes every column at once.

#### Solution

The code is the same row-by-row walk with the three sets folded into three shifting integers.

```python
from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        boards: List[List[str]] = []
        queens: List[int] = []

        def backtrack(
            row: int, columns: int, positive_diagonals: int, negative_diagonals: int
        ) -> None:
            if row == n:
                boards.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
                return
            open_columns = (
                ~(columns | positive_diagonals | negative_diagonals)
            ) & ((1 << n) - 1)
            while open_columns:
                col_bit = open_columns & -open_columns
                open_columns ^= col_bit
                col = col_bit.bit_length() - 1
                queens.append(col)
                backtrack(
                    row + 1,
                    columns | col_bit,
                    (positive_diagonals | col_bit) << 1,
                    (negative_diagonals | col_bit) >> 1,
                )
                queens.pop()

        backtrack(0, 0, 0, 0)
        return boards
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n!)`

The pruned tree is identical to the set version; each candidate now costs a few integer ops instead of three hashed membership tests.

##### Space Complexity: `O(n)`

Three integers and the `queens` stack (plus the output); the state travels in the call arguments, so nothing to undo.

#### Key Insights

- Passing state as arguments replaces the undo bookkeeping: each branch
  owns its integers.
- `open_columns & -open_columns` peels the lowest set bit, iterating only
  the legal columns rather than testing all `n`.
- The shifts `(pos | bit) << 1` and `(neg | bit) >> 1` are the whole
  diagonal idea: each diagonal's index moves one column over per row.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^n * n²)` - every column assignment built, then validated pairwise.
- **Permutations Library**: `O(n! * n²)` - distinct columns enforced, validation unchanged.
- **Row-by-Row Backtracking**: `O(n!)` - constant-time attack tests prune mid-construction.
- **Bitmask Backtracking**: `O(n!)` - same tree, cheaper per-candidate constants.

### Space Complexity

- **Brute Force**: `O(n²)` - one copied column list per depth level along the recursion path.
- **Permutations Library**: `O(n)` - one permutation tuple at a time.
- **Row-by-Row Backtracking**: `O(n)` - recursion depth plus three sets.
- **Bitmask Backtracking**: `O(n)` - recursion depth plus three integers; no set or dict overhead.

### Trade-offs

- The Brute Force needs no insights beyond "how queens attack," but `n^n`
  growth caps it around `n = 5`.
- The Permutations Library is the shortest correct code in the file and the
  clearest statement of the distinct-columns theorem; it still finishes
  boards it should have abandoned.
- Row-by-Row Backtracking is the canonical interview answer: pruned,
  constant-time tests, and easy to extend (count solutions, print one).
- Bitmask Backtracking buys a real constant factor (about `4-5x` by
  `n = 12` on CPython) at the cost of bit-level readability.

### When to Use Each

- **Brute Force**: as the derivation's first step; in practice only to
  cross-check tiny boards.
- **Permutations Library**: when `n` is tiny and code length matters more
  than speed.
- **Row-by-Row Backtracking**: the default: clear, pruned, and the version
  interviewers expect (recommended here).
- **Bitmask Backtracking**: when `n` grows past what the set version
  handles comfortably (competition sizes, counting all solutions).

### Optimization Notes

- Symmetry halves the work twice: mirror boards come in pairs, so searching
  only half of row 0's columns and mirroring the results doubles throughput
  (not implemented above).
- The `row - col` diagonal can be kept non-negative by offsetting with `n - 1`;
  Python's negative integers already make the plain difference a valid dict
  or set key.
- Bitmask state passed as arguments removes all undo logic; with sets, the
  add/recurse/remove discipline is the correctness-critical part.
