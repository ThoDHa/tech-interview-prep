# [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/)

**Medium** | **25 minutes** | **Array, Binary Search, Matrix**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/search_a_2d_matrix/solution.py`](../../practice/search_a_2d_matrix/solution.py)

You are given an `m x n` 2-D integer array `matrix` and an integer `target`.

* Each row in `matrix` is sorted in *non-decreasing* order.
* The first integer of every row is greater than the last integer of the previous row.

Return `true` if `target` exists within `matrix` or `false` otherwise.

Can you write a solution that runs in `O(log(m * n))` time?

## Examples

### Example 1

**Input:** `matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]], target = 10`

**Output:** `true`

### Example 2

**Input:** `matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]], target = 15`

**Output:** `false`

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10000 <= matrix[i][j], target <= 10000`

## Deriving the Solution

The two row properties together mean the matrix read row by row is one sorted list of `m * n` values: each row is non-decreasing, and every row's first value exceeds the previous row's last. Every solution below exploits that flattened order; they differ in how many binary searches they need to locate `target` in it.

1. **Start literal.** Scan every cell. Linear in `m * n`, which ignores the
   sortedness the problem hands over: see [Staircase Search](#staircase-search).
2. **Two binary searches.** Binary-search the first column for the row that
   could contain `target` (last row whose first value is `<= target`), then
   binary-search that row. Two logarithmic searches: see
   [Two Binary Searches](#two-binary-searches).
3. **One virtual search.** If the flattened matrix is sorted, search it as a
   flat list: decode a virtual index `p` into `matrix[p // n][p % n]`. A single
   `O(log(m * n))` search, the follow-up's target: see
   [Single Binary Search](#single-binary-search).

## Solutions

### Staircase Search

#### Derivation

Before reaching for binary search, the sortedness already buys a directional walk. Start at a corner where the two sorted directions diverge: at the top-right corner, moving left decreases the values while moving down increases them. From there every comparison eliminates a full row or a full column:

1. Start at `row = 0`, `col = n - 1` (top-right).
2. If `matrix[row][col] == target`, return `true`.
3. If `matrix[row][col] > target`, the whole column `col` is too large for this
   and every lower row: move `col -= 1`.
4. If `matrix[row][col] < target`, the entire row `row` is too small: move
   `row += 1`.
5. Running off the grid means `target` is absent: return `false`.

#### Walkthrough

Trace the staircase on Example 1: `matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]]`, `target = 10`:

```text
row=0 col=3   value 8    8 < 10   eliminate row 0    -> row=1
row=1 col=3   value 13   13 > 10  eliminate col 3    -> col=2
row=1 col=2   value 12   12 > 10  eliminate col 2    -> col=1
row=1 col=1   value 11   11 > 10  eliminate col 1    -> col=0
row=1 col=0   value 10   10 == 10 -> found
```

Each step discarded a whole row or column, and the walk stayed inside the staircase shape (the cells `8, 13, 12, 11, 10` form a descending path), which is where the name comes from. It found `10` after four eliminations, matching the expected Output `true`.

#### Solution

The code is the corner walk from the walkthrough.

```python
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row, col = 0, len(matrix[0]) - 1
        while row < len(matrix) and col >= 0:
            value = matrix[row][col]
            if value == target:
                return True
            if value > target:
                # This column is too large for every remaining row
                col -= 1
            else:
                # This row is too small for the target
                row += 1
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

Every step eliminates one row or one column, so the walk has at most `m + n - 1` steps.

##### Space Complexity: `O(1)`

Only the two cursors are stored.

#### Key Insights

- The corner choice is what matters: top-left and bottom-right corners give no
  information (both neighbors are larger, or both smaller), the other two split
  the search space.
- `O(m + n)` beats `O(m * n)` but loses to binary search on tall, wide matrices.
- The same walk solves the weaker variant where rows are sorted but rows do not
  chain (LeetCode's Search a 2D Matrix II); this problem's chaining property is
  what unlocks the logarithmic solutions below.

### Two Binary Searches

#### Derivation

The staircase walk discards one row or column at a time, but the flattened order supports discarding half at once. The row that can contain `target` is the last row whose first value is `<= target`: rows are chained, so everything above is entirely smaller and everything below starts larger. Finding that row is a binary search over the first column, and checking it is a binary search over one row:

1. Binary search `col 0` over rows for the largest `row` with
   `matrix[row][0] <= target`; none means `false`.
2. Binary search `target` inside `matrix[row]`.
3. Report whether step 2 hit.

#### Walkthrough

Trace both searches on Example 2: `matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]]`, `target = 15`:

```text
row search (first column [1, 10, 14], find last start <= 15):
   lo=0 hi=2  mid=1: 10 <= 15 -> lo=2
   lo=2 hi=2  mid=2: 14 <= 15 -> lo=3
   row = 2
row 2 search ([14, 20, 30, 40], find 15):
   lo=0 hi=3  mid=1: 20 > 15 -> hi=0
   lo=0 hi=0  mid=0: 14 < 15 -> lo=1
   lo=1 > hi=0: not found
```

The row search correctly names row `2` as the only candidate: row `1` ends at `13` and row `2` starts at `14`, so `15` would have to live in row `2`. The in-row search proves it does not. Both searches exhausted their ranges without a hit, matching the expected Output `false`.

#### Solution

The code is the two searches from the walkthrough, each a plain half-interval loop. `bisect_right` names the first row start `> target`, so `row - 1` is the last row whose first value is `<= target`:

```python
from bisect import bisect_left, bisect_right
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        starts = [row[0] for row in matrix]
        row = bisect_right(starts, target) - 1
        if row < 0:
            return False
        values = matrix[row]
        position = bisect_left(values, target)
        return position < len(values) and values[position] == target
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log m + log n)`

One binary search over `m` row starts, one over the `n` values of the chosen row; the two searches run sequentially and their costs add.

##### Space Complexity: `O(m)`

The list of row-start values; a hand-rolled index-based row search would reduce this to `O(1)`.

#### Key Insights

- Chained rows are what make the row choice unambiguous: "last start
  `<= target`" is exact, not a guess to be corrected later.
- Two `O(log)` searches costing `log m + log n` are asymptotically identical to
  one search costing `log(m * n)`, since `log(m * n) = log m + log n`; the next
  solution's advantage is elegance, not a complexity class.
- Building the `starts` list trades `O(m)` memory for clarity; it is also what
  a library `bisect` needs, since it searches a flat sequence.

### Single Binary Search

#### Derivation

The row search and the row scan are both binary searches over the same flattened sorted sequence, split only by a row boundary. Treating the matrix as one virtual list removes the seam: a virtual position `p` between `0` and `m * n - 1` decodes to `matrix[p // n][p % n]`, and one binary search over `p` does both jobs:

1. Set `left = 0` and `right = m * n - 1`.
2. While `left <= right`, decode `mid` to `value = matrix[mid // n][mid % n]`.
3. On `value == target` return `true`; on `value < target` set `left = mid + 1`;
   otherwise `right = mid - 1`.
4. Exhausted range means absent: return `false`.

#### Invariant and Bound

The loop preserves a half-open truth: every value at a virtual position `< left` is `< target`, and every value at a position `> right` is `> target`. Each branch maintains it: `value < target` makes all positions `<= mid` too small (the flattened sequence is non-decreasing), so `left = mid + 1`; `value > target` makes all positions `>= mid` too large, so `right = mid - 1`; the equality branch returns. The interval halves every iteration, so it empties in `ceil(log2(m * n)) + 1` iterations, and an empty interval with the invariant intact means `target` occurs nowhere: `false`.

#### Walkthrough

Trace the virtual search on Example 1: `matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]]`, `target = 10`, so `m * n = 12` and `right` starts at `11`:

```text
left=0  right=11  mid=5   matrix[1][1] = 11   11 > 10   -> right=4
left=0  right=4   mid=2   matrix[0][2] = 4    4  < 10   -> left=3
left=3  right=4   mid=3   matrix[0][3] = 8    8  < 10   -> left=4
left=4  right=4   mid=4   matrix[1][0] = 10   10 == 10  -> found
```

The decodes hop across the row seam without ceremony: `mid = 4` is virtual position `4`, which is row `4 // 4 = 1`, column `4 % 4 = 0`, the row-start `10`. The loop found it in four probes, matching the expected Output `true` for Example 1.

#### Solution

The code is the walkthrough's single half-interval loop over virtual positions.

```python
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        rows, columns = len(matrix), len(matrix[0])
        left, right = 0, rows * columns - 1
        while left <= right:
            mid = (left + right) // 2
            value = matrix[mid // columns][mid % columns]
            if value == target:
                return True
            if value < target:
                left = mid + 1
            else:
                right = mid - 1
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log(m * n))`

The virtual interval halves each iteration; `log(m * n)` equals `log m + log n`, matching the two-search version while running a single loop.

##### Space Complexity: `O(1)`

Only the four boundary/scalar variables are stored.

#### Key Insights

- The `p // n`, `p % n` decode is the whole trick: it imports the flat binary
  search into a 2-D structure with no preprocessing.
- `mid = (left + right) // 2` cannot overflow in Python, though the
  `left + (right - left) // 2` spelling is the portable habit for languages
  where it can.
- This is the follow-up's `O(log(m * n))` answer, and the pattern generalizes:
  any row-major-sorted grid supports flat-array search via index arithmetic.

## Comparison of Solutions

### Time Complexity

- **Staircase Search**: `O(m + n)` - one row or column eliminated per step.
- **Two Binary Searches**: `O(log m + log n)` - a row search, then an in-row search.
- **Single Binary Search**: `O(log(m * n))` - one search over virtual flat positions.

### Space Complexity

- **Staircase Search**: `O(1)` - two cursors.
- **Two Binary Searches**: `O(m)` - the extracted row-start list.
- **Single Binary Search**: `O(1)` - boundary variables only.

### Trade-offs

- The staircase needs no chaining between rows, so it works on the weaker
  matrix variant too; it pays `O(m + n)` for that generality.
- The two-search version maps directly onto library `bisect` calls and reads
  declaratively, but carries an `O(m)` helper list.
- The single search is the tightest and the one the follow-up asks for, at the
  cost of index arithmetic that must be reasoned through once.

### When to Use Each

- **Staircase Search**: When the rows are sorted but not chained, or in
  languages where a flattened decode is awkward.
- **Two Binary Searches**: When the codebase already has a battle-tested
  `bisect`-style helper and clarity is paramount.
- **Single Binary Search**: The interview target for this problem and the
  default whenever the chaining property holds (recommended here).

### Optimization Notes

- `rows * columns - 1` is computed once; recomputing `len(matrix[0])` inside
  the loop is a (small) repeated cost.
- The decode uses `columns` for both `//` and `%` because the grid is
  rectangular; jagged row lengths would break the virtual ordering assumption.
- For the equivalent `O(m + n)` staircase on unchained rows, start from the
  bottom-left corner instead; the elimination logic mirrors.
