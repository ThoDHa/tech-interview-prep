# [Num of Possible Unique Strings](https://www.fastprep.io/problems/amazon-find-number-of-possible-unique-strings)

**Hard** | **NN minutes** | **String, Math**

Given a string of lowercase characters, pick substring of any length in it and reverse them. Find the number of possible unique strings.


Function Description 
Complete the function findNumberOfPossibleUniqueStrings in the editor.



findNumberOfPossibleUniqueStrings has the following parameter:


String s: the input stringReturns 
int: the number of possible unique strings

## Examples

### Example 1

**Input:** `s = "abc"`

**Output:** `4`

**Explanation:** Possible unique strings:

Substring of length 1:
Reversing a single character results in same original string.
For example reverse a in abc, gives abc


Substring of length 2:
Reverse ab (substring of length 2) in abc results in bac
Reverse bc (substring of length 2) in abc results in acb


Substring of length 3:
Reverse abc (substring of length 3) in abc results in cba

So return result as 4

## Constraints

- `The length of the input string is 1 to 105`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
