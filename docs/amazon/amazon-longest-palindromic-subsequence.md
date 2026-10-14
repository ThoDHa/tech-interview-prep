# [Longest Palindromic Subsequence](https://www.fastprep.io/problems/amazon-longest-palindromic-subsequence)

**Medium** | **NN minutes** | **String, Dynamic Programming**

Given a string s, return the length of its longest subsequence that reads the same from left to right and right to left.

A subsequence keeps the relative order of selected characters but does not need to use contiguous positions.

## Examples

### Example 1

**Input:** `s = "bbbab"`

**Output:** `4`

**Explanation:** One longest palindromic subsequence is bbbb.

### Example 2

**Input:** `s = "cbbd"`

**Output:** `2`

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-longest-palindromic-subsequence; fill them in. -->

## Solutions

### Subsequence Enumeration

#### Derivation

The most literal reading of "the longest palindromic subsequence" generates candidates and tests them: every way of deleting characters from `s` is a candidate, and the longest one that reads the same in both directions is the answer. Checking longest first lets the search stop at the first hit:

1. For each `size` from `len(s)` down to `1`, enumerate every
   `itertools.combinations` of positions in `s` of that size and read off the
   candidate string.
2. Test each candidate with `_is_palindrome`, a two-pointer scan from the ends
   toward the middle.
3. Return the first `size` that passes; `0` never occurs because every single
   character is itself a palindrome.

#### Walkthrough

Trace the search on Example 2: `s = "cbbd"`. The longest possible size is `4`, and the candidates appear in position order:

```text
size 4: "cbbd" reversed "dbbc"  != -> no
size 3: "cbb"  "c" vs "b"       != -> no
        "cbd"  "c" vs "d"       != -> no
        "cbd"  (positions 0,2,3) != -> no
        "bbd"  "b" vs "d"       != -> no
size 2: "cb" no   "cd" no   "bd" no
        "bb"  'b' == 'b' -> yes -> return 2
```

The size-2 candidate `"bb"` survives the two-pointer test, so the function returns `2`, matching the expected Output for Example 2. On Example 1 (`s = "bbbab"`) the same search passes first at size 4 with `"bbbb"`, matching its expected Output.

#### Solution

The code is the longest-first candidate loop with the two-pointer palindrome test.

```python
from itertools import combinations


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        for size in range(len(s), 0, -1):
            for positions in combinations(range(len(s)), size):
                candidate = "".join(s[position] for position in positions)
                if self._is_palindrome(candidate):
                    return size
        return 0

    def _is_palindrome(self, candidate: str) -> bool:
        left, right = 0, len(candidate) - 1
        while left < right:
            if candidate[left] != candidate[right]:
                return False
            left += 1
            right -= 1
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

`s` has up to `2^n` subsequences and each palindrome test scans the candidate once; even longest-first pruning leaves the search exponential in the worst case (answer `2` on a string of distinct letters).

##### Space Complexity: `O(n)`

The current candidate string of up to `n` characters.

#### Key Insights

- Transcribes the definition directly: enumerate, test, return the first hit.
- The two-pointer scan is the entire palindrome machinery; nothing about substructure is exploited.
- Exponential in practice: a 30-character string of distinct letters already outlasts any budget.

### Top-Down Memoization

#### Derivation

The enumeration wastes work because it never remembers what substrings can do. Ask a sharper question: `dp(i, j)` is the longest palindromic subsequence length inside `s[i..j]`, the substring from index `i` through index `j`. The end characters decide the split. When `s[i] == s[j]`, both ends sit on the palindrome, and the inner part `dp(i + 1, j - 1)` extends by exactly `2`; the two equal letters can never do better apart, since any palindrome inside `s[i..j]` that uses both ends uses them as its outermost pair. When they differ, the answer cannot use both ends, so the best of shrinking each end is taken. The answer for `(i, j)` depends only on `(i, j)`, which makes the pairs [memoizable](https://en.wikipedia.org/wiki/Memoization):

1. `dp(i, j)` returns `0` when `i > j` (empty interval) and `1` when `i == j`
   (one character is a palindrome of length 1).
2. When `s[i] == s[j]`, return `2 + dp(i + 1, j - 1)`.
3. Otherwise return `max(dp(i + 1, j), dp(i, j - 1))`, computing each branch
   once and caching it in `memo`.

The entry point is the full interval: `dp(0, len(s) - 1)`.

#### Walkthrough

Trace the calls on Example 1: `s = "bbbab"`. The end pair is `s[0] = 'b'` and `s[4] = 'b'`, so the outer call takes the match branch and delegates to the inner interval:

```text
dp(0,4) s[0]='b' == s[4]='b' -> 2 + dp(1,3)
  dp(1,3) s[1]='b' vs s[3]='a' -> max(dp(2,3), dp(1,2))
    dp(2,3) s[2]='b' vs s[3]='a' -> max(dp(3,3) -> 1, dp(2,2) -> 1) = 1
    dp(1,2) s[1]='b' == s[2]='b' -> 2 + dp(2,1) = 2 + 0 = 2
  -> max(1, 2) = 2
-> 2 + 2 = 4
```

The mismatch branch at `dp(1, 3)` is the decisive beat: `dp(1, 2)` keeps the two `b`s and scores `2`, while `dp(2, 3)` keeps the lone `b` and scores `1`. Note the crossed interval `dp(2, 1)` inside the match at `dp(1, 2)`: the inner interval between the two adjacent `b`s is empty, so its base case returns `0`. The final answer is `2 + 2 = 4`, matching the expected Output for Example 1; on Example 2 (`"cbbd"`) every end pair differs except the middle `b`s, and the same process returns `2`.

#### Solution

The code is the walkthrough's recursion with the cache check on entry and the store before each return.

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        memo = {}

        def dp(left: int, right: int) -> int:
            if left > right:
                return 0
            if left == right:
                return 1
            if (left, right) in memo:
                return memo[(left, right)]
            if s[left] == s[right]:
                result = 2 + dp(left + 1, right - 1)
            else:
                result = max(dp(left + 1, right), dp(left, right - 1))
            memo[(left, right)] = result
            return result

        return dp(0, len(s) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each distinct `(left, right)` pair is computed once, in constant work plus recursion into smaller intervals; there are `n²` pairs.

##### Space Complexity: `O(n²)`

The memo holds one entry per interval and the recursion stack reaches `n` frames deep.

#### Key Insights

- The recurrence reads directly off the definition of a palindrome: equal ends wrap the best inner palindrome, unequal ends force one side to be dropped.
- On the match branch the interval shrinks by two, which is why `dp(i + 1, j - 1)` may cross (`left > right`) and needs its empty-interval base case of `0`.
- Memoization turns the exponential candidate space into one computation per interval, which is the single idea every later solution refines.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still spends call frames re-walking the same order. Flip the direction: the intervals form a table `dp` where `dp[i][j]` is the longest palindromic subsequence length inside `s[i..j]`. The table fills by interval length instead of by recursion: length-1 intervals are the base case `1`, and every longer interval reads only the diagonal band beneath it, so filling lengths `2` up to `n` in increasing order needs no stack:

1. Allocate `dp` of size `n × n`; set `dp[i][i] = 1` for every index.
2. For each `length` from `2` to `n`, for each start `i` with
   `j = i + length - 1` inside the string:
   - `s[i] == s[j]`: `dp[i][j] = dp[i + 1][j - 1] + 2`.
   - Otherwise: `dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])`.
3. Return `dp[0][n - 1]`.

#### Recurrence

Let `dp[i][j]` be the longest palindromic subsequence length inside `s[i..j]`:

$$ dp[i][j] = \begin{cases}
1, & i = j \\[4pt]
0, & i > j \\[4pt]
dp[i+1][j-1] + 2, & i < j,\ s[i] = s[j] \\[4pt]
\max(dp[i+1][j],\ dp[i][j-1]), & i < j,\ s[i] \neq s[j]
\end{cases} $$

```text
dp[i][i] = 1                            (single character)
dp[i][j] = 0                            (empty interval, i > j)
dp[i][j] = dp[i + 1][j - 1] + 2         (s[i] == s[j]: both ends join)
dp[i][j] = max(dp[i + 1][j],            (otherwise: drop s[i])
               dp[i][j - 1])            (           or drop s[j])
```

The base cases encode the one-character and empty intervals; the match term wraps the inner interval's answer with the two equal ends, and the mismatch term carries the best of dropping either end. Every cell reads a shorter interval, which is why the fill by increasing length never recurses. The answer is `dp[0][n - 1]`.

#### Walkthrough

Trace the fill on Example 2: `s = "cbbd"`. Rows are start indices `i`, columns end indices `j`; cells with `i > j` stay empty:

```text
        j0  j1  j2  j3
  i0     1   1   2   2
  i1         1   2   2
  i2             1   1
  i3                 1
```

Length 2: `[0][1]` (`"c"`,`"b"` differ) takes `max(0, 0) = 1`; `[1][2]` (`"b"`,`"b"` match) takes `dp[2][1] + 2 = 2`; `[2][3]` differs and takes `1`. Length 3: `[0][2]` (`"c"` vs `"b"`) takes `max(dp[1][2] = 2, dp[0][1] = 1) = 2`; `[1][3]` (`"b"` vs `"d"`) takes `max(dp[2][3] = 1, dp[1][2] = 2) = 2`. Length 4: `[0][3]` (`"c"` vs `"d"`) takes `max(dp[1][3] = 2, dp[0][2] = 2) = 2`. The answer `dp[0][3] = 2` matches the expected Output; on Example 1 the same fill reaches `dp[0][4] = 4`.

#### Solution

The code is the length-by-length fill of the walkthrough's table.

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        size = len(s)
        dp = [[0] * size for _ in range(size)]
        for i in range(size):
            dp[i][i] = 1
        for length in range(2, size + 1):
            for i in range(size - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        return dp[0][size - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

One constant-work comparison per interval cell; there are `n²` cells.

##### Space Complexity: `O(n²)`

The full table.

#### Key Insights

- Same recurrence as the memoized recursion, evaluated in an order that needs no stack: every dependency is a shorter interval, already filled.
- Filling by interval length replaces the recursion's natural top-down order; sweeping rows or columns alone would read cells that are not filled yet.
- `dp[0][n - 1]` is the answer by construction: it is the full string's interval.

### Space-Optimized Two-Row DP

#### Derivation

The table fill reads, for cell `(i, j)`, only `dp[i + 1][j - 1]`, `dp[i + 1][j]`, and `dp[i][j - 1]`: the previous length diagonal and the cell just built. Intervals three or more shorter than the current one are dead weight. Following the LCS pattern, the whole table collapses to two rows indexed by start position, `next_row` for the diagonal state one step ahead and `current_row` under construction, with the row rotation (`next_row = current_row`) playing the role the length increment played in the table version. The diagonal read `dp[i + 1][j - 1]` is exactly `next_row[j - 1]`: one row down, one column left:

1. Initialize `next_row` to a row of `size` zeros, standing for intervals of
   length `0`.
2. Sweep `i` from `size - 1` down to `0`, building `current_row` rightward:
   set `current_row[i] = 1`, then for each `j` above `i` apply the cell rule
   with `diagonal = next_row[j - 1]`.
3. Replace `next_row` with `current_row` after each start index.
4. Return `next_row[size - 1]`, the full-string interval `dp[0][size - 1]`.

#### Walkthrough

Trace the two rolling rows on Example 2: `s = "cbbd"`. Each line shows `current_row` after start index `i` finishes, written for columns `0` through `3`:

```text
start i=3   current_row = [_, _, _, 1]      (column j must be >= i)
start i=2   current_row = [_, _, 1, 1]      diagonal next_row[2] = 0 under j=3
start i=1   current_row = [_, 1, 2, 2]      j=2: s[1]==s[2] 'b' -> next_row[1] + 2 = 2
                                            j=3: s[1]='b' vs 'd' -> max(next_row[2]=1, 2)=2
start i=0   current_row = [1, 1, 2, 2]      j=1: 'c' vs 'b' -> max(next_row[1]=1, 1)=1
                                            j=2: 'c' vs 'b' -> max(next_row[2]=2, 1)=2
                                            j=3: 'c' vs 'd' -> max(next_row[3]=2, 2)=2
```

The rotation after `i = 0` leaves `next_row = [1, 1, 2, 2]`, and the full-string interval `dp[0][3]` sits at its last cell: `next_row[3] = 2`, matching the expected Output for Example 2. On Example 1 (`"bbbab"`) the same sweep builds `[1, 1, 3, 3, 4]` row by row and returns `4`.

#### Solution

The code is the walkthrough's start-index loop: build `current_row` from `next_row`, then rotate.

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        size = len(s)
        next_row = [0] * size
        for i in range(size - 1, -1, -1):
            current_row = [0] * size
            current_row[i] = 1
            diagonal = 0
            for j in range(i + 1, size):
                if s[i] == s[j]:
                    current_row[j] = diagonal + 2
                else:
                    current_row[j] = max(next_row[j], current_row[j - 1])
                diagonal = next_row[j]
            next_row = current_row
        return next_row[size - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

One comparison per interval cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `size` cells; the rotated-away row is garbage-collected.

#### Key Insights

- Sweeping start indices downward lets one scalar, `diagonal`, carry `dp[i + 1][j - 1]`: the value is read before it is rotated out of reach.
- `diagonal` must lag one column behind `j`; capturing `next_row[j]` after the cell update keeps the old row's value for the next step's diagonal.
- Merging the length-1 base case into the loop (`current_row[i] = 1`) removes the separate initialization sweep the table version needed.

### Top-Down Memoization with functools.cache

#### Derivation

The memo dict is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dp(left, right)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the recurrence itself untouched:

1. Keep the memoized recursion's structure: the same two base cases, the same
   end-character test, the same two-branch `max`.
2. Replace the `memo` dict with `@cache` on `dp`, keyed automatically by the
   arguments `(left, right)`.
3. Return `dp(0, len(s) - 1)`.

The one behavioral cost: `@cache` keeps every argument pair alive for the life of the process, so the memory profile matches the dict version but cannot be freed early.

#### Walkthrough

Trace the decorated recursion on Example 2: `s = "cbbd"`. The call sequence matches the Top-Down Memoization pattern; each line is one cache state change:

```text
dp(0,3) 'c' vs 'd' -> max(dp(1,3), dp(0,2))
  dp(1,3) 'b' vs 'd' -> max(dp(2,3) -> 1, dp(1,2))
    dp(1,2) 'b'=='b' -> 2 + dp(2,1) = 2 + 0 = 2
  -> 2
  dp(0,2) 'c' vs 'b' -> max(dp(1,2) ** cached: 2 **, dp(0,1) -> 1) = 2
-> 2
```

The revisited `dp(1, 2)` is served from the cache instead of recomputing. The final answer is `2`, matching the expected Output for Example 2; on Example 1 (`"bbbab"`) the same decorated recursion returns `4`.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        @cache
        def dp(left: int, right: int) -> int:
            if left > right:
                return 0
            if left == right:
                return 1
            if s[left] == s[right]:
                return 2 + dp(left + 1, right - 1)
            return max(dp(left + 1, right), dp(left, right - 1))

        return dp(0, len(s) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

The cache admits each `(left, right)` pair once; the body is constant work.

##### Space Complexity: `O(n²)`

The cache plus the recursion stack, same as the dict version.

#### Key Insights

- `functools.cache` is the dict-based memo with the ceremony removed: same asymptotics, three fewer lines, no key-tuple mistakes.
- The recursion body becomes the recurrence in its purest form, which makes it the version to quote in an interview after sketching the dict.
- Unlike the dict version it caches the crossed-interval exits too (every `left > right` call), harmless here because they all return the same `0`.

## Comparison of Solutions

### Time Complexity

- **Subsequence Enumeration**: `O(2^n × n)` - every subsequence of `s` is palindrome-tested.
- **Top-Down Memoization**: `O(n²)` - one computation per interval.
- **Bottom-Up 2-D DP**: `O(n²)` - one comparison per table cell.
- **Space-Optimized Two-Row DP**: `O(n²)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(n²)` - the dict memo with library bookkeeping.

### Space Complexity

- **Subsequence Enumeration**: `O(n)` - the current candidate only.
- **Top-Down Memoization**: `O(n²)` - the memo dict plus the recursion stack.
- **Bottom-Up 2-D DP**: `O(n²)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.
- **Top-Down Memoization with functools.cache**: `O(n²)` - the decorator's cache plus the recursion stack.

### Trade-offs

- Enumeration is the definitional baseline; exponential time makes it a correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(n²)` cache; the table versions trade the stack for an evaluation order.
- The two-row table is the production form: same time as everything else at linear memory, at the cost of tracking one diagonal scalar by hand.

### When to Use Each

- **Subsequence Enumeration**: tiny inputs, or as the brute-force oracle when checking the DP versions.
- **Top-Down Memoization**: when deriving the recurrence live; the recursion writes itself from the definition.
- **Bottom-Up 2-D DP**: when the table itself matters, for example to also reconstruct the subsequence by walking it from `dp[0][n - 1]` toward the diagonal.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the memoized recursion without the dict ceremony.

### Optimization Notes

- Both recursive versions stack roughly `n` frames before any memo populates; a 10,000-character input would pass Python's default recursion limit of 1000, so prefer the bottom-up versions at that scale.
- On the match branch the interval shrinks by two, so the recursion depth is bounded by the number of matched pairs plus the number of drops, not by `2n`.
- Reconstruction of the actual subsequence needs the full table: start at `dp[0][n - 1]`, take both ends on matches, and walk toward the larger neighbor on mismatches, which is the one feature the space optimization gives up.
- A common pitfall is computing the longest palindromic *substring* instead: the two problems share the interval shape but the subsequence version never requires contiguity, so its recurrence reads three neighbors rather than testing a contiguous window.
