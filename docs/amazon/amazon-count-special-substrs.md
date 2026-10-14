# [Count Special Substrings](https://www.fastprep.io/problems/amazon-count-special-substrs)

**Medium** | **NN minutes** | **String, Prefix Sum, Hash Table**

Imagine you're working with Amazon's data analysis team, specifically focusing on analyzing customer behavior through clickstream data. This data consists of sequences of user actions on the website, represented as binary strings. A '1' could represent a significant action (like adding an item to the cart or making a purchase), and a '0' could represent a less significant action (like browsing or viewing a product).

You are given a binary string s that represents a user's interaction history. A behavior pattern (substring) is considered "special" if the number of insignificant actions ('0's) equals the square of the number of significant actions ('1's) within that pattern. That is, a substring is special when cnt0 = cnt1 * cnt1, where cnt0 is the count of '0's and cnt1 is the count of '1's in the substring.

The challenge is to identify and count all "special" behavior patterns in the user's interaction history. These patterns might indicate critical points in the user's journey where their browsing behavior was well-balanced with key actions, which could be important for understanding user engagement or predicting future purchases.

Only non-empty substrings are counted. Index notation s[i,j] in the examples refers to the inclusive-inclusive substring spanning positions i through j (both endpoints included).

Complete the function countSpecialSubstrings in the editor.

countSpecialSubstrings has the following parameter:

String s: a binary string representing a user's interaction historyint: the count of special behavior patterns (non-empty substrings)

## Examples

### Example 1

**Input:** `s = "010001"`

**Output:** `3`

**Explanation:** The special binary substrings are s[0,1] ("10"), s[2,3] ("01"), and s[3,4] ("10"). Each has 1 significant action ('1') and 1 insignificant action ('0'), satisfying cnt0 = cnt1 * cnt1 (1 = 1 * 1).

### Example 2

**Input:** `s = "10010"`

**Output:** `3`

**Explanation:** The special binary substrings are s[0,1] ("10"), s[2,3] ("01"), and s[3,4] ("10"). Each has 1 significant action ('1') and 1 insignificant action ('0'), satisfying cnt0 = cnt1 * cnt1 (1 = 1 * 1).

## Constraints

- `1 ≤ |s| ≤ 10^5`
- `s consists of '0' and '1' only.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
