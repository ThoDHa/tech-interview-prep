# [Compute Beauty of Array Products](https://www.fastprep.io/problems/amazon-compute-beauty-of-array-products)

**Hard** | **NN minutes** | **Array, Sliding Window, Segment Tree**

The Amazon distribution center consists of arrays of products, each possessing unique attributes. The task at hand is to compute the beauty of these product arrays, with the goal of achieving an efficient selection process.



More specifically, there are arrays of products, and each array corresponds to a list of attributes. The beauty of a subarray B = [products[l], products[l+1], ..., products[r]] is quantified by counting the indices i that satisfy these conditions:


l ≤ i ≤ rfor every index j such that i < j ≤ r, products[i] > products[j]
An array B is a subarray of an array A if B can be obtained from A by deletion of several (possibly, zero or all) elements from the beginning and several (possibly, zero or all) elements from the end. In particular, an array is a subarray of itself.



The beautiness of the entire array of products is determined by the sum of beauty values across all subarrays of a given size k.



Given an array products of size n and an integer k. Compute the total beautiness of the array of products.

## Examples

### Example 1

**Input:** `products = [3, 6, 2, 9, 4, 1]`, `k = 3`

**Output:** `8`

**Explanation:** So, the beauty of the array numbers is 2 + 1 + 2 + 3 = 8.

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
