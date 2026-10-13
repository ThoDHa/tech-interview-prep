# [Get Min Change](https://www.fastprep.io/problems/amazon-get-minimum-changes)

**Medium** | **NN minutes** | **Array, Hash Table**

Amazon's software developers are working on enhancing their inventory management system with a new pricing adjustment operation on an array of products, where the price of the i^th product is given by prod_price[i]. The objective is to determine the minimum number of price adjustments needed to ensure that the Amazon price algorithm yields the same price for the sums of all subarrays of length k within the array prod_price.



Price adjustment operations can be performed as follows:



Modify any number of values in the array prod_price[i] to positive integers.
Given the array prod_price and a positive integer k, find the minimum number of changes required so that the sum of elements in all contiguous segments of length k is equal.



Note: A subarray is a contiguous segment of an array.

## Examples

### Example 1

**Input:** `prod_price = [5, 7, 7, 8]`, `k = 2`

**Output:** `2`

**Explanation:** Given, n = 4, prod_price = [5, 7, 7, 8] and k = 2.



The minimum number of changes required is 2.

### Example 2

**Input:** `prod_price = [1, 3, 2, 2, 3]`, `k = 3`

**Output:** `1`

**Explanation:** Here, n = 5, prod_price = [1, 3, 2, 2, 3] and k = 3.



The number of distinct values = 2. Modify the values of prod_price[2] to 1, and the subarray sums are [1+3+1, 3+1+2, 1+2+3] = [5, 6, 6].



Now the number of distinct values = 1. So the minimum number of changes required is 1.

## Constraints

- `:))`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
