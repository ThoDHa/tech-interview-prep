# [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/)

**Hard** | **40 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/distinct_subsequences/solution.py`](../../practice/distinct_subsequences/solution.py)

You are given two strings `s` and `t`, both consisting of english letters.

Return the number of distinct **subsequences** of `s` which are equal to `t`.

## Examples

### Example 1

**Input:** `s = "caaat", t = "cat"`

**Output:** `3`

**Explanation:** There are 3 ways you can generate `"cat"` from `s`.
* (c)aa(at)
* (c)a(a)a(t)
* (ca)aa(t)

### Example 2

**Input:** `s = "xxyxy", t = "xy"`

**Output:** `5`

**Explanation:** There are 5 ways you can generate `"xy"` from `s`.
* (x)x(y)xy
* (x)xyx(y)
* x(x)(y)xy
* x(x)yx(y)
* xxy(x)(y)

## Constraints

- `1 <= s.length, t.length <= 1000`
- `s` and `t` consist of English letters.

## Deriving the Solution

A subsequence of `s` equal to `t` is a set of positions in `s` spelling `t` in order, so counting them is counting position choices. Walking `s` left to right, each character is either consumed by the next character of `t` (only possible on a match) or skipped, and the count for a position pair splits exactly along that fork. Every solution below walks the same fork; they differ in which pairs they re-derive and how many results they keep in memory.

1. **Start literal.** Walk `s` with an index into `t` and count the ways by
   trying both choices at every character. The fork tree costs `O(2^m)`:
   see [Brute Force Enumeration](#brute-force-enumeration).
2. **Spot the overlap.** A branch's future depends only on `(i, j)`, the
   positions reached in `s` and `t`, never on which earlier characters were
   consumed, so the same pairs recur across different skip histories.
   Memoizing them collapses the tree to one solve per pair: see
   [Top-Down Memoization](#top-down-memoization).
3. **Tabulate the pairs.** The pairs form a two-dimensional grid
   `(prefix of s, prefix of t)` where each cell needs only the row above.
   Filling the grid row by row needs no recursion: see
   [Bottom-Up 2-D DP](#bottom-up-2-d-dp).
4. **Keep one row.** Sweeping `t` right to left inside a single row lets the
   row hold both the previous and the current generation, `O(n)` space, same
   time: see [Space-Optimized One-Row DP](#space-optimized-one-row-dp).
5. **Hand the cache to the library.** Step 2's memo dict is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the two base cases and the skip/match fork stay
   exactly as written: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Enumeration

#### Derivation

The most literal reading of "count the subsequences equal to `t`" builds them position by position. Walking `s`, each character either joins the subsequence under construction (matching the next character of `t`) or is skipped; the construction succeeds when all of `t` is matched, and dies when `s` runs out first. Trying both choices at every character enumerates every way:

1. Define `dfs(i, j)` as the number of ways to form `t[j:]` from `s[i:]`.
2. Return `1` when `j == len(t)`: the whole of `t` is matched, and there is
   exactly one way to have done it.
3. Return `0` when `i == len(s)`: `s` is exhausted with `t` incomplete.
4. Otherwise start with the skip count `dfs(i + 1, j)`; when
   `s[i] == t[j]`, add the match count `dfs(i + 1, j + 1)`.
5. Return `dfs(0, 0)`.

#### Walkthrough

The full tree on Example 1 (`s = "caaat"`, `t = "cat"`) makes 23 calls. The opening chain hunts a `'c'` and finds it immediately, after which the `'a'`-matching subtree carries the whole count. Tracing `dfs(1, 1)`, the count of ways to form `"at"` from `"aaat"`, shows the fork structure:

```text
dfs(1, 1) 'a' vs 'a'  MATCH
  dfs(2, 1) skip branch: 'a' vs 'a'  MATCH
    dfs(3, 1) skip branch: 'a' vs 'a'  MATCH
      dfs(4, 1) skip branch: 't' vs 'a' -> dfs(5, 1) -> 0
      dfs(4, 2) match branch:  't' vs 't' MATCH -> dfs(5, 3) -> 1
      dfs(3, 1) -> 1                      [a@3 + t@4]
    dfs(3, 2) match branch: 'a' vs 't' -> dfs(4, 2) -> 1
    dfs(2, 1) -> 2                        [a@2 + t@4], [a@3 + t@4]
  dfs(2, 2) match branch: 'a' vs 't' -> dfs(3, 2) -> 1
  dfs(1, 1) -> 3                          [a@1], [a@2], [a@3] + t@4
```

Three ways to place the `'a'`, each with the forced trailing `'t'`, so `dfs(1, 1)` returns `3` and the root (whose `'c'` is matched immediately) returns `3`, matching the expected Output for Example 1. Example 2's five ways come from the same fork structure on `"xxyxy"`.

#### Solution

The code is the walkthrough's fork: skip every character, additionally match on a hit.

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        def dfs(i: int, j: int) -> int:
            if j == len(t):
                return 1
            if i == len(s):
                return 0
            # Skip s[i]; on a match, also consume it with t[j]
            count = dfs(i + 1, j)
            if s[i] == t[j]:
                count += dfs(i + 1, j + 1)
            return count

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^m)`

Each character of `s` forks into skip and (on a match) match branches, so the tree grows exponentially in `len(s)`; matching alphabets are the worst case.

##### Space Complexity: `O(m)`

The recursion stack, one frame per consumed character of `s`.

#### Key Insights

- Transcribes the counting rule directly: skip is free, match is conditional,
  and completed targets count once each.
- Correct on every input, including `t` longer than `s` (the tree simply
  dies everywhere) and repeated letters (every position choice is counted).
- The same `(i, j)` pairs recur across different skip histories, which is
  the redundancy the next solution removes.

### Top-Down Memoization

#### Derivation

The enumeration re-solves futures it has already seen: reaching `(i, j)` after skipping three characters faces the same subproblem as reaching it after one skip and one near-miss. A branch's future depends only on `(i, j)`, never on how much of `s` was burned getting there, so each pair is a [memoizable](https://en.wikipedia.org/wiki/Memoization) state with `(m + 1) × (n + 1)` of them:

1. Keep the enumeration's recursion unchanged.
2. Add a `memo` keyed by `(i, j)`; check it on entry and store before every
   return.

#### Walkthrough

Trace the recursion with hits marked on Example 1: `s = "caaat"`, `t = "cat"`. The first branch chains skip calls that never find another `'c'` and stores a column of zeros; the real work is the `dfs(1, 1)` subtree:

```text
dfs(0, 0) 'c' vs 'c'  MATCH
  dfs(1, 0) skip branch: 'a' vs 'c'
    ... chain of skips down to dfs(5, 0) -> 0, each level stored ...
  dfs(1, 0) -> 0  stored
  dfs(1, 1) 'a' vs 'a'  MATCH
    dfs(2, 1) 'a' vs 'a'  MATCH
      dfs(3, 1) 'a' vs 'a'  MATCH
        dfs(4, 1) 't' vs 'a'
          dfs(5, 1) -> 0  (s exhausted)
        dfs(4, 2) 't' vs 't'  MATCH
          dfs(5, 2) -> 0  (s exhausted)
          dfs(5, 3) -> 1  (all of t matched)
        dfs(4, 2) -> 1  stored
      dfs(3, 1) -> 1  stored
      dfs(3, 2) 'a' vs 't'
        dfs(4, 2) -> 1  ** memo hit **
      dfs(3, 2) -> 1  stored
    dfs(2, 1) -> 2  stored
    dfs(2, 2) 'a' vs 't'
      dfs(3, 2) -> 1  ** memo hit **
    dfs(2, 2) -> 1  stored
  dfs(1, 1) -> 3  stored
dfs(0, 0) -> 3  stored
```

Two repeat arrivals are answered from the memo: `dfs(4, 2)` under `dfs(3, 2)` and `dfs(3, 2)` under `dfs(2, 2)`. Twelve states are computed against the brute tree's 23 calls, and the root returns `3`, matching the expected Output for Example 1. On Example 2 (`s = "xxyxy"`, `t = "xy"`) the savings grow: 9 states, against a brute tree of 22 calls that re-derives the same suffix counts repeatedly.

#### Solution

The code is the enumeration with a dict in front of it.

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        memo = {}

        def dfs(i: int, j: int) -> int:
            if j == len(t):
                return 1
            if i == len(s):
                return 0
            if (i, j) in memo:
                return memo[(i, j)]
            result = dfs(i + 1, j)
            if s[i] == t[j]:
                result += dfs(i + 1, j + 1)
            memo[(i, j)] = result
            return result

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

At most `(m + 1) × (n + 1)` states, each solved once with one recursion into a match branch; the skip branch is the same pair one row later.

##### Space Complexity: `O(m * n)`

The memo's entries plus a recursion stack of up to `m + n` frames.

#### Key Insights

- The state `(i, j)` is a complete summary of the skip history: nothing else
  about which characters were consumed changes the count.
- The two base cases stay outside the memo: caching constant `0`s and `1`s
  saves nothing over returning them.
- The match branch's recursion `dfs(i + 1, j + 1)` is the only place `j`
  moves, which is why the state count is linear in both strings rather than
  exponential.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still asks from the top: "how many ways to form `t[j:]` from `s[i:]`?". Flip it: `dp[i][j]` is the number of ways to form the first `j` characters of `t` from the first `i` of `s`. Column 0 is the empty-target base (`1` everywhere: one way to form nothing); row 0 beyond it is `0` (no source). Each interior cell takes the count without `s[i - 1]` and, on a match, adds the count of forming `t[:j - 1]` from `s[:i - 1]` with `s[i - 1]` as the finishing character. Filling row by row never reads an undecided cell:

1. Allocate `dp` of size `(m + 1) x (n + 1)`; set `dp[i][0] = 1` for every
   `i` and `dp[0][j] = 0` for `j > 0`.
2. For each `i` in `1..m` and `j` in `1..n`:
   - `dp[i][j] = dp[i - 1][j]` (skip `s[i - 1]`),
   - plus `dp[i - 1][j - 1]` when `s[i - 1] == t[j - 1]` (match it).
3. Return `dp[m][n]`.

The `- 1` offsets exist because the table counts prefixes while the strings are position-indexed: cell `(i, j)` decides with `s[i - 1]` and `t[j - 1]`.

#### Recurrence

Let \(dp_i[j]\) be the number of distinct subsequences of the first `i` characters of `s` equal to the first `j` characters of `t`:

$$ dp_i[j] = dp_{i-1}[j] + dp_{i-1}[j-1] \cdot [\,s[i-1] = t[j-1]\,], \qquad dp_i[0] = 1,\ dp_0[j > 0] = 0 $$

```text
dp_i[0] = 1                    (empty t: one way, choose nothing)
dp_0[j] = 0 for j > 0          (empty s: cannot form nonempty t)
dp_i[j] = dp_(i-1)[j]
          + dp_(i-1)[j-1]      (only when s[i - 1] == t[j - 1])
```

The bracketed term is 1 on a match and 0 otherwise: the skip count always carries, and the match count joins only when the characters agree. Both terms read row `i - 1`, so no cell ever sees the character it is deciding about twice. The answer is \(dp_m[n]\).

#### Walkthrough

Trace the fill on Example 1: `s = "caaat"`, `t = "cat"`. Rows are `s` prefixes, columns are `t` prefixes:

```text
        ''  c  a  t
  ''     1  0  0  0
  c      1  1  0  0
  a      1  1  1  0
  a      1  1  2  0
  a      1  1  3  0
  t      1  1  3  3
```

Row `c` matches once (`dp[1][1] = 1`); each `'a'` row adds the diagonal: `dp[3][2] = dp[2][2] + dp[2][1] = 1 + 1 = 2` (`"ca"` with either the first or second `'a'`), and `dp[4][2] = 2 + 1 = 3`. The final row matches `'t'`: `dp[5][3] = dp[4][3] + dp[4][2] = 0 + 3 = 3`, matching the expected Output for Example 1. Example 2 fills the same way to `5`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = 1
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp[i][j] = dp[i - 1][j]
                if s[i - 1] == t[j - 1]:
                    dp[i][j] += dp[i - 1][j - 1]
        return dp[m][n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

One copy plus one conditional add per table cell.

##### Space Complexity: `O(m * n)`

The full table.

#### Key Insights

- Column 0's unconditional `1` encodes "form the empty string by choosing
  nothing", the seed every match chain ultimately reads.
- The recurrence is the memoized recursion transposed: skip is the copy,
  match is the diagonal add.
- Counts only ever grow along matches, so a row of zeros above a mismatching
  column stays zero, the structure the failing cases exploit.

### Space-Optimized One-Row DP

#### Derivation

Cell `(i, j)` reads only row `i - 1`: the cell above and the cell above-left. Older rows are dead weight, so the whole table collapses to one row `dp` where `dp[j]` counts the ways to form `t[:j]` from the `s` prefix processed so far. The copy term (`dp[i - 1][j]`) is the value already sitting in the row, and sweeping `j` right to left makes `dp[j - 1]` still hold the previous row's value when the match term reads it, so a single row does the work of two:

1. Initialize `dp` of size `n + 1` with `dp[0] = 1` and the rest `0`.
2. For each character `s[i - 1]`, sweep `j` from `min(i, n)` down to `1`:
   when `s[i - 1] == t[j - 1]`, update `dp[j] += dp[j - 1]`.
3. Return `dp[n]`.

A non-matching character updates nothing: skipping it is the identity, which is why the loop body is one conditional add.

#### Walkthrough

Trace the single row on Example 1: `s = "caaat"`, `t = "cat"`, one line per consumed character:

```text
start            dp = [1, 0, 0, 0]
s[0]='c'         dp = [1, 1, 0, 0]     dp[1] += dp[0]
s[1]='a'         dp = [1, 1, 1, 0]     dp[2] += dp[1]
s[2]='a'         dp = [1, 1, 2, 0]     dp[2] += dp[1]
s[3]='a'         dp = [1, 1, 3, 0]     dp[2] += dp[1]
s[4]='t'         dp = [1, 1, 3, 3]     dp[3] += dp[2]
```

Each line equals the corresponding table row of the Bottom-Up 2-D DP: during the third `'a'`, `dp[2]` reads `dp[1] = 1` before `dp[2]` is updated, which is the above-left cell, and the untouched `dp[3]` meanwhile keeps carrying the previous generation. The final `dp[n]` is `3`, matching the expected Output for Example 1; repeated-letter corner cases like an all-same-letter array or a target built from one repeated letter accumulate the same way, one add per matching pair.

#### Solution

The code is the walkthrough's sweeps: one conditional add per matching pair, right to left.

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        n = len(t)
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(1, len(s) + 1):
            for j in range(min(i, n), 0, -1):
                if s[i - 1] == t[j - 1]:
                    dp[j] += dp[j - 1]
        return dp[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

One comparison per `(s prefix, t prefix)` pair, with an add on matches.

##### Space Complexity: `O(n)`

The single row of `n + 1` entries.

#### Key Insights

- The descending sweep is the whole trick: it freezes `dp[j - 1]` at the
  previous generation's value so each character of `s` is consumed at most
  once per counted subsequence.
- The `min(i, n)` cap is a pure bounds win: `t[:j]` cannot be formed from
  fewer than `j` characters of `s`, so those cells are still zero anyway.
- `dp[0] = 1` never changes: the empty target has exactly one formation, and
  every match chain bottoms out there.

### Top-Down Memoization with functools.cache

#### Derivation

Step 2's memo is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dfs(i, j)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the two base cases and the skip/match fork untouched:

1. Keep the memoized recursion's structure: the same two base cases, the
   same skip-plus-conditional-match count.
2. Replace the `memo` dict with `@cache` on `dfs`, keyed automatically by the
   arguments `(i, j)`.
3. Return `dfs(0, 0)`.

The one behavioral cost: `@cache` also stores the base-case results and keeps every pair alive for the life of the process, so the memory profile matches or slightly exceeds the dict version.

#### Walkthrough

Trace the decorated recursion on Example 1: `s = "caaat"`, `t = "cat"`. The call sequence is identical to the Top-Down Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dfs(0, 0) -> ... identical descent ...
dfs(4, 2) -> 1                       ** cached: no recompute **
dfs(3, 2) -> 1                       ** cached: no recompute **
dfs(0, 0) -> 3
```

16 distinct `(i, j)` calls are cached (the dict version stored only the 12 interior states), each of the 2 repeat arrivals is a hit, and the answer is `3`, matching the expected Output for Example 1.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        @cache
        def dfs(i: int, j: int) -> int:
            if j == len(t):
                return 1
            if i == len(s):
                return 0
            result = dfs(i + 1, j)
            if s[i] == t[j]:
                result += dfs(i + 1, j + 1)
            return result

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
- Caching base cases is harmless: there are only two distinct results.
- The recursion body is the counting rule in its purest form, which makes it
  the version to quote in an interview after sketching the dict.

## Comparison of Solutions

### Time Complexity

- **Brute Force Enumeration**: `O(2^m)` - every skip/match history is walked.
- **Top-Down Memoization**: `O(m * n)` - one solve per `(i, j)` state.
- **Bottom-Up 2-D DP**: `O(m * n)` - one update per table cell.
- **Space-Optimized One-Row DP**: `O(m * n)` - the same cells, one row at a time.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the dict memo with library bookkeeping.

### Space Complexity

- **Brute Force Enumeration**: `O(m)` - the recursion stack.
- **Top-Down Memoization**: `O(m * n)` - the memo plus the stack.
- **Bottom-Up 2-D DP**: `O(m * n)` - the full table.
- **Space-Optimized One-Row DP**: `O(n)` - the single row.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the decorator's cache plus the stack.

### Trade-offs

- Enumeration is the definitional baseline; exponential time makes it a
  correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(m * n)` cache; the
  table versions trade the stack for an evaluation order.
- The one-row table is the production form: same time as everything else at
  linear memory.

### When to Use Each

- **Brute Force Enumeration**: tiny inputs, or as the brute-force oracle when
  checking the DP versions.
- **Top-Down Memoization**: when deriving the recurrence live; the skip/match
  fork writes itself from the definition.
- **Bottom-Up 2-D DP**: when the full table matters, for example to
  reconstruct a witnessing position set by walking it backward.
- **Space-Optimized One-Row DP**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the dict ceremony.

### Optimization Notes

- Iterating the shorter string as `t` minimizes the one-row version's
  footprint from `O(max(m, n))` to `O(min(m, n))`; the count is unchanged by
  the argument order.
- Counts grow combinatorially (all-equal strings produce binomial-coefficient
  answers), so Python's arbitrary-precision integers are load-bearing; in
  fixed-width languages the LeetCode variant asks for the count modulo a
  prime instead.
- The match branch is the only place `j` advances, which caps the recursion
  depth at `m + n` and keeps the state space rectangular rather than
  exponential.
