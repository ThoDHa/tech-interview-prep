# [Longest Perfect Anagrams](https://www.fastprep.io/problems/amazon-longest-perfect-anagrams)

**Hard** | **NN minutes** | **String, Hash Table, Sliding Window**

Developers at Amazon continuously develop algorithms to ensure the security of users' accounts through strong passwords.



One such algorithm is based upon the concept of perfect anagrams.



A string x is an anagram of y if it is possible to rearrange the letters in x to get y. For example, "bat" and "tab" are anagrams, 'bats' and 'tab' are not.
Two strings a and b are said to be perfect anagrams if a and b are anagrams of each other and a is not equal to b.

For example,


Strings "dog" and "god" are anagrams and perfect anagrams.Strings "baba" and "baba" are anagrams but not perfect anagrams because the strings are equal.Strings "abbac" and "caaba" are not anagrams because they do not contain exactly the same characters.
Given a string s, find the maximum length of two of its substrings that are perfect anagrams. If no such substrings exist, return -1.



Note: A substring is a contiguous subsegment of a string. For example, "xy" is a substring of "xyz" but "xz" is not.



Complete the function longestPerfectAnagrams in the editor.



longestPerfectAnagrams has the following parameter:



string s: a string

int: the length of the longest substring pair which are perfect anagrams or -1 if no such pair exists.

## Examples

### Example 1

**Input:** `s = "abcacb"`

**Output:** `4`

**Explanation:** The string s = "abcacbab",



Pairs of substrings such as ("ca", "ac"), ("abc", "acb"), ("bca", "acb"), ("bcac", "cacb"), etc. are perfect anagrams.
Among these, the longest are ("bcac", "cacb").

It can be proven that no two substrings of length greater than 4 in the given string are perfect anagrams. Return 4.

### Example 2

**Input:** `s = "cabcab"`

**Output:** `3`

**Explanation:** ("cab","bca") , ('abc,'bca'') are two such 3 length substrings

### Example 3

**Input:** `s = "aabbcc"`

**Output:** `-1`

**Explanation:** There are no perfect anagram. a & a , b&b , c& c are exctly same.

## Constraints

- `1 ≤ |s| ≤ 10^5`
- `string s contains lowercase English characters only.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
