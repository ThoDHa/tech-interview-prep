# [Next Perfect String](https://www.fastprep.io/problems/amazon-next-greater-perfect-string)

**Hard** | **NN minutes** | **String, Greedy**

A perfect string is a string in which no two adjacent characters are the same.

You are given a starting string s, which may or may not itself be a perfect string. Return the lexicographically smallest perfect string that is strictly greater than s.

The returned string must have the same length as s. If no such perfect string exists, return "-1".

For example, for s = "abzzzcd" the answer is "acababa". For s = "zzab" the answer is "-1", because there is no perfect string lexicographically greater than "zzab".

## Examples

### Example 1

**Input:** `s = "abzzzcd"`

**Output:** `"acababa"`

**Explanation:** "abzzzcd" is not perfect (it contains adjacent equal characters 'zz'). The lexicographically smallest perfect string strictly greater than "abzzzcd" of the same length is "acababa".

### Example 2

**Input:** `s = "zzab"`

**Output:** `"-1"`

**Explanation:** There is no perfect string lexicographically greater than "zzab", so the answer is "-1".

## Constraints

- `s consists of lowercase English letters ('a' to 'z').`
- `The returned perfect string must have the same length as s.`
- `The returned string must be the lexicographically smallest string that is strictly greater than s and contains no two equal adjacent characters.`
- `If no valid perfect string exists, return "-1".`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
