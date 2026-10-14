# [Count Distinct Passwords](https://www.fastprep.io/problems/amazon-count-distinct-passwords)

**Hard** | **NN minutes** | **String, Hash Table**

Weak passwords are likely to be hacked and misused. Due to this, developers at Amazon regularly come up with new algorithms to check the health of user passwords. A new algorithm estimates the variability of a password as the number of distinct password strings that can be obtained by reversing any one substring of the original password. Given the original password that consists of lowercase English characters, find its variability.



Note: A substring is a contiguous sequence of characters within a string. For example 'bcd', 'a', 'abcd' are substrings of the string 'abcd' whereas the strings 'bd', 'acd' are not.

## Examples

### Example 1

**Input:** `password = "abc"`

**Output:** `4`

**Explanation:** The following strings can be formed from password = 'abc':



Reversing any substring of length 1 gives the original string "abc".Reversing the substring "ab" gives a new string "bac".Reversing the substring "bc" gives a new string "acb".Reversing the substring "abc" gives a new string "cba".

There are 4 distinct password strings that can be obtained from password. Return 4.

### Example 2

**Input:** `password = "abaa"`

**Output:** `4`

**Explanation:** The strings that can be formed are "abaa", "aaba", "baaa" and "aaab".

## Constraints

- `All characters in password are lowercase English letters ascii[a-z]`
- `1 ≤ length of password ≤ 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
