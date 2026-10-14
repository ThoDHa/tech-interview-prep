# [Edit Distance](https://leetcode.com/problems/edit-distance/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/edit_distance/solution.py`](../../practice/edit_distance/solution.py)

You are given two strings `word1` and `word2`, each consisting of lowercase English letters.

You are allowed to perform three operations on `word1` an unlimited number of times:

* Insert a character at any position
* Delete a character at any position
* Replace a character at any position

Return the minimum number of operations to make `word1` equal `word2`.

## Examples

### Example 1

**Input:** `word1 = "monkeys", word2 = "money"`

**Output:** `2`

**Explanation:** `monkeys` -> `monkey` (remove `s`)
`monkey` -> `money`  (remove `k`)

### Example 2

**Input:** `word1 = "neatcdee", word2 = "neetcode"`

**Output:** `3`

**Explanation:** `neatcdee` -> `neetcdee`  (replace `a` with `e`)
`neetcdee` -> `neetcde`   (remove last `e`)
`neetcde`  -> `neetcode`  (insert `o`)

## Constraints

- `0 <= word1.length, word2.length <= 100`
- `word1` and `word2` consist of lowercase English letters.

## Deriving the Solution

Turning `word1` into `word2` is a sequence of decisions: align the two strings from the front, and at each alignment either the current characters match (free) or one of the three operations spends a move. The remaining work after a decision depends only on the two positions the alignment has reached, which makes "minimum operations for these remainders" a question with a fixed answer per position pair. Every solution below searches the same decision space; they differ in how much of it they re-derive.

1. **Start literal.** Try every operation at every mismatch and keep the
   cheapest outcome. The operation tree branches three ways per mismatch and
   costs `O(3^(m + n))`: see [Brute Force Recursion](#brute-force-recursion).
2. **Cache the states.** A branch's future depends only on `(i, j)`, the
   positions reached in `word1` and `word2`, never on the operations already
   spent, so the same pairs recur across different operation histories.
   Memoizing them collapses the tree to one solve per pair: see
   [Top-Down Memoization](#top-down-memoization).
3. **Tabulate the pairs.** The pairs form a two-dimensional grid
   `(prefix of word1, prefix of word2)` where each cell needs only the row
   above and the current row's left neighbor. Filling the grid row by row
   needs no recursion: see [Bottom-Up 2-D DP](#bottom-up-2-d-dp).
4. **Keep two rows.** Building row `i` reads row `i - 1` and the current
   row's left neighbor, so two rows suffice, `O(n)` space, same time: see
   [Space-Optimized Two-Row DP](#space-optimized-two-row-dp).
5. **Hand the cache to the library.** Step 2's memo dict is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the base cases, the match test, and the three-way
   minimum stay exactly as written: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Recursion

#### Derivation

The most literal reading aligns the two strings from the front. When the current characters agree, they cost nothing and both advance. When they differ, exactly one operation applies at the front: replace `word1[i]` into `word2[j]` (both advance), delete `word1[i]` (only `i` advances), or insert `word2[j]` into `word1` (only `j` advances). Trying all three and keeping the cheapest enumerates every operation sequence:

1. Define `dfs(i, j)` as the minimum operations turning `word1[i:]` into
   `word2[j:]`.
2. Return `len(word2) - j` when `i == len(word1)`: insert everything left of
   `word2`.
3. Return `len(word1) - i` when `j == len(word2)`: delete everything left of
   `word1`.
4. When `word1[i] == word2[j]`, return `dfs(i + 1, j + 1)`.
5. Otherwise return `1 + min(dfs(i + 1, j + 1), dfs(i + 1, j),
   dfs(i, j + 1))`: replace, delete, insert.
6. Return `dfs(0, 0)`.

#### Walkthrough

The tree is small enough on Example 1 to list whole: `word1 = "monkeys"`, `word2 = "money"`. The shared prefix `m`, `o`, `n` falls through three free matches to the first mismatch:

```text
dfs(0, 0)  'm' match
  dfs(1, 1)  'o' match
    dfs(2, 2)  'n' match
      dfs(3, 3)  'k' vs 'e' mismatch
        dfs(4, 4)  'e' vs 'y' mismatch
          dfs(5, 5) -> 2  (w2 exhausted: delete 'y', 's')
          dfs(5, 4)  'y' match
            dfs(6, 5) -> 1  (w2 exhausted: delete 's')
          dfs(5, 4) -> 1
          dfs(4, 5) -> 3  (w2 exhausted: delete 3 chars)
        dfs(4, 4) -> 2  (1 + min(2, 1, 3))
        dfs(4, 3)  'e' match
          dfs(5, 4)  'y' match
            dfs(6, 5) -> 1  (w2 exhausted)
          dfs(5, 4) -> 1
        dfs(4, 3) -> 1
        dfs(3, 4)  'k' vs 'y' mismatch
          dfs(4, 5) -> 3  (w2 exhausted)
          dfs(4, 4) -> 2  (1 + min(2, 1, 3))
          dfs(3, 5) -> 4  (w2 exhausted)
        dfs(3, 4) -> 3  (1 + min(3, 2, 4))
      dfs(3, 3) -> 2  (1 + min(2, 1, 3))
    dfs(2, 2) -> 2
  dfs(1, 1) -> 2
dfs(0, 0) -> 2
```

The winning line deletes `k` (`dfs(3, 3)`'s delete branch, reaching the free `'e'` match) and then deletes `s`, for `2` total, matching the expected Output for Example 1; Example 2's answer `3` follows the same fork structure through its replace/delete/insert chain.

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

Every mismatch forks into three branches, so the tree grows exponentially in the combined length; long shared prefixes prune nothing on adversarial inputs.

##### Space Complexity: `O(m + n)`

The recursion stack, one frame per consumed character.

#### Key Insights

- Transcribes the operation set directly: match is free, and the three
  operations are the three ways one pointer advances.
- The two base cases convert leftover suffixes into pure deletes or pure
  inserts, which is where every branch eventually lands.
- The same `(i, j)` states are re-derived across different operation
  histories (visible above: `dfs(4, 4)` runs twice), which is the redundancy
  the next solution removes.

### Top-Down Memoization

#### Derivation

The recursion re-solves futures it has already seen: the mismatch at `dfs(3, 3)` and the one at `dfs(3, 4)` both descend into `dfs(4, 4)`, yet the subtree below is walked twice. A branch's future depends only on `(i, j)`, never on the operations that got there, so each pair is a [memoizable](https://en.wikipedia.org/wiki/Memoization) state with `(m + 1) × (n + 1)` of them:

1. Keep the recursion unchanged.
2. Add a `memo` keyed by `(i, j)`; check it on entry and store before every
   return.

#### Walkthrough

Trace the recursion with hits marked on Example 1: `word1 = "monkeys"`, `word2 = "money"`. The descent matches the brute force until the memo absorbs the repeats:

```text
dfs(0, 0)  'm' match
  dfs(1, 1)  'o' match
    dfs(2, 2)  'n' match
      dfs(3, 3)  'k' vs 'e' mismatch
        dfs(4, 4)  'e' vs 'y' mismatch
          dfs(5, 5) -> 2  (w2 exhausted)
          dfs(5, 4)  'y' match
            dfs(6, 5) -> 1  (w2 exhausted)
          dfs(5, 4) -> 1  stored
          dfs(4, 5) -> 3  (w2 exhausted)
        dfs(4, 4) -> 2  (1 + min(2, 1, 3))  stored
        dfs(4, 3)  'e' match
          dfs(5, 4) -> 1  ** memo hit **
        dfs(4, 3) -> 1  stored
        dfs(3, 4)  'k' vs 'y' mismatch
          dfs(4, 5) -> 3  (w2 exhausted)
          dfs(4, 4) -> 2  ** memo hit **
          dfs(3, 5) -> 4  (w2 exhausted)
        dfs(3, 4) -> 3  (1 + min(3, 2, 4))  stored
      dfs(3, 3) -> 2  (1 + min(2, 1, 3))  stored
    dfs(2, 2) -> 2  stored
  dfs(1, 1) -> 2  stored
dfs(0, 0) -> 2  stored
```

Two repeat arrivals are answered from the memo (`dfs(5, 4)` and `dfs(4, 4)`), so 8 states are stored against the brute tree's 20 calls. The root returns `2`, matching the expected Output for Example 1. On denser mismatch patterns the ratio widens fast: the tree branches three ways per mismatch while the state count stays rectangular.

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

##### Time Complexity: `O(m * n)`

At most `(m + 1) × (n + 1)` states, each solved once with constant work plus three recursions into smaller pairs.

##### Space Complexity: `O(m * n)`

The memo's entries plus a recursion stack of up to `m + n` frames.

#### Key Insights

- The state `(i, j)` is a complete summary of the operation history: which
  operations were spent cannot change the minimum that remains.
- The two base cases stay outside the memo: their answers are arithmetic,
  not computed.
- Memoization alone already reaches the optimal complexity class; the table
  versions that follow change only the evaluation order and the memory.

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

Let \(dp_i[j]\) be the edit distance between the first `i` characters of `word1` and the first `j` of `word2`:

$$ dp_i[j] = \begin{cases} j, & i = 0 \\ i, & j = 0 \\ dp_{i-1}[j-1], & i, j > 0,\ \text{word1}[i-1] = \text{word2}[j-1] \\ 1 + \min\!\begin{cases} dp_{i-1}[j] \\ dp_i[j-1] \\ dp_{i-1}[j-1] \end{cases} & i, j > 0,\ \text{word1}[i-1] \neq \text{word2}[j-1] \end{cases} $$

```text
dp_0[j] = j                          (insert j characters)
dp_i[0] = i                          (delete i characters)
dp_i[j] = dp_(i-1)[j-1]              (when word1[i - 1] == word2[j - 1])
dp_i[j] = 1 + min(dp_(i-1)[j],      (delete word1[i - 1])
                  dp_i[j-1],        (insert word2[j - 1])
                  dp_(i-1)[j-1])    (replace word1[i - 1] with word2[j - 1])
```

The three mismatch terms are the three operations priced at one move each, each pointing at the state the operation hands over. The answer is \(dp_m[n]\), the full strings' distance.

#### Walkthrough

Trace the fill on Example 1: `word1 = "monkeys"`, `word2 = "money"`. Rows are `word1` prefixes, columns are `word2` prefixes:

```text
        ''  m  o  n  e  y
  ''     0  1  2  3  4  5
  m      1  0  1  2  3  4
  o      2  1  0  1  2  3
  n      3  2  1  0  1  2
  k      4  3  2  1  1  2
  e      5  4  3  2  1  2
  y      6  5  4  3  2  1
  s      7  6  5  4  3  2
```

The shared prefix holds the diagonal at `0` until row `k`, where the mismatch lifts the row to `1 + min(1, 1, 0) = 1` at `[k][e]`; rows `e` and `y` each inherit free matches on the diagonal (`[e][e] = 1`, `[y][y] = 1`). The bottom-right cell is `2`, matching the expected Output for Example 1: delete `s`, delete `k`. Example 2's table fills the same way to `3`.

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

##### Time Complexity: `O(m * n)`

One comparison plus one three-way minimum per table cell.

##### Space Complexity: `O(m * n)`

The full table.

#### Key Insights

- The border rows encode the base cases as arithmetic: converting a prefix
  into the empty string costs its length.
- The free-match rule (`dp[i][j] = dp[i - 1][j - 1]`) is what makes shared
  prefixes cheap; a forced-cost variant would have to take a minimum on
  matches too.
- The table orientation matches the recursion's suffix indexing flipped to
  prefixes, which is why every cell reads only up-and-left neighbors.

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

Trace the two rolling rows on Example 1: `word1 = "monkeys"`, `word2 = "money"`:

```text
i=0         previous = [0, 1, 2, 3, 4, 5]
i=1 (m)     current  = [1, 0, 1, 2, 3, 4]
i=2 (o)     current  = [2, 1, 0, 1, 2, 3]
i=3 (n)     current  = [3, 2, 1, 0, 1, 2]
i=4 (k)     current  = [4, 3, 2, 1, 1, 2]
i=5 (e)     current  = [5, 4, 3, 2, 1, 2]
i=6 (y)     current  = [6, 5, 4, 3, 2, 1]
i=7 (s)     current  = [7, 6, 5, 4, 3, 2]
```

Each row equals the corresponding table row from the Bottom-Up 2-D DP walkthrough, and the unneeded predecessor is discarded as soon as its successor exists. In row `k`, cell `[k][e]` takes `1 + min(previous[e] = 1, current[n] = 1, previous[n] = 0) = 1`, the diagonal replace being cheapest. The final `previous[n]` is `2`, matching the expected Output for Example 1; Example 2's last row ends in `3`.

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

##### Time Complexity: `O(m * n)`

One comparison per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `n + 1` cells; the discarded predecessor is garbage-collected.

#### Key Insights

- The dependency pattern of the recurrence determines its memory: anything a
  cell does not read can be freed.
- `current` must be a fresh row per `i`; updating `previous` in place would overwrite
  the diagonal `previous[j - 1]` before it is read.
- Iterating the shorter string as `word2` minimizes the row width; the
  distance is unchanged by the argument order.

### Top-Down Memoization with functools.cache

#### Derivation

Step 2's memo is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dfs(i, j)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the base cases, the match test, and the three-way minimum untouched:

1. Keep the memoized recursion's structure: the same two base cases, the
   same match shortcut and three-way fork.
2. Replace the `memo` dict with `@cache` on `dfs`, keyed automatically by the
   arguments `(i, j)`.
3. Return `dfs(0, 0)`.

The one behavioral cost: `@cache` also stores the base-case results and keeps every pair alive for the life of the process, so the memory profile matches or slightly exceeds the dict version.

#### Walkthrough

Trace the decorated recursion on Example 1: `word1 = "monkeys"`, `word2 = "money"`. The call sequence is identical to the Top-Down Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dfs(0, 0) -> ... identical descent ...
dfs(5, 4) -> 1                       ** cached: no recompute **
dfs(4, 4) -> 2                       ** cached: no recompute **
dfs(0, 0) -> 2
```

12 distinct `(i, j)` calls are cached (the dict version stored only the 8 interior states), each of the 3 repeat arrivals is a hit, and the answer is `2`, matching the expected Output for Example 1.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        @cache
        def dfs(i: int, j: int) -> int:
            if i == len(word1):
                return len(word2) - j
            if j == len(word2):
                return len(word1) - i
            if word1[i] == word2[j]:
                return dfs(i + 1, j + 1)
            return 1 + min(
                dfs(i + 1, j + 1),
                dfs(i + 1, j),
                dfs(i, j + 1),
            )

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

The cache admits each `(i, j)` pair once; the body is constant work.

##### Space Complexity: `O(m * n)`

The decorator's cache plus the recursion stack.

#### Key Insights

- `functools.cache` is the dict-based memo with the ceremony removed: same
  asymptotics, three fewer lines, no key-tuple mistakes.
- Caching base cases is harmless: their results are simple arithmetic.
- The recursion body is the operation set in its purest form, which makes it
  the version to quote in an interview after sketching the dict.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(3^(m + n))` - three branches per mismatch.
- **Top-Down Memoization**: `O(m * n)` - one solve per `(i, j)` state.
- **Bottom-Up 2-D DP**: `O(m * n)` - one update per table cell.
- **Space-Optimized Two-Row DP**: `O(m * n)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the dict memo with library bookkeeping.

### Space Complexity

- **Brute Force Recursion**: `O(m + n)` - the recursion stack.
- **Top-Down Memoization**: `O(m * n)` - the memo plus the stack.
- **Bottom-Up 2-D DP**: `O(m * n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the decorator's cache plus the stack.

### Trade-offs

- The brute force derives straight from the operation set and is correct by
  construction, but unusable beyond roughly 15 characters per string.
- The memoized recursions carry a call stack and an `O(m * n)` cache; the
  table versions trade the stack for an evaluation order.
- The two-row table is the production form: same time as everything else at
  linear memory.

### When to Use Each

- **Brute Force Recursion**: tiny inputs, or as the brute-force oracle when
  checking the faster versions.
- **Top-Down Memoization**: when deriving live; the fork writes itself from
  the operation list.
- **Bottom-Up 2-D DP**: when the full table matters, for example to
  reconstruct the operation sequence by walking it backward.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the dict ceremony.

### Optimization Notes

- Iterating the shorter string as `word2` shrinks the two-row version's
  footprint from `O(max(m, n))` to `O(min(m, n))`.
- A fourth operation, transposing two adjacent characters, turns this into
  the Damerau-Levenshtein distance: the cell then also reads
  `dp[i - 2][j - 2]` plus one when both characters swap pairwise.
- Reconstruction of an actual operation sequence needs the full table: walk
  from `dp[m][n]`, preferring the free-match diagonal, then the cheapest
  mismatch neighbor, which is the one feature the space optimization gives
  up.
