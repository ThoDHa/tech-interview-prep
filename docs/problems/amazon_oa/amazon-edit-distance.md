# [Edit Distance](https://www.fastprep.io/problems/amazon-edit-distance)

**Medium** | **NN minutes** | **String, Dynamic Programming**

Given two strings word1 and word2, return the minimum number of single-character operations needed to transform word1 into word2.

Each operation is one of the following:

Insert one character.Delete one character.Replace one character.

## Examples

### Example 1

**Input:** `word1 = "horse"`, `word2 = "ros"`

**Output:** `3`

**Explanation:** Replace h with r, delete the second r, and delete e.

### Example 2

**Input:** `word1 = "intention"`, `word2 = "execution"`

**Output:** `5`

**Explanation:** A minimum transformation uses five insert, delete, or replace operations.

### Example 3

**Input:** `word1 = ""`, `word2 = "abc"`

**Output:** `3`

**Explanation:** Insert a, b, and c.

## Constraints

- `0 <= word1.length <= 500.`
- `0 <= word2.length <= 500.`
- `Both strings contain only lowercase English letters.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
