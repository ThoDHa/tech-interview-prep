# [Find Days S2 Subsequence of S1](https://www.fastprep.io/problems/amazon-find-days-s2-subsequence-of-s1)

**Hard** | **NN minutes** | **String, Binary Search, Prefix Sum**

Given two strings s1 and s2, find till how many days is s2 a subsequence of s1 if on every day we delete all the strings in s1 from start to end inclusive.


Function Description 
Complete the function findDaysS2SubsequenceOfS1 in the editor.



findDaysS2SubsequenceOfS1 has the following parameters:



1. String s1: the original string
2. String s2: the subsequence to find
3. int[] start: the start indices
4. int[] end: the end indices
Returns 
int: the number of days s2 is a subsequence of s1

## Examples

### Example 1

**Input:** `s1 = "abcdefghabc"`, `s2 = "abc"`, `start = [0, 0, 1, 2, 9]`, `end = [1, 2, 3, 3, 10]`

**Output:** `4`

**Explanation:** An educated guess 🐹~~ 

On day 1, deleting from index 0 to 1, the string becomes "cdefghabc" and "abc" is still a subsequence.
On day 2, deleting from index 0 to 2, the string becomes "defghabc" and "abc" is still a subsequence.
On day 3, deleting from index 1 to 3, the string becomes "dghabc" and "abc" is still a subsequence.
On day 4, deleting from index 2 to 3, the string becomes "dhabc" and "abc" is still a subsequence.
On day 5, deleting from index 9 to 10, the string becomes "dh" and "abc" is no longer a subsequence.
Therefore, the answer is 4 days.

## Constraints

- `🍋🍋`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
