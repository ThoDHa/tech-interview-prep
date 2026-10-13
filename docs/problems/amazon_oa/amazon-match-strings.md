# [Match Strings](https://www.fastprep.io/problems/amazon-match-strings)

**Easy** | **NN minutes** | **String, Two Pointers**

Special thanks: MasterKhan contributed this problem.


Amazon is developing an efficient string matching library. Develop a prototype service that matches a simple pattern with a text. There are two arrays of strings, text, and pat, each of size n. Each string in pat is a regex expression that contains exactly one wildcard character (*).



A wildcard character (*) matches any sequence of zero or more lowercase English letters. A regex matches some string if it is possible to replace the wildcard character with some sequence of characters such that the regex expression becomes equal to the string. No other character can be changed. For example, regex "abc*bcd" matches "abcbcd", "abcefgbcd" and "abccbcd" whereas it does not match the strings "abcbd", "abzbcd", "abcd".



For every i from 1 to n, your task is to find out whether pat[i] matches text[i]. Return the answer as an array of strings of size n where the ith string is "YES" if pat[i] matches text[i], and "NO" otherwise.



Note: The implementation shall not use any in build regex libraries.

## Examples

### Example 1

**Input:** `text = ["code", "coder"]`, `pat = ["co*d", "co*er"]`

**Output:** `["NO", "YES"]`

**Explanation:** Given n = 2, text = ["code", "coder"], pat = ["co*d", "co*er"],



text[0] = "code", pat[0] = "co*d", "NO", the suffixes do not matchtext[1] = "coder", pat[1] = "co*er", "YES", the prefixes and suffixes match

Here prefix of a string is defined as any substring that starts at the beginning of the string and suffix of a string is defined as any substring that ends at the end of the string.

Return ["NO", "YES"].

### Example 2

**Input:** `text = ["hackerrank", "hackerrnak"]`, `pat = ["hac*rank", "hac*rank"]`

**Output:** `["YES", "NO"]`

**Explanation:** The prefixes and suffixes must match. The suffix in text[1] is "rnak".

## Constraints

- `1 ≤ n ≤ 10`
- `1 ≤ |text[i]|, |pat[i]| ≤ 10^5`
- `text[i] contains only lowercase English characters.`
- `pat[i] contains exactly one wildcard character and other lowercase English characters.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
