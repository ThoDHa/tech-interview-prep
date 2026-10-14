# [Interleaving String](https://leetcode.com/problems/interleaving-string/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/interleaving_string/solution.py`](../../practice/interleaving_string/solution.py)

You are given three strings `s1`, `s2`, and `s3`. Return `true` if `s3` is formed by **interleaving** `s1` and `s2` together or `false` otherwise.

**Interleaving** two strings `s` and `t` is done by dividing `s` and `t` into `n` and `m` substrings respectively, where the following conditions are met

* `|n - m| <= 1`, i.e. the difference between the number of substrings of `s` and `t` is at most `1`.
* `s = s1 + s2 + ... + sn`
* `t = t1 + t2 + ... + tm`
* **Interleaving** `s` and `t` is  `s1 + t1 + s2 + t2 + ...` or `t1 + s1 + t2 + s2 + ...`

You may assume that `s1`, `s2` and `s3` consist of lowercase English letters.

## Examples

### Example 1

**Input:** `s1 = "aaaa", s2 = "bbbb", s3 = "aabbbbaa"`

**Output:** `true`

**Explanation:** We can split `s1` into `["aa", "aa"]`, `s2` can remain as `"bbbb"` and `s3` is formed by interleaving `["aa", "aa"]` and `"bbbb"`.

### Example 2

**Input:** `s1 = "", s2 = "", s3 = ""`

**Output:** `true`

### Example 3

**Input:** `s1 = "abc", s2 = "xyz", s3 = "abxzcy"`

**Output:** `false`

**Explanation:** We can't split `s3` into `["ab", "xz", "cy"]` as the order of characters is not maintained.

## Constraints

- `0 <= s1.length, s2.length <= 100`
- `0 <= s3.length <= 200`

## Deriving the Solution

An interleaving merges the two strings while each keeps its own relative order, which is a decision process: read `s3` left to right and, at every position, decide whether this character comes from `s1` or from `s2`. A wrong choice must be undoable, and whether a suffix of `s3` can still be formed depends only on how much of `s1` and `s2` each side has already consumed, not on the order the characters were taken in. That dependence shape is what every solution below exploits.

1. **Start literal.** Build every merge character by character and compare the
   finished ones against `s3`. The merge tree holds
   `C(m + n, m)` leaves: see [Merge Enumeration](#merge-enumeration).
2. **Spot the waste.** A branch's fate depends only on `(i, j)`, the amounts
   of `s1` and `s2` already consumed, because those two numbers fix which
   position of `s3` comes next. Many merge orders reach the same pair, so the
   pairs are cacheable states: see
   [Top-Down Memoization](#top-down-memoization).
3. **Tabulate the pairs.** The pairs form a two-dimensional grid
   `(prefix of s1, prefix of s2)` where each cell needs only the cell above
   and the cell to the left. Filling the grid row by row needs no recursion:
   see [Bottom-Up 2-D DP](#bottom-up-2-d-dp).
4. **Keep two rows.** Building row `i` reads row `i - 1` and the current
   row's left neighbor, so two rows suffice, `O(n)` space, same time: see
   [Space-Optimized Two-Row DP](#space-optimized-two-row-dp).
5. **Hand the cache to the library.** Step 2's memo dict is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the two base rules and the two-character tests stay
   exactly as written: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Merge Enumeration

#### Derivation

The most literal reading of "interleaving" builds merges and tests them. At every step the next character of the merge is either the next unused character of `s1` or the next unused one of `s2`; when both are exhausted the merge is complete and is compared against `s3`. The first matching merge answers `True`; exhausting the tree answers `False`:

1. Define `dfs(i, j, built)` as the search over merges of `s1[i:]` and
   `s2[j:]` extending the string `built` built so far.
2. When `i == len(s1)` and `j == len(s2)`, the merge is complete: return
   `built == s3`.
3. Try taking the next character from `s1` when one exists, recursing with
   `dfs(i + 1, j, built + s1[i])`.
4. If that branch did not answer `True`, try taking the next character from
   `s2` the same way.
5. Return `dfs(0, 0, "")`.

#### Walkthrough

The official examples either answer on a forced single path (Example 1) or need all twenty leaves (Example 3), so a tailored input shows both a failed merge and a found one: `s1 = "ab"`, `s2 = "cd"`, `s3 = "acbd"`:

```text
take s1[0]='a'
  take s1[1]='b'
    take s2[0]='c'
      take s2[1]='d'
        leaf "abcd"  == "acbd"?  no
  take s2[0]='c'
    take s1[1]='b'
      take s2[1]='d'
        leaf "acbd"  == "acbd"?  yes -> return True
```

The search commits to the all-of-`s1`-first merge, fails, backtracks to the second character choice, and the second merge matches, so the root returns `True`. The example's brevity hides the cost: with `m + n = 200` the tree has `C(200, 100)` leaves.

#### Solution

The code is the walkthrough's merge tree: one fork per character, one completion test.

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        def dfs(i: int, j: int, built: str) -> bool:
            if i == len(s1) and j == len(s2):
                return built == s3
            # Try the next character from s1, then from s2
            if i < len(s1) and dfs(i + 1, j, built + s1[i]):
                return True
            return j < len(s2) and dfs(i, j + 1, built + s2[j])

        return dfs(0, 0, "")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(m + n, m) * (m + n))`

Every way of choosing which `m` of the `m + n` positions come from `s1` is a leaf, and each leaf comparison (and each `built` string extension) scans up to `m + n` characters.

##### Space Complexity: `O(m + n)`

The recursion stack is one frame per merged character, and `built` holds up to `m + n` characters.

#### Key Insights

- Transcribes the definition directly: merge by choosing a source per
  character, compare when complete.
- The `built` string makes each step pay `O(m + n)`; carrying indices only
  (as the later solutions do) reduces each step to `O(1)`.
- The exponential leaf count is the entire cost story; everything that
  follows removes repeated work rather than adding insight.

### Top-Down Memoization

#### Derivation

The enumeration re-explores subtrees it has already seen whenever the same amounts of `s1` and `s2` have been consumed by different orders. Those two amounts are all that matters: `built` is redundant, since its content is forced to be a prefix of `s3` of length `i + j` whenever the search is still meaningful, and the next character to match is `s3[i + j]`. So each pair `(i, j)` is a [memoizable](https://en.wikipedia.org/wiki/Memoization) state, with `(m + 1) × (n + 1)` of them, and the string argument disappears entirely:

1. Return `False` up front when `len(s3) != len(s1) + len(s2)`: every
   interleaving consumes all three strings, so unequal lengths can never
   match.
2. Define `dfs(i, j)` as "can the first `i` characters of `s1` and the first
   `j` of `s2` interleave into the first `i + j` of `s3`?".
3. When both strings are consumed, return `True`.
4. Otherwise the next character is `s3[i + j]`; answer `True` when taking it
   from `s1` (`s1[i] == s3[i + j]` and `dfs(i + 1, j)`) or from `s2`
   (`s2[j] == s3[i + j]` and `dfs(i, j + 1)`).
5. Store each `(i, j)` answer before returning it.

#### Walkthrough

Neither official example exercises a memo hit: Example 1 walks a forced path and Examples 2 and 3 finish before any state repeats. A tailored input, the classic failing interleaving `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbbaccc"`, shows the caching at work; the tree prunes with stored answers on the second visit:

```text
dfs(0, 0)  s3[0]='a' matches: s1
  dfs(1, 0)  s3[1]='a' matches: s1
    dfs(2, 0)  s3[2]='d' matches: s2
      dfs(2, 1)  s3[3]='b' matches: s1+s2
        dfs(3, 1)  s3[4]='b' matches: s2
          dfs(3, 2)  s3[5]='b' matches: s2
            dfs(3, 3)  s3[6]='a' matches: neither
            dfs(3, 3) -> False  stored
          dfs(3, 2) -> False  stored
        dfs(3, 1) -> False  stored
        dfs(2, 2)  s3[4]='b' matches: s1+s2
          dfs(3, 2) -> False  ** memo hit **
          dfs(2, 3)  s3[5]='b' matches: s1
            dfs(3, 3) -> False  ** memo hit **
          dfs(2, 3) -> False  stored
        dfs(2, 2) -> False  stored
      dfs(2, 1) -> False  stored
    dfs(2, 0) -> False  stored
  dfs(1, 0) -> False  stored
dfs(0, 0) -> False  stored
```

The search descends `s1` while the `'a'`s hold, branches at `(2, 1)` where both sources offer `'b'`, and the second branch's subtree is largely answered from the memo: `dfs(3, 2)` and `dfs(3, 3)` are hits. Nine states are solved in total and the root returns `False`, matching the expected answer for this input: at `(3, 3)` the next needed character is `s3[6] = 'a'`, and neither remaining suffix supplies it (`s1` offers `'c'`, `s2` offers `'b'`).

#### Solution

The code is the walkthrough's state recursion with the length gate in front.

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s3) != len(s1) + len(s2):
            return False
        memo = {}

        def dfs(i: int, j: int) -> bool:
            if i == len(s1) and j == len(s2):
                return True
            if (i, j) in memo:
                return memo[(i, j)]
            k = i + j
            result = (i < len(s1) and s1[i] == s3[k] and dfs(i + 1, j)) or (
                j < len(s2) and s2[j] == s3[k] and dfs(i, j + 1)
            )
            memo[(i, j)] = result
            return result

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

At most `(m + 1) × (n + 1)` states, each solved once with two constant-time character tests.

##### Space Complexity: `O(m * n)`

The memo's entries plus a recursion stack of up to `m + n` frames.

#### Key Insights

- Dropping `built` is the key step: the consumed amounts `(i, j)` already
  determine both the next character and the prefix that must have been built.
- The length gate is not an optimization but a correctness guard for the
  memoized form: without it, states past the end of `s3` would index out of
  range.
- A greedy reading fails on shared characters: when `s1[i] == s2[j]` both
  branches must be tried, which is exactly the structure the memo makes
  affordable.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still asks from the top. Flip it: `dp[i][j]` is `True` exactly when the first `i` characters of `s1` and the first `j` of `s2` interleave into the first `i + j` of `s3`. Cell `(0, 0)` is `True` (both prefixes empty, empty `s3` prefix trivially formed); row 0 and column 0 inherit along a single path (`s2`-only and `s1`-only prefixes); each interior cell is reachable from the cell above by consuming an `s1` character or from the left by consuming an `s2` character, testing the character of `s3` at position `i + j - 1`. Filling row by row never reads an undecided cell:

1. Allocate `dp` of size `(m + 1) x (n + 1)`; set `dp[0][0] = True`.
2. Fill row 0: `dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]`. Fill
   column 0 symmetrically with `s1`.
3. For each `i` in `1..m` and `j` in `1..n`, with `k = i + j - 1`:
   `dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[k]) or
   (dp[i][j - 1] and s2[j - 1] == s3[k])`.
4. Return `dp[m][n]`.

#### Walkthrough

Trace the fill on the successful classic input `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`. Rows are `s1` prefixes, columns are `s2` prefixes; `T` marks reachable cells:

```text
        ''  d  b  b  c  a
  ''     T  .  .  .  .  .
  a      T  .  .  .  .  .
  a      T  T  T  T  T  .
  b      .  T  T  .  T  .
  c      .  .  T  T  T  T
  c      .  .  .  T  .  T
```

The `'a'` rows reach across all five columns because either source supplies the leading `'a'`s; row `b` then can only continue from cells holding `s2`-offered continuations, and the bottom-right cell is `T`, matching the expected answer `true` for this input. On the failing input `s3 = "aadbbbaccc"` from the Top-Down Memoization walkthrough, the same table computes an all-`.` last row and returns `False`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if len(s3) != m + n:
            return False
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                k = i + j - 1
                dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[k]) or (
                    dp[i][j - 1] and s2[j - 1] == s3[k]
                )
        return dp[m][n]
```

#### Recurrence

Let \(dp_i[j]\) be whether the first `i` characters of `s1` and the first `j` of `s2` interleave into the first `i + j` of `s3`, writing \(k = i + j - 1\):

$$ dp_i[j] = (dp_{i-1}[j] \wedge s_1[i-1] = s_3[k]) \vee (dp_i[j-1] \wedge s_2[j-1] = s_3[k]), \qquad dp_0[0] = \text{True} $$

```text
dp_0[0] = True
dp_i[0] = dp_(i-1)[0] and s1[i - 1] == s3[i - 1]     (s1-only prefixes)
dp_0[j] = dp_0[j-1] and s2[j - 1] == s3[j - 1]       (s2-only prefixes)
dp_i[j] = (dp_(i-1)[j] and s1[i - 1] == s3[k])
          or (dp_i[j-1] and s2[j - 1] == s3[k])      (k = i + j - 1)
```

The two disjuncts are the only moves an interleave allows at its last position: `s3[k]` came from `s1` (cell above) or from `s2` (cell to the left). Both readings sit in the same partially filled row or the row above, so the row-by-row fill never consults an undecided cell. The answer is \(dp_m[n]\), guarded by the length check \(|s_3| = m + n\) that keeps every \(k\) in range.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

One `and`/`or` test pair per table cell.

##### Space Complexity: `O(m * n)`

The full table.

#### Key Insights

- The cell test is the memoized recursion with the cache replaced by the
  table: same two character tests, same two neighbors.
- Row 0 and column 0 are single-path borders: they encode "formed using only
  `s2`" and "formed using only `s1`".
- The table answers existence questions (which cells are reachable), not
  counts, because the question is a decision, not a tally.

### Space-Optimized Two-Row DP

#### Derivation

Cell `(i, j)` reads only `dp[i - 1][j]` and `dp[i][j - 1]`: the previous row and the cell just built. Row `i - 2` and older are dead weight, so the whole table collapses to two rows, `previous` for row `i - 1` and `current` under construction. Row rotation (`previous = current`) plays the role the index decrement played in the recursion, and the borders move into the loop: `current[0]` inherits from `previous[0]` alone:

1. Initialize `previous` to row 0: `previous[0] = True`, then
   `previous[j] = previous[j - 1] and s2[j - 1] == s3[j - 1]`.
2. For each `i` in `1..m`, build `current` from `previous`:
   `current[0] = previous[0] and s1[i - 1] == s3[i - 1]`, and for `j` in `1..n`, with
   `k = i + j - 1`: `current[j] = (previous[j] and s1[i - 1] == s3[k]) or
   (current[j - 1] and s2[j - 1] == s3[k])`.
3. Replace `previous` with `current` and continue.
4. Return `previous[n]`, the last row's last cell.

#### Walkthrough

Trace the two rolling rows on the successful classic input `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`:

```text
i=0 (s2 only)  previous = [T, ., ., ., ., .]
i=1 (a)        current  = [T, ., ., ., ., .]
i=2 (a)        current  = [T, T, T, T, T, .]
i=3 (b)        current  = [., T, T, ., T, .]
i=4 (c)        current  = [., ., T, T, T, T]
i=5 (c)        current  = [., ., ., T, ., T]
```

Each row equals the corresponding table row from the Bottom-Up 2-D DP walkthrough, and the unneeded predecessor is discarded as soon as its successor exists. The final `previous[n]` is `T`, matching the expected answer `true` for this input; on the failing variant the final cell is `.`, returning `False`.

#### Solution

The code is the walkthrough's row loop: build `current` from `previous`, then rotate.

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if len(s3) != m + n:
            return False
        previous = [True] + [False] * n
        for j in range(1, n + 1):
            previous[j] = previous[j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, m + 1):
            current = [False] * (n + 1)
            current[0] = previous[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, n + 1):
                k = i + j - 1
                from_s1 = previous[j] and s1[i - 1] == s3[k]
                from_s2 = current[j - 1] and s2[j - 1] == s3[k]
                current[j] = from_s1 or from_s2
            previous = current
        return previous[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

One test pair per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `n + 1` cells; the discarded predecessor is garbage-collected.

#### Key Insights

- The dependency pattern of the recurrence determines its memory: a cell
  reads its top and left neighbors only, so one spare row suffices.
- `current` must be a fresh row per `i`; updating `previous` in place would destroy
  the top neighbor `previous[j]` before it is read.
- Iterating the shorter string as `s2` minimizes the row width; the answer is
  unchanged by the argument order.

### Top-Down Memoization with functools.cache

#### Derivation

Step 2's memo is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dfs(i, j)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the base rule and the two character tests untouched:

1. Keep the memoized recursion's structure: the length gate, the shared-
   completion base case, the two-character tests.
2. Replace the `memo` dict with `@cache` on `dfs`, keyed automatically by the
   arguments `(i, j)`.
3. Return `dfs(0, 0)`.

The one behavioral cost: `@cache` keeps every argument pair alive for the life of the process, so the memory profile matches the dict version but cannot be freed early.

#### Walkthrough

Trace the decorated recursion on the failing classic input from the Top-Down Memoization walkthrough, `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbbaccc"`. The call sequence is identical; the only difference is where a repeat lookup lands:

```text
dfs(0, 0) -> dfs(1, 0) -> dfs(2, 0) -> dfs(2, 1)
  ... identical descent ...
dfs(3, 3) -> False                    ** cached: no recompute **
dfs(3, 2) -> False                    ** cached: no recompute **
dfs(0, 0) -> False
```

9 distinct `(i, j)` states are evaluated exactly once each (2 hits, 9 misses), and the answer is `False`, matching the expected answer for this input.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s3) != len(s1) + len(s2):
            return False

        @cache
        def dfs(i: int, j: int) -> bool:
            if i == len(s1) and j == len(s2):
                return True
            k = i + j
            return (i < len(s1) and s1[i] == s3[k] and dfs(i + 1, j)) or (
                j < len(s2) and s2[j] == s3[k] and dfs(i, j + 1)
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
- The recursion body becomes the interleaving definition in its purest form,
  which makes it the version to quote in an interview after sketching the
  dict.
- The length gate stays outside the recursion: it is a property of the whole
  input, not of a state.

## Comparison of Solutions

### Time Complexity

- **Merge Enumeration**: `O(C(m + n, m) * (m + n))` - every merge is built and compared.
- **Top-Down Memoization**: `O(m * n)` - one solve per `(i, j)` state.
- **Bottom-Up 2-D DP**: `O(m * n)` - one test pair per cell.
- **Space-Optimized Two-Row DP**: `O(m * n)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the dict memo with library bookkeeping.

### Space Complexity

- **Merge Enumeration**: `O(m + n)` - the stack plus the `built` string.
- **Top-Down Memoization**: `O(m * n)` - the memo plus the stack.
- **Bottom-Up 2-D DP**: `O(m * n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the decorator's cache plus the stack.

### Trade-offs

- Enumeration is the definitional baseline; its leaf count grows
  combinatorially, making it a correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(m * n)` cache; the
  table versions trade the stack for an evaluation order.
- The two-row table is the production form: same time as everything else at
  linear memory.

### When to Use Each

- **Merge Enumeration**: tiny inputs, or as the brute-force oracle when
  checking the DP versions.
- **Top-Down Memoization**: when deriving live; dropping the `built` string
  for the `(i, j)` pair is the insight worth stating.
- **Bottom-Up 2-D DP**: when the reachable-cell map itself matters, for
  example to reconstruct a witnessing interleaving by walking it backward.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the dict ceremony.

### Optimization Notes

- The length gate rejects `len(s3) != m + n` in constant time and is also
  what keeps every state's `s3[i + j]` access in bounds.
- Greedy matching (always take from `s1` when it matches) fails on inputs
  where both sources hold the same character but only one choice leaves a
  completable suffix.
- Reconstruction of an actual interleaving needs the full table: walk from
  `dp[m][n]`, preferring the top neighbor when it is `True` and its character
  test passes, which is the one feature the space optimization gives up.
