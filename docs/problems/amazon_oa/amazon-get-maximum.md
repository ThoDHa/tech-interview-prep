# [Get Maximum](https://www.fastprep.io/problems/amazon-get-maximum)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

Amazon Fresh is a grocery store designed from the ground up to offer a seamless grocery shopping experience to consumers. As part of a stock clearance exercise at the store, given the number of fresh products, follow the rules given below to stack the products in an orderly manner.


There are a total of n piles of products.The number of products in each pile is represented by the array numProducts.Select any subarray from the array numProducts and pick up products from that subarrayThe number of products you pick from the i-th pile is strictly less than the number of products you pick from the (i+1)th pile for all indices i of the subarray.
Find the maximum number of products that can be picked.

## Examples

### Example 1

**Input:** `numProducts = [7, 4, 5, 2, 6, 5]`

**Output:** `12`

**Explanation:** These are some ways strictly increasing subarrays can be chosen (1-based index):

• Choose subarray from indices (1, 3) and pick products (3, 4, 5) respectively from each index, which is 12 products. Note that we are forced to pick only 3 products from index 1 as the maximum number of products we can pick from index 2 is 4, and we need to make sure that it is greater than the number of products picked from index 1.

• Choose subarray from indices (3, 6) and pick products (1, 2, 4, 5) respectively from each index, which is 12 products. Similar to the above case, we are forced to pick only 1 product from index 3 as the maximum number of products at index 4 is only 2.

• Choose subarray from indices (3, 5) and pick products [1, 2, 6] respectively from each index, which is 9 products.

* Choose subarray from indices (1, 1) and pick all the 7 products.

The max num of products is 12 :)

### Example 2

**Input:** `numProducts = [2, 9, 4, 7, 5, 2]`

**Output:** `16`

**Explanation:** A few examples of how you can pick the products (1-based index):

• Choose subarray from indices (1, 2) and pick products (2, 9) respectively from each index, which is 11 products.

• Choose subarray from indices (1, 4) and pick products (2, 3, 4, 7), which is 16 products.

• Choose subarray from indices (1, 5) and pick products (1, 2, 3, 4, 5), which is 15 products.

### Example 3

**Input:** `numProducts = [2, 5, 6, 7]`

**Output:** `20`

**Explanation:** Take all the products as they already are in incresing order.

(p.s. the source image is super blurry, I kinda think output is 20)

## Constraints

- `1 ≤ n ≤ 5000`
- `1 ≤ numProducts[i] ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
