# [Edit Distance](https://leetcode.com/problems/edit-distance/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/edit_distance/solution.py`](../../practice/edit_distance/solution.py)

You are given two strings `word1` and `word2`, each consisting of lowercase English letters.

You are allowed to perform three operations on `word1` an unlimited number of times:

* Insert a character at any position
* Delete a character at any position
* Replace a character at any position

Return the minimum number of operations to make `word1` equal `word2`.

## Examples

### Example 1

**Input:** `word1 = "monkeys", word2 = "money"`

**Output:** `2`

**Explanation:** `monkeys` -> `monkey` (remove `s`)
`monkey` -> `money`  (remove `k`)

### Example 2

**Input:** `word1 = "neatcdee", word2 = "neetcode"`

**Output:** `3`

**Explanation:** `neatcdee` -> `neetcdee`  (replace `a` with `e`)
`neetcdee` -> `neetcde`   (remove last `e`)
`neetcde`  -> `neetcode`  (insert `o`)

## Constraints

- `0 <= word1.length, word2.length <= 100`
- `word1` and `word2` consist of lowercase English letters.

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See _TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
