# [Get Min Removal](https://www.fastprep.io/problems/amazon-get-min-removal)

**Easy** | **NN minutes** | **Hash Table, Greedy, Sorting**

There are n products in an Amazon catalogue, where the category of the i^th product is represented by the array catalogue.



The catalogue will be called valid if the number of distinct product categories in it is at most k. If the catalogue is not valid initially, then make it valid by removing some products from the catalogue.



Given n products and an array catalogue, find the minimum number of products to remove from the catalogue to make it valid.

## Examples

### Example 1

**Input:** `catalogue = [3, 3, 5, 7]`, `k = 1`

**Output:** `2`

**Explanation:** We can also remove [3, 3, 5] or [3, 3, 7]. However, the number of removed products in these cases is 3, which is not the minimum.

Hence, the answer is 2.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ k ≤ 10^5`
- `1 ≤ catalogue[i] ≤ 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
