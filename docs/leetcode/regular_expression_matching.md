# [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/)

**Hard** | **40 minutes** | **String, Dynamic Programming, Recursion**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Regular expression](https://en.wikipedia.org/wiki/Regular_expression)

**Practice:** [`practice/regular_expression_matching/solution.py`](../../practice/regular_expression_matching/solution.py)

You are given an input string `s` consisting of lowercase english letters, and a pattern `p` consisting of lowercase english letters, as well as `'.'`, and `'*'` characters.

Return `true` if the pattern matches the **entire** input string, otherwise return `false`.

* `'.'` Matches any single character
* `'*'` Matches zero or more of the preceding element.

## Examples

### Example 1

**Input:** `s = "aa", p = ".b"`

**Output:** `false`

**Explanation:** Regardless of which character we choose for the `'.'` in the pattern, we cannot match the second character in the input string.

### Example 2

**Input:** `s = "nnn", p = "n*"`

**Output:** `true`

**Explanation:** `'*'` means zero or more of the preceding element, `'n'`. We choose `'n'` to repeat three times.

### Example 3

**Input:** `s = "xyz", p = ".*z"`

**Output:** `true`

**Explanation:** The pattern `".*"` means zero or more of any character, so we choose `".."` to match `"xy"` and `"z"` to match `"z"`.

## Constraints

- `1 <= s.length <= 20`
- `1 <= p.length <= 20`
- Each appearance of `'*'`, will be preceded by a valid character or `'.'`.

## Deriving the Solution

Matching is a chain of small decisions: does the next pattern token eat the next string character, and if the token carries a `*`, how many characters does it absorb. Every solution below walks the string with the pattern, one token at a time; they differ only in whether the walker remembers the answers it has already computed.

1. **Start literal.** Recurse on the two fronts: a plain token (a letter or
   `.`) must match the current character, and a starred token forks into "zero
   copies" and "one more copy". Every match configuration is explored, so the
   answer falls out, at exponential cost in the worst case: see
   [Brute Force](#brute-force).
2. **Spot the waste.** The state of every decision is just the pair of
   positions, how much of `s` and how much of `p` are already consumed, and
   different branches reach the same pair over and over.
3. **Cache the pairs.** One dictionary lookup per repeated state collapses the
   exponential tree to at most `m * n` computed states, `O(1)` work each: see
   [Top-Down Memoization](#top-down-memoization).
4. **Tabulate backwards.** The cache keys are grid coordinates, so the same
   relation fills an `(m + 1) x (n + 1)` table bottom-up, no recursion at all:
   see [Bottom-Up DP](#bottom-up-dp).
5. **Hand the cache to the library.** The dictionary is bookkeeping that
   [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)
   implements: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most literal reading walks both strings with two indices and decides one pattern position at a time. At position `j`, the token `p[j]` either matches `s[i]` (same letter, or the wildcard `.`) or it does not; the only wrinkle is a following `*`, which turns `p[j]` into a token that may consume any number of characters, including zero:

1. Define `match(i, j)` as whether `s[i:]` is entirely matched by `p[j:]`.
2. Base case: `j == len(p)` means the pattern is spent, so the match holds
   exactly when the string is spent too, `i == len(s)`.
3. Compute `first`: whether `i < len(s)` and `p[j]` matches `s[i]` (equal
   letter, or `p[j] == '.'`).
4. If `p[j + 1] == '*'`, the token `p[j] + '*'` has two futures: drop it and
   match `s[i:]` with `p[j + 2:]` (`match(i, j + 2)`), or let it eat one more
   character (`first and match(i + 1, j)`), staying on the same token so it
   can eat again. Return the disjunction.
5. Otherwise the token is single: return `first and match(i + 1, j + 1)`.

The "eat one more, stay" branch is what lets a star absorb a whole run: each copy consumes one character of `s` while `j` holds still.

#### Walkthrough

Trace the recursion on a tailored input that exercises zero copies, an absorbing star, and a wildcard-free tail: `s = "aab"`, `p = "c*a*b"` (`c*` must vanish, `a*` absorbs the two `a`s, `b` matches). Each line is a call returning; children print above their parent:

```text
    match(0, 4) -> False    single: first = False, so match(1, 5) = False
      match(1, 4) -> False    single: first = False, so match(2, 5) = False
          match(3, 5) -> True    base case: pattern spent, string spent
        match(2, 4) -> True    single: first = True, so match(3, 5) = True
      match(2, 2) -> True    skip: match(2, 4) = True;  use one: first = False, match(3, 2) = False
    match(1, 2) -> True    skip: match(1, 4) = False;  use one: first = True, match(2, 2) = True
  match(0, 2) -> True    skip: match(0, 4) = False;  use one: first = True, match(1, 2) = True
match(0, 0) -> True    skip: match(0, 2) = True;  use one: first = False, match(1, 0) = True, conjunction False
-> True
```

The root tries `c*`: the skip branch `match(0, 2)` (drop `c*` entirely) succeeds, so the use branch (`c` cannot match `a`) is never needed past its first `False`. Inside, `a*` first runs its skip branch to the end (`match(2, 4)`: `b` left in both) and then absorbs one `a` per level until the base case `match(3, 5)` returns `True`. The root returns `True`: `c*` matches nothing, `a*` matches `"aa"`, `b` matches `"b"`.

#### Solution

The code is the walkthrough's two futures around the `*` peek, one step otherwise.

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        def match(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)
            first = i < len(s) and (p[j] == s[i] or p[j] == ".")
            if j + 1 < len(p) and p[j + 1] == "*":
                return match(i, j + 2) or (first and match(i + 1, j))
            return first and match(i + 1, j + 1)

        return match(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^(m + n))`

Each starred token forks the recursion in two, and the fork repeats: sibling branches re-derive the same `(i, j)` states, so on adversarial patterns like `a*a*a*...c` against a long run the call tree grows exponentially in the input lengths.

##### Space Complexity: `O(m + n)`

No table is kept; the recursion stack reaches depth `m + n` along the deepest consume-everything chain.

#### Key Insights

- Looking one character ahead (`p[j + 1] == '*'`) folds the two-character star
  token into a single-index recursion: no token preprocessing is needed.
- The same state `(i, j)` is reachable by many branch orders, which is invisible
  to correctness and fatal to cost; that observation is the whole bridge to the
  memoized version.
- `first` guards the string end: a pattern like `a*` on an empty string must
  succeed through the zero-copies branch alone.

### Top-Down Memoization

#### Derivation

The Brute Force's every decision is a pure function of the consumed prefixes: `match(i, j)` cannot depend on how the recursion arrived at `(i, j)`. Two branches that meet at the same pair are therefore asking one question twice, and a [cache](https://en.wikipedia.org/wiki/Memoization) keyed by the pair turns the second asking into a lookup. Nothing about the recursion changes; the answers are simply remembered:

1. Keep `match(i, j)` verbatim from the Brute Force, base case included.
2. Before computing, check `memo` for the key `(i, j)` and return a stored
   answer.
3. Otherwise compute the same two futures, store the answer under `(i, j)`,
   and return it.
4. At most `(m + 1) * (n + 1)` distinct states exist, and each does `O(1)`
   work, so the exponential tree collapses to a polynomial budget.

#### Walkthrough

The classic failure input shows the reuse best: `s = "mississippi"`, `p = "mis*is*p*."`. The pattern runs out of string long before the string runs out of pattern, and every near-miss suffix is re-probed by several branches; with the memo, each state is computed once and repeated visits are hits. Note that on this input no visit is actually a hit in the naive traversal order (the first probe of each state is already the last), so the memo pays off on this input by bounding the state space, not by serving lookups:

```text
      match(2, 4) -> False    single: first = False, so match(3, 5) = False
        match(3, 4) -> False    single: first = False, so match(4, 5) = False
                  match(6, 10) -> False    base case: pattern spent, string has letters left
                match(5, 9) -> False    single: first = True, so match(6, 10) = False
              match(5, 7) -> False    skip: match(5, 9) = False;  use one: first = False, match(6, 7) = False
                    match(7, 10) -> False    base case: pattern spent, string has letters left
                  match(6, 9) -> False    single: first = True, so match(7, 10) = False
                match(6, 7) -> False    skip: match(6, 9) = False;  use one: first = False, match(7, 7) = False
                      match(8, 10) -> False    base case: pattern spent, string has letters left
                    match(7, 9) -> False    single: first = True, so match(8, 10) = False
                  match(7, 7) -> False    skip: match(7, 9) = False;  use one: first = False, match(8, 7) = False
                match(7, 5) -> False    skip: match(7, 7) = False;  use one: first = False, match(8, 5) = False
              match(6, 5) -> False    skip: match(6, 7) = False;  use one: first = True, match(7, 5) = False
            match(5, 5) -> False    skip: match(5, 7) = False;  use one: first = True, match(6, 5) = False
          match(4, 4) -> False    single: first = True, so match(5, 5) = False
        match(4, 2) -> False    skip: match(4, 4) = False;  use one: first = False, match(5, 2) = False
      match(3, 2) -> False    skip: match(3, 4) = False;  use one: first = True, match(4, 2) = False
    match(2, 2) -> False    skip: match(2, 4) = False;  use one: first = True, match(3, 2) = False
  match(1, 1) -> False    single: first = True, so match(2, 2) = False
match(0, 0) -> False    single: first = True, so match(1, 1) = False
-> False
```

The tree dies early everywhere: `s*` cannot absorb the double `s`, and `p*` cannot absorb `ssippi`'s consonants, so every branch bottoms out in the base case with string letters remaining. The root returns `False`, matching the known verdict for this input. On inputs where branches do reconverge (the `a*a*` shapes in the next section), the same code serves the repeated states from `memo` instead of recomputing them.

#### Solution

The Brute Force recursion with the memo check and store wrapped around the split.

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        memo = {}

        def match(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)
            if (i, j) in memo:
                return memo[(i, j)]
            first = i < len(s) and (p[j] == s[i] or p[j] == ".")
            if j + 1 < len(p) and p[j + 1] == "*":
                answer = match(i, j + 2) or (first and match(i + 1, j))
            else:
                answer = first and match(i + 1, j + 1)
            memo[(i, j)] = answer
            return answer

        return match(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

At most `(m + 1) * (n + 1)` states exist; each runs its body once, with `O(1)` work (one character comparison, one peek, two recursive reads), and every other visit is a dictionary hit.

##### Space Complexity: `O(m * n)`

The memo holds one entry per computed state, and the recursion stack reaches depth `m + n`.

#### Key Insights

- The state space is the product of the two consumed lengths: remembering
  `(i, j)` pairs is sufficient because the recursion reads nothing else.
- Memoization does not shorten the deepest path (still `m + n`); it collapses
  the tree's width, which is where the exponential lived.
- The base case sits before the memo check, so `(*, len(p))` states are never
  stored: harmless here, and the source of the behavioural note in the last
  solution.

### Bottom-Up DP

#### Derivation

The memo's keys are coordinates: `i` into `s`, `j` into `p`. Any recursion over coordinates can be re-expressed as [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) over a grid, with `dp[i][j]` holding `match(i, j)`: does `s[i:]` match `p[j:]`. The recursion reads strictly larger coordinates (`i + 1`, `j + 1`, `j + 2`), so filling rows bottom-up and columns right-to-left has every dependency ready before its reader arrives:

1. Let `dp[i][j]` be whether `s[i:]` is matched by `p[j:]`; size the table
   `(m + 1) x (n + 1)` so the empty suffixes exist.
2. Seed `dp[m][n] = True`: empty pattern matches empty string.
3. Seed the last row: `dp[m][j]` is true only when `p[j:]` can vanish, which
   means `p[j]` is followed by `*` and `dp[m][j + 2]` is true.
4. Fill the rest moving `i` from `m - 1` down and `j` from `n - 1` down,
   applying the same two futures as the recursion.
5. Return `dp[0][0]`.

#### Recurrence

Let `dp[i][j]` record whether `s[i:]` is entirely matched by `p[j:]`, with `m = len(s)`, `n = len(p)`:

$$ dp[i][j] = \begin{cases}
\text{true}, & i = m \wedge j = n \quad \text{(seed: empty pattern matches empty string)} \\[4pt]
dp[m][j+2], & i = m \wedge p[j+1] = \texttt{*} \quad \text{(seed: trailing tokens must vanish)} \\[4pt]
dp[i][j+2] \vee \bigl(first \wedge dp[i+1][j]\bigr), & p[j+1] = \texttt{*} \\[4pt]
first \wedge dp[i+1][j+1], & \text{otherwise}
\end{cases} $$

```text
dp[m][n] = true
dp[m][j] = dp[m][j + 2]     when p[j + 1] == '*'   (trailing tokens must vanish)
dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])   when p[j + 1] == '*'
dp[i][j] = first and dp[i + 1][j + 1]                 otherwise
first    = i < m and (p[j] == s[i] or p[j] == '.')
answer   = dp[0][0]
```

`first` is the single-character compatibility of `p[j]` with `s[i]`. The star's zero-copies term `dp[i][j + 2]` drops the token; the extend term `dp[i + 1][j]` consumes one character and stays on the token.

#### Walkthrough

Let us fill the table on `s = "aab"`, `p = "c*a*b"`, the input the Brute Force traced: `m = 3`, `n = 5`, `T` marks `True` and `.` marks `False`. Rows fill bottom-up, columns right-to-left within a row:

```text
seed     dp[3][5] = True    empty pattern matches empty string
seed     row i = 3: . . . . . T
row 3    j = 2    p[3] = '*'    dp[3][2] = dp[3][4] = False
row 3    j = 0    p[1] = '*'    dp[3][0] = dp[3][2] = False
i = 2, j = 4    p[4] = 'b' vs 'b'    single match: True, dp[3][5] = True   -> True
i = 2, j = 3    p[3] = '*' vs 'b'    single match: False, dp[3][4] = False   -> False
i = 2, j = 2    p[2] = 'a' + '*' vs 'b'    zero copies: dp[2][4] = True;  extend: 'a' absorbs 'b' = False, dp[3][2] = False   -> True
i = 2, j = 1    p[1] = '*' vs 'b'    single match: False, dp[3][2] = False   -> False
i = 2, j = 0    p[0] = 'c' + '*' vs 'b'    zero copies: dp[2][2] = True;  extend: 'c' absorbs 'b' = False, dp[3][0] = False   -> True
row 2 done: T . T . T .
i = 1, j = 4    p[4] = 'b' vs 'a'    single match: False, dp[2][5] = False   -> False
i = 1, j = 3    p[3] = '*' vs 'a'    single match: False, dp[2][4] = True   -> False
i = 1, j = 2    p[2] = 'a' + '*' vs 'a'    zero copies: dp[1][4] = False;  extend: 'a' absorbs 'a' = True, dp[2][2] = True   -> True
i = 1, j = 1    p[1] = '*' vs 'a'    single match: False, dp[2][2] = True   -> False
i = 1, j = 0    p[0] = 'c' + '*' vs 'a'    zero copies: dp[1][2] = True;  extend: 'c' absorbs 'a' = False, dp[2][0] = True   -> True
row 1 done: T . T . . .
i = 0, j = 4    p[4] = 'b' vs 'a'    single match: False, dp[1][5] = False   -> False
i = 0, j = 3    p[3] = '*' vs 'a'    single match: False, dp[1][4] = False   -> False
i = 0, j = 2    p[2] = 'a' + '*' vs 'a'    zero copies: dp[0][4] = False;  extend: 'a' absorbs 'a' = True, dp[1][2] = True   -> True
i = 0, j = 1    p[1] = '*' vs 'a'    single match: False, dp[1][2] = True   -> False
i = 0, j = 0    p[0] = 'c' + '*' vs 'a'    zero copies: dp[0][2] = True;  extend: 'c' absorbs 'a' = False, dp[1][0] = True   -> True
row 0 done: T . T . . .
-> dp[0][0] = True
```

The row-3 seeding is the vanish rule at work: `a*` is followed by the plain token `b`, so `dp[3][2] = dp[3][4] = False`, and `c*` then reads that `False` at `dp[3][2]`; the row therefore stays all `False` but for the seed. Row 2 (the last input letter) builds the `b` match at `dp[2][4]`, and `a*`'s zero-copies term lifts `dp[2][2]` to `True` because dropping `a*` leaves the already-matching `b` suffix; row 1 chains `a*` through its extend term (`dp[1][2]`), and the root reads `dp[0][0] = True` via `c*`'s zero-copies term pointing at it, the same `True`s the recursion found, matching the walkthrough verdict for this input.

#### Solution

The code is the table fill from the walkthrough: seed the base row, then sweep backwards.

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        # dp[i][j] = does s[i:] match p[j:]
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True
        # Trailing "x*" tokens can each match nothing, so the empty string
        # suffix of s is matched by any all-vanishing pattern suffix.
        for j in range(n - 2, -1, -1):
            if p[j + 1] == "*":
                dp[m][j] = dp[m][j + 2]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                first = p[j] == s[i] or p[j] == "."
                if j + 1 < n and p[j + 1] == "*":
                    dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])
                else:
                    dp[i][j] = first and dp[i + 1][j + 1]
        return dp[0][0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

Every one of the `(m + 1) * (n + 1)` cells is computed exactly once, with `O(1)` work: one comparison, one peek, and a fixed number of reads of already-final cells.

##### Space Complexity: `O(m * n)`

The `dp` table holds one boolean per suffix pair.

#### Key Insights

- The table is the memo turned upright: same cells, same values, filled in the
  reverse of the order the recursion discovered them.
- The base-row seeding is the one place the bottom-up form needs care: the
  recursion's `i == len(s)` check becomes an explicit last row that only
  vanish-capable pattern suffixes may enter.
- Reading direction (backwards here, forwards in many write-ups) is a
  convention: what matters is that `dp[i][j]` only ever reads cells whose
  recurrences are already final.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the token-matching recursion, and a dictionary that stops it from re-answering a state it has already decided. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recursion and its base case stay on the page exactly as the Brute Force wrote them:

1. Keep `match(i, j)` verbatim from the Brute Force: base case, `first`,
   star peek, and both futures.
2. Decorate it with `@cache`, so each distinct `(i, j)` runs the body at most
   once and every later request is answered from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the
   `memo = {}` declaration, the `if (i, j) in memo` lookup, and the
   `memo[(i, j)] = ...` store.
4. Because `match` is defined inside `isMatch`, each call builds a fresh
   function object with a fresh cache, so nothing leaks between inputs.

One behavioural difference follows from where the decorator sits. The hand-rolled version answers `j == len(p)` before it ever consults `memo`, so base-case keys are never stored and their one-line body re-runs on every visit; `@cache` wraps the entire body, so those keys are cached like any other state.

#### Walkthrough

Trace `s = "aaaa"`, `p = "a*a*"`: two stars over one run of letters, so both stars compete for the same characters and the two branches reconverge constantly. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
    match(0, 4) -> False    base case, now cached under key (0, 4)
      match(1, 4) -> False    base case, now cached under key (1, 4)
        match(2, 4) -> False    base case, now cached under key (2, 4)
          match(3, 4) -> False    base case, now cached under key (3, 4)
            match(4, 4) -> True    base case, now cached under key (4, 4)
          match(4, 2) -> True    skip: match(4, 4) = True;  use one: first = False, match(5, 2) = False, now cached under key (4, 2)
        match(3, 2) -> True    skip: match(3, 4) = False;  use one: first = True, match(4, 2) = True, now cached under key (3, 2)
      match(2, 2) -> True    skip: match(2, 4) = False;  use one: first = True, match(3, 2) = True, now cached under key (2, 2)
    match(1, 2) -> True    skip: match(1, 4) = False;  use one: first = True, match(2, 2) = True, now cached under key (1, 2)
  match(0, 2) -> True    skip: match(0, 4) = False;  use one: first = True, match(1, 2) = True, now cached under key (0, 2)
    match(1, 2) -> True    ** cache hit, the body does not run **
      match(2, 2) -> True    ** cache hit, the body does not run **
        match(3, 2) -> True    ** cache hit, the body does not run **
          match(4, 2) -> True    ** cache hit, the body does not run **
        match(4, 0) -> True    skip: match(4, 2) = True;  use one: first = False, match(5, 0) = False, now cached under key (4, 0)
      match(3, 0) -> True    skip: match(3, 2) = True;  use one: first = True, match(4, 0) = True, now cached under key (3, 0)
    match(2, 0) -> True    skip: match(2, 2) = True;  use one: first = True, match(3, 0) = True, now cached under key (2, 0)
  match(1, 0) -> True    skip: match(1, 2) = True;  use one: first = True, match(2, 0) = True, now cached under key (1, 0)
match(0, 0) -> True    skip: match(0, 2) = True;  use one: first = True, match(1, 0) = True, now cached under key (0, 0)
-> True
```

The first star's subtree computes and caches the whole `j = 2` column; the second star's subtree then re-requests exactly those states and gets every one from the cache, including the four hits shown. The root returns `True`: the first `a*` matches nothing, the second absorbs all four letters. The base-case keys `(0, 4)` through `(3, 4)` are cached too, which is the behavioural difference from the hand-rolled memo, whose `j == len(p)` check runs before any caching.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs.
        @cache
        def match(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)
            first = i < len(s) and (p[j] == s[i] or p[j] == ".")
            if j + 1 < len(p) and p[j + 1] == "*":
                return match(i, j + 2) or (first and match(i + 1, j))
            return first and match(i + 1, j + 1)

        return match(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

- The cache admits each of the `(m + 1) * (n + 1)` states into the body exactly
  once, and each admission does one comparison, one peek, and two cache-backed
  reads
- Every other call is a tuple-keyed dictionary lookup, constant time on small
  integer pairs

##### Space Complexity: `O(m * n)`

- The decorator's cache holds one entry per distinct `(i, j)`, including the
  base-case keys the hand-rolled memo never stored
- The recursion still descends to depth `m + n`, so the stack is a lower-order
  term next to the cache

#### Key Insights

- `@cache` keys on the argument tuple, so it is a drop-in replacement only when
  the arguments are hashable and the function is genuinely pure; `match` reads
  nothing but `i`, `j`, `s`, and `p`, which is what licenses the substitution.
- Caching the base-case keys adds `m + 1` extra entries that all hold trivial
  facts; with a cheaper base case being cached the effect would be a win, so
  the asymmetry is worth noticing but not worth code.
- The decorator form makes the memoization-optimal complexity visible at a
  glance: exponential in the Brute Force, linear-in-states the moment results
  are remembered, whichever bookkeeping does the remembering.

## Comparison of Solutions

The practice harness's `practice/regular_expression_matching/reference.py` implements the **Top-Down Memoization** solution.

### Time Complexity

- **Brute Force**: `O(2^(m + n))` - every starred token forks the search and sibling branches repeat states.
- **Top-Down Memoization**: `O(m * n)` - each state computed once, `O(1)` work per state.
- **Bottom-Up DP**: `O(m * n)` - the same states as table cells, each filled once.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the decorator reproduces the memoized run times.

### Space Complexity

- **Brute Force**: `O(m + n)` - recursion stack only.
- **Top-Down Memoization**: `O(m * n)` - memo entries plus the stack.
- **Bottom-Up DP**: `O(m * n)` - the full `dp` table.
- **Top-Down Memoization with functools.cache**: `O(m * n)` - the decorator's cache plus the stack.

### Trade-offs

- The Brute Force is the direct transcription of the token rules and the
  easiest version to trust, but adversarial inputs (`a*a*a*...` against long
  runs) blow it up exponentially.
- Both memoized versions bound the work by the state count at the price of a
  table; the recursion shape, and with it the correctness argument, is
  untouched.
- The Bottom-Up DP removes the recursion stack and its depth concern, paying
  for that with explicit base-row seeding and a fill order to get right.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny inputs.
- **Top-Down Memoization** (recommended): the default; the smallest change from
  the natural recursion, and the state count bound falls out of the key set.
- **Bottom-Up DP**: when recursion depth matters, or when the grid form is the
  one the interviewer wants to see.
- **Top-Down Memoization with functools.cache**: the Pythonic tidy-up when the
  recursive shape is wanted and the memo should not be hand-maintained.

### Optimization Notes

- The `*`-peek (`p[j + 1] == '*'`) is what keeps the recursion single-indexed
  per string: a token-based preprocessing step (compiling `p` into atomic
  tokens first) reaches the same recursion with longer lines and no gain.
- Star handling differs across solutions only in bookkeeping: the two futures
  (zero copies, one more copy) are identical in all four. The classic trap is
  writing the extend branch as `match(i + 1, j + 2)`, which consumes one
  character and also drops the token, allowing only single copies.
- Rolling the bottom-up table to two rows (`O(n)` space) is mechanical because
  `dp[i][*]` reads only `dp[i + 1][*]` and `dp[i][j + 1]`/`dp[i][j + 2]`, but
  the boolean table is small enough that the savings rarely matter at
  `m, n <= 20`.
- This recursion is the textbook NFA simulation: the states `(i, j)` are
  configuration pairs, the memo is the visited set, and Thompson's
  construction reaches the same `O(m * n)` bound with the same idea in
  different clothes.
