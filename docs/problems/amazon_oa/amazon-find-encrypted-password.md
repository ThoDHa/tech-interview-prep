# [Find Encrypted Password](https://www.fastprep.io/problems/amazon-find-encrypted-password)

**Easy** | **NN minutes** | **String, Sorting**

The developers at Amazon employ several algorithms for encrypting passwords. In one algorithm, they encrypt palindromic passwords. A palindromic password reads the same forward and backward.

The algorithm rearranges the characters so that the result:

is a rearrangement of the original palindromic password,is also a palindrome, andis lexicographically smallest among all such palindromic rearrangements.Given an original palindromic password containing only lowercase English letters, find the encrypted password.

A string s is lexicographically smaller than a string t of the same length if the first character where they differ is smaller in s. For example, abcd is smaller than abdc but larger than abad.

The encrypted password may be the same as the original password when it is already the lexicographically smallest valid rearrangement.

## Examples

### Example 1

**Input:** `password = "babab"`

**Output:** `"abbba"`

**Explanation:** Rearrange babab to form abbba. It uses the same characters, is a palindrome, and is the lexicographically smallest valid rearrangement, so return abbba.

### Example 2

**Input:** `password = "yxxy"`

**Output:** `"xyyx"`

**Explanation:** Rearrange yxxy to form xyyx, which is a palindrome and the lexicographically smallest valid rearrangement.

### Example 3

**Input:** `password = "ded"`

**Output:** `"ded"`

**Explanation:** ded is already the lexicographically smallest palindromic rearrangement of its characters, so it remains unchanged.

## Constraints

- `1 ≤ |password| ≤ 10^5`
- `password contains only lowercase English letters.`
- `password is a palindrome.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
