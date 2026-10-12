# [Lexicographically Smallest After One Substring Rotation](https://www.fastprep.io/problems/amazon-lexicographically-smallest-after-one-substring-rotation)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given a string s. You must choose one non-empty contiguous substring of s and rotate that substring to the right by one position exactly once.

Rotating a substring to the right by one position moves its last character to the front of that substring, while every other character in the substring shifts one position to the right.

Return the lexicographically smallest string that can be obtained after performing the operation.

## Examples

### Example 1

**Input:** `s = "baca"`

**Output:** `"abac"`

**Explanation:** Choose the whole string baca. Rotating it right by one position moves the last character to the front, giving abac, which is the lexicographically smallest result obtainable.

### Example 2

**Input:** `s = "cba"`

**Output:** `"acb"`

**Explanation:** Choose the whole string "cba". Rotating it right gives "acb", which is the smallest possible result.

## Constraints

- `s is non-empty.`
- `The operation must be performed exactly once. Choosing a substring of length 1 leaves the string unchanged.`

## Solutions

### Rotate Every Substring

#### Derivation

The operation picks a substring `[left..right]` and moves its last character to the front of that substring. The baseline tries all `n(n+1)/2` substrings, builds each result, and keeps the lexicographically smallest:

1. For every `(left, right)` pair, construct the rotated string.
2. Track the minimum.

#### Walkthrough

Example 1, `s = "baca"`: rotating the whole string moves `a` (the last character) to the front, giving `"abac"`; every shorter substring either leaves the leading `b` in place or moves a no-smaller character forward, so `"abac"` wins, matching the expected output. Example 2, `s = "cba"`: the whole-string rotation gives `"acb"`, and no other rotation beats it (moving `a` anywhere earlier requires the whole-string window).

#### Solution

```python
from typing import List, Tuple


class Solution:
    def solve(self, s: List[str]) -> str:
        """Return the lexicographically smallest one-rotation result.

        Time:  O(n^3): O(n^2) substrings, each rebuild costing O(n).
        Space: O(n) per candidate.
        """
        text = s if isinstance(s, str) else "".join(s)
        best = text
        length = len(text)
        for left in range(length):
            for right in range(left, length):
                candidate = (
                    text[:left] + text[right] + text[left:right] + text[right + 1 :]
                )
                if candidate < best:
                    best = candidate
            if best < text[:1] + chr(0):
                break
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

Quadratic substring count with a linear string build each.

##### Space Complexity: `O(n)`

One candidate at a time.

#### Key Insights

- A rotation can only improve the string when the moved character is strictly smaller than the character it lands before.
- The best window always ends at a position whose character beats the window's head.

### Pruned Scan Over Improvement Points

#### Derivation

Two prunings collapse the search. First, a rotation of `[left..right]` changes the string only at positions `left` and `left + 1..right` (shifted right), so it can beat the original only if `s[right] < s[left]`: the moved character must strictly improve the position it lands on. Second, among windows sharing the same `left`, the improvement is decided by the pair `(s[right], s[left])` compared lexicographically against the original prefix there, so scanning rights in increasing order of character (and taking the longest run when equal characters tie) suffices. The pruned scan still visits all `(left, right)` pairs in the worst case but skips the build whenever `s[right] >= s[left]`, which in practice eliminates most of the cube:

1. For each `left`, scan `right > left` with `s[right] < s[left]`.
2. Build the candidate only for those pairs; keep the minimum.
3. Early-exit when a candidate smaller than any rotation from later lefts could be is found (a leading-character bound).

#### Walkthrough

Example 1, `"baca"`: `left = 0` has `s[0] = b`; rights with smaller characters are the `a` at 1 and the `a` at 3. Rotating `[0..1]` gives `"abca"`? Building it: `a + b + ca` -> `"abca"`... checking against `right = 3`: `a + bac + ""` = `"abac"`, which is smaller, and it matches the expected output. Example 2, `"cba"`: `left = 0`, rights 1 (`b`) and 2 (`a`); the `a` rotation gives `"acb"`, the answer.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, s: List[str]) -> str:
        """Return the lexicographically smallest one-rotation result.

        Time:  O(n^2) worst case: each improving pair builds one
            candidate; pairs with s[right] >= s[left] are skipped
            without a build.
        Space: O(n).
        """
        text = s if isinstance(s, str) else "".join(s)
        length = len(text)
        best = text
        for left in range(length):
            head = text[left]
            if left > 0 and best[:left] < text[:left]:
                break
            for right in range(left + 1, length):
                if text[right] < head:
                    candidate = (
                        text[:left]
                        + text[right]
                        + text[left:right]
                        + text[right + 1 :]
                    )
                    if candidate < best:
                        best = candidate
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The pair scan is quadratic; builds happen only at improving pairs, and the early-exit bounds trailing lefts once the best prefix is unbeatable.

##### Space Complexity: `O(n)`

One candidate at a time.

#### Key Insights

- The comparison `s[right] < s[left]` is a constant-time rejection of every non-improving window.
- The early-exit compares the best-so-far prefix against the original prefix: once later lefts cannot produce a smaller prefix, the search ends.

## Comparison of Solutions

### Time Complexity

- **Rotate Every Substring**: `O(n^3)` - all windows, all builds.
- **Pruned Scan Over Improvement Points**: `O(n^2)` worst case, typically far less.

### Space Complexity

- Both `O(n)`.

### Trade-offs

- The cubic rung is definitionally correct with zero reasoning.
- The pruned rung pays a small comparison per pair to skip nearly all string builds.

### When to Use Each

- **Rotate Every Substring**: the oracle in tests.
- **Pruned Scan Over Improvement Points**: every practical input.

### Optimization Notes

- A suffix-array formulation answers the strongest-rotation question in `O(n log n)`, but the constant factors and code weight dwarf the pruned scan at interview scales.
- Equal-character runs (rotating within a run of the same letter changes nothing) admit a further skip when scanning rights.
