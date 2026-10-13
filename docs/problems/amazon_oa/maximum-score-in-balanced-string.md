# [Maximum Score in Balanced String](https://www.fastprep.io/problems/maximum-score-in-balanced-string)

**Medium** | **NN minutes** | **String, Stack**

Given a string s consisting of parentheses, you need to find the maximum score possible in a balanced substring of s. The score of a substring is calculated by choosing two indices i and j (0 <= i < j < len(s)) such that s[i] is an opening parenthesis "(" and s[j] is a closing parenthesis ")". The score of the substring is defined as j - i, i.e., the difference between the indices.



Write a function/method that takes a string s as input and returns the maximum score that can be obtained from a balanced substring of s.



Note



The input string s will only consist of opening and closing parentheses. A balanced substring is a substring that has an equal number of opening and closing parentheses.

## Examples

### Example 1

**Input:** `s = "(())"`

**Output:** `4`

**Explanation:** There are two possible balanced substrings: "( ( ) )" (3-0) + (2-1) = 4 or (2-0) + (3-1) = 4

### Example 2

**Input:** `s = "()()"`

**Output:** `3`

**Explanation:** We dont need to use the two parenthesis in the middle :)

Updated on 02-04-2025, relative image will be uploaded next time :P

## Constraints

- `N/A (feel free to contact us if you know about it. TYSM!`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
