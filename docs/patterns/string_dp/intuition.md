# String DP - Intuition Guide

**Reference:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

## The Mental Model: Filling a Grid

Imagine you have two strings written along the edges of a grid:
- First string `s` along the rows (top to bottom)
- Second string `t` along the columns (left to right)

Each cell `(i, j)` represents the answer for comparing `s[0:i]` with `t[0:j]`.

```
        ""  a   b   c
    ┌───┬───┬───┬───┐
""  │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┤
a   │ 0 │ 1 │ 1 │ 1 │
    ├───┼───┼───┼───┤
c   │ 0 │ 1 │ 1 │ 2 │
    └───┴───┴───┴───┘
```

You fill this grid row by row, and each cell only needs its neighbors:
- Diagonal (top-left): both strings shrink
- Up: first string shrinks
- Left: second string shrinks

## Why String DP?

String DP works because string comparison has **optimal substructure**:
- The best answer for long strings depends only on answers for shorter strings
- We can systematically build from empty strings to full strings

## Core Insight

The transition depends on whether current characters match:

```
Match:      s[i-1] == t[j-1]
            → Look diagonal (both consumed)

Mismatch:   s[i-1] != t[j-1]
            → Look up, left, or diagonal (try all options)
```

## Pattern 1: LCS (Longest Common Subsequence)

**The insight**: If characters match, include them. If not, try skipping either character.

```
s = "ace", t = "abcde"

        ""  a   b   c   d   e
    ┌───┬───┬───┬───┬───┬───┐
""  │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┼───┼───┤
a   │ 0 │ 1 │ 1 │ 1 │ 1 │ 1 │  a=a: +1
    ├───┼───┼───┼───┼───┼───┤
c   │ 0 │ 1 │ 1 │ 2 │ 2 │ 2 │  c=c: +1
    ├───┼───┼───┼───┼───┼───┤
e   │ 0 │ 1 │ 1 │ 2 │ 2 │ 3 │  e=e: +1
    └───┴───┴───┴───┴───┴───┘
                        └── Answer: 3
```

The code:
```python
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1  # Include this character
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Skip one char
```

## Pattern 2: Edit Distance

**The insight**: Each cell is the minimum edits to transform. Three operations mean three choices.

```
s = "horse", t = "ros"

        ""  r   o   s
    ┌───┬───┬───┬───┐
""  │ 0 │ 1 │ 2 │ 3 │  Insert all
    ├───┼───┼───┼───┤
h   │ 1 │ 1 │ 2 │ 3 │  h≠r: min(replace, delete, insert)
    ├───┼───┼───┼───┤
o   │ 2 │ 2 │ 1 │ 2 │  o=o: diagonal (no cost)
    ├───┼───┼───┼───┤
r   │ 3 │ 2 │ 2 │ 2 │  r≠s: +1
    ├───┼───┼───┼───┤
s   │ 4 │ 3 │ 3 │ 2 │  s=s: diagonal
    ├───┼───┼───┼───┤
e   │ 5 │ 4 │ 4 │ 3 │  Answer: 3
    └───┴───┴───┴───┘
```

The code:
```python
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1]  # No operation needed
else:
    dp[i][j] = 1 + min(
        dp[i-1][j-1],  # Replace s[i-1] with t[j-1]
        dp[i-1][j],    # Delete s[i-1]
        dp[i][j-1]     # Insert t[j-1]
    )
```

## Pattern 3: Palindrome Subsequence

**The insight**: A palindrome reads the same forwards and backwards.

The LPS of string `s` = LCS of `s` and `reverse(s)`.

```
s = "bbbab"
t = "babbb" (reversed)

LCS = "bbbb" (length 4)
```

Why does this work? The length identity `LPS(s) = |LCS(s, reverse(s))|` holds: every palindromic subsequence of `s` is a common subsequence of `s` and its reverse, and one can show the longest common subsequence always has palindromic length. Note the claim is about lengths only: not every common subsequence is itself a palindrome (in `s = "abab"`, `"ab"` is common to both directions yet not a palindrome).

### The Substring Variant: Longest Palindromic Substring

**The insight**: A substring must be contiguous, so LCS-with-reverse no longer applies. Compare the two ends of an interval instead: `s[i..j]` is a palindrome exactly when its endpoints match and the inside is already a palindrome.

```python
# Interval DP: dp[i][j] = True if s[i..j] is a palindrome
dp[i][j] = s[i] == s[j] and (length <= 2 or dp[i+1][j-1])
```

Each cell depends on the shorter interval inside it, so fill by **increasing length**: all single characters first, then pairs, then longer spans.

```
s = "babad"

         b     a     b     a     d
       ┌─────┬─────┬─────┬─────┬─────┐
b      │  T  │  .  │  T  │  .  │  .  │   dp[0][2]: 'b'=='b' and dp[1][1] → "bab"
       ├─────┼─────┼─────┼─────┼─────┤
a      │     │  T  │  .  │  T  │  .  │   dp[1][3]: 'a'=='a' and dp[2][2] → "aba"
       ├─────┼─────┼─────┼─────┼─────┤
b      │     │     │  T  │  .  │  .  │
       ├─────┼─────┼─────┼─────┼─────┤
a      │     │     │     │  T  │  .  │
       ├─────┼─────┼─────┼─────┼─────┤
d      │     │     │     │     │  T  │
       └─────┴─────┴─────┴─────┴─────┘

Longest True cell: dp[0][2] → answer "bab" (length 3)
```

The fill loop, tracking the longest True cell:

```python
for length in range(1, n + 1):          # shorter intervals first
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j] and (length <= 2 or dp[i+1][j-1]):
            dp[i][j] = True             # record (i, j) if longest so far
```

This is O(n²) time and O(n²) space. Expand-around-center achieves the same O(n²) time in O(1) space by growing outward from each of the 2n-1 centers.

## Pattern 4: Regex Matching

**The insight**: Handle `*` by considering "use it" vs "skip it".

```
s = "aab", p = "c*a*b"

c*  → 0 or more 'c' (we use 0)
a*  → 0 or more 'a' (we use 2)
b   → exactly 'b' (we use 1)

Result: MATCH
```

The tricky part is `*`:
```python
if p[j-1] == '*':
    # Option 1: Use zero of p[j-2]
    dp[i][j] = dp[i][j-2]

    # Option 2: Use one or more of p[j-2]
    if p[j-2] == '.' or p[j-2] == s[i-1]:
        dp[i][j] = dp[i][j] or dp[i-1][j]
```

## Common Mistakes

### Mistake 1: Off-by-one indexing

```python
# ❌ Wrong: dp indices and string indices are off by 1
if s[i] == t[j]:

# ✅ Right: dp[i][j] corresponds to s[0:i], so character is s[i-1]
if s[i-1] == t[j-1]:
```

### Mistake 2: Wrong base cases for Edit Distance

```python
# ❌ Wrong: Forgetting base cases
dp = [[0] * (n+1) for _ in range(m+1)]

# ✅ Right: Empty string requires i deletions or j insertions
for i in range(m+1):
    dp[i][0] = i
for j in range(n+1):
    dp[0][j] = j
```

### Mistake 3: Regex `*` looks at wrong index

```python
# ❌ Wrong: Looking at j-1 for the character before *
if p[j-1] == s[i-1]:

# ✅ Right: * is at j-1, so the character is at j-2
if p[j-2] == s[i-1]:
```

## Corner Cases

- One or both strings empty: the zero row and column are the base cases; edit distance is the other length, LCS is 0
- Identical strings: the diagonal alone; LCS is the full length and edit distance is zero
- No shared characters: LCS is 0; every cell comes from skip moves
- Single-character strings: the smallest grid that still exercises both match and mismatch paths
- All-one-character strings ("bbbb"): every substring is a palindrome; keep scanning for the longest True instead of stopping at the first
- Palindrome spans of length 1 and 2: the length <= 2 short-circuit is what seeds the interval fill
- Regex on an empty string or a pattern like "c*a*b": zero-use of each star must be explored, and the j-2 lookback assumes a character exists before the star

## Practice Progression

Build string DP skill through this sequence:

1. **[Longest Common Subsequence](../../problems/longest_common_subsequence.md)**: the canonical two-string grid. Match means diagonal plus one; mismatch means the best of skipping either character.

2. **[Longest Palindromic Substring](../../problems/longest_palindromic_substring.md)**: one string against itself, as interval DP. Endpoints match and the inside is a palindrome; fill by increasing length.

3. **Longest Palindromic Subsequence** (LC 516): reuse LCS by comparing the string with its own reverse.

4. **[Edit Distance](../../problems/edit_distance.md)**: three operations become three neighbor cells; take the minimum and add one.

5. **[Regular Expression Matching](../../problems/regular_expression_matching.md)**: the hardest transition. Each `*` branches into "use zero" and "use one more" of the preceding character.

## Quick Pattern Recognition

| Clue | Pattern |
|------|---------|
| "longest common subsequence" | LCS |
| "minimum operations to convert" | Edit Distance |
| "palindrome subsequence" | LCS with reverse |
| "palindromic substring" | Interval DP or expand-around-center |
| "match pattern with . or *" | Regex DP |
| "delete operation for two strings" | LCS-based |

## Visual Summary

```
String DP: Compare s[0:i] with t[0:j]

           ┌─────────────┐
           │ dp[i-1][j-1]│───► Match: usually this
           └──────┬──────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌─────────────┐  ┌────────┐
│dp[i-1] │  │  dp[i][j]   │  │dp[i]   │
│  [j]   │  │  (current)  │  │ [j-1]  │
└────────┘  └─────────────┘  └────────┘
Delete s[i]                  Insert t[j]
    │                             │
    └──────────┬──────────────────┘
               │
               ▼
         Mismatch: combine
         these options
```
