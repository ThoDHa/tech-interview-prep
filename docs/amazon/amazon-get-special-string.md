# [Special String](https://www.fastprep.io/problems/amazon-get-special-string)

**Hard** | **NN minutes** | **String, Greedy**


Developers at Amazon are working on a text generation utility for one of their new products.



Currently, the utility generates only special strings. A string is special if there are no matching adjacent characters. Given a string s of length n, generate a special string of length n that is lexicographically greater than s. If multiple such special strings are possible, then return the lexicographically smallest string among them.



Notes:



Special String: A string is special if there are no two adjacent characters that are the same.Lexicographical Order: This is a generalization of the way words are alphabetically ordered in dictionaries. For example, "abc" is lexicographically smaller than "abd" because 'c' comes before 'd' in the alphabet.
A string a is lexicographically smaller than a string b if and only if one of the following conditions holds:



a is a prefix of b, but is not equal to b.In the first position where a and b differ, the character in a comes before the character in b in the alphabet. For example, "abc" is smaller than "abd" because 'c' comes before 'd'.
Important Considerations:


If the character is 'z', it is the last character in the alphabet and cannot be increased further. The string should not wrap around to 'a after 'z'The output string must not have any adjacent characters that are the same.

## Examples

### Example 1

**Input:** `s = "abbd"`

**Output:** `"abca"`

**Explanation:** Some of the special strings that are lexicographically greater than s are shown -




The lexicographically smallest special string that is greater than "abbd" is "abca".

### Example 2

**Input:** `s = "abccde"`

**Output:** `"abcdab"`

**Explanation:** Some valid special strings that are lexicographically greater than s = "abccde" include abcdab and abcdbc.

The lexicographically smallest special string greater than abccde is abcdab.

### Example 3

**Input:** `s = "zzab"`

**Output:** `"-1"`

**Explanation:** There is no special string of length 4 that is lexicographically greater than "zzab".

## Constraints

- `1 ≤ |s| ≤ 10^6`
- `s consists of lowercase English letters only.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
