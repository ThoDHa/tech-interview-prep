# [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/longest_common_subsequence/solution.py`](../../practice/longest_common_subsequence/solution.py)

Given two strings `text1` and `text2`, return the length of the *longest common subsequence* between the two strings if one exists, otherwise return `0`.

A **subsequence** is a sequence that can be derived from the given sequence by deleting some or no elements  without changing the relative order of the remaining characters.

* For example, `"cat"` is a subsequence of `"crabt"`.

A **common subsequence** of two strings is a subsequence that exists in both strings.

## Examples

### Example 1

**Input:** `text1 = "cat", text2 = "crabt"`

**Output:** `3`

**Explanation:** The longest common subsequence is "cat" which has a length of 3.

### Example 2

**Input:** `text1 = "abcd", text2 = "abcd"`

**Output:** `4`

### Example 3

**Input:** `text1 = "abcd", text2 = "efgh"`

**Output:** `0`

## Constraints

- `1 <= text1.length, text2.length <= 1000`
- `text1` and `text2` consist of only lowercase English characters.

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See _TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
