# [Count Maximum Profitable Groups](https://www.fastprep.io/problems/count-maximum-profitable-groups)

**Medium** | **NN minutes** | **Array, Stack**


A team of analysts at Amazon needs to analyze the stock prices of Amazon over a period of several months.



A group of consecutively chosen months is said to be maximum profitable if the price in its first or last month is the maximum for the group. More formally, a group of consecutive months [l, r] (1 ≤ l ≤ r ≤ n) is said to be maximum profitable if either:


stockPrice[l] = max(stockPrice[l], stockPrice[l + 1], ..., stockPrice[r])or, stockPrice[r] = max(stockPrice[l], stockPrice[l + 1], ..., stockPrice[r])
Given prices over n consecutive months, find the number of maximum profitable groups which can be formed. Note that the months chosen must be consecutive, i.e., you must choose a subarray of the given array.

## Examples

### Example 1

**Input:** `stockPrice = [3, 1, 3, 5]`

**Output:** `10`

**Explanation:** The 10 possible groups are [3], [3, 1], [3, 1, 3], [3, 1, 3, 5], [1], [1, 3], [1, 3, 5], [3], [3, 5], [5]
In each group, the maximum price is in either the first or last position.

### Example 2

**Input:** `stockPrice = [1, 5, 2]`

**Output:** `5`

**Explanation:** There are 6 possible groups: [1], [1, 5], [1, 5, 2], [5], [5, 2], [2].
Only [1, 5, 2], is not maximum profitable because its maximum value 5 is not at either end of the group.

### Example 3

**Input:** `stockPrice = [2, 3, 2]`

**Output:** `5`

**Explanation:** All 5 groups other than prices [2, 3, 2] are maximum profitable. In [2, 3, 2], the 
maximum value 3 is neither the first nor the last element. Return 5.

## Constraints

- `1 ≤ n ≤ 5 * 10^5`
- `1 ≤ stockPrice[i] ≤ 10^8`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
