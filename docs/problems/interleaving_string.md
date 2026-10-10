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

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See _TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
