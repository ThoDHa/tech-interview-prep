# [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/longest_common_subsequence/solution.py`](../../practice/longest_common_subsequence/solution.py)

Given two strings `text1` and `text2`, return the length of the *longest common subsequence* between the two strings if one exists, otherwise return `0`.

A **subsequence** is a sequence that can be derived from the given sequence by deleting some or no elements  without changing the relative order of the remaining characters.

* For example, `"cat"` is a subsequence of `"crabt"`.

A **common subsequence** of two strings is a subsequence that exists in both strings.

## Examples

### Example 1

**Input:** `text1 = "cat", text2 = "crabt"`

**Output:** `3`

**Explanation:** The longest common subsequence is "cat" which has a length of 3.

### Example 2

**Input:** `text1 = "abcd", text2 = "abcd"`

**Output:** `4`

### Example 3

**Input:** `text1 = "abcd", text2 = "efgh"`

**Output:** `0`

## Constraints

- `1 <= text1.length, text2.length <= 1000`
- `text1` and `text2` consist of only lowercase English characters.

## Deriving the Solution

A common subsequence is a sequence of positions in `text1` and a sequence of positions in `text2` that spell the same characters in the same order, so the question "how long is the longest one?" decomposes over prefix pairs: decide what the current pair of last characters contributes, then hand the remains to a smaller pair. Every solution below works through the same prefix pairs; they differ in which pairs they re-derive and how many results they keep in memory.

1. **Start literal.** Enumerate every subsequence of `text1` and test whether
   it appears as a subsequence of `text2`, longest first. There are `2^m`
   subsequences, so this dies long before the stated bounds of `1000`
   characters: see [Subsequence Enumeration](#subsequence-enumeration).
2. **Spot the overlap.** Testing a subsequence re-derives knowledge about its
   prefixes over and over: the question "how much of this prefix pair
   matches?" is asked about the same prefixes in countless combinations. The
   answer for a pair depends only on the pair, so the pairs are cacheable
   states: see [Top-Down Memoization](#top-down-memoization).
3. **Tabulate the pairs.** The pairs form a two-dimensional grid
   `(prefix of text1, prefix of text2)` where each cell needs only the cell
   diagonally above-left, the cell above, and the cell to the left. Filling
   the grid row by row from `("", "")` needs no recursion at all, one
   comparison per cell, `O(m * n)`: see [Bottom-Up 2-D DP](#bottom-up-2-d-dp).
4. **Keep two rows.** Building row `i` reads row `i - 1` and the current
   row's left neighbor, so the full table is never needed: two rows suffice,
   `O(n)` space, same `O(m * n)` time: see
   [Space-Optimized Two-Row DP](#space-optimized-two-row-dp).
5. **Hand the cache to the library.** Step 2's memo dict is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the match test and the two base cases stay exactly as
   written: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Subsequence Enumeration

#### Derivation

The most literal reading of "the longest common subsequence" generates candidates and tests them: every way of deleting characters from `text1` is a candidate, and the longest one that also fits inside `text2` as a subsequence is the answer. Checking longest first lets the search stop at the first hit:

1. For each length from `min(m, n)` down to `1`, enumerate every
   `itertools.combinations` of positions in `text1` of that length and read
   off the candidate string.
2. For each candidate, walk through `text2` and test whether the candidate's
   characters appear in order (a two-pointer scan).
3. Return the first candidate that passes; `0` when no candidate of any
   length passes.

#### Walkthrough

Trace the search on Example 1: `text1 = "cat"`, `text2 = "crabt"`. Length 3 has exactly one candidate, and it passes:

```text
length 3: "cat"  in "crabt" as subsequence?  c..a..t  yes -> return 3
```

The two-pointer check aligns `c`, `a`, `t` against positions `0`, `2`, `4` of `"crabt"`. On Example 3 (`"abcd"` versus `"efgh"`) every candidate from length 4 down to length 1 fails to align, so the loop exhausts and returns `0`.

#### Solution

The code is the longest-first candidate loop with the two-pointer subsequence test.

```python
from itertools import combinations


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        for size in range(min(len(text1), len(text2)), 0, -1):
            for positions in combinations(range(len(text1)), size):
                candidate = "".join(text1[i] for i in positions)
                if self._is_subsequence(candidate, text2):
                    return size
        return 0

    def _is_subsequence(self, candidate: str, text: str) -> bool:
        cursor = 0
        for ch in text:
            if cursor < len(candidate) and candidate[cursor] == ch:
                cursor += 1
        return cursor == len(candidate)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^m * n)`

`text1` has up to `2^m` subsequences and each subsequence test scans `text2` once; even longest-first pruning leaves the search exponential in the worst case (answer 0).

##### Space Complexity: `O(m)`

The current candidate string of up to `m` characters.

#### Key Insights

- Transcribes the definition directly: enumerate, test, return the first hit.
- The two-pointer test is the entire subsequence machinery; nothing about
  optimality is exploited.
- Exponential in practice: a 30-character input with no common subsequence
  already outlasts any budget.

### Top-Down Memoization

#### Derivation

The enumeration wastes work because it never remembers what prefixes can do. Ask a sharper question: `dp(i, j)` is the LCS length of `text1[i:]` and `text2[j:]`. The last characters decide the split. When `text1[i] == text2[j]`, that character can be matched immediately and the rest is the smaller pair `(i + 1, j + 1)`. When they differ, at least one of the two characters is unused, so the best of dropping each is taken. The answer for `(i, j)` depends only on `(i, j)`, which makes the pairs [memoizable](https://en.wikipedia.org/wiki/Memoization):

1. `dp(i, j)` returns `0` when either suffix is empty (nothing left to
   match).
2. When `text1[i] == text2[j]`, return `1 + dp(i + 1, j + 1)`.
3. Otherwise return `max(dp(i + 1, j), dp(i, j + 1))`, computing each branch
   once and caching it in `memo`.

`max` is safe on the mismatch branch because an unused character cannot be part of the LCS of these suffixes.

#### Walkthrough

Trace the calls on Example 1: `text1 = "cat"`, `text2 = "crabt"`:

```text
dp(0,0) 'c'=='c' -> 1 + dp(1,1)
  dp(1,1) 'a' vs 'r'  -> max(dp(2,1), dp(1,2))
    dp(2,1) 't' vs 'r' -> max(dp(3,1), dp(2,2))
      dp(3,1) i out of range -> 0
      dp(2,2) 't' vs 'a' -> max(dp(3,2), dp(2,3))
        dp(3,2) -> 0
        dp(2,3) 't' vs 'b' -> max(dp(3,3), dp(2,4))
          dp(3,3) -> 0
          dp(2,4) 't'=='t' -> 1 + dp(3,5) = 1 + 0 = 1
        -> 1
      -> 1
    dp(1,2) 'a'=='a' -> 1 + dp(2,3) = 1 + 1 = 2
  -> 2
-> 3
```

The mismatch chain `dp(2,1) -> dp(2,2) -> dp(2,3) -> dp(2,4)` walks `'t'` across `"rabt"` until it finds its partner, then the `'a'` branch reuses that result through `dp(2,3)`, which is already cached. The final answer is `3`, matching the expected Output for Example 1. Example 2's identical strings take the match branch at every step and return `4`; Example 3 never matches and returns `0`.

#### Solution

The code is the walkthrough's recursion with the cache check on entry and the store before each return.

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        memo = {}

        def dp(i: int, j: int) -> int:
            if i == len(text1) or j == len(text2):
                return 0
            if (i, j) in memo:
                return memo[(i, j)]
            if text1[i] == text2[j]:
                result = 1 + dp(i + 1, j + 1)
            else:
                result = max(dp(i + 1, j), dp(i, j + 1))
            memo[(i, j)] = result
            return result

        return dp(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

Each distinct `(i, j)` pair is computed once, in constant work plus recursion into smaller pairs; there are `m * n` pairs.

##### Space Complexity: `O(m * n)`

The memo holds one entry per pair and the recursion stack reaches `m + n` frames deep in the worst case.

#### Key Insights

- The recurrence reads directly off the definition of a subsequence: either
  the current characters match (count it, move both) or one is dropped.
- Memoization turns the exponential candidate space into one computation per
  prefix pair, which is the single idea every later solution refines.
- The base cases live at the grid's right and bottom edges: an empty suffix
  matches an empty suffix only.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still spends call frames re-walking the same order. Flip the direction: the pairs form a table `dp` where `dp[i][j]` is the LCS length of the first `i` characters of `text1` and the first `j` of `text2`. Row 0 and column 0 are the empty-suffix base cases, all zero, and each interior cell reads only its diagonal, top, and left neighbors, so the table fills row by row with no recursion:

1. Allocate `dp` of size `(m + 1) x (n + 1)`; row 0 and column 0 stay `0`.
2. Sweep `i` over `1..m` and `j` over `1..n`:
   - `text1[i - 1] == text2[j - 1]`: `dp[i][j] = dp[i - 1][j - 1] + 1`.
   - Otherwise: `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`.
3. Return `dp[m][n]`.

The `- 1` offsets exist because the table is prefix-indexed while the strings are position-indexed: cell `(i, j)` decides with characters `text1[i - 1]` and `text2[j - 1]`.

#### Recurrence

Let \(dp_i[j]\) be the LCS length of the first `i` characters of `text1` and the first `j` of `text2`:

$$ dp_i[j] = dp_{i-1}[j-1] + 1 \;\text{if } text1[i-1] = text2[j-1], \quad \max(dp_{i-1}[j],\ dp_i[j-1]) \;\text{otherwise} $$

```text
dp_0[j] = 0 for all j, dp_i[0] = 0 for all i
dp_i[j] = dp_(i-1)[j-1] + 1        (when text1[i - 1] == text2[j - 1])
dp_i[j] = max(dp_(i-1)[j], dp_i[j-1])  (otherwise)
```

The match term takes the diagonal plus one because both strings advance together; the otherwise term carries the best of dropping one character from either string. Both readings of a cell sit in already-filled rows and columns, which is why the row-by-row fill never recurses. The answer is \(dp_m[n]\).

#### Walkthrough

Trace the table fill on Example 1: `text1 = "cat"`, `text2 = "crabt"`. Rows are `text1` prefixes, columns are `text2` prefixes:

```text
            ''  c  r  a  b  t
      ''     0  0  0  0  0  0
  c   [1]    0  1  1  1  1  1
  a   [2]    0  1  1  2  2  2
  t   [3]    0  1  1  2  2  3
```

Cell `[1][1]` matches `'c'` and takes `0 + 1`; row `[2]` matches `'a'` against column `a` and takes `1 + 1 = 2` at `[2][3]`; row `[3]` matches `'t'` at column `t` for `dp[2][4] + 1 = 3`. The bottom-right cell is `3`, matching the expected Output for Example 1. Example 3's disjoint alphabets never enter the match branch, so every cell stays `0`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

One constant-work comparison per table cell.

##### Space Complexity: `O(m * n)`

The full table.

#### Key Insights

- Same recurrence as the memoized recursion, evaluated in an order that
  needs no stack: every dependency is already filled.
- The zero border encodes both base cases at once, which is why the loops
  start at index 1.
- `dp[m][n]` is the answer by construction: it is the LCS of the full
  strings.

### Space-Optimized Two-Row DP

#### Derivation

The table fill reads, for cell `(i, j)`, only `dp[i - 1][j - 1]`, `dp[i - 1][j]`, and `dp[i][j - 1]`: the previous row and the cell just built. Row `i - 2` and older are dead weight, so the whole table collapses to two rows, `previous` for row `i - 1` and `current` under construction. Row rotation (`previous = current`) plays the role the index decrement played in the recursion:

1. Initialize `previous` to a row of `n + 1` zeros.
2. For each `i` in `1..m`, build `current` from `previous`:
   - `text1[i - 1] == text2[j - 1]`: `current[j] = previous[j - 1] + 1`.
   - Otherwise: `current[j] = max(previous[j], current[j - 1])`.
3. Replace `previous` with `current` and continue.
4. Return `previous[n]`, the last row's last cell.

#### Walkthrough

Trace the two rolling rows on Example 1: `text1 = "cat"`, `text2 = "crabt"`:

```text
start      previous = [0, 0, 0, 0, 0, 0]
after i=1  current  = [0, 1, 1, 1, 1, 1]
after i=2  current  = [0, 1, 1, 2, 2, 2]
after i=3  current  = [0, 1, 1, 2, 2, 3]
```

Each row equals the corresponding table row from the Bottom-Up 2-D DP walkthrough, and the unneeded predecessor is discarded as soon as its successor exists. The final `previous[n]` is `3`, matching the expected Output for Example 1; on Example 3 every row stays all zeros and `previous[n]` returns `0`.

#### Solution

The code is the walkthrough's row loop: build `current` from `previous`, then rotate.

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        width = len(text2)
        previous = [0] * (width + 1)
        for i in range(1, len(text1) + 1):
            current = [0] * (width + 1)
            for j in range(1, width + 1):
                if text1[i - 1] == text2[j - 1]:
                    current[j] = previous[j - 1] + 1
                else:
                    current[j] = max(previous[j], current[j - 1])
            previous = current
        return previous[width]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

One comparison per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `n + 1` cells; the third row from the rotation is garbage-collected.

#### Key Insights

- The dependency pattern of a recurrence determines its memory: anything a
  cell does not read can be freed.
- `current` must be a fresh row per `i`; writing into `previous` in place would
  overwrite the diagonal `previous[j - 1]` before it is read.
- Iterating over the shorter string as `text2` minimizes the row width; the
  answer is unchanged by the argument order.

### Top-Down Memoization with functools.cache

#### Derivation

Step 2's memo is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dp(i, j)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the recurrence itself untouched:

1. Keep the memoized recursion's structure: the same two base cases, the
   same match test, the same two-branch `max`.
2. Replace the `memo` dict with `@cache` on `dp`, keyed automatically by the
   arguments `(i, j)`.
3. Return `dp(0, 0)`.

The one behavioral cost: `@cache` keeps every argument pair alive for the life of the process, so the memory profile matches the dict version but cannot be freed early.

#### Walkthrough

Trace the decorated recursion on Example 1: `text1 = "cat"`, `text2 = "crabt"`. The call sequence is identical to the Top-Down Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dp(0,0) 'c'=='c' -> 1 + dp(1,1)
  ... identical descent through dp(1,1), dp(2,1), dp(2,2), dp(2,3), dp(2,4) ...
dp(2,4) 't'=='t' -> 1 + dp(3,5) = 1
dp(1,2) 'a'=='a' -> 1 + dp(2,3)   ** cached: no recompute **
-> 3
```

Eleven distinct `(i, j)` states are evaluated exactly once each (11 misses, 1 hit on the revisited `dp(2, 3)`), and the final answer is `3`, matching the expected Output for Example 1.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        @cache
        def dp(i: int, j: int) -> int:
            if i == len(text1) or j == len(text2):
                return 0
            if text1[i] == text2[j]:
                return 1 + dp(i + 1, j + 1)
            return max(dp(i + 1, j), dp(i, j + 1))

        return dp(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

The cache admits each `(i, j)` pair once; the body is constant work.

##### Space Complexity: `O(m * n)`

The cache plus the recursion stack, same as the dict version.

#### Key Insights

- `functools.cache` is the dict-based memo with the ceremony removed: same
  asymptotics, three fewer lines, no key-tuple mistakes.
- The recursion body becomes the recurrence in its purest form, which makes
  it the version to quote in an interview after sketching the dict.
- Unlike the dict version it caches the border exits too (every `i == m` or
  `j == n` call), harmless here because they all return the same `0`.

## Comparison of Solutions

### Time Complexity

- **Subsequence Enumeration**: `O(2^m * n)` - every subsequence of `text1` is tested against `text2`.
- **Top-Down Memoization**: `O(m * n)` - one computation per prefix pair.
- **Bottom-Up 2-D DP**: `O(m * n)` - one comparison per table cell.
- **Space-Optimized Two-Row DP**: `O(m * n)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the dict memo with library bookkeeping.

### Space Complexity

- **Subsequence Enumeration**: `O(m)` - the current candidate only.
- **Top-Down Memoization**: `O(m * n)` - the memo dict plus the recursion stack.
- **Bottom-Up 2-D DP**: `O(m * n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the decorator's cache plus the recursion stack.

### Trade-offs

- Enumeration is the definitional baseline; exponential time makes it a
  correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(m * n)` cache; the
  table versions trade the stack for an evaluation order.
- The two-row table is the production form: same time as everything else at
  linear memory.

### When to Use Each

- **Subsequence Enumeration**: tiny inputs, or as the brute-force oracle when
  checking the DP versions.
- **Top-Down Memoization**: when deriving the recurrence live; the recursion
  writes itself from the definition.
- **Bottom-Up 2-D DP**: when the table itself matters, for example to also
  reconstruct the subsequence by walking it backward.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the dict ceremony.

### Optimization Notes

- Swapping the arguments so the shorter string is `text2` shrinks the
  two-row version's footprint from `O(max(m, n))` to `O(min(m, n))`.
- Reconstruction of the actual subsequence needs the full table: walk from
  `dp[m][n]`, moving diagonally on matches and toward the larger neighbor
  otherwise, which is the one feature the space optimization gives up.
- The mismatch branch's `max` never needs `dp[i - 1][j - 1]`: a matched pair
  is never worse than dropping a character, which the recurrence's match
  branch already accounts for.

