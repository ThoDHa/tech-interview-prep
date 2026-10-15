# [Is Regex Matching](https://www.fastprep.io/problems/amazon-is-regex-matching)

**Hard** | **NN minutes** | **Dynamic Programming, String, Parsing**


The developers at Amazon are developing a regex matching library for their NLP use cases. A prototype regex matching has the following requirements:


The regex expression contains lowercase English letters, '(', ')', '.', and '*'.'.' matches with exactly one lowercase English letter.A regular expression followed by '*' matches with zero or more occurrences of the regular expression.If an expression is enclosed in parentheses '(' and ')', it is treated as one expression and any asterisk '*' applies to the whole expression. It is guaranteed that no expression enclosed within parenthesis contains any '*' but is always followed by '*'. Also, there is no nested brackets sequence in the given regex expression for the prototype.
For example,


Regex "(ab)*d" matches with the strings "d", "ababd", "abd", but not with the strings "abbd", "abab".Regex "ab*d" matches with the strings "abbbd", "ad", "abd", but not with strings "ababd".Regex "a(b.d)*" matches with the strings "abcdbcd", "abcdbed", "abed", "a" but not with strings "bcd", "abd".Regex "(.)*" matches with the strings "a", "aa", "aaa", "b", "bb" and many more but not "ac", "and", or "bcd" for example.
Given an array, arr, of length k containing strings consisting of lowercase English letters only and a string regex of length n, for each of them find whether the given regex matches with the string or not and report an array of strings "YES" or "NO" respectively.



Complete the function isRegexMatching in the editor.



isRegexMatching has the following parameters:



regex: A regex
arr[k]: An array of strings

string[]: An array of strings of size k where the ith string is "YES" if the ith string in arr matches with regex, otherwise it is "NO".

## Examples

### Example 1

**Input:** `regex = "ab(e.r)*e"`, `arr = ["abbeere", "abefretre"]`

**Output:** `["NO", "YES"]`

**Explanation:** Here, n = 9, regex = "ab(e.r)*e", k = 2, arr = ["abbeere", "abefretre"]



arr[0] = "abbeere" doesn't match the regex "ab(e.r)*e".arr[1] = "abefretre" matches the regex "ab(e.r)*e", if we replace '*' with 2 occurrences of "e.r", i.e. it becomes "abe.re.re". Now, replace both '.' with 'f' and 't' respectively.

Hence, the answer is ["NO", "YES"].

### Example 2

**Input:** `regex = "..()*e*"`, `arr = ["code", "abeee", "cd"]`

**Output:** `["NO", "YES", "YES"]`

**Explanation:** Here, n = 8, regex = "..()*ex", k = 3, arr = ["code", "abeeee", "cd"]



arr[0] = "code" doesn't matches the regex "..()*ex".arr[1] = "abeeee" matches the regex "..()*ex", if we replace first '*' with 0 occurrences of "" (an empty string) and second '*' with 3 occurrences of "e", i.e. it becomes "..eee". Now, replace both '.' with 'a' and 'b' respectively.arr[2] = "cd" matches the regex "..()*ex", if we replace first '*' with 0 occurrences of "" and second '*' with 0 occurrences of "e", i.e. it becomes "..". Now, replace both '.' with 'c' and 'd' respectively.

Hence, the answer is ["NO", "YES", "YES"].

## Constraints

- `N/A`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
