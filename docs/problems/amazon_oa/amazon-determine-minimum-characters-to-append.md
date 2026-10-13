# [Min Chars to Append](https://www.fastprep.io/problems/amazon-determine-minimum-characters-to-append)

**Easy** | **NN minutes** | **String, Two Pointers**

You are given two strings, searchWord and resultWord. You may append characters only to the end of searchWord. Return the minimum number of characters that must be appended so that resultWord is a subsequence of the resulting searchWord.

A subsequence is formed by deleting zero or more characters without changing the order of the remaining characters. Equivalently, match the longest prefix of resultWord as a subsequence of searchWord; the unmatched suffix of resultWord is what must be appended.

## Examples

### Example 1

**Input:** `searchWord = "abcz"`, `resultWord = "azdb"`

**Output:** `2`

**Explanation:** The prefix az of resultWord appears in order in searchWord at indices 0 and 3. The unmatched suffix is db, whose length is 2. Appending it produces abczdb, which contains azdb as a subsequence.

## Constraints

- `1 <= searchWord.length, resultWord.length <= 100000`
- `Both strings contain only lowercase English letters.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
