# [Longest Common Subsequence Length](https://www.fastprep.io/problems/amazon-longest-common-subsequence-length)

**Medium** | **NN minutes** | **String, Dynamic Programming**

Given two lowercase strings first and second, return the length of their longest common subsequence.

A subsequence is formed by deleting zero or more characters without changing the relative order of the remaining characters. The characters in a common subsequence must appear in both strings in the same relative order; they do not need to occupy consecutive positions.

## Examples

### Example 1

**Input:** `first = "abcde"`, `second = "ace"`

**Output:** `3`

**Explanation:** The string ace appears in both inputs in the same relative order.

### Example 2

**Input:** `first = "abc"`, `second = "def"`

**Output:** `0`

**Explanation:** The two strings share no character, so the longest common subsequence is empty.

## Constraints

- `0 <= first.length, second.length <= 1000`
- `first and second contain only lowercase English letters.`

## Solutions

### Subsequence Enumeration

#### Derivation

The most literal reading of "the longest common subsequence" generates candidates and tests them: every way of deleting characters from `first` is a candidate, and the longest one that also fits inside `second` as a subsequence is the answer. Checking longest first lets the search stop at the first hit:

1. For each `size` from `min(len(first), len(second))` down to `1`, enumerate
   every `itertools.combinations` of positions in `first` of that size and
   read off the candidate string.
2. For each candidate, walk through `second` and test whether the candidate's
   characters appear in order (a two-pointer scan), implemented in
   `_is_subsequence`.
3. Return the first `size` that passes; `0` when no candidate of any size passes.

#### Walkthrough

Trace the search on Example 1: `first = "abcde"`, `second = "ace"`. The longest possible size is `3`, and the size-3 candidates appear in position order:

```text
size 3: "abc" in "ace"?  a matches, b never does          -> no
        "abd" in "ace"?  a matches, d never does          -> no
        "abe" in "ace"?  a matches, b never does          -> no
        "acd" in "ace"?  a, then c, then d never does     -> no
        "ace" in "ace"?  a, c, e all match in order       -> yes -> return 3
```

The two-pointer test aligns each candidate against `"ace"` left to right; the fifth candidate aligns fully, so the function returns `3`, matching the expected Output for Example 1. On Example 2 (`"abc"` versus `"def"`) the two strings share no character, so every candidate from size 3 down to size 1 fails to align and the loop exhausts, returning `0`.

#### Solution

The code is the longest-first candidate loop with the two-pointer subsequence test.

```python
from itertools import combinations


class Solution:
    def solve(self, first: str, second: str) -> int:
        for size in range(min(len(first), len(second)), 0, -1):
            for positions in combinations(range(len(first)), size):
                candidate = "".join(first[position] for position in positions)
                if self._is_subsequence(candidate, second):
                    return size
        return 0

    def _is_subsequence(self, candidate: str, text: str) -> bool:
        cursor = 0
        for character in text:
            if cursor < len(candidate) and candidate[cursor] == character:
                cursor += 1
        return cursor == len(candidate)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^m × n)`

`first` has up to `2^m` subsequences and each subsequence test scans `second` once; even longest-first pruning leaves the search exponential in the worst case (answer `0`).

##### Space Complexity: `O(m)`

The current candidate string of up to `m` characters.

#### Key Insights

- Transcribes the definition directly: enumerate, test, return the first hit.
- The two-pointer test is the entire subsequence machinery; nothing about optimality is exploited.
- Exponential in practice: a 30-character input with no common subsequence already outlasts any budget.

### Top-Down Memoization

#### Derivation

The enumeration wastes work because it never remembers what prefixes can do. Ask a sharper question: `dp(i, j)` is the LCS length of `first[i:]` and `second[j:]`. The current characters decide the split. When `first[i] == second[j]`, that character can be matched immediately and the rest is the smaller pair `(i + 1, j + 1)`. When they differ, at least one of the two characters is unused, so the best of dropping each is taken. The answer for `(i, j)` depends only on `(i, j)`, which makes the pairs [memoizable](https://en.wikipedia.org/wiki/Memoization):

1. `dp(i, j)` returns `0` when either suffix is empty (nothing left to match).
2. When `first[i] == second[j]`, return `1 + dp(i + 1, j + 1)`.
3. Otherwise return `max(dp(i + 1, j), dp(i, j + 1))`, computing each branch
   once and caching it in `memo`.

`max` is safe on the mismatch branch because an unused character cannot be part of the LCS of these suffixes.

#### Walkthrough

Trace the calls on Example 1: `first = "abcde"`, `second = "ace"`:

```text
dp(0,0) 'a'=='a' -> 1 + dp(1,1)
  dp(1,1) 'b' vs 'c'  -> max(dp(2,1), dp(1,2))
    dp(2,1) 'c'=='c' -> 1 + dp(3,2)
      dp(3,2) 'd' vs 'e' -> max(dp(4,2), dp(3,3))
        dp(4,2) 'e'=='e' -> 1 + dp(5,3) = 1 + 0 = 1
        dp(3,3) j past end -> 0
      -> 1
    -> 2
    dp(1,2) 'b' vs 'e' -> max(dp(2,2), dp(1,3))
      dp(2,2) 'c' vs 'e' -> max(dp(3,2) ** cached: 1 **, dp(2,3) -> 0) = 1
      dp(1,3) j past end -> 0
    -> 1
  -> 2
-> 3
```

The mismatch chain `dp(3,2) -> dp(4,2)` walks `'e'` to the end of `second`, and the later branch `dp(2,2)` reuses the cached `dp(3,2)` instead of recomputing it. The final answer is `3`, matching the expected Output for Example 1; Example 2's disjoint alphabets take the mismatch branch at every step and return `0`.

#### Solution

The code is the walkthrough's recursion with the cache check on entry and the store before each return.

```python
class Solution:
    def solve(self, first: str, second: str) -> int:
        memo = {}

        def dp(i: int, j: int) -> int:
            if i == len(first) or j == len(second):
                return 0
            if (i, j) in memo:
                return memo[(i, j)]
            if first[i] == second[j]:
                result = 1 + dp(i + 1, j + 1)
            else:
                result = max(dp(i + 1, j), dp(i, j + 1))
            memo[(i, j)] = result
            return result

        return dp(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

Each distinct `(i, j)` pair is computed once, in constant work plus recursion into smaller pairs; there are `m × n` pairs.

##### Space Complexity: `O(m × n)`

The memo holds one entry per pair and the recursion stack reaches `m + n` frames deep in the worst case.

#### Key Insights

- The recurrence reads directly off the definition of a subsequence: either the current characters match (count it, move both) or one is dropped.
- Memoization turns the exponential candidate space into one computation per prefix pair, which is the single idea every later solution refines.
- The base cases live at the grid's right and bottom edges: an empty suffix matches an empty suffix only.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still spends call frames re-walking the same order. Flip the direction: the pairs form a table `dp` where `dp[i][j]` is the LCS length of the first `i` characters of `first` and the first `j` of `second`. Row 0 and column 0 are the empty-suffix base cases, all zero, and each interior cell reads only its diagonal, top, and left neighbors, so the table fills row by row with no recursion:

1. Allocate `dp` of size `(m + 1) × (n + 1)`; row 0 and column 0 stay `0`.
2. Sweep `i` over `1..m` and `j` over `1..n`:
   - `first[i - 1] == second[j - 1]`: `dp[i][j] = dp[i - 1][j - 1] + 1`.
   - Otherwise: `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`.
3. Return `dp[m][n]`.

The `- 1` offsets exist because the table is prefix-indexed while the strings are position-indexed: cell `(i, j)` decides with characters `first[i - 1]` and `second[j - 1]`.

#### Recurrence

Let `dp[i][j]` be the LCS length of the first `i` characters of `first` and the first `j` of `second`:

$$ dp[i][j] = \begin{cases}
0, & i = 0 \text{ or } j = 0 \\[4pt]
dp[i-1][j-1] + 1, & first[i-1] = second[j-1] \\[4pt]
\max(dp[i-1][j],\ dp[i][j-1]), & \text{otherwise}
\end{cases} $$

```text
dp[0][j] = 0 for all j, dp[i][0] = 0 for all i
dp[i][j] = dp[i-1][j-1] + 1             (when first[i - 1] == second[j - 1])
dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (otherwise)
```

The match term takes the diagonal plus one because both strings advance together; the otherwise term carries the best of dropping one character from either string. Both readings of a cell sit in already-filled rows and columns, which is why the row-by-row fill never recurses. The answer is `dp[m][n]`.

#### Walkthrough

Trace the table fill on Example 1: `first = "abcde"`, `second = "ace"`. Rows are `first` prefixes, columns are `second` prefixes:

```text
        ''  a  c  e
  ''     0  0  0  0
  a      0  1  1  1
  b      0  1  1  1
  c      0  1  2  2
  d      0  1  2  2
  e      0  1  2  3
```

Cell `[1][1]` matches `'a'` and takes `0 + 1`; row `[3]` matches `'c'` against column `c` and takes `dp[2][1] + 1 = 2` at `[3][2]`; row `[5]` matches `'e'` at column `e` for `dp[4][2] + 1 = 3`. The bottom-right cell is `3`, matching the expected Output for Example 1. Example 2's disjoint alphabets never enter the match branch, so every cell stays `0` and `dp[3][3]` returns `0`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
class Solution:
    def solve(self, first: str, second: str) -> int:
        m, n = len(first), len(second)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if first[i - 1] == second[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One constant-work comparison per table cell.

##### Space Complexity: `O(m × n)`

The full table.

#### Key Insights

- Same recurrence as the memoized recursion, evaluated in an order that needs no stack: every dependency is already filled.
- The zero border encodes both base cases at once, which is why the loops start at index 1.
- `dp[m][n]` is the answer by construction: it is the LCS of the full strings.

### Space-Optimized Two-Row DP

#### Derivation

The table fill reads, for cell `(i, j)`, only `dp[i - 1][j - 1]`, `dp[i - 1][j]`, and `dp[i][j - 1]`: the previous row and the cell just built. Row `i - 2` and older are dead weight, so the whole table collapses to two rows, `previous` for row `i - 1` and `current` under construction. Row rotation (`previous = current`) plays the role the index decrement played in the recursion:

1. Initialize `previous` to a row of `n + 1` zeros.
2. For each `i` in `1..m`, build `current` from `previous`:
   - `first[i - 1] == second[j - 1]`: `current[j] = previous[j - 1] + 1`.
   - Otherwise: `current[j] = max(previous[j], current[j - 1])`.
3. Replace `previous` with `current` and continue.
4. Return `previous[n]`, the last row's last cell.

#### Walkthrough

Trace the two rolling rows on Example 1: `first = "abcde"`, `second = "ace"`:

```text
start      previous = [0, 0, 0, 0]
after i=1  current  = [0, 1, 1, 1]
after i=2  current  = [0, 1, 1, 1]
after i=3  current  = [0, 1, 2, 2]
after i=4  current  = [0, 1, 2, 2]
after i=5  current  = [0, 1, 2, 3]
```

Each row equals the corresponding table row from the Bottom-Up 2-D DP walkthrough, and the unneeded predecessor is discarded as soon as its successor exists. The final `previous[n]` is `3`, matching the expected Output for Example 1; on Example 2 every row stays all zeros and `previous[n]` returns `0`.

#### Solution

The code is the walkthrough's row loop: build `current` from `previous`, then rotate.

```python
class Solution:
    def solve(self, first: str, second: str) -> int:
        width = len(second)
        previous = [0] * (width + 1)
        for i in range(1, len(first) + 1):
            current = [0] * (width + 1)
            for j in range(1, width + 1):
                if first[i - 1] == second[j - 1]:
                    current[j] = previous[j - 1] + 1
                else:
                    current[j] = max(previous[j], current[j - 1])
            previous = current
        return previous[width]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One comparison per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `n + 1` cells; the third row from the rotation is garbage-collected.

#### Key Insights

- The dependency pattern of a recurrence determines its memory: anything a cell does not read can be freed.
- `current` must be a fresh row per `i`; writing into `previous` in place would overwrite the diagonal `previous[j - 1]` before it is read.
- Iterating over the shorter string as `second` minimizes the row width; the answer is unchanged by the argument order.

### Top-Down Memoization with functools.cache

#### Derivation

The memo dict is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dp(i, j)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the recurrence itself untouched:

1. Keep the memoized recursion's structure: the same two base cases, the same
   match test, the same two-branch `max`.
2. Replace the `memo` dict with `@cache` on `dp`, keyed automatically by the
   arguments `(i, j)`.
3. Return `dp(0, 0)`.

The one behavioral cost: `@cache` keeps every argument pair alive for the life of the process, so the memory profile matches the dict version but cannot be freed early.

#### Walkthrough

Trace the decorated recursion on Example 1: `first = "abcde"`, `second = "ace"`. The call sequence is identical to the Top-Down Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dp(0,0) 'a'=='a' -> 1 + dp(1,1)
  ... identical descent through dp(1,1), dp(2,1), dp(3,2), dp(4,2) ...
dp(1,2) 'b' vs 'e' -> max(dp(2,2), dp(1,3))
  dp(2,2) 'c' vs 'e' -> max(dp(3,2) ** cached: no recompute **, dp(2,3) -> 0)
-> 3
```

Each distinct `(i, j)` state is evaluated exactly once, and the revisited `dp(3, 2)` is served from the cache. The final answer is `3`, matching the expected Output for Example 1; Example 2 returns `0` through the same border base cases.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def solve(self, first: str, second: str) -> int:
        @cache
        def dp(i: int, j: int) -> int:
            if i == len(first) or j == len(second):
                return 0
            if first[i] == second[j]:
                return 1 + dp(i + 1, j + 1)
            return max(dp(i + 1, j), dp(i, j + 1))

        return dp(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The cache admits each `(i, j)` pair once; the body is constant work.

##### Space Complexity: `O(m × n)`

The cache plus the recursion stack, same as the dict version.

#### Key Insights

- `functools.cache` is the dict-based memo with the ceremony removed: same asymptotics, three fewer lines, no key-tuple mistakes.
- The recursion body becomes the recurrence in its purest form, which makes it the version to quote in an interview after sketching the dict.
- Unlike the dict version it caches the border exits too (every `i == m` or `j == n` call), harmless here because they all return the same `0`.

## Comparison of Solutions

### Time Complexity

- **Subsequence Enumeration**: `O(2^m × n)` - every subsequence of `first` is tested against `second`.
- **Top-Down Memoization**: `O(m × n)` - one computation per prefix pair.
- **Bottom-Up 2-D DP**: `O(m × n)` - one comparison per table cell.
- **Space-Optimized Two-Row DP**: `O(m × n)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(m × n)` - the dict memo with library bookkeeping.

### Space Complexity

- **Subsequence Enumeration**: `O(m)` - the current candidate only.
- **Top-Down Memoization**: `O(m × n)` - the memo dict plus the recursion stack.
- **Bottom-Up 2-D DP**: `O(m × n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.
- **Top-Down Memoization with functools.cache**: `O(m × n)` - the decorator's cache plus the recursion stack.

### Trade-offs

- Enumeration is the definitional baseline; exponential time makes it a correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(m × n)` cache; the table versions trade the stack for an evaluation order.
- The two-row table is the production form: same time as everything else at linear memory.

### When to Use Each

- **Subsequence Enumeration**: tiny inputs, or as the brute-force oracle when checking the DP versions.
- **Top-Down Memoization**: when deriving the recurrence live; the recursion writes itself from the definition.
- **Bottom-Up 2-D DP**: when the table itself matters, for example to also reconstruct the subsequence by walking it backward.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the memoized recursion without the dict ceremony.

### Optimization Notes

- Swapping the arguments so the shorter string is `second` shrinks the two-row version's footprint from `O(max(m, n))` to `O(min(m, n))`.
- The stated bounds allow either string to be empty (`0 <= first.length, second.length <= 1000`); every approach returns `0` for that case through empty sweep ranges, zero borders, or the base cases, with no special-casing.
- At the constraint maximum (`m = n = 1000`) both recursive versions can stack up roughly `m + n = 2000` frames, past Python's default recursion limit of 1000; raise the limit with `sys.setrecursionlimit` or prefer the bottom-up versions, which need no call stack at all.
- Reconstruction of the actual subsequence needs the full table: walk from `dp[m][n]`, moving diagonally on matches and toward the larger neighbor otherwise, which is the one feature the space optimization gives up.
