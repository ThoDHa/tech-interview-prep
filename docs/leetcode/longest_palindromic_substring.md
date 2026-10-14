# [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Longest palindromic substring](https://en.wikipedia.org/wiki/Longest_palindromic_substring) · [Manacher's algorithm](https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher%27s_algorithm) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

**Practice:** [`practice/longest_palindromic_substring/solution.py`](../../practice/longest_palindromic_substring/solution.py)

Given a string `s`, return the longest palindromic substring in `s`.

## Examples

### Example 1

**Input:** `s = "babad"`

**Output:** `"bab"`

**Explanation:** `"aba"` is also a valid answer.

### Example 2

**Input:** `s = "cbbd"`

**Output:** `"bb"`

## Constraints

- `1 <= s.length <= 1000`
- `s` consist of only digits and English letters.

## Deriving the Solution

A substring is a palindrome exactly when its mirrored characters all match. Every solution below verifies that mirror property; they differ in how much already-verified matching they reuse instead of re-checking characters from scratch.

1. **Start literal.** Enumerate every substring and check each one by walking
   two pointers inward. `O(n^2)` substrings at `O(n)` per check costs `O(n^3)`: see [Brute Force](#brute-force).
2. **Reuse the inner verdict.** Checking `s[i..j]` re-walks `s[i+1..j-1]`, a
   span some earlier check already verified. Record every verdict in a table: `s[i..j]` is a palindrome exactly when its ends match and `s[i+1..j-1]` is, so each cell costs `O(1)` and the whole table `O(n^2)` time, at `O(n^2)` space: see [Bottom-Up DP](#bottom-up-dp).
3. **Grow from centers instead.** Rather than asking "is this substring a
   palindrome?" for every span, ask "how far does the palindrome around this center reach?". Only `2n - 1` centers exist, and expanding each until its first mismatch visits none of the doomed substrings, keeping `O(n^2)` time while dropping the table to `O(1)` space: see [Expand Around Center](#expand-around-center).
4. **Reuse across centers.** Expansion still re-compares characters that lie
   inside an already-discovered palindrome, where symmetry has predetermined them. Seeding each new center with its mirror's radius means no character is ever matched twice, reaching `O(n)`: see [Manacher's Algorithm](#manachers-algorithm).

## Solutions

### Brute Force

#### Derivation

The most direct idea is to look at every possible substring and check whether it reads the same forwards and backwards, remembering the longest one that does. A substring is a palindrome exactly when its mirrored characters all match, which a simple inward two-pointer walk verifies by hand.

1. For each start index `i`, consider every end index `j >= i`, covering all
   `O(n^2)` substrings.
2. Before paying for a palindrome check, skip any substring no longer than the
   best found so far, since it cannot improve the answer.
3. Check `s[i..j]` with `is_palindrome`, which compares `s[left]` and `s[right]`
   while walking the two pointers toward the middle.
4. When a longer palindrome is found, record its start and length, and finally
   return the recorded slice `s[start:start + max_len]`.

#### Walkthrough

Trace the Brute Force on Example 1, `s = "babad"` (indices `0:b 1:a 2:b 3:a 4:d`). Start with `start = 0`, `max_len = 0`. Each step considers the substring `s[i..j]`, first applying the length guard `j - i + 1 > max_len`, and only paying for `is_palindrome` when the guard passes. The best `(start, max_len)` updates whenever a longer palindrome is confirmed.

| Step | `i`, `j` | `s[i..j]` | guard `len > max_len`? | palindrome? | `start`, `max_len` after |
|------|----------|-----------|------------------------|-------------|--------------------------|
| 1 | `0, 0` | `"b"` | yes (`1 > 0`) | yes | `0`, `1` |
| 2 | `0, 1` | `"ba"` | yes (`2 > 1`) | no | `0`, `1` |
| 3 | `0, 2` | `"bab"` | yes (`3 > 1`) | yes | `0`, `3` |
| 4 | `0, 3` | `"baba"` | yes (`4 > 3`) | no | `0`, `3` |
| 5 | `0, 4` | `"babad"` | yes (`5 > 3`) | no | `0`, `3` |
| 6 | `1, 1` | `"a"` | no (`1 > 3` is false) | skipped | `0`, `3` |
| 7 | `1, 2` | `"ab"` | no (`2 > 3` is false) | skipped | `0`, `3` |
| 8 | `1, 3` | `"aba"` | no (`3 > 3` is false) | skipped | `0`, `3` |
| 9 | `1, 4` | `"abad"` | yes (`4 > 3`) | no | `0`, `3` |

The remaining pairs (`2, 2`, `2, 3`, `2, 4`, `3, 3`, `3, 4`, and `4, 4`) all span `3` or fewer characters, so the length guard skips every one of them without a palindrome check: this is exactly the pruning the guard buys. Note step 8: `"aba"` is itself a valid palindrome, but it ties the current best length of `3` rather than beating it, so the guard skips it and the earlier `"bab"` is kept.

The loop ends with `start = 0`, `max_len = 3`, so the return value is `s[0:3] = "bab"`, which matches the expected Output `"bab"`.

#### Solution

The code is the walkthrough's double loop, with the length guard placed before each palindrome check.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)

        def is_palindrome(left: int, right: int) -> bool:
            # Walk inward from both ends, comparing mirrored characters.
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        start, max_len = 0, 0
        # Try every substring s[i..j] and keep the longest palindrome.
        for i in range(n):
            for j in range(i, n):
                if j - i + 1 > max_len and is_palindrome(i, j):
                    start, max_len = i, j - i + 1

        return s[start:start + max_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

There are `O(n^2)` substrings, and each palindrome check walks up to `O(n)` characters, giving `O(n^3)` in the worst case (for example, a string of identical characters where every check runs to completion).

##### Space Complexity: `O(1)`

Only a handful of integer indices are tracked. The returned substring is output, not auxiliary working space.

#### Key Insights

- Enumerating all substrings and verifying each one by hand needs no insight
  about palindrome structure, making it the most self-derivable approach.
- The length guard (`j - i + 1 > max_len`) prunes substrings that cannot beat the
  current best, a cheap optimization that does not change the asymptotic bound.
- The cubic cost comes from re-checking overlapping substrings from scratch; every
  later approach removes this redundancy by reusing already-verified work.

### Bottom-Up DP

#### Derivation

The Brute Force's cubic cost comes from a specific redundancy: verifying `s[i..j]` re-walks its interior `s[i+1..j-1]`, a span whose verdict an earlier, shorter check already established. Instead of discarding those verdicts, record them. Define `dp[i][j]` to be `True` when the substring `s[i..j]` (inclusive) is a palindrome. A substring is a palindrome exactly when its two ends match and the inside is already known to be a palindrome, which gives the [recurrence](https://en.wikipedia.org/wiki/Dynamic_programming):

`dp[i][j] = (s[i] == s[j]) and (j - i < 2 or dp[i + 1][j - 1])`

Because `dp[i][j]` depends on the shorter substring `dp[i + 1][j - 1]`, we fill the table in increasing order of substring length so every dependency is ready first.

1. Seed every single character as a palindrome (`dp[i][i] = True`).
2. For each `length` from 2 to `n`, scan all start indices `i` and set `j = i + length - 1`.
3. When `s[i] == s[j]` and either the span is length 2 or the inner substring is a
   palindrome, mark `dp[i][j]` and update the best `(start, max_len)` seen so far.
4. Return the recorded slice `s[start:start + max_len]`.

#### Recurrence

Let `dp[i][j]` be true when `s[i..j]` (inclusive) is a palindrome. Peeling one character off each end reduces the question to a shorter span:

$$ dp[i][j] = \begin{cases} \text{true}, & j - i < 2 \ \text{ and } \ s[i] = s[j] \\[4pt] \bigl(s[i] = s[j]\bigr) \wedge dp[i+1][j-1], & j - i \ge 2 \end{cases} $$

```text
dp[i][j] = True                                  for j - i < 2 and s[i] == s[j]
dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]   for j - i >= 2
```

The answer is the longest span with \(dp[i][j]\) true. Because the state at \((i, j)\) depends on \((i+1, j-1)\), a span two characters shorter, the table must be filled in increasing order of length rather than row by row, otherwise the dependency is not yet computed. Spans of length 1 and 2 have no inner substring, so they terminate the recursion on the character comparison alone.

#### Walkthrough

Let us fill the table on Example 1: `s = "babad"` (indices `0:b 1:a 2:b 3:a 4:d`). Seeding the diagonal marks every single character a palindrome and sets the starting best to `start = 0`, `max_len = 1`. The loops then try each `length` in increasing order, testing `s[i] == s[j]` first and consulting the inner cell only for spans of length 3 or more:

```text
length=2   (0,1) "ba"   b != a         (1,2) "ab"   a != b
           (2,3) "ba"   b != a         (3,4) "ad"   a != d
length=3   (0,2) "bab"  b == b, dp[1][1] True -> dp[0][2] = True, best = (0, 3)
           (1,3) "aba"  a == a, dp[2][2] True -> dp[1][3] = True, 3 not > 3
           (2,4) "bad"  b != d
length=4   (0,3) "baba" b != a         (1,4) "abad" a != d
length=5   (0,4) "babad" b != d
```

No length-2 span has matching ends, so every even-length palindrome is ruled out. At length 3, `dp[0][2]` becomes `True` because its ends match and the inner cell `dp[1][1]` is already `True`, updating the best to `(start, max_len) = (0, 3)`. The cell `dp[1][3]` (`"aba"`) also becomes `True` but only ties `max_len`, so the earlier find is kept. Every longer span fails its end comparison, leaving `s[0:3] = "bab"` as the returned slice, which matches the expected Output.

#### Solution

The code fills the table exactly as the walkthrough does: diagonal first, then increasing lengths.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s

        # dp[i][j] is True when the substring s[i..j] (inclusive) is a palindrome.
        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1

        # Base case: every single character is a palindrome.
        for i in range(n):
            dp[i][i] = True

        # Fill by increasing length, since dp[i][j] depends on dp[i+1][j-1].
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] != s[j]:
                    continue
                # Length-2 spans have no inner substring; longer ones defer to it.
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length > max_len:
                        start, max_len = i, length

        return s[start:start + max_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Filling the `n × n` table touches each `(i, j)` pair once with constant work per cell.

##### Space Complexity: `O(n^2)`

The `dp` table stores `n × n` boolean entries.

#### Key Insights

- The recurrence builds longer palindromes from shorter verified ones, the hallmark
  of dynamic programming.
- Iterating by substring length guarantees `dp[i + 1][j - 1]` is computed before
  `dp[i][j]` needs it.
- The length-2 base case (`j - i < 2`) covers adjacent equal characters that have no
  inner substring to consult.
- This trades `O(n^2)` space for an explicit, tabular view of which substrings are
  palindromes, useful when the full palindrome table is itself the goal.

### Expand Around Center

#### Derivation

The DP table spends `O(n^2)` memory recording a verdict for every substring, yet most of those verdicts are `False` and never help. Flip the question: instead of asking "is this substring a palindrome?", ask "how far does the palindrome around this center reach?". A palindrome mirrors around its center, and every palindromic substring has one, but that center is either a single character (odd length, like `"aba"`) or the gap between two characters (even length, like `"bb"`). There are `n` single-character centers and `n - 1` gap centers, so `2n - 1` centers in total.

The idea is to try every possible center and expand outward as long as the characters on both sides match, recording the longest palindrome seen.

1. Define a helper `expand(left, right)` that walks the [two pointers](https://usaco.guide/silver/two-pointers) outward
   while they stay in bounds and `s[left] == s[right]`.
2. When the loop stops, the pointers have overshot by one, so return
   `(left + 1, right - 1)` as the inclusive bounds of the matched palindrome.
3. For each index `i`, expand once with `(i, i)` for the odd case and once with
   `(i, i + 1)` for the even case.
4. Track the widest `(start, end)` window across all expansions using
   `r - l > end - start` as the comparison.
5. Return the slice `s[start:end + 1]`.

Comparing widths with `r - l` avoids recomputing lengths and naturally keeps the first-found palindrome when ties occur, which is acceptable since any longest palindromic substring is a valid answer.

#### Walkthrough

Let us expand every center on Example 1: `s = "babad"` (indices `0:b 1:a 2:b 3:a 4:d`). For each `i`, the odd expansion starts from `(i, i)` and the even expansion from `(i, i + 1)`; each grows while the flanking characters match and returns the inclusive bounds it reached. The best `(start, end)` updates whenever a wider window appears:

```text
i=0  expand(0, 0) -> (0, 0) "b"        expand(0, 1): b != a -> empty
                                       best (start, end) = (0, 0)
i=1  expand(1, 1): grows, b == b, then falls off the left edge -> (0, 2) "bab"
     expand(1, 2): a != b -> empty     best (start, end) = (0, 2)
i=2  expand(2, 2): grows, a == a, then b != d -> (1, 3) "aba"  ties, no update
     expand(2, 3): b != a -> empty     best (start, end) = (0, 2)
i=3  expand(3, 3) -> (3, 3) "a"        expand(3, 4): a != d -> empty
i=4  expand(4, 4) -> (4, 4) "d"        expand(4, 5): right out of bounds -> empty
```

The decisive expansion is the odd one at `i = 1`: it grows from `"a"` to `"bab"` and stops only when `left` falls off the string, returning bounds `(0, 2)`. The center at `i = 2` finds `"aba"`, but its width `r - l = 2` does not beat `end - start = 2`, so the first palindrome is kept. The final slice `s[0:3]` is `"bab"`, matching the expected Output.

#### Solution

The code is the walkthrough's two expansions per index, sharing one `expand` helper.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # Track the bounds of the best palindrome found so far
        start, end = 0, 0

        def expand(left: int, right: int) -> tuple[int, int]:
            # Grow outward while the characters keep matching
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Step back to the last valid (inclusive) bounds
            return left + 1, right - 1

        for i in range(len(s)):
            # Odd-length palindrome centered on a single character
            l1, r1 = expand(i, i)
            if r1 - l1 > end - start:
                start, end = l1, r1
            # Even-length palindrome centered between two characters
            l2, r2 = expand(i, i + 1)
            if r2 - l2 > end - start:
                start, end = l2, r2

        return s[start:end + 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

There are `2n - 1` centers, and each expansion can extend up to `O(n)` steps in the worst case (for example, a string of identical characters like `"aaaa"`). The product gives `O(n^2)`.

##### Space Complexity: `O(1)`

Only a constant number of integer pointers are used. The returned substring is output, not auxiliary working space, so the extra space is constant.

#### Key Insights

- Every palindrome is defined by its center, so iterating over `2n - 1` centers
  covers all palindromes without enumerating substrings explicitly.
- Handling odd and even lengths separately with `(i, i)` and `(i, i + 1)` is the
  clean way to capture both forms with one helper.
- Expanding outward stops the moment a mismatch appears, so most centers do far
  less than `O(n)` work in practice.
- Tracking bounds instead of the substring itself keeps each comparison `O(1)`
  and defers the single slice to the very end.

### Manacher's Algorithm

#### Derivation

Expand Around Center still wastes comparisons: when a center lies inside a long palindrome that has already been discovered, symmetry has predetermined part of its expansion, yet the expansion re-verifies those characters anyway. [Manacher's algorithm](https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher%27s_algorithm) achieves linear time by never re-examining characters it already knows to match. It first transforms the string so that odd- and even-length palindromes are handled uniformly, then reuses palindrome symmetry to give each new center a head start.

1. Transform `s` into `t` by inserting `#` between every character and wrapping
   it in `^` and `$` sentinels (for example `"aba"` becomes `"^#a#b#a#$"`). Now every palindrome in `t` is odd-length, and the distinct sentinels stop any expansion at the boundaries.
2. Keep `p[i]`, the radius of the palindrome centered at `i` in `t`, along with
   the `center`/`right` of the rightmost-reaching palindrome found so far.
3. For each `i`, find its `mirror = 2 * center - i`. If `i` lies inside the
   current palindrome (`i < right`), seed `p[i]` with `min(right - i, p[mirror])`, borrowing the mirror's work without overstepping the known right edge.
4. Expand from this seed while the characters straddling `i` still match. The
   sentinels guarantee the inner `while` halts without explicit bounds checks.
5. If the new palindrome extends past `right`, update `center` and `right`.
6. The largest radius is the answer's length; convert its center back to the
   original index with `start = (center_idx - max_radius) // 2`.

The radius in the transformed string equals the palindrome length in the original string, which is why `max_radius` doubles as both the length and the slice width.

#### Walkthrough

Let us run the scan on Example 1: `s = "babad"`, which transforms to `t = "^#b#a#b#a#d#$"` (indices 0 through 12). Each line below shows one center `i`: the seed borrowed from its mirror when `i < right`, the radius `p[i]` after expansion, and the `center`/`right` of the rightmost palindrome afterward:

```text
i=1  (#)  no seed    expansion fails at once      p[1]=0   center=1,  right=1
i=2  (b)  no seed    # == #, then ^ stops it      p[2]=1   center=2,  right=3
i=3  (#)  no seed    a != b                       p[3]=0
i=4  (a)  no seed    grows to #b#a#b#             p[4]=3   center=4,  right=7
i=5  (#)  mirror=3   seed min(7-5, p[3]=0) = 0    b != a   p[5]=0
i=6  (b)  mirror=2   seed min(7-6, p[2]=1) = 1    grows: a == a, # == #,
                     then d != b                  p[6]=3   center=6,  right=9
i=7  (#)  mirror=5   seed min(9-7, p[5]=0) = 0    a != b   p[7]=0
i=8  (a)  mirror=4   seed min(9-8, p[4]=3) = 1    d != b   p[8]=1
i=9  (#)  no seed    d != a                       p[9]=0
i=10 (d)  no seed    # == #, then $ stops it      p[10]=1  center=10, right=11
i=11 (#)  no seed    $ != d                       p[11]=0
```

The interesting move is `i = 6`: it lies inside the palindrome around `center = 4` (whose `right` edge is `7`), so its mirror `2 * 4 - 6 = 2` contributes `p[2] = 1` for free, and expansion resumes from radius 1 instead of
0. The seed at `i = 8` shows the other clamp: its mirror's radius 3 exceeds
`right - i = 1`, so only 1 may be borrowed, since nothing beyond `right` has been examined yet.

The final radius array is `p = [0, 0, 1, 0, 3, 0, 3, 0, 1, 0, 1, 0, 0]`, so `max_radius = 3`, first reached at `center_idx = 4`. Converting back to the original string, `start = (4 - 3) // 2 = 0`, and the radius doubles as the length, giving `s[0:3] = "bab"`: the expected Output.

#### Solution

The code is the walkthrough's scan: seed from the mirror, expand, and advance `center`/`right` when the new palindrome reaches further.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        # Transform "abc" into "^#a#b#c#$": the interleaved '#' makes every
        # palindrome odd-length, and the '^'/'$' sentinels never match each
        # other so expansion stops at the boundaries without index checks.
        t = "^#" + "#".join(s) + "#$"
        n = len(t)

        # p[i] is the radius of the palindrome centered at i in the transformed
        # string; that radius equals the length of the corresponding palindrome
        # in the original string.
        p = [0] * n

        # center/right describe the rightmost-reaching palindrome found so far.
        center, right = 0, 0
        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                # Reuse the mirror's radius, but never claim more than what the
                # current palindrome already guarantees up to its right edge.
                p[i] = min(right - i, p[mirror])
            # Attempt to grow past the reused portion.
            while t[i + p[i] + 1] == t[i - p[i] - 1]:
                p[i] += 1
            if i + p[i] > right:
                center, right = i, i + p[i]

        max_radius = max(p)
        center_idx = p.index(max_radius)
        start = (center_idx - max_radius) // 2
        return s[start:start + max_radius]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The transformed string has length `2n + 3`. The `right` boundary only ever moves forward, and each inner expansion step advances it, so across the whole run the total expansion work is bounded by `O(n)`.

##### Space Complexity: `O(n)`

The transformed string `t` and the radius array `p` each hold `O(n)` entries.

#### Key Insights

- Interleaving `#` characters removes the odd/even special-casing that the other
  approaches handle with two separate expansions per center.
- The mirror trick reuses already-computed radii so that characters inside the
  current rightmost palindrome are never compared twice.
- The `^` and `$` sentinels make the expansion loop boundary-safe, eliminating
  index range checks entirely.
- The radius in the padded string maps directly to the substring length, so the
  final slice falls out of a single index computation.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^3)` - `O(n^2)` substrings, each checked in up to `O(n)`.
- **Bottom-Up DP**: `O(n^2)` - fills every `(i, j)` cell once.
- **Expand Around Center**: `O(n^2)` - `2n - 1` centers, each expanding up to `O(n)`.
- **Manacher's Algorithm**: `O(n)` - the right boundary only moves forward, bounding total work.

### Space Complexity

- **Brute Force**: `O(1)` - only a few integer indices.
- **Bottom-Up DP**: `O(n^2)` - the full boolean substring table.
- **Expand Around Center**: `O(1)` - only a few integer pointers.
- **Manacher's Algorithm**: `O(n)` - the padded string and the radius array.

### Trade-offs

- The Brute Force approach is the simplest to derive, checking every substring
  directly, but pays a cubic price by re-verifying overlapping substrings from scratch.
- The Bottom-Up DP approach makes the palindrome relationships explicit in a
  table that is straightforward to reason about, at the cost of quadratic memory.
- The Expand Around Center approach matches the time bound with constant space and
  often stops early on most centers, though its center-expansion invariant is a little less obvious than a filled table.
- Manacher's Algorithm reaches the optimal `O(n)` time but pays for it in
  conceptual complexity: the string transform, mirror reuse, and index back-conversion are easy to get subtly wrong under interview pressure.

### When to Use Each

- **Brute Force**: As a baseline to confirm correctness, or when `n` is tiny and
  clarity outweighs efficiency.
- **Bottom-Up DP**: When the tabular formulation is clearer to derive, or when
  the palindrome table itself is needed for a related subproblem.
- **Expand Around Center**: For the best space usage and the simplest fast solution in
  practice; the recommended interview answer.
- **Manacher's Algorithm**: When `O(n)` time is genuinely required on very large
  inputs and the extra implementation cost is justified.

### Optimization Notes

- Brute Force drops a full factor of `n` by moving from re-checking every substring
  to either of the `O(n^2)` approaches, which reuse already-verified palindromes.
- Bottom-Up DP and Expand Around Center share the `O(n^2)` time floor; the difference
  is purely `O(n^2)` versus `O(1)` space.
- Expand Around Center stops each expansion at the first mismatch, so it usually does
  less than the worst-case work, whereas the table always does the full `O(n^2)`.
- Manacher's Algorithm is the only sub-quadratic option here; its `#`-padding trick
  also unifies the odd/even cases that the other approaches handle separately.
