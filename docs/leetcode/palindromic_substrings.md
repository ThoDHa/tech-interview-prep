# [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)

**Medium** | **25 minutes** | **Two Pointers, String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Manacher's algorithm](https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher%27s_algorithm)

**Practice:** [`practice/palindromic_substrings/solution.py`](../../practice/palindromic_substrings/solution.py)

Given a string `s`, return the number of substrings within `s` that are palindromes.

A **palindrome** is a string that reads the same forward and backward.

## Examples

### Example 1

**Input:** `s = "abc"`

**Output:** `3`

**Explanation:** "a", "b", "c".

### Example 2

**Input:** `s = "aaa"`

**Output:** `6`

**Explanation:** "a", "a", "a", "aa", "aa", "aaa". Note that different substrings are counted as different palindromes even if the string contents are the same.

## Constraints

- `1 <= s.length <= 1000`
- `s` consists of lowercase English letters.

## Deriving the Solution

Every palindrome mirrors around a center, and its length is fixed by how far that mirror reaches before a pair of characters disagrees. The solutions below ask about palindromes at ever coarser granularity: each substring on its own, verdicts shared between overlapping spans, centers instead of spans, and finally symmetry shared between centers.

1. **Start literal.** Enumerate every substring `s[i..j]` and verify each with
   an inward two-pointer walk. `O(n^2)` spans at `O(n)` per check costs
   `O(n^3)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Verifying `s[i..j]` re-walks its interior
   `s[i+1..j-1]`, a span some shorter check already settled. Record every
   verdict in a table: `s[i..j]` is a palindrome exactly when its ends match
   and its inside is one, so each cell costs `O(1)` and counting the `True`
   cells answers the problem in `O(n^2)` time: see [Bottom-Up DP](#bottom-up-dp).
3. **Grow from centers.** A table stores a verdict for every span, but the
   problem only asks for a count. Every palindromic substring is identified by
   its center, and only `2n - 1` centers exist (`n` characters plus `n - 1`
   gaps). Expanding each center outward confirms one palindrome per successful
   comparison and stops at the first mismatch, visiting none of the doomed
   spans, which keeps `O(n^2)` time and drops the space to `O(1)`: see
   [Expand Around Center](#expand-around-center).
4. **Reuse across centers.** Expansion still re-compares characters that lie
   inside an already-discovered palindrome, where symmetry has predetermined
   them. Seeding each new center with its mirror's radius means no character
   comparison is wasted, reaching `O(n)`: see
   [Manacher's Algorithm](#manachers-algorithm).

## Solutions

### Brute Force

#### Derivation

The most direct reading treats every substring as its own yes/no question: is `s[i..j]` a palindrome? The check needs no insight about palindrome structure, only an inward walk comparing mirrored characters, and the problem's answer is how many questions come back yes.

1. For each start index `i`, consider every end index `j >= i`, covering all
   `O(n^2)` substrings.
2. Check `s[i..j]` with `is_palindrome`, which compares `s[left]` and
   `s[right]` while walking the two pointers toward the middle.
3. Increment `count` for every span that passes.
4. Return `count`.

#### Walkthrough

Trace the Brute Force on Example 2: `s = "aaa"` (indices `0:a 1:a 2:a`). Every span is checked and counted, left to right by start index:

| Step | `i`, `j` | substring | check | palindrome? | `count` after |
|------|----------|-----------|-------|-------------|---------------|
| 1 | `0, 0` | `"a"` | single character | yes | `1` |
| 2 | `0, 1` | `"aa"` | `s[0] == s[1]` | yes | `2` |
| 3 | `0, 2` | `"aaa"` | `s[0] == s[2]` | yes | `3` |
| 4 | `1, 1` | `"a"` | single character | yes | `4` |
| 5 | `1, 2` | `"aa"` | `s[1] == s[2]` | yes | `5` |
| 6 | `2, 2` | `"a"` | single character | yes | `6` |

All six spans pass, so `count` reads `6`, matching the expected Output for Example 2. Identical characters are this approach's worst case: every check walks all the way to its middle, which is why the cubic bound below is real on plausible inputs rather than an adversarial corner.

#### Solution

The code is the walkthrough's double loop with the inward walk as its check.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)

        def is_palindrome(left: int, right: int) -> bool:
            # Walk inward from both ends, comparing mirrored characters.
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        count = 0
        # Try every substring s[i..j] and count the palindromes.
        for i in range(n):
            for j in range(i, n):
                if is_palindrome(i, j):
                    count += 1
        return count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

There are `O(n^2)` substrings and each palindrome check walks up to `O(n)` characters inward. The bound is tight: on a string of identical characters every check runs to completion.

##### Space Complexity: `O(1)`

Only the loop indices are tracked; the check itself allocates nothing.

#### Key Insights

- This problem is a counting variant of the longest-palindromic-substring question: the same enumeration and the same check apply, with the best-so-far bookkeeping replaced by a counter.
- The check needs no insight about palindrome structure, which makes this the most self-derivable approach and a natural correctness oracle for the faster ones.
- The cubic cost comes from re-walking overlapping substrings from scratch; every later approach reuses work an earlier, shorter check already did.

### Bottom-Up DP

#### Derivation

The Brute Force re-walks the interior of nearly every span it checks, yet the verdict on `s[i+1..j-1]` was established by an earlier, shorter check and then thrown away. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) keeps those verdicts: `dp[i][j]` records whether `s[i..j]` is a palindrome, and a span extends a shorter one exactly when its ends match and its inside is already verified. The problem's answer is the number of `True` cells:

1. Seed every single character as a palindrome (`dp[i][i] = True`), counting
   `n` of them.
2. For each `length` from 2 to `n`, scan all start indices `i` and set
   `j = i + length - 1`.
3. When `s[i] == s[j]` and either the span has length 2 or `dp[i + 1][j - 1]`
   is `True`, mark `dp[i][j]` and increment `count`.
4. Return `count`.

Because `dp[i][j]` depends on the span two characters shorter, filling in increasing order of length guarantees every interior verdict is ready before it is consulted.

#### Recurrence

Let `dp[i][j]` be true when `s[i..j]` (inclusive) is a palindrome. Peeling one character off each end reduces the question to a shorter span:

$$ dp[i][j] = \begin{cases} \text{true}, & j - i < 2 \ \text{ and } \ s[i] = s[j] \\[4pt] \bigl(s[i] = s[j]\bigr) \wedge dp[i+1][j-1], & j - i \ge 2 \end{cases} $$

```text
dp[i][j] = True                                  for j - i < 2 and s[i] == s[j]
dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]   for j - i >= 2
```

Spans of length 1 and 2 have no inner substring, so they terminate on the character comparison alone. Each `True` cell is one palindromic substring, so the answer is the number of cells the recurrence sets, read out of `count` as the table fills.

#### Walkthrough

Let us fill the table on Example 2: `s = "aaa"` (indices `0:a 1:a 2:a`). The diagonal seeds three single-character palindromes, then each length sweep extends spans whose ends match and whose interior is already `True`:

```text
length=1   (0,0) True   (1,1) True   (2,2) True          count = 3
length=2   (0,1) "aa"   a == a -> True                   count = 4
           (1,2) "aa"   a == a -> True                   count = 5
length=3   (0,2) "aaa"  a == a, dp[1][1] True -> True    count = 6
```

The length-3 cell is the recurrence in action: its ends match and `dp[1][1]`, the single-character interior, was set `True` on the diagonal. The counter reads `6`, matching the expected Output for Example 2.

#### Solution

The code fills the table exactly as the walkthrough does: diagonal first, then increasing lengths, counting each `True` cell as it is set.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # dp[i][j] is True when the substring s[i..j] (inclusive) is a palindrome.
        dp = [[False] * n for _ in range(n)]
        count = 0

        # Base case: every single character is a palindrome.
        for i in range(n):
            dp[i][i] = True
            count += 1

        # Fill by increasing length, since dp[i][j] depends on dp[i+1][j-1].
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] != s[j]:
                    continue
                # Length-2 spans have no inner substring; longer ones defer to it.
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    count += 1

        return count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Filling the `n × n` table touches each `(i, j)` pair once with constant work per cell.

##### Space Complexity: `O(n^2)`

The `dp` table stores `n × n` boolean entries, all to produce a single number.

#### Key Insights

- The table is the same one Longest Palindromic Substring fills; only the accumulation changes, from the longest `True` span to the number of them.
- Iterating by substring length guarantees `dp[i + 1][j - 1]` is computed before `dp[i][j]` needs it.
- The table records every palindromic span explicitly, which earns its keep only when the full palindrome structure is queried again; for this problem it is `O(n^2)` memory spent on one integer.

### Expand Around Center

#### Derivation

The DP table pays `O(n^2)` memory to record a verdict for every span, yet the problem asks only how many spans qualify. Flip the question: instead of "is this span a palindrome?", ask "how many palindromes grow from this center?". Every palindromic substring mirrors around a center, which is either a single character (odd length, like `"aba"`) or the gap between two characters (even length, like `"bb"`); there are `n` character centers and `n - 1` gap centers, so `2n - 1` in total. Expanding a center outward, every successful mirror comparison confirms exactly one more palindromic substring, and the first mismatch ends that center's crop, so no doomed span is ever visited:

1. Define a helper `expand(left, right)` that counts one palindrome per
   iteration while the pointers stay in bounds and `s[left] == s[right]`,
   stepping both outward, then returns the tally.
2. For each index `i`, expand once from `(i, i)` for odd-length palindromes
   and once from `(i, i + 1)` for even-length palindromes.
3. Add both tallies into `total`.
4. Return `total`.

#### Walkthrough

Let us expand every center on Example 2: `s = "aaa"` (indices `0:a 1:a 2:a`). Each line is one expansion; the subtotal is what it added to `total`:

```text
i=0  expand(0, 0): s[0] == s[0] -> 1, then left out of bounds
     expand(0, 1): s[0] == s[1] -> 1, then right out of bounds   running 2
i=1  expand(1, 1): s[1] == s[1] -> 1, s[0] == s[2] -> 2
     expand(1, 2): s[1] == s[2] -> 1, then right out of bounds   running 5
i=2  expand(2, 2): s[2] == s[2] -> 1, then right out of bounds
     expand(2, 3): right starts out of bounds -> 0               running 6
```

The center at `i = 1` is the revealing one: its odd expansion survives two radii, confirming `"a"` and then `"aaa"`, and its even expansion confirms the `"aa"` spanning indices `1` and `2`, three palindromes from one position. The total reads `2 + 3 + 1 = 6`, matching the expected Output for Example 2. Example 1 (`s = "abc"`) is the opposite shape: every expansion confirms only its center character and every gap expansion fails immediately, giving `1 + 1 + 1 = 3`.

#### Solution

The code is the walkthrough's two expansions per index, each successful comparison worth one palindrome.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)

        def expand(left: int, right: int) -> int:
            # Each successful comparison confirms one palindromic substring
            # centered on this pair of pointers.
            count = 0
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
            return count

        total = 0
        for i in range(n):
            # Odd-length palindromes centered on the character at i.
            total += expand(i, i)
            # Even-length palindromes centered on the gap after i.
            total += expand(i, i + 1)
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

There are `2n - 1` centers and each expansion walks at most `O(n)` steps before leaving the string or hitting a mismatch (a string of identical characters reaches the full walk). The product gives `O(n^2)`, but mismatching centers stop after one comparison, so typical inputs do far less work than the table version.

##### Space Complexity: `O(1)`

Only the pointers and the two counters; no table survives the call.

#### Key Insights

- Counting is the formulation expand-around-center was built for: each successful outward step is itself one palindromic substring, so the answer needs no bookkeeping beyond a counter.
- The `(i, i)` and `(i, i + 1)` expansions fold both parities into one helper; no length guard is needed anywhere, since a single-character string expands once from `(0, 0)` and never from `(0, 1)`.
- This dominates the Bottom-Up DP for this problem: the same `O(n^2)` time bound with constant space and early-exit centers.

### Manacher's Algorithm

#### Derivation

Expand Around Center still re-compares characters that lie inside a palindrome already found: when a new center sits within a long known palindrome, symmetry has already fixed part of its expansion, yet the loop verifies those pairs again. [Manacher's algorithm](https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher%27s_algorithm) removes the waste by giving each new center its mirror's radius as a seed, so every character comparison either pushes the known frontier forward or is answered outright.

1. Transform `s` into `t` by inserting `#` between every character and wrapping
   it in `^` and `$` sentinels (for example `"aba"` becomes `"^#a#b#a#$"`), so
   every palindrome in `t` is odd-length and the sentinels stop any expansion
   without bounds checks.
2. Keep `p[i]`, the radius of the palindrome centered at `i` in `t`, along with
   the `center`/`right` of the rightmost-reaching palindrome found so far.
3. For each `i`, find its `mirror = 2 * center - i`. If `i` lies inside the
   current palindrome (`i < right`), seed `p[i]` with `min(right - i, p[mirror])`.
4. Expand from the seed while the characters straddling `i` still match.
5. If the new palindrome extends past `right`, update `center` and `right`.
6. A radius-`r` palindrome in `t` nests exactly `(r + 1) // 2` palindromic
   substrings of `s` (one per layer, lengths `1..r` stepping by 2 around a
   letter center, `2..r` around a `#` center), so the answer is
   `sum((p[i] + 1) // 2)`.

#### Walkthrough

Let us run the scan on Example 2: `s = "aaa"`, which transforms to `t = "^#a#a#a#$"` (indices 0 through 8). Each line shows one center `i`: the seed borrowed from its mirror when `i < right`, the radius `p[i]` after expansion, and the `center`/`right` of the rightmost palindrome afterward:

```text
i=1  (#)  no seed    expansion fails at once      p[1]=0   center=1,  right=1
i=2  (a)  no seed    # == #, then ^ stops it      p[2]=1   center=2,  right=3
i=3  (#)  no seed    a == a, # == #, then ^       p[3]=2   center=3,  right=5
i=4  (a)  mirror=2   seed min(5-4, p[2]=1) = 1    grows: a == a, # == #,
                      then $ != ^                  p[4]=3   center=4,  right=7
i=5  (#)  mirror=3   seed min(7-5, p[3]=2) = 2    $ != a   p[5]=2
i=6  (a)  mirror=2   seed min(7-6, p[2]=1) = 1    $ != a   p[6]=1
i=7  (#)  no seed    $ != a                       p[7]=0
```

The decisive move is `i = 4`: it lies inside the palindrome around `center = 3` (whose right edge is `5`), borrows its mirror's radius `1`, which already certifies the `# == #` pair straddling it, and grows from there to `3`, spending fresh comparisons only outside the seed (`a == a`, then the outer `# == #`). The centers `i = 5` and `i = 6` borrow from their mirrors too, but they sit at that palindrome's right edge, where the seed already reaches the `$` boundary and every further comparison fails at once; their radii come entirely from the borrowed work.

The radius array is `p = [0, 0, 1, 2, 3, 2, 1, 0, 0]`, and the per-center counts `(p[i] + 1) // 2` are `1` (the `"a"` at `i=2`), `1` (`"aa"` at `i=3`), `2` (`"a"` and `"aaa"` at `i=4`), `1` (`"aa"` at `i=5`), and `1` (`"a"` at `i=6`), summing to `6`, the expected Output for Example 2.

#### Solution

The code is the walkthrough's scan: seed from the mirror, expand, advance `center`/`right`, then convert radii to the count.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        # Transform "aaa" into "^#a#a#a#$": the interleaved '#' makes every
        # palindrome odd-length, and the '^'/'$' sentinels never match each
        # other so expansion stops at the boundaries without index checks.
        t = "^#" + "#".join(s) + "#$"
        n = len(t)

        # p[i] is the radius of the palindrome centered at i in the transformed
        # string; each radius nests (p[i] + 1) // 2 palindromic substrings of s.
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

        return sum((radius + 1) // 2 for radius in p)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The transformed string's length is `2n + 3` for an original length `n`. The `right` boundary only ever moves forward, and every inner expansion step pushes it forward, so across the whole run the total expansion work is bounded by `O(n)`.

##### Space Complexity: `O(n)`

The transformed string `t` and the radius array `p` each hold `O(n)` entries.

#### Key Insights

- The mirror seed is the whole speedup: a center inside a known palindrome inherits everything symmetry has already proven, and pays only for genuinely new comparisons.
- The counting twist is free: instead of converting one maximal radius back to a substring slice, the radii sum through `(p[i] + 1) // 2`, one palindrome per nested layer.
- The `min(right - i, p[mirror])` clamp is what keeps the reuse honest: the mirror's radius is only certified inside the current palindrome's right edge.
- The added conceptual weight (transform, mirrors, clamps) buys a factor of `n`, which matters only near the constraint cap of 1000 characters.

## Comparison of Solutions

The practice harness's `practice/palindromic_substrings/reference.py` implements the **Expand Around Center** solution.

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

- The Brute Force is the direct transcription of the definition and the easiest to trust, but it pays a cubic price re-walking overlapping spans, which identical-character inputs make painfully real.
- The Bottom-Up DP reuses interior verdicts to reach `O(n^2)` time, at the cost of an `O(n^2)` table that this problem never reads again.
- The Expand Around Center matches the DP's time bound with constant space and stops most centers early, at the price of an odd/even center distinction the table handles implicitly.
- Manacher's Algorithm reaches linear time but carries the transform, mirror seeding, and clamping, the easiest machinery in the file to get subtly wrong under pressure.

### When to Use Each

- **Brute Force**: As the derivational baseline and a correctness oracle for checking the faster versions on small strings.
- **Bottom-Up DP**: When the full palindrome table is itself needed by a follow-up query, or when the tabular formulation is the one you can derive confidently.
- **Expand Around Center** (recommended): The default answer; the same quadratic bound at constant space, with counting falling out of the expansion for free.
- **Manacher's Algorithm**: When the input sits near the constraint cap and the linear bound genuinely matters, or when the interviewer asks to beat `O(n^2)`.

### Optimization Notes

- The Brute Force drops a full factor of `n` by moving to either of the `O(n^2)` approaches, which reuse already-verified palindrome structure instead of re-walking it.
- Bottom-Up DP and Expand Around Center share the `O(n^2)` time floor; the difference is purely the `O(n^2)` table versus `O(1)` counters, plus the center version's early exits on mismatching centers.
- The radius-to-count conversion `(p[i] + 1) // 2` is what turns Manacher's longest-palindrome machinery into a counter: each nested layer of a transformed palindrome strips to one distinct palindromic substring of the original.
- This problem is the counting twin of Longest Palindromic Substring: the same center expansion appears there tracking the widest window instead of a tally, and the same DP table appears there keeping the longest `True` span.
