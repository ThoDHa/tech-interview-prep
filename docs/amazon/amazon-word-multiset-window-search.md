# [Find Word-Multiset Windows](https://www.fastprep.io/problems/amazon-word-multiset-window-search)

**Medium** | **NN minutes** | **Array, String, Hash Table, Sliding Window**

You are given a tokenized text textWords and a nonempty list targetWords. Return every word index at which a consecutive window contains exactly the same multiset of words as targetWords.

Order within a matching window does not matter, duplicate target words retain their multiplicity, matching is case-sensitive, and result indices must be ascending.

## Examples

### Example 1

**Input:** `textWords = ["red","blue","green","blue","red"]`, `targetWords = ["blue","red"]`

**Output:** `[0,3]`

**Explanation:** The first and last two-word windows each contain one red and one blue word.

### Example 2

**Input:** `textWords = ["a","a","b","a"]`, `targetWords = ["a","a"]`

**Output:** `[0]`

**Explanation:** Only the first window contains two copies of a.

## Constraints

- `1 <= targetWords.length <= textWords.length <= 100000.`
- `Every word is a nonempty ASCII string of length at most 40.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
