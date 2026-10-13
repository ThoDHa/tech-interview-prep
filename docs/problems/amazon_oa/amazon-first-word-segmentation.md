# [First Valid Word Segmentation](https://www.fastprep.io/problems/amazon-first-word-segmentation)

**Medium** | **NN minutes** | **String, Dynamic Programming, Backtracking**

Given a continuous lowercase string s and an array dictionary representing the words accepted by isWord, split s into a sequence of dictionary words whose concatenation is exactly s.

At each position, consider possible next words by increasing end position, so the shortest possible next prefix is tried first. Return the first complete segmentation found by that order. At least one valid segmentation is guaranteed.

## Examples

### Example 1

**Input:** `s = "myhousehavecat"`, `dictionary = ["my","house","have","cat"]`

**Output:** `["my","house","have","cat"]`

**Explanation:** Each returned piece is accepted by the dictionary, and their concatenation is myhousehavecat.

### Example 2

**Input:** `s = "aaaa"`, `dictionary = ["a","aa"]`

**Output:** `["a","a","a","a"]`

**Explanation:** Both one- and two-character words are valid, but increasing end positions try a before aa. Repeating that choice reaches a complete segmentation.

### Example 3

**Input:** `s = "catsanddog"`, `dictionary = ["cats","dog","sand","and","cat"]`

**Output:** `["cat","sand","dog"]`

**Explanation:** At index 0, cat ends before cats and can lead to a complete segmentation, so it begins the returned sequence.

## Constraints

- `1 <= s.length <= 500, and s contains only lowercase English letters.`
- `1 <= dictionary.length <= 5000.`
- `Dictionary words are distinct, contain only lowercase English letters, and have lengths from 1 through 50.`
- `The total number of characters across dictionary is at most 10^5.`
- `At least one valid segmentation of s exists.`
- `Possible next words are considered by increasing end position.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
