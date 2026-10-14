# [Split Prefix Suffix](https://www.fastprep.io/problems/amazon-split-prefix-suffix)

**Medium** | **NN minutes** | **String, Prefix Sum, Hash Table**

Amazon Prime Day is a day where many items are put on sale for Amazon Prime members. A list of sale items is assembled where each item is assigned a category denoted by a lowercase English letter.



Since the sale is to be held on two different days, the company has decided to split the list of items into two contiguous non-empty sub-lists - a prefix and a suffix. To ensure that both days share a sufficient number of similar items, they also need to split it in a way such that the number of distinct categories shared by both sub-lists is greater than k.



Formally, given a string, categories, find the number of ways to split the string into exactly two contiguous non-empty substrings such that the number of distinct characters occurring in both the substrings is greater than a given integer k.

## Examples

### Example 1

**Input:** `categories = "abbcac"`, `k = 1`

**Output:** `2`

## Constraints

- `1 ≤ length(categories) ≤ 10^5`
- `0 ≤ k ≤ 26`
- `The string categories consists of lowercase English characters.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
