# [Maxmimum Times Word Removed](https://www.fastprep.io/problems/amazon-maximum-times-word-removed)

**Easy** | **NN minutes** | **String, Hash Table**


Amazon Engineering maintains a large number of logs of operations across all products. A software engineer is debugging an issue in a product. An efficient way to analyze logs is to write automated scripts to check for patterns. The engineer wants to find the maximum number of times a target word can be obtained by rearranging a subset of characters in a log entry.



Given a log entry s and target word t, the target word can be obtained by selecting some subset of characters from s that can be rearranged to form string t and removing them from s. Determine the maximum number of times the target word can be removed from the given log entry.



Note: Both strings s and t consist only of lowercase English letters.



Complete the function maximumTimesWordRemoved in the editor.



maximumTimesWordRemoved has the following parameters:     


String s: a log entryString t: a target wordint: the maximum number of times the target word can be removed

## Examples

### Example 1

**Input:** `s = "abacbc"`, `t = "bca"`

**Output:** `2`

**Explanation:** All characters were removed from s.

### Example 2

**Input:** `s = "abdadccacd"`, `t = "edac"`

**Output:** `0`

**Explanation:** It is not possible to form the target word t from the characters in s.

## Constraints

- `Both string s and t consist only of lowercase English letters. (there might be some other constraints, will add once find out 😘)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
