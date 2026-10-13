# [Max Number of Products You can Pick](https://www.fastprep.io/problems/amazon-maximum-number-of-products-you-can-pick)

**Hard** | **NN minutes** | **Dynamic Programming, Array**

You have an array of products, where each element contains how much product you have
products = [2, 9, 4, 7, 5, 3]. Pick a subarray of products. Starting from the
beginning of the subarray, pick some number of products. One restriction: the number of products
you pick have to be strictly increasing.



For example, you choose [7, 5, 3], you pick 4 products out of 7, 5 out of 5, there's
nothing to pick from [3]. But you can pick [1, 2, 3], a total of 6 products.



The ask is to find the maximum number of products you can pick. The answer for the above example is 16.
Because you pick [2, 9, 4, 7] subarray and [2, 3, 4, 7] products out of it.



Constraints: 1 <= len(products) <= 5000 the array length won't exceed 5000
1 <= products[i] <= 10^9, the stocks per product won't exceed 10^9

## Examples

### Example 1

**Input:** `products = [2, 9, 4, 7, 5, 3]`

**Output:** `16`

**Explanation:** The optimal subarray to pick from is [2, 9, 4, 7]. You can pick the following number of products:



From the first product: 2
From the second product: 3 (since it must be strictly more than the previous pick)
From the third product: 4 (since it must be strictly more than the previous pick)
From the fourth product: 7 (since it must be strictly more than the previous pick)

The total number of products picked is 2 + 3 + 4 + 7 = 16.

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
