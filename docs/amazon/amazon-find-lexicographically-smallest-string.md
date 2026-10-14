# [Find Lexicographically Smallest String](https://www.fastprep.io/problems/amazon-find-lexicographically-smallest-string)

**Hard** | **NN minutes** | **String, Greedy**

Given a lowercase string s, find the lexicographically smallest lowercase string t that has the same length as s, is strictly greater than s, and has no two equal adjacent characters.

Lexicographic order uses the usual alphabet order from a through z. Return "-1" if no such string exists.

## Examples

### Example 1

**Input:** `s = "abbcd"`

**Output:** `"abcab"`

**Explanation:** The string "abcab" is greater than "abbcd", has the same length, and has no equal adjacent characters. Any smaller string greater than "abbcd" either keeps the invalid adjacent bb or cannot be completed validly.

## Constraints

- `s consists only of lowercase English letters from a through z.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
