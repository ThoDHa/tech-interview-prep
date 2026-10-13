# [Erase Pairs](https://www.fastprep.io/problems/erase-pairs)

**Medium** | **NN minutes** | **Stack, String**

You are given a string S. In one move you can erase from S a pair of identical letters. Find the shortest possible string that can be created this way. 
If there are many such strings, choose the alphabetically (lexicographically) smallest one. 
Note that there is no limit to the number of moves.


Write a function:



given a string S of length N, returns the shortest string (or the first alphabetically, in the case of a draw) created by erasing pairs of identical letters from S.

## Examples

### Example 1

**Input:** `S = "CBCAAXA"`

**Output:** `"BAX"`

**Explanation:** For the input string S, you can make, for example, two moves:

First, erase a pair of letters "C": "CBCAAXA" ➝ "BAAXA".

Then, erase a pair of letters "A": "BAAXA" ➝ "BAX".

Thus the string "BAX" is created. There is no way to create a shorter string. The other string of length 3 that can be created is "BXA", but "BAX" is the first alphabetically. The function should return "BAX".

### Example 2

**Input:** `S = "ZYXZYZY"`

**Output:** `"XYZ"`

**Explanation:** First, erase a pair of letters "Y": "ZYXZYZY" ➝ "ZXZYZ".

Then, erase a pair of letters "Z": "ZXZYZ" ➝ "XYZ".

The other strings of length 3 that can be created are "ZYX", "YXZ", "XZY" and "ZXY", but "XYZ" is alphabetically the first, so the function should return "XYZ".

### Example 3

**Input:** `S = "ABCBACDDAA"`

**Output:** `" "`

**Explanation:** For S = "ABCBACDDAA" all five pairs of identical letters can be erased. The function should return "" (empty string).

## Constraints

- `N/A (If you know about it, feel free to contact us ;D tysm!`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
