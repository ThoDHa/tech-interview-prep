# [Get Redundant Substrings](https://www.fastprep.io/problems/amazon-get-redundant-substrings)

**Hard** | **NN minutes** | **String, Prefix Sum, Hash Table**

Data analysts at Amazon are building a utility to identify redundant words in advertisements.

They define a string as redundant if the length of the string, |word| = a * V + b * C, where a and b are given integers and V and C are the numbers of vowels and consonants in the string. Note that for any substring, |word| = V + C, so a substring is redundant when V + C = a * V + b * C.

Given a string word, and two integers a and b, find the number of redundant substrings of word.

A substring is a contiguous, non-empty group of characters in a string. For example, "bcb" is a substring of "abcba", while "bba" is not. The empty substring is not counted.

Vowels are the letters a, e, i, o, u; all other lowercase English letters are consonants.

## Examples

### Example 1

**Input:** `word = "abbacc"`, `a = -1`, `b = 2`

**Output:** `5`

**Explanation:** The condition |word| = a*V + b*C with a=-1, b=2 reduces to C = 2V. The non-empty substrings of "abbacc" satisfying this are "abb" (V=1, C=2), "bba" (V=1, C=2), "bac" (V=1, C=2), "acc" (V=1, C=2), and "abbacc" (V=2, C=4), giving 5 redundant substrings.

### Example 2

**Input:** `word = "akljfs"`, `a = -2`, `b = 1`

**Output:** `15`

**Explanation:** The condition |word| = a*V + b*C with a=-2, b=1 reduces to V = 0, i.e. substrings containing no vowels. In "akljfs" only the index-0 character 'a' is a vowel, so the vowel-free substrings are exactly the non-empty substrings of "kljfs" (length 5), of which there are 5*6/2 = 15.

## Constraints

- `1 ≤ |word| ≤ 10^5`
- `-10^3 ≤ a ≤ 10^3`
- `-10^3 ≤ b ≤ 10^3`
- `word contains lowercase English letters, [a-z].`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
