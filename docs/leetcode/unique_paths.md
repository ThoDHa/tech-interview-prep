# [Unique Paths](https://leetcode.com/problems/unique-paths/)

**Medium** | **20 minutes** | **Math, Dynamic Programming, Combinatorics**

**Pattern:** [Grid DP](../patterns/grid_dp/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Combination](https://en.wikipedia.org/wiki/Combination)

**Practice:** [`practice/unique_paths/solution.py`](../../practice/unique_paths/solution.py)

There is a robot on an `m x n` grid. The robot is initially located at the top-left corner (i.e., `grid[0][0]`). The robot tries to move to the bottom-right corner (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time.

Given the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to `2 * 10^9`.

## Examples

### Example 1

![Unique Paths Example 1](assets/unique_paths_example1.png)

**Input:** `m = 3`, `n = 7`

**Output:** `28`

### Example 2

**Input:** `m = 3`, `n = 2`

**Output:** `3`

**Explanation:** From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

## Constraints

- `1 <= m, n <= 100`

## Deriving the Solution

A path is nothing but a sequence of down and right steps, and the number of paths onward from any cell depends only on that cell, never on how the robot arrived there. Every solution below exploits that one observation, ending with a formulation that skips the grid entirely.

1. **Start literal.** From any cell the robot steps down or right, so the count
   from a cell is the count from the cell below plus the count from the cell to its right. Recurse on both choices: correct but `O(2^(m + n))`, since nothing is remembered: see [Recursion](#recursion).
2. **Spot the waste.** Many distinct routes pass through the same cell, and the
   recursion re-derives that cell's count once per route. The answer from `(i, j)` never changes, yet it is recomputed exponentially often.
3. **Cache it.** Store each cell's count the first time it is computed and answer
   every later visit from the cache. Only `m × n` distinct cells exist, so the work collapses to `O(m × n)`: see [Top-Down Memoization](#top-down-memoization).
4. **Fill the table directly.** The memo is a table filled lazily in whatever
   order the recursion demands. Filling it row by row with an explicit loop removes the recursion and its stack entirely: see [Bottom-Up DP](#bottom-up-dp).
5. **Shrink the table.** Each row of that table reads only the row above it, so a
   single reusable row of `n` counts is enough: see [Space-Optimized DP](#space-optimized-dp).
6. **Count instead of build.** Every path is exactly `m - 1` downs and `n - 1`
   rights in some order, so the answer is the number of ways to place the downs among `m + n - 2` moves: one binomial coefficient, computed in `O(min(m, n))` time: see [Combinatorics](#combinatorics).
7. **Let the library hold the cache.** The memo's membership test and store are
   a mechanical wrapper around the recursion, and `functools.cache` is exactly that wrapper. Decorating `count` deletes the dictionary bookkeeping while the recurrence, the two base cases, and the top-down framing stay visible: see [Top-Down Memoization with `functools.cache`](#top-down-memoization-with-functoolscache).
8. **Let the library evaluate the coefficient.** With the binomial derived and
   proved in step 6, the multiply-then-divide loop is only a strategy for evaluating it in exact integers, and `math.comb` already implements that strategy, collapsing the solution to a single call: see [Library One-Liner with `math.comb`](#library-one-liner-with-mathcomb).

## Solutions

### Recursion

#### Derivation

The most direct idea mirrors the problem statement exactly: from any cell the robot may step down or step right, so the number of paths from a cell is the sum of the paths from the cell below and the cell to its right. [Recurse](https://en.wikipedia.org/wiki/Recursion_(computer_science)) on both choices and add the results, with no table and no memory of past work:

1. Start at the top-left cell `(0, 0)`.
2. If the current cell is the bottom-right corner, this branch is one complete path, so return `1`.
3. If the current cell has stepped past the last row or column, the branch is invalid, so return `0`.
4. Otherwise return the sum of recursing down `(i + 1, j)` and recursing right `(i, j + 1)`.

This enumerates every down/right path by brute force, recomputing shared subproblems each time it reaches them.

#### Walkthrough

Example 1 (`m = 3`, `n = 7`) has 28 paths, far too many to draw by hand, so this trace uses the smaller Example 2: `m = 3`, `n = 2`, whose expected Output is `3`. The grid is 3 rows by 2 columns, so the corner is cell `(2, 1)`, and a cell is "off the grid" once `i >= 3` or `j >= 2`.

The recursion forms a call tree. Each `count(i, j)` first checks the two base cases, then returns `count(i + 1, j)` (step down) plus `count(i, j + 1)` (step right). Reading the tree top-down shows each call; the `->` lines show what each call returns as results combine back up:

```text
count(0,0)
  count(1,0)                    down from start
    count(2,0)
      count(3,0) -> 0           i >= m, off the grid
      count(2,1) -> 1           corner reached
    -> 0 + 1 = 1
    count(1,1)
      count(2,1) -> 1           corner reached
      count(1,2) -> 0           j >= n, off the grid
    -> 1 + 0 = 1
  -> 1 + 1 = 2                  count(1,0) returns 2
  count(0,1)                    right from start
    count(1,1)
      count(2,1) -> 1           corner reached
      count(1,2) -> 0           off the grid
    -> 1 + 0 = 1
    count(0,2) -> 0             off the grid
  -> 1 + 0 = 1                  count(0,1) returns 1
-> 2 + 1 = 3
```

The root `count(0, 0)` adds its down branch (`2`) and its right branch (`1`) to return `3`, which matches the expected Output `3`. Notice `count(2,1)` and `count(1,1)` are each evaluated more than once: that repeated work is exactly the waste the DP solutions remove.

#### Solution

The code is the call tree from the walkthrough: two base cases, then the down branch plus the right branch.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Count paths from cell (i, j) to the bottom-right corner
        def count(i: int, j: int) -> int:
            # Reached the destination: exactly one way to "finish"
            if i == m - 1 and j == n - 1:
                return 1
            # Fell off the grid: this branch contributes no path
            if i >= m or j >= n:
                return 0
            # Every path either steps down or steps right
            return count(i + 1, j) + count(i, j + 1)

        return count(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^(m + n))`

Each call branches into two recursive calls and the recursion runs up to `m + n` levels deep, so the call tree grows exponentially. The same cell is recomputed many times because nothing is cached.

##### Space Complexity: `O(m + n)`

No auxiliary table is built, but the recursion stack reaches a depth of `m + n - 2` along the longest down-and-right path.

#### Key Insights

- Reads straight off the problem statement: a path is a sequence of down and right moves, so paths split into "go down" plus "go right".
- It is simple but wasteful: it recomputes the same `(i, j)` subproblem on every path that passes through it.
- The exponential blow-up motivates caching shared subproblems, which the DP solutions do next.

### Top-Down Memoization

#### Derivation

The pure recursion pays for its honesty: it re-solves `count(i, j)` on every route that passes through `(i, j)`, and its `O(2^(m + n))` call tree times out on the 23 x 12 full-size case. The observation that repairs it is that the number of paths from `(i, j)` to the corner depends only on the cell itself, not on how the robot arrived there, so the result of `count(i, j)` can be stored the first time it is computed and returned instantly on every later visit. There are only `m × n` distinct cells, so with the cache each cell's body executes at most once and every repeated visit is a constant-time lookup. The memo is the same table the Bottom-Up DP below fills explicitly; [memoization](https://en.wikipedia.org/wiki/Memoization) simply fills it lazily, in whatever order the recursion demands, while keeping the top-down framing that reads straight off the problem statement:

1. Keep the `count(i, j)` recursion and its two base cases exactly as in the
   Recursion solution.
2. Before branching, return `memo[(i, j)]` when the pair is already in the
   dictionary.
3. Otherwise compute `count(i + 1, j) + count(i, j + 1)` once, store it under
   `(i, j)`, and return it.
4. The answer is `count(0, 0)`.

#### Walkthrough

Like the Recursion walkthrough, this trace uses Example 2 (`m = 3`, `n = 2`), which is small enough to draw and reaches the same cell along two different routes, so it exercises the memo. The trace indents one level per call; base cases (corner, off grid) return before the memo is consulted, so only interior cells are stored:

```text
count(0,0)                       compute
  count(1,0)                     down; compute
    count(2,0)                   compute
      count(3,0) -> 0            off the grid
      count(2,1) -> 1            corner reached
    memo[(2,0)] = 0 + 1 = 1
    count(1,1)                   compute
      count(2,1) -> 1            corner reached
      count(1,2) -> 0            off the grid
    memo[(1,1)] = 1 + 0 = 1
  memo[(1,0)] = 1 + 1 = 2
  count(0,1)                     right; compute
    count(1,1) -> 1              ** memo hit, no recursion **
    count(0,2) -> 0              off the grid
  memo[(0,1)] = 1 + 0 = 1
memo[(0,0)] = 2 + 1 = 3
```

The cell `(1, 1)` is reached twice: once through the down branch `(1, 0)` and once through the right branch `(0, 1)`. The pure recursion re-expanded it both times; here the second visit answers from `memo[(1, 1)]` without recursing. The call returns `3`, matching the expected Output for Example 2.

#### Solution

The code is the Recursion solution with the memo lookup and store wrapped around the branch; nothing else changes.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Cache of computed results keyed by cell (i, j)
        memo = {}

        # Count paths from cell (i, j) to the bottom-right corner
        def count(i: int, j: int) -> int:
            # Reached the destination: exactly one way to "finish"
            if i == m - 1 and j == n - 1:
                return 1
            # Fell off the grid: this branch contributes no path
            if i >= m or j >= n:
                return 0
            # Return the cached count if this cell was already solved
            if (i, j) in memo:
                return memo[(i, j)]
            # Every path either steps down or steps right
            memo[(i, j)] = count(i + 1, j) + count(i, j + 1)
            return memo[(i, j)]

        return count(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each of the `m × n` cells is fully computed at most once: the first call for a cell does constant work plus two recursive calls, and every subsequent call for that cell returns the cached value in constant time. Total work is therefore proportional to the number of distinct cells.

##### Space Complexity: `O(m × n)`

The memo can hold one entry per cell, which dominates at `O(m × n)`. The recursion stack adds `O(m + n)` on top, since every call advances `i` or `j` by one and the chain from `(0, 0)` to the corner is at most `m + n - 2` frames deep (at most 198 under the constraints, safely below CPython's default limit).

#### Key Insights

- **Overlapping subproblems**: Many distinct paths share the same suffix from a cell to the corner. The pure recursion recomputes that suffix count once per path passing through the cell; the memo computes it exactly once
- **State is just the cell**: The path count from `(i, j)` is independent of the route taken to reach it, which is precisely the property that makes the `(i, j)` pair a valid memo key
- **Timeout becomes tractable**: The 23 x 12 case that defeats the pure recursion needs only `23 × 12 = 276` cached states here, so the exponential blow-up disappears without changing the recurrence
- **Bridge to bottom-up**: The memo holds the same values as the Bottom-Up DP table; rewriting the lazy, recursion-driven fill as an explicit loop over cells yields the next solution

### Bottom-Up DP

#### Derivation

The memoized recursion still carries a call stack and fills its table in an order dictated by the call tree. Ask the question from the other direction instead: how many paths reach cell `(i, j)` from the origin? The robot only moves down or right, so it can only arrive from the cell above `(i-1, j)` or the cell to the left `(i, j-1)`, giving `paths[i][j] = paths[i-1][j] + paths[i][j-1]`. The first row and first column have exactly one path each (keep moving right, or keep moving down), which seeds the table. Filling the table row by row is the same information the memo holds, computed with a plain double loop and no recursion: the textbook [bottom-up approach](https://en.wikipedia.org/wiki/Dynamic_programming):

1. Allocate `dp` as an `m × n` table filled with `1`. The first row and first
   column really are all `1`, and every other cell will be overwritten.
2. For `i` from `1` to `m - 1` and `j` from `1` to `n - 1`, set
   `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
3. Return `dp[m-1][n-1]`.

#### Recurrence

Let `dp[i][j]` be the number of distinct paths from the origin to cell \((i, j)\). The robot only moves down or right, so it arrives from exactly one of two cells:

$$ dp[i][j] = \begin{cases} 1, & i = 0 \ \text{ or } \ j = 0 \\[4pt] dp[i-1][j] + dp[i][j-1], & i, j \ge 1 \end{cases} $$

```text
dp[i][j] = 1                            for i == 0 or j == 0
dp[i][j] = dp[i - 1][j] + dp[i][j - 1]  for i >= 1 and j >= 1
```

The first row and first column are `1` because there is a single monotone path along an edge. The answer is \(dp[m-1][n-1]\).

#### Walkthrough

Let us fill the table by hand on Example 1: `m = 3`, `n = 7`, expected Output `28`. The table starts as three rows of `1`s; row `0` and column `0` keep those values, and each later cell becomes the cell above plus the cell to the left:

```text
start   dp[0] = [1, 1, 1, 1,  1,  1,  1]    one path along the top edge
        dp[1] = [1, 1, 1, 1,  1,  1,  1]    initialized; only dp[1][0] is final
        dp[2] = [1, 1, 1, 1,  1,  1,  1]    initialized; only dp[2][0] is final
i = 1   dp[1] = [1, 2, 3, 4,  5,  6,  7]    dp[1][j] = dp[0][j] + dp[1][j-1]
i = 2   dp[2] = [1, 3, 6, 10, 15, 21, 28]   dp[2][j] = dp[1][j] + dp[2][j-1]
```

Two cells in detail: `dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2`, and the final cell `dp[2][6] = dp[1][6] + dp[2][5] = 7 + 21 = 28`.

The function returns `dp[2][6] = 28`, matching the expected Output for Example 1.

#### Solution

The code is the row fill from the walkthrough: seed the table with `1`s, then sweep the interior cells in order.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Create DP table where dp[i][j] = paths to reach cell (i, j)
        dp = [[1] * n for _ in range(m)]

        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                # Paths to current cell = paths from above + paths from left
                dp[i][j] = dp[i-1][j] + dp[i][j-1]

        return dp[m-1][n-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

We fill each cell of the DP table exactly once.

##### Space Complexity: `O(m × n)`

We store the entire 2D DP table.

#### Key Insights

- **Subproblem structure**: The number of paths to any cell depends only on paths to adjacent cells, making this ideal for dynamic programming
- **Boundary conditions**: The first row and column naturally have exactly 1 path each, serving as base cases for the recurrence relation

### Space-Optimized DP

#### Derivation

The 2D table wastes memory: once row `i` is filled, row `i - 1` is never read again, yet the table keeps every row alive. Since computing the current row needs only the previous row, a single row can be updated in place. The recurrence stays the same; only the storage changes. In `dp[j] += dp[j-1]`, the old value of `dp[j]` is the cell above (not yet overwritten this pass) and the freshly updated `dp[j-1]` is the cell to the left, so one row plays both roles:

1. Initialize `dp = [1] * n`: the first row of the table.
2. For each subsequent row `i` from `1` to `m - 1`, sweep `j` from `1` to
   `n - 1`, updating `dp[j] += dp[j-1]` in place.
3. Return `dp[n-1]`.

#### Walkthrough

Let us run the single row on Example 1 again: `m = 3`, `n = 7`. Each pass of the outer loop turns the row for grid row `i - 1` into the row for grid row `i`, overwriting it left to right:

```text
start   dp = [1, 1, 1, 1, 1, 1, 1]         row 0: one path to each cell
i = 1   j = 1: dp[1] = 1 + 1 = 2           old dp[1] is the cell above,
        j = 2: dp[2] = 1 + 2 = 3           fresh dp[j-1] is the cell to the left
        j = 3 .. 6 continue the sweep
        dp = [1, 2, 3, 4, 5, 6, 7]         row 1 complete
i = 2   dp = [1, 3, 6, 10, 15, 21, 28]     row 2 overwrites row 1 in place
```

The rows that appear are exactly the rows of the 2D table, computed without ever storing more than one of them. The function returns `dp[6] = 28`, matching the expected Output for Example 1.

#### Solution

The code is the in-place row sweep from the walkthrough.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Use only one row for space optimization
        dp = [1] * n

        for i in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j-1]

        return dp[n-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The same number of cell updates as the 2D DP, just stored in a single row.

##### Space Complexity: `O(n)`

We keep only one row of results.

#### Key Insights

- **Space optimization opportunity**: Since we only need the previous row to calculate the current row, we can reduce space complexity from O(m×n) to O(n)
- **In-place update correctness**: `dp[j] += dp[j-1]` works because the old `dp[j]` represents the cell above and the updated `dp[j-1]` represents the cell to the left

### Combinatorics

#### Derivation

Every DP above still touches all `m × n` cells, but the grid is scaffolding: a path never turns back, so it is fully described by the order of its moves. The robot makes exactly `m - 1` down moves and `n - 1` right moves, `m + n - 2` moves in total, and choosing which positions hold the down moves determines the entire path. The question collapses to "in how many ways can we choose `m - 1` positions out of `m + n - 2`?", the [binomial coefficient](https://en.wikipedia.org/wiki/Combination) `C(m+n-2, m-1)`. By symmetry `C(m+n-2, m-1) = C(m+n-2, n-1)`, so the loop iterates over the smaller of the two counts, and it multiplies before dividing to keep every intermediate value an exact integer:

1. Set `total_moves = m + n - 2` and `k = min(m - 1, n - 1)`.
2. Build the coefficient one factor at a time: for `i` in `range(k)`, update
   `result = result * (total_moves - i) // (i + 1)`.
3. Return `result`.

#### Closed Form

Every path is a sequence of \(m-1\) down moves and \(n-1\) right moves in some order, so a path is fully determined by choosing which of the \(m+n-2\) positions hold the down moves:

$$ \text{paths}(m, n) = \binom{m+n-2}{\,m-1\,} = \binom{m+n-2}{\,n-1\,} = \frac{(m+n-2)!}{(m-1)!\,(n-1)!} $$

```text
paths(m, n) = (m + n - 2) choose (m - 1)
            = (m + n - 2) choose (n - 1)
            = (m + n - 2)! / ((m - 1)! * (n - 1)!)
```

The two binomials are equal by the symmetry \(\binom{a}{b} = \binom{a}{a-b}\), which is what lets the loop iterate over the smaller of \(m-1\) and \(n-1\). The coefficient can be built one factor at a time:

$$ \binom{a}{k} = \prod_{i=0}^{k-1} \frac{a - i}{i + 1} $$

```text
(a choose k) = product over i = 0 .. k - 1 of (a - i) / (i + 1)
               (empty product is 1, so (a choose 0) = 1)
```

Building it that way keeps every partial result an exact integer, because the product of any \(i+1\) consecutive integers is divisible by \((i+1)!\). That is why the code can use floor division inside the loop without ever losing a remainder.

#### Walkthrough

Let us evaluate the formula on Example 1: `m = 3`, `n = 7`. The path has `m - 1 = 2` downs and `n - 1 = 6` rights, and the loop builds the coefficient one factor at a time; after each iteration `i`, `result` equals `C(total_moves, i + 1)`:

```text
total_moves = 3 + 7 - 2 = 8        8 moves: 2 downs and 6 rights
k = min(2, 6) = 2                  choose positions for the 2 downs
i = 0   result = 1 * 8 // 1 = 8    C(8, 1)
i = 1   result = 8 * 7 // 2 = 28   C(8, 2)
```

The loop ends with `result = C(8, 2) = 28`: there are 28 ways to place the two down moves among eight positions, matching the expected Output for Example 1.

#### Solution

The code is the factor-by-factor product from the walkthrough.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Total moves needed: (m-1) down + (n-1) right = (m+n-2) total moves
        # Choose (m-1) positions for down moves out of (m+n-2) total positions
        # This equals C(m+n-2, m-1) = C(m+n-2, n-1), so iterate the smaller side
        total_moves = m + n - 2
        k = min(m - 1, n - 1)

        # Calculate C(total_moves, k) efficiently
        result = 1
        for i in range(k):
            result = result * (total_moves - i) // (i + 1)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(min(m, n))`

We compute a single binomial coefficient, iterating over `min(m-1, n-1)` terms.

##### Space Complexity: `O(1)`

We use only a constant number of variables.

#### Key Insights

- **Mathematical elegance**: The combinatorics approach provides the most efficient solution by recognizing this as a "choose k from n" problem
- **Overflow avoidance**: Multiplying before dividing within the loop keeps intermediate values integral

### Top-Down Memoization with `functools.cache`

#### Derivation

The memoized recursion spends four of its lines on bookkeeping that has nothing to do with counting paths: allocating `memo`, testing membership, assigning the computed value, and returning it. [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) performs exactly that lookup-compute-store cycle, keyed on the call's argument tuple, so decorating `count` deletes all four lines while the recurrence, the two base cases, and the top-down framing stay on the page unchanged. What moves is the dictionary handling; what stays is every line that expresses the algorithm, which is why this is the memoization above rather than a new idea.

One detail changes substance rather than style. The decorator wraps the entire function, so the corner and off-grid answers are cached too, whereas the hand-rolled memo returned from its base cases before ever consulting the dictionary. The cache therefore holds a few boundary cells the memo never stored, and repeat visits to those cells now answer from the cache instead of re-running the two comparisons.

1. Keep the `count(i, j)` recursion, its two base cases, and its
   down-plus-right sum exactly as in the Top-Down Memoization solution.
2. Define `count` inside `uniquePaths` and decorate it with `@cache`, so a fresh
   cache is created on every call and the closure captures this call's `m` and `n`.
3. Delete the `memo` dictionary, the `(i, j) in memo` test, and the store: the
   decorator keys on `(i, j)` and serves every repeat call from its own table.
4. The answer is still `count(0, 0)`.

#### Walkthrough

This trace uses Example 2 (`m = 3`, `n = 2`, expected Output `3`), the same case the Top-Down Memoization walkthrough traced, so the two can be compared line for line. Indentation is one level per call, and every call is now routed through the cache before the body runs:

```text
count(0,0)                       miss, compute
  count(1,0)                     down; miss, compute
    count(2,0)                   miss, compute
      count(3,0) -> 0            off the grid; cached
      count(2,1) -> 1            corner reached; cached
    count(2,0) = 0 + 1 = 1       cached
    count(1,1)                   miss, compute
      count(2,1) -> 1            ** cache hit, base case not re-run **
      count(1,2) -> 0            off the grid; cached
    count(1,1) = 1 + 0 = 1       cached
  count(1,0) = 1 + 1 = 2         cached
  count(0,1)                     right; miss, compute
    count(1,1) -> 1              ** cache hit, no recursion **
    count(0,2) -> 0              off the grid; cached
  count(0,1) = 1 + 0 = 1         cached
count(0,0) = 2 + 1 = 3           cached
```

The cell `(1, 1)` is reached twice and answered from the cache the second time, just as in the hand-rolled version. The visible difference is `(2, 1)`, the corner: the manual memo re-ran its base-case test on the second visit because base cases returned before the lookup, while `@cache` serves it as a hit. The cache ends holding nine entries: the five interior cells the manual memo stored, plus the corner and the three off-grid cells it never did. The call returns `3`, matching the expected Output for Example 2.

#### Solution

The Top-Down Memoization code with the dictionary handling replaced by the decorator; the recursion body is untouched.

```python
from functools import cache


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Count paths from cell (i, j) to the bottom-right corner. Defined
        # inside the method so each call gets a fresh cache and the closure
        # captures this call's m and n.
        @cache
        def count(i: int, j: int) -> int:
            # Reached the destination: exactly one way to "finish"
            if i == m - 1 and j == n - 1:
                return 1
            # Fell off the grid: this branch contributes no path
            if i >= m or j >= n:
                return 0
            # Every path either steps down or steps right
            return count(i + 1, j) + count(i, j + 1)

        return count(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The recurrence is unchanged, so each of the `m × n` cells still runs its body at most once and every repeated visit is a constant-time hit. The decorator's hit path hashes the `(i, j)` tuple and reads a dictionary, the same two operations the hand-rolled memo performed inline, so the constant factor is comparable rather than free.

##### Space Complexity: `O(m × n)`

The cache holds one entry per cell the recursion reaches, which is the `m × n` interior cells plus the `O(m + n)` boundary cells just past the last row and column, so it is `O(m × n)` overall. The recursion stack adds `O(m + n)` frames, at most 198 under the constraints. `cache` is unbounded by design, but the closure is discarded when `uniquePaths` returns, so nothing survives the call.

#### Key Insights

- Only the bookkeeping moves to the library: the recurrence, the base cases, and
  the fact that a cell's count depends on the cell alone are what make `(i, j)` a valid cache key, and none of that is something `@cache` supplies.
- Decorating the inner closure is a correctness requirement, not a style choice.
  A cached method or module-level function keyed on `(i, j)` alone would carry results across calls with different `m` and `n` and answer for the wrong grid.
- `@cache` memoizes the base cases as well, which the hand-rolled memo skipped by
  returning early: nine cached entries against five on the 3 x 2 grid, buying the deletion of the lookup and store lines.
- The cache grows without bound, which is harmless here because `m, n <= 100`
  caps it near `10^4` entries and it dies with the enclosing call; a long-lived cached function would want `functools.lru_cache(maxsize=...)` instead.

### Library One-Liner with `math.comb`

#### Derivation

The Combinatorics section does the load-bearing work: it derives that a path is determined by choosing which `m - 1` of the `m + n - 2` moves are downs, and proves that building `C(m+n-2, m-1)` one factor at a time keeps every partial value an exact integer. What remains after that derivation is arithmetic, and [`math.comb`](https://docs.python.org/3/library/math.html#math.comb) evaluates binomial coefficients exactly. So the loop, the `min(m - 1, n - 1)` symmetry reduction, and the multiply-before-divide ordering all move into the library, leaving one line that states the closed form and nothing else.

1. Read the closed form off the Combinatorics derivation: the answer is
   `C(m + n - 2, m - 1)`, the number of ways to place the down moves.
2. Pass those two numbers to `math.comb(m + n - 2, m - 1)`, which computes the
   coefficient in exact integer arithmetic.
3. Return that value. No `min(m - 1, n - 1)` selection is written, because
   `math.comb` applies the symmetry `C(a, b) = C(a, a - b)` internally and iterates the smaller side itself.

#### Walkthrough

There is no loop left to trace, so the trace is what the two arguments mean and what the library evaluates. On Example 1 (`m = 3`, `n = 7`, expected Output `28`):

```text
m + n - 2 = 3 + 7 - 2 = 8      8 moves in total: 2 downs and 6 rights
m - 1     = 3 - 1     = 2      choose the 2 positions holding the down moves
math.comb(8, 2) = 8! / (2! * 6!) = (8 * 7) / (2 * 1) = 28
```

The single call returns `28`, matching the expected Output for Example 1. The symmetric form agrees, as the derivation promised: `math.comb(8, 6)` is also `28`, so writing `n - 1` in place of `m - 1` would be equally correct.

#### Solution

One call, evaluating the coefficient the section above derives.

```python
import math


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # A path is m-1 downs and n-1 rights in some order, so the count is the
        # number of ways to choose which m-1 of the m+n-2 moves are downs.
        return math.comb(m + n - 2, m - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(min(m, n))`

`math.comb(a, k)` reduces `k` to `min(k, a - k)` and then combines that many factors, which is the same `min(m - 1, n - 1)` factor count the hand-rolled loop performs, so the two carry the same bound. CPython implements the combination in C over exact integers rather than in a Python loop, so the constant factor is far smaller even though the asymptotics match.

##### Space Complexity: `O(1)`

A single integer result and a couple of intermediate values, with no table, cache, or recursion stack. The answer is bounded by `2 * 10^9` per the problem statement, so it fits in one machine word's worth of digits.

#### Key Insights

- The one-liner is only legitimate because the section above it derives the
  binomial: `math.comb` evaluates a formula it cannot explain, and being able to explain why the count is `C(m+n-2, m-1)` is what an interviewer is testing.
- It hides both things the hand-rolled loop existed to get right: the symmetry
  reduction to the smaller of `m - 1` and `n - 1`, and the multiply-then-divide ordering that keeps every partial product an exact integer.
- Python's unbounded integers mean neither version can overflow; the same
  formula in a fixed-width language still needs the loop's ordering to keep intermediate values in range.
- `math.comb` requires Python 3.8 or newer, so the explicit loop remains the
  portable form on older interpreters.

## Comparison of Solutions

### Time Complexity

- **Recursion**: `O(2^(m + n))` - Enumerates every down/right path, recomputing shared subproblems
- **Top-Down Memoization**: `O(m × n)` - Computes each distinct cell once; repeated visits are constant-time cache hits
- **Bottom-Up DP**: `O(m × n)` - Fills every cell of the DP table once
- **Space-Optimized DP**: `O(m × n)` - Same number of cell updates, just stored in a single row
- **Combinatorics**: `O(min(m, n))` - Computes a single binomial coefficient
- **Top-Down Memoization with `functools.cache`**: `O(m × n)` - The same recurrence, with the lookup and store performed by the decorator instead of inline
- **Library One-Liner with `math.comb`**: `O(min(m, n))` - The same binomial coefficient, combined from `min(m-1, n-1)` factors in C rather than in a Python loop

### Space Complexity

- **Recursion**: `O(m + n)` - Recursion stack depth along the longest path, no table allocated
- **Top-Down Memoization**: `O(m × n)` - One memo entry per cell, plus `O(m + n)` recursion stack
- **Bottom-Up DP**: `O(m × n)` - Stores the entire 2D DP table
- **Space-Optimized DP**: `O(n)` - Keeps only one row of results
- **Combinatorics**: `O(1)` - Uses a constant number of variables
- **Top-Down Memoization with `functools.cache`**: `O(m × n)` - One cache entry per reached cell, boundary cells included, plus `O(m + n)` recursion stack
- **Library One-Liner with `math.comb`**: `O(1)` - A single integer result, with no table, cache, or stack

### Trade-offs

- The recursion solution reads straight off the problem statement and uses no extra structures, but recomputes the same subproblems exponentially many times
- The memoized solution keeps the recursion's natural top-down framing while eliminating the exponential recomputation, at the cost of a per-cell cache and recursion overhead
- The 2D DP solution replaces the recursion with an explicit table fill that mirrors the recurrence directly, but wastes memory storing rows it no longer needs
- The 1D DP solution keeps the same intuitive logic while collapsing storage to a single row, at the cost of slightly less obvious indexing
- The combinatorics solution is the fastest and lightest, but trades away the transparent grid intuition for a mathematical insight
- The `functools.cache` memoization keeps the recurrence identical while deleting four lines of dictionary handling, at the cost of caching the base cases too and of a decorator that hides where the lookup happens
- The `math.comb` one-liner is the shortest correct program on the page, but it states the closed form without evaluating it in the open, so it is only defensible to someone who can reproduce the Combinatorics derivation on request

### When to Use Each

- **Recursion**: As a first, self-derivable formulation of the recurrence, and the teaching baseline that Top-Down Memoization builds on directly
- **Top-Down Memoization**: When the recursive framing feels most natural and adding a cache is the quickest correct step up from the brute force
- **Bottom-Up DP**: When clarity is paramount or the grid will be extended with obstacles or weights that break the pure combinatorial form
- **Space-Optimized DP**: When the DP structure is still needed but memory is constrained
- **Combinatorics**: When raw speed and minimal space are the priority and the problem stays a clean down/right path count
- **Top-Down Memoization with `functools.cache`**: The Pythonic form of the memoized recursion, and the one to write when the grid gains obstacles or weights that keep the DP framing but make the closed form invalid
- **Library One-Liner with `math.comb`**: When the derivation has already been stated and the shortest, fastest evaluation of it is wanted; avoid it as an opening answer, since it shows the result without showing the reasoning

### Optimization Notes

- The memo dict keyed on `(i, j)` caps the recursion at one computation per cell, bringing the brute force to the same `O(m × n)` work as the table fills
- The 1D DP works because `dp[j] += dp[j-1]` reuses the old value of `dp[j]` (the cell above) and the freshly updated `dp[j-1]` (the cell to the left)
- The combinatorics solution is the recommended optimum: it multiplies before dividing within the loop to keep intermediate values integral and avoid overflow
- Iterating the binomial coefficient over `min(m-1, n-1)` terms keeps the work minimal regardless of grid orientation
- `functools.cache` reproduces the memo dict's asymptotics exactly, so it is a code-volume optimization rather than a speed one; the win over the manual memo is four deleted lines, not fewer operations
- `math.comb` applies the `min(m-1, n-1)` reduction and the exact-integer ordering internally and runs the product in C, so it beats the hand-rolled loop on constant factor while matching its `O(min(m, n))` bound
