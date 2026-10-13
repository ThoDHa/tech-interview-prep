# [Get Discount Pairs](https://www.fastprep.io/problems/get-discount-pairs)

**Easy** | **NN minutes** | **Array, Hash Table, Math**

Amazon is offering a discount on every purchase of a pair of products whose price sum is divisible by x. Given the prices of n products, count the number of unordered index pairs (i, j) such that 0 <= i < j < n and (prices[i] + prices[j]) is divisible by x.

Return the number of such pairs.

## Examples

### Example 1

**Input:** `x = 60`, `prices = [31, 25, 85, 29, 35]`

**Output:** `3`

**Explanation:** The answer is 3 based on the pairs (31, 29), (25, 35), and (85, 35). Each pair sums to a number divisible by x.

## Constraints

- `1 ≤ x ≤ 2 * 109`
- `1 ≤ n ≤ 105`
- `1 ≤ prices[i] ≤ 109`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
