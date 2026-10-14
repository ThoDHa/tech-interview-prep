# [Longest Increasing Path In a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

**Hard** | **40 minutes** | **Array, Dynamic Programming, Depth-First Search, Breadth-First Search, Graph, Topological Sort, Memoization, Matrix**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

**Practice:** [`practice/longest_increasing_path_in_a_matrix/solution.py`](../../practice/longest_increasing_path_in_a_matrix/solution.py)

You are given a 2-D grid of integers `matrix`, where each integer is greater than or equal to `0`.

Return the length of the longest strictly increasing path within `matrix`.

From each cell within the path, you can move either horizontally or vertically. You **may not** move **diagonally**.

## Examples

### Example 1

**Input:** `matrix = [[5,5,3],[2,3,6],[1,1,1]]`

**Output:** `4`

**Explanation:** The longest increasing path is `[1, 2, 3, 6]` or `[1, 2, 3, 5]`.

### Example 2

**Input:** `matrix = [[1,2,3],[2,1,4],[7,6,5]]`

**Output:** `7`

**Explanation:** The longest increasing path is `[1, 2, 3, 4, 5, 6, 7]`.

## Constraints

- `1 <= matrix.length, matrix[i].length <= 100`

## Deriving the Solution

A path is a chain of cells where each step moves to a strictly larger neighbor, so "longest" has two natural searches: start a walk at every cell and extend it, or ask for every cell "how long is the path that ends here?". Strictness does double duty: it makes the walks acyclic (a path can never revisit a smaller value), which means every cell has a well-defined answer that other cells can build on. Every solution below is one of the two searches, with or without memory.

1. **Start literal.** Run a depth-first search from every cell, extending into
   any strictly larger neighbor, and keep the deepest walk. Without memory the
   same cell's answer is re-derived once per route that reaches it, and the
   total work grows exponentially: see [Brute Force DFS](#brute-force-dfs).
2. **Remove the recursion.** Fix an order the dependencies respect: process
   cells by increasing value, so every strictly smaller neighbor is settled
   before the cell that could continue it. One relaxed pass per cell in that
   order needs no stack, but pays a sort: see
   [Bottom-Up DP with Value-Sorted Sweep](#bottom-up-dp-with-value-sorted-sweep).
3. **Cache instead of ordering.** The sort buys an evaluation order that the
   recursion implies for free: memoize the depth-first search so each cell's
   answer is computed once and every later visit is a lookup. One pass per
   cell, no sort, `O(rows * cols)`: see
   [DFS with Memoization](#dfs-with-memoization).
4. **Hand the cache to the library.** Step 3's memo grid is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the neighbor probes stay exactly as written: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force DFS

#### Derivation

The most literal reading of "longest increasing path" walks them all. Starting from any cell, the path continues into any of the four neighbors holding a strictly larger value; the walk ends at a cell whose neighbors are all smaller or equal. Trying every starting cell and every continuation enumerates every path, and the deepest one is the answer:

1. Define `dfs(r, c)` as the length of the longest strictly increasing path
   that starts at `(r, c)`.
2. Initialize `best = 1` (the cell alone is always a path).
3. For each of the four neighbors `(nr, nc)` inside the grid with
   `matrix[nr][nc] > matrix[r][c]`, take `1 + dfs(nr, nc)` into `best`.
4. Return `best`.
5. Return the maximum of `dfs(r, c)` over all cells.

#### Walkthrough

Trace the search from the deepest cell on Example 1: `matrix = [[5,5,3],[2,3,6],[1,1,1]]`, starting at `dfs(2, 0)`, the `1` in the bottom-left corner. Only one neighbor is larger at each fork until the value-`5`/`6` fork:

```text
dfs(2, 0) '1'  larger neighbors: (1, 0)='2'
  dfs(1, 0) '2'  larger neighbors: (0, 0)='5', (1, 1)='3'
    dfs(0, 0) '5'  none larger            -> 1
    dfs(1, 1) '3'  larger: (0, 1)='5', (1, 2)='6'
      dfs(0, 1) '5'  none larger          -> 1
      dfs(1, 2) '6'  none larger          -> 1
      dfs(1, 1) -> 1 + max(1, 1) = 2
    dfs(1, 0) -> 1 + max(1, 2) = 3
  dfs(2, 0) -> 1 + 3 = 4
```

The walk `1 -> 2 -> 3 -> 5` (or `1 -> 2 -> 3 -> 6`) has 4 cells, so `dfs(2, 0)` returns `4`. Taking the maximum over all nine starting cells gives `4`, matching the expected Output for Example 1 (the per-cell values are `[[1, 1, 2], [3, 2, 1], [4, 3, 2]]`, and the search makes 26 calls to produce them). Example 2's answer `7` comes from `dfs` at the `1` at position `(1, 1)`.

#### Solution

The code is the walkthrough's per-cell walk with no memory.

```python
from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])

        def dfs(r: int, c: int) -> int:
            best = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            return best

        return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(4^(rows * cols))`

Each call branches into at most four larger neighbors and a path visits any cell at most once (strict increase forbids revisits), so the tree under one start holds up to `4^(rows * cols)` leaves; summed over all starts the work is exponential in the grid size.

##### Space Complexity: `O(rows * cols)`

The recursion stack, one frame per cell along the current path; a snake-shaped grid reaches every cell before returning.

#### Key Insights

- Transcribes the path definition directly: extend into larger neighbors,
  count cells, keep the deepest.
- Correct by exhaustion; no cell's answer is ever assumed, only recomputed.
- The re-derivations are visible even on Example 1: `dfs(1, 2)` runs twice,
  once under each route to the value-`3` fork's two children.

### Bottom-Up DP with Value-Sorted Sweep

#### Derivation

The brute force re-derives answers because it never fixes an evaluation order. The dependency structure supplies one: `dfs(r, c)` reads only neighbors holding strictly larger values, so processing cells in increasing value order settles every supplier before its consumer. Flipping the question to "longest path ending here" turns the recursion into a single relaxation sweep with no stack: `dp[r][c]` is the longest increasing path that ends at `(r, c)`, and each cell extends the best already-settled smaller neighbor:

1. Sort all cells by value ascending.
2. Initialize `dp[r][c] = 1` everywhere (a path can always end at its own
   cell).
3. Sweep the sorted cells; for each `(r, c)`, look at the four neighbors:
   when `matrix[nr][nc] < matrix[r][c]`, take
   `dp[r][c] = max(dp[r][c], dp[nr][nc] + 1)`.
4. Return the maximum of `dp`.

#### Invariant

The sweep reads a neighbor's `dp` value only when that neighbor holds a strictly smaller cell value, and the cells are processed in nondecreasing value order, so every read neighbor was processed in an earlier iteration and its `dp` entry is final. Equal-valued neighbors are never read (the comparison is strict), so ties in the sort order cannot produce a read of an unsettled cell. At the end of the sweep, `dp[r][c]` is the length of the longest increasing path ending at `(r, c)`: either the cell alone (`1`) or one more than the best path ending at a smaller neighbor, and induction over the sorted order extends the claim to every cell.

#### Walkthrough

Trace the sweep on Example 1. The sorted order is `(1 at (2,0)), (1 at (2,1)), (1 at (2,2)), (2 at (1,0)), (3 at (0,2)), (3 at (1,1)), (5 at (0,0)), (5 at (0,1)), (6 at (1,2))`, and each line shows the row of `dp` updated when that cell is processed (`dp` holds longest paths ending at each cell):

```text
values 1 at row 2   dp rows 0, 1, 2 all [1, 1, 1]   (no smaller neighbors anywhere)
value 2 at (1,0)    dp row 1 becomes [2, 1, 1]      (dp[1][0] = dp[2][0] + 1)
value 3 at (0,2)    dp[0][2] stays 1                (neighbors 5 and 6 are larger)
value 3 at (1,1)    dp[1][1] = dp[1][0] + 1 = 3
value 5 at (0,0)    dp[0][0] = dp[1][0] + 1 = 3
value 5 at (0,1)    dp[0][1] = dp[1][1] + 1 = 4
value 6 at (1,2)    dp[1][2] = dp[1][1] + 1 = 4
```

The final table is `[[3, 4, 1], [2, 3, 4], [1, 1, 1]]` and its maximum is `4`, matching the expected Output for Example 1; the `4` entries are the same two paths found by the brute force, read in the ending-at orientation. Example 2's sweep peaks at `7` for the cell holding `7`.

#### Solution

The code is the walkthrough's sweep: sort once, relax each cell against its smaller settled neighbors.

```python
from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        dp = [[1] * cols for _ in range(rows)]
        cells = sorted(
            (matrix[r][c], r, c) for r in range(rows) for c in range(cols)
        )
        best = 1
        for value, r, c in cells:
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] < value:
                    dp[r][c] = max(dp[r][c], dp[nr][nc] + 1)
            best = max(best, dp[r][c])
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * cols * log(rows * cols))`

The sort dominates; the sweep itself is four constant-work neighbor probes per cell.

##### Space Complexity: `O(rows * cols)`

The `dp` table plus the sorted cell list.

#### Key Insights

- Flipping "longest path starting here" to "longest path ending here" is
  what makes a bottom-up order exist: dependencies point from smaller values
  to larger ones.
- Strict increase is the acyclicity guarantee: the value order is a valid
  topological order, so one pass suffices without any relaxation-until-fixed-
  point loop.
- The price of removing the recursion is the sort; the next solution gets
  the same one-pass-per-cell guarantee without it.

### DFS with Memoization

#### Derivation

The sorted sweep pays `O(rows * cols * log(rows * cols))` to discover an order the recursion already implies. A cell's answer depends only on the cell: strict increase forbids cycles, so "longest increasing path starting at `(r, c)`" is a well-defined, repeatable question. [Memoizing](https://en.wikipedia.org/wiki/Memoization) the brute-force `dfs` therefore turns every re-derivation into a lookup, keeps the starting-at orientation, and needs no sort:

1. Keep the brute-force recursion unchanged.
2. Add a `memo` grid; on entry return the stored value when nonzero, and
   store `best` before returning.
3. Return the maximum of `dfs(r, c)` over all cells.

`memo` stores path lengths, which are at least `1`, so `0` is a safe "not computed yet" marker.

#### Walkthrough

Trace the memoized loop over all cells in row-major order on Example 1. Computed entries are marked `stored`; repeat arrivals are marked as hits:

```text
dfs(0, 0) '5' -> 1  stored
dfs(0, 1) '5' -> 1  stored
dfs(0, 2) '3' -> 1 + dfs(1, 2) = 2  stored   (also probes dfs(0, 1) ** hit **)
dfs(1, 0) '2' -> 1 + max(dfs(0, 0) ** hit **, dfs(1, 1)) = 3  stored
  dfs(1, 1) '3' -> 1 + max(dfs(0, 1) ** hit **, dfs(1, 2) ** hit **) = 2  stored
dfs(1, 1) -> 2  ** hit **
dfs(1, 2) -> 1  ** hit **
dfs(2, 0) '1' -> 1 + dfs(1, 0) = 4  stored
dfs(2, 1) '1' -> 1 + dfs(1, 1) = 3  stored
dfs(2, 2) '1' -> 1 + dfs(1, 2) = 2  stored
```

Each cell's answer is computed exactly once (9 stores) and every other arrival is a lookup: 9 hits in total, one under `dfs(0, 2)`, three under the `dfs(1, 0)` descent, two at the `dfs(1, 1)` and `dfs(1, 2)` starts, and three across the bottom row. The memo table is `[[1, 1, 2], [3, 2, 1], [4, 3, 2]]`, whose maximum is `4`, matching the expected Output for Example 1.

#### Solution

The code is the brute-force recursion with a memo grid in front of it.

```python
from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        memo = [[0] * cols for _ in range(rows)]

        def dfs(r: int, c: int) -> int:
            if memo[r][c]:
                return memo[r][c]
            best = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            memo[r][c] = best
            return best

        return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * cols)`

Every cell's answer is computed once with four constant-work neighbor probes; every repeat visit is an `O(1)` lookup.

##### Space Complexity: `O(rows * cols)`

The memo grid plus a recursion stack that reaches one frame per cell along the current path.

#### Key Insights

- Strict increase is what makes plain memoization sound: no cycles means no
  computation-in-progress can be re-entered, so no visited set is needed.
- The memo and the sort are two routes to the same topological guarantee;
  the memo's comes free from the recursion structure.
- CPython's default recursion limit (~1000) is below the worst-case stack
  depth (`rows * cols`); deep grids need a raised limit around the search,
  which the practice reference carries.

### Top-Down Memoization with functools.cache

#### Derivation

Step 3's memo grid is not part of the recurrence. The grid, the zero-check, and the store all exist to remember what `dfs(r, c)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the neighbor probes untouched:

1. Keep the memoized recursion's structure: the same four neighbor probes
   with the bounds and strictness tests.
2. Replace the `memo` grid with `@cache` on `dfs`, keyed automatically by the
   arguments `(r, c)`.
3. Return the maximum of `dfs(r, c)` over all cells.

The one behavioral cost: `@cache` keeps every visited pair alive for the life of the process, so the memory profile matches the grid version but cannot be freed early.

#### Walkthrough

Trace the decorated recursion on Example 1. The call sequence is identical to the DFS with Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dfs(0, 0), dfs(0, 1), dfs(0, 2) computed
dfs(1, 0) descends: dfs(0, 0) and dfs(1, 1) -> dfs(0, 1), dfs(1, 2)
  ... identical descent ...
dfs(2, 0) -> 1 + dfs(1, 0) = 4
```

9 distinct `(r, c)` calls are cached (9 misses, 9 hits from the later starts descending into settled cells), and the answer is `4`, matching the expected Output for Example 1.

#### Solution

The code is the memoized recursion with the grid replaced by the decorator.

```python
from functools import cache
from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])

        @cache
        def dfs(r: int, c: int) -> int:
            best = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            return best

        return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * cols)`

The cache admits each `(r, c)` pair once; the body is four neighbor probes.

##### Space Complexity: `O(rows * cols)`

The decorator's cache plus the recursion stack.

#### Key Insights

- `functools.cache` is the grid-based memo with the ceremony removed: same
  asymptotics, no sentinel value, no index arithmetic for the cache.
- A dict keyed by `(r, c)` also suits ragged or sparse grids where a dense
  memo grid would be wasted; for this dense problem the two are equivalent.
- The recursion body is the path definition in its purest form, which makes
  it the version to quote in an interview after sketching the memo.

## Comparison of Solutions

### Time Complexity

- **Brute Force DFS**: `O(4^(rows * cols))` - every increasing path is walked, repeatedly.
- **Bottom-Up DP with Value-Sorted Sweep**: `O(rows * cols * log(rows * cols))` - the sort dominates the one-pass sweep.
- **DFS with Memoization**: `O(rows * cols)` - one solve per cell, no sort.
- **Top-Down Memoization with functools.cache**: `O(rows * cols)` - the grid memo with library bookkeeping.

### Space Complexity

- **Brute Force DFS**: `O(rows * cols)` - the recursion stack.
- **Bottom-Up DP with Value-Sorted Sweep**: `O(rows * cols)` - the `dp` table plus the sorted cell list.
- **DFS with Memoization**: `O(rows * cols)` - the memo grid plus the stack.
- **Top-Down Memoization with functools.cache**: `O(rows * cols)` - the decorator's cache plus the stack.

### Trade-offs

- The brute force derives straight from the path definition and is correct by
  exhaustion, but unusable beyond roughly a 4x4 grid.
- The sorted sweep removes the stack and gives an iterative form, paying a
  logarithmic factor and the ending-at orientation.
- The memoized DFS is the tightest: linear time, no sort, no ordering logic,
  only the recursion the definition wrote.

### When to Use Each

- **Brute Force DFS**: tiny grids, or as the brute-force oracle when checking
  the faster versions.
- **Bottom-Up DP with Value-Sorted Sweep**: when an iterative, stack-free
  form is required (languages or environments with tight recursion limits),
  accepting the sort.
- **DFS with Memoization**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the grid ceremony.

### Optimization Notes

- Neighbor deltas as a tuple of pairs (`((1, 0), (-1, 0), (0, 1), (0, -1))`)
  keep the probe loop branch-free; bounds come first in the `and` chain so
  indexing never runs off the grid.
- The value-sorted sweep extends naturally to an implicit order: counting
  sort over bounded values would drop the log factor, at the cost of a value-
  range array.
- The same memoized DFS answers "longest decreasing path" by flipping one
  comparison, and the two versions share the memo only if the orientation is
  fixed; mixing orientations in one cache is a bug.
