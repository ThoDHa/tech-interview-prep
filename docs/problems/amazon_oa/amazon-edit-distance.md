# [Edit Distance](https://www.fastprep.io/problems/amazon-edit-distance)

**Medium** | **NN minutes** | **String, Dynamic Programming**

Given two strings word1 and word2, return the minimum number of single-character operations needed to transform word1 into word2.

Each operation is one of the following:

Insert one character.Delete one character.Replace one character.

## Examples

### Example 1

**Input:** `word1 = "horse"`, `word2 = "ros"`

**Output:** `3`

**Explanation:** Replace h with r, delete the second r, and delete e.

### Example 2

**Input:** `word1 = "intention"`, `word2 = "execution"`

**Output:** `5`

**Explanation:** A minimum transformation uses five insert, delete, or replace operations.

### Example 3

**Input:** `word1 = ""`, `word2 = "abc"`

**Output:** `3`

**Explanation:** Insert a, b, and c.

## Constraints

- `0 <= word1.length <= 500.`
- `0 <= word2.length <= 500.`
- `Both strings contain only lowercase English letters.`

## Solutions

### Brute Force Recursion

#### Derivation

The most literal reading aligns the two strings from the front. When the current characters agree, they cost nothing and both advance. When they differ, exactly one operation applies at the front, and each operation has a characteristic effect on the two positions: replace turns `word1[i]` into `word2[j]`, so both advance; delete removes `word1[i]`, so only `i` advances; insert conjures `word2[j]` into `word1`, so only `j` advances. Trying all three at every mismatch and keeping the cheapest outcome enumerates every operation sequence:

1. Define `dfs(i, j)` as the minimum operations turning `word1[i:]` into
   `word2[j:]`.
2. Return `len(word2) - j` when `i == len(word1)`: insert everything left of
   `word2`.
3. Return `len(word1) - i` when `j == len(word2)`: delete everything left of
   `word1`.
4. When `word1[i] == word2[j]`, return `dfs(i + 1, j + 1)`.
5. Otherwise return `1 + min(dfs(i + 1, j + 1), dfs(i + 1, j), dfs(i, j + 1))`:
   replace, delete, insert.
6. Return `dfs(0, 0)`.

#### Walkthrough

Example 1 has no shared prefix to fall through (`h` meets `r` immediately), so the tree is bushy from the root: `word1 = "horse"`, `word2 = "ros"`. Branches are listed in the code's order, replace, delete, insert, and each line shows the returned or propagated value:

```text
dfs(0,0)  'h' vs 'r' mismatch
  R dfs(1,1)  'o' match
    dfs(2,2)  'r' vs 's' mismatch
      R dfs(3,3) -> 2  (w2 exhausted: delete 's', 'e')
      D dfs(3,2)  's' match
        dfs(4,3) -> 1  (w2 exhausted: delete 'e')
      dfs(3,2) -> 1
      I dfs(2,3) -> 3  (w2 exhausted: delete 3 chars)
    dfs(2,2) -> 2  (1 + min(2, 1, 3))
  dfs(1,1) -> 2
  D dfs(1,0)  'o' vs 'r' mismatch
    R dfs(2,1)  'r' vs 'o' mismatch
      R dfs(3,2) -> 1  (seen above)
      D dfs(3,1)  'r' match
        dfs(4,2)  's' vs 'o' mismatch
          R dfs(5,3) -> 0  (w1 exhausted: insert nothing)
          D dfs(5,2) -> 1  (w1 exhausted: insert 's')
          I dfs(4,3) -> 1  (w2 exhausted: delete 'e')
        dfs(4,2) -> 1  (1 + min(0, 1, 1))
      dfs(3,1) -> 1
      I dfs(2,2) -> 2  (seen above)
    dfs(2,1) -> 2  (1 + min(1, 1, 2))
    D dfs(2,0)  'r' match
      dfs(3,1) -> 1
    dfs(2,0) -> 1
    I dfs(1,1) -> 2  (seen above)
  dfs(1,0) -> 2  (1 + min(2, 1, 2))
  I dfs(0,1)  'h' vs 'o' mismatch
    R dfs(1,2)  'o' vs 's' mismatch
      R dfs(2,3) -> 3  (w2 exhausted)
      D dfs(2,2) -> 2  (seen above)
      I dfs(1,3) -> 4  (w2 exhausted)
    dfs(1,2) -> 3  (1 + min(3, 2, 4))
    D dfs(1,1) -> 2  (seen above)
    I dfs(0,2)  'h' vs 's' mismatch
      R dfs(1,3) -> 4  (w2 exhausted)
      D dfs(1,2) -> 3  (seen above)
      I dfs(0,3) -> 5  (w2 exhausted)
    dfs(0,2) -> 4  (1 + min(4, 3, 5))
  dfs(0,1) -> 3  (1 + min(3, 2, 4))
dfs(0,0) -> 3  (1 + min(2, 2, 3))
```

The winning line replaces `h` with `r` (`dfs(1,1)`), lets `o` match for free, replaces `r` with `s` at `dfs(2,2)` (its cheapest branch is the delete `dfs(3,2)`, which then rides the free `s` match), for `3` total. Three states were re-derived across different branches (`dfs(3,2)` twice, `dfs(2,2)` twice, `dfs(1,1)` twice), visible above as "seen above" repeats, and the repeats multiply on longer inputs.

#### Solution

The code is the walkthrough's operation tree: one match shortcut, one three-way fork.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        def dfs(i: int, j: int) -> int:
            if i == len(word1):
                return len(word2) - j
            if j == len(word2):
                return len(word1) - i
            if word1[i] == word2[j]:
                return dfs(i + 1, j + 1)
            return 1 + min(
                dfs(i + 1, j + 1),  # replace word1[i] with word2[j]
                dfs(i + 1, j),      # delete word1[i]
                dfs(i, j + 1),      # insert word2[j]
            )

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^(m + n))`

Every mismatch forks into three branches, so the tree grows exponentially in the combined length; long shared prefixes prune nothing on mismatch-heavy inputs.

##### Space Complexity: `O(m + n)`

The recursion stack, one frame per consumed character.

#### Key Insights

- Transcribes the operation set directly: a match is free, and the three operations are the three ways the alignment pointers advance.
- The two base cases convert leftover suffixes into pure inserts or pure deletes, which is where every branch eventually lands.
- The same `(i, j)` states are re-derived across different operation histories (three such repeats appear in the Example 1 trace), which is the redundancy the next solution removes.

### Top-Down Memoization

#### Derivation

The recursion re-solves futures it has already seen: in the Example 1 trace, the state `dfs(2, 2)` is walked twice and `dfs(1, 1)` twice more. A branch's future depends only on `(i, j)`, the positions reached in the two strings, never on the operations that got there, so each pair is a [memoizable](https://en.wikipedia.org/wiki/Memoization) state and there are only `(m + 1) × (n + 1)` of them. Caching turns the exponential tree into one solve per pair:

1. Keep the recursion unchanged.
2. Add a `memo` keyed by `(i, j)`; check it on entry and store before every
   return.

#### Walkthrough

Trace the same Example 1 tree with the memo active, `word1 = "horse"`, `word2 = "ros"`. Base cases answer directly; every interior state stores before returning; repeat arrivals are answered from the memo:

```text
dfs(0,0)  'h' vs 'r' mismatch
  R dfs(1,1)  'o' match
    dfs(2,2)  'r' vs 's' mismatch
      R dfs(3,3) -> 2  (w2 exhausted)
      D dfs(3,2)  's' match
        dfs(4,3) -> 1  (w2 exhausted)
      dfs(3,2) -> 1  stored
      I dfs(2,3) -> 3  (w2 exhausted)
    dfs(2,2) -> 2  (1 + min(2, 1, 3))  stored
  dfs(1,1) -> 2  stored
  D dfs(1,0)  'o' vs 'r' mismatch
    R dfs(2,1)  'r' vs 'o' mismatch
      R dfs(3,2) -> 1  ** memo hit **
      D dfs(3,1)  'r' match
        dfs(4,2)  's' vs 'o' mismatch
          R dfs(5,3) -> 0  (w1 exhausted)
          D dfs(5,2) -> 1  (w1 exhausted)
          I dfs(4,3) -> 1  (w2 exhausted)
        dfs(4,2) -> 1  (1 + min(0, 1, 1))  stored
      dfs(3,1) -> 1  stored
      I dfs(2,2) -> 2  ** memo hit **
    dfs(2,1) -> 2  (1 + min(1, 1, 2))  stored
    D dfs(2,0)  'r' match
      dfs(3,1) -> 1  ** memo hit **
    dfs(2,0) -> 1  stored
    I dfs(1,1) -> 2  ** memo hit **
  dfs(1,0) -> 2  (1 + min(2, 1, 2))  stored
  I dfs(0,1)  'h' vs 'o' mismatch
    R dfs(1,2)  'o' vs 's' mismatch
      R dfs(2,3) -> 3  (w2 exhausted)
      D dfs(2,2) -> 2  ** memo hit **
      I dfs(1,3) -> 4  (w2 exhausted)
    dfs(1,2) -> 3  (1 + min(3, 2, 4))  stored
    D dfs(1,1) -> 2  ** memo hit **
    I dfs(0,2)  'h' vs 's' mismatch
      R dfs(1,3) -> 4  (w2 exhausted)
      D dfs(1,2) -> 3  ** memo hit **
      I dfs(0,3) -> 5  (w2 exhausted)
    dfs(0,2) -> 4  (1 + min(4, 3, 5))  stored
  dfs(0,1) -> 3  (1 + min(3, 2, 4))  stored
dfs(0,0) -> 3  (1 + min(2, 2, 3))  stored
```

Eight repeat arrivals were answered from the memo (`dfs(3,2)`, `dfs(2,2)` three times, `dfs(3,1)`, `dfs(1,1)` twice, `dfs(1,2)`), so 12 states are stored against the brute tree's 27 calls. The root returns `3`, matching Example 1's Output. On longer, denser mismatch patterns the ratio widens fast: the tree branches three ways per mismatch while the state count stays rectangular.

#### Solution

The code is the recursion with a dict in front of it.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        memo = {}

        def dfs(i: int, j: int) -> int:
            if i == len(word1):
                return len(word2) - j
            if j == len(word2):
                return len(word1) - i
            if (i, j) in memo:
                return memo[(i, j)]
            if word1[i] == word2[j]:
                result = dfs(i + 1, j + 1)
            else:
                result = 1 + min(
                    dfs(i + 1, j + 1),
                    dfs(i + 1, j),
                    dfs(i, j + 1),
                )
            memo[(i, j)] = result
            return result

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each of the `(m + 1) × (n + 1)` states is solved at most once, and a solve spends constant work on top of its recursive calls.

##### Space Complexity: `O(m × n)`

The memo holds one entry per solved state, and the recursion stack adds at most `m + n` frames.

#### Key Insights

- Memoization changes the count of solves, not the recursion: the state definition `(i, j)` and the transition are exactly the brute force's.
- The state count is the product of the positions, never the operation histories, which is why the collapse is from exponential to quadratic.
- The base cases sit before the memo check and need no storage: their answers are already `O(1)` arithmetic.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still asks from the top: "how many operations do the suffixes need?". Flip it: `dp[i][j]` is the minimum operations turning the first `i` characters of `word1` into the first `j` of `word2`. Row 0 and column 0 are the base cases (`j` inserts, `i` deletes); each interior cell either inherits the diagonal on a free match or takes one plus the best of the replace, delete, and insert neighbors. Filling row by row never reads an undecided cell:

1. Allocate `dp` of size `(m + 1) x (n + 1)`; set `dp[0][j] = j` and
   `dp[i][0] = i`.
2. For each `i` in `1..m` and `j` in `1..n`:
   - `word1[i - 1] == word2[j - 1]`: `dp[i][j] = dp[i - 1][j - 1]`.
   - Otherwise: `dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1],
     dp[i - 1][j - 1])`.
3. Return `dp[m][n]`.

The `- 1` offsets exist because the table counts prefixes while the strings are position-indexed: cell `(i, j)` decides with `word1[i - 1]` and `word2[j - 1]`.

#### Recurrence

Let `dp[i][j]` be the edit distance between the first `i` characters of `word1` and the first `j` of `word2`:

$$ dp[i][j] = \begin{cases} j, & i = 0 \\ i, & j = 0 \\ dp[i-1][j-1], & i, j > 0,\ \text{word1}[i-1] = \text{word2}[j-1] \\ 1 + \min\!\begin{cases} dp[i-1][j] \\ dp[i][j-1] \\ dp[i-1][j-1] \end{cases} & i, j > 0,\ \text{word1}[i-1] \neq \text{word2}[j-1] \end{cases} $$

```text
dp[0][j] = j                          (insert j characters)
dp[i][0] = i                          (delete i characters)
dp[i][j] = dp[i - 1][j - 1]           (when word1[i - 1] == word2[j - 1])
dp[i][j] = 1 + min(dp[i - 1][j],      (delete word1[i - 1])
                   dp[i][j - 1],      (insert word2[j - 1])
                   dp[i - 1][j - 1])  (replace word1[i - 1] with word2[j - 1])
```

The three mismatch terms are the three operations priced at one move each, each pointing at the state the operation hands over. The answer is `dp[m][n]`, the full strings' distance.

#### Walkthrough

Trace the fill on Example 1: `word1 = "horse"`, `word2 = "ros"`. Rows are `word1` prefixes, columns are `word2` prefixes:

```text
        ''  r  o  s
  ''     0  1  2  3
  h      1  1  2  3
  o      2  2  1  2
  r      3  2  2  2
  s      4  3  3  2
  e      5  4  4  3
```

Three cells carry the trace: `[o][o]` is a free match, inheriting the diagonal `1`; `[r][r]` inherits `dp[2][0] = 2` the same way; and `[e][s]` takes the mismatch minimum `1 + min(dp[4][3] = 2, dp[5][2] = 4, dp[4][2] = 3) = 3`, the delete being cheapest. The bottom-right cell is `3`, matching the expected Output for Example 1: replace `h` with `r`, delete `r`, delete `e`. Example 3 (`""` into `"abc"`) is the pure base case: row 0 reads `0, 1, 2, 3` and nothing else fills.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            dp[i][0] = i
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # delete word1[i - 1]
                        dp[i][j - 1],      # insert word2[j - 1]
                        dp[i - 1][j - 1],  # replace
                    )
        return dp[m][n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One comparison plus one three-way minimum per table cell.

##### Space Complexity: `O(m × n)`

The full table.

#### Key Insights

- The border row and column encode the base cases as arithmetic: converting a prefix into the empty string costs its length, which is also the whole story of Example 3.
- The free-match rule (`dp[i][j] = dp[i - 1][j - 1]`) is what makes shared characters cheap; a forced-cost variant would have to take a minimum on matches too.
- The table orientation matches the recursion's suffix indexing flipped to prefixes, which is why every cell reads only up-and-left neighbors, and why no recursion is needed to fill it.

### Space-Optimized Two-Row DP

#### Derivation

Cell `(i, j)` reads only `dp[i - 1][j - 1]`, `dp[i - 1][j]`, and `dp[i][j - 1]`: the previous row and the cell just built. Row `i - 2` and older are dead weight, so the whole table collapses to two rows, `previous` for row `i - 1` and `current` under construction. Row rotation (`previous = current`) plays the role the index decrement played in the recursion, and the border moves into the loop (`current[0] = i`):

1. Initialize `previous` to `list(range(n + 1))`, row 0.
2. For each `i` in `1..m`, build `current` from `previous`:
   `current[0] = i`, and for `j` in `1..n`:
   - `word1[i - 1] == word2[j - 1]`: `current[j] = previous[j - 1]`.
   - Otherwise: `current[j] = 1 + min(previous[j], current[j - 1], previous[j - 1])`.
3. Replace `previous` with `current` and continue.
4. Return `previous[n]`, the last row's last cell.

#### Walkthrough

Trace the two rolling rows on Example 1: `word1 = "horse"`, `word2 = "ros"`:

```text
i=0         previous = [0, 1, 2, 3]
i=1 (h)     current  = [1, 1, 2, 3]
i=2 (o)     current  = [2, 2, 1, 2]
i=3 (r)     current  = [3, 2, 2, 2]
i=4 (s)     current  = [4, 3, 3, 2]
i=5 (e)     current  = [5, 4, 4, 3]
```

Each row equals the corresponding table row from the Bottom-Up 2-D DP walkthrough, and the unneeded predecessor is discarded as soon as its successor exists. In row `e`, the last cell takes `1 + min(previous[3] = 2, current[2] = 4, previous[2] = 3) = 3`, the delete being cheapest. The final `previous[3]` is `3`, matching the expected Output for Example 1. Example 3 (`word1 = ""`, `word2 = "abc"`) never enters the row loop, so `previous` stays the initial `[0, 1, 2, 3]` and `previous[3] = 3` falls straight out of row 0.

#### Solution

The code is the walkthrough's row loop: build `current` from `previous`, then rotate.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        previous = list(range(n + 1))
        for i in range(1, m + 1):
            current = [i] + [0] * n
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    current[j] = previous[j - 1]
                else:
                    current[j] = 1 + min(
                        previous[j],      # delete word1[i - 1]
                        current[j - 1],   # insert word2[j - 1]
                        previous[j - 1],  # replace word1[i - 1] with word2[j - 1]
                    )
            previous = current
        return previous[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One comparison per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `n + 1` cells; the discarded predecessor is garbage-collected.

#### Key Insights

- Row `i` only ever consults row `i - 1`, so the two-row collapse loses nothing; the full table is worth its space only when the operations themselves must be reconstructed.
- `previous = current` is the whole state machine: the recursion's `i - 1` becomes a rotation, and the base case `dp[i][0] = i` becomes `current[0] = i`.
- With `m` the shorter string, naming the rows after `word2` caps the memory at the smaller length; the code above keeps `word2` in the rows for readability.

### Top-Down Memoization with functools.cache

#### Derivation

The memo dict in [Top-Down Memoization](#top-down-memoization) is bookkeeping, not logic: check on entry, store before return, and the stored key is spelled twice. [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) takes over exactly that bookkeeping: decorating the recursion gives it the same per-state caching with zero explicit memory lines, while the base cases, the match test, and the three-way minimum stay exactly as the brute force wrote them:

1. Keep the brute force recursion unchanged.
2. Decorate it with `@cache`.

The decoration stores by argument tuple, which replaces `memo[(i, j)]` verbatim; nothing else moves.

#### Walkthrough

The cached recursion visits the same states as the Top-Down Memoization trace on Example 1 (`word1 = "horse"`, `word2 = "ros"`), stores the same 12 interior states, and answers the same 8 repeat arrivals from the cache; the only visible difference is that no line of code mentions the store. Reading that trace with "stored" relabeled "cached" is the whole walkthrough: the root still descends `replace` first through the free `o` match to the `r`/`s` mismatch, the delete branch `dfs(3, 2) -> 1` is the first cached value to be hit, and the root combines `1 + min(2, 2, 3) = 3`, matching Example 1's Output.

#### Solution

The brute force recursion plus one decorator line.

```python
from functools import cache


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @cache
        def distance(i: int, j: int) -> int:
            if i == len(word1):
                return len(word2) - j
            if j == len(word2):
                return len(word1) - i
            if word1[i] == word2[j]:
                return distance(i + 1, j + 1)
            return 1 + min(
                distance(i + 1, j + 1),
                distance(i + 1, j),
                distance(i, j + 1),
            )

        return distance(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The cache memoizes by argument tuple, so each of the `(m + 1) × (n + 1)` states is computed once, exactly as with the explicit dict.

##### Space Complexity: `O(m × n)`

The cache holds one entry per computed state, plus at most `m + n` stack frames.

#### Key Insights

- `@cache` replaces the memo dict's three bookkeeping lines with one decorator, leaving the recursion's logic untouched; the algorithm is provably the one from Top-Down Memoization.
- The cache lives as long as the closure does, which is fine inside one call and worth remembering if the decorated function ever escapes to a second input.
- Cache hits require hashable arguments; plain integers make `(i, j)` hashing free of surprises.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(3^(m + n))` - every mismatch forks three subtrees.
- **Top-Down Memoization**: `O(m × n)` - one solve per position pair.
- **Bottom-Up 2-D DP**: `O(m × n)` - one constant-work fill per cell.
- **Space-Optimized Two-Row DP**: `O(m × n)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(m × n)` - identical states, caching delegated to the decorator.

### Space Complexity

- **Brute Force Recursion**: `O(m + n)` - recursion stack only.
- **Top-Down Memoization**: `O(m × n)` - memo dict plus stack.
- **Bottom-Up 2-D DP**: `O(m × n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - two rows.
- **Top-Down Memoization with functools.cache**: `O(m × n)` - the decorator's cache plus stack.

### Trade-offs

- The Brute Force Recursion approach is the direct transcription of the operation set and the base for everything else, but its exponential blowup makes it viable only for toy inputs.
- The Top-Down Memoization approach keeps the recursion's shape and buys quadratic time with one dict; the cost is carrying the cache bookkeeping inside the logic.
- The Bottom-Up 2-D DP approach removes the recursion entirely, which makes the fill order explicit and the operations reconstructable from the finished table, at the price of the full `O(m × n)` table.
- The Space-Optimized Two-Row DP approach cuts memory to one row pair, but it discards older rows, so reconstructing which operations were used is no longer possible from the table alone.
- The functools.cache variant is the shortest correct expression of the memoized recursion, giving up explicit control of the cache in exchange for deleting its bookkeeping.

### When to Use Each

- **Brute Force Recursion**: To establish the state definition and transitions before optimizing; never for the constraint sizes.
- **Top-Down Memoization**: When the suffix formulation is the clearest to explain and the cache should stay visible.
- **Bottom-Up 2-D DP**: When the operation sequence itself must be recovered (walk the table back from `dp[m][n]`), or when recursion depth is a concern.
- **Space-Optimized Two-Row DP (Recommended)**: The default for the real OA: quadratic time, linear space, no recursion limit exposure, and only the last-row answer needed.
- **Top-Down Memoization with functools.cache**: For a quick, low-risk transcription when the recursion is already written and Python is the interview language.

### Optimization Notes

- The state space `(m + 1) × (n + 1)` is the ceiling for every approach except the brute force; the fastest and the smallest-memory solutions differ only in which cells they keep resident.
- Recursion depth is a real constraint here: `word1` and `word2` can each reach 500 characters, putting the top-down stack near `m + n = 1000` frames, right at Python's default recursion limit; the bottom-up fills have no such exposure.
- The two-row collapse names `word2`'s length for the row size; swapping the arguments so the shorter string forms the rows bounds the memory by `min(m, n)` at the cost of one line.
- All three quadratic approaches spend their time in the same three-way `min`; vectorizing the inner loop or bit-parallelizing the row (the domain of the Myers bit-vector algorithm) is beyond what an OA asks but is the next rung for very large inputs.
