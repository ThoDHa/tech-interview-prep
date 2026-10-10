# [Target Sum](https://leetcode.com/problems/target-sum/)

**Medium** | **25 minutes** | **Array, Dynamic Programming, Backtracking**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

**Practice:** [`practice/target_sum/solution.py`](../../practice/target_sum/solution.py)

You are given an array of integers `nums` and an integer `target`.

For each number in the array, you can choose to either add or subtract it to a total sum.

* For example, if `nums = [1, 2]`, one possible sum would be `"+1-2=-1"`.

If `nums=[1,1]`, there are **two different ways** to sum the input numbers to get a sum of `0`: `"+1-1"` and `"-1+1"`.

Return the number of **different ways** that you can build the expression such that the total sum equals `target`.

## Examples

### Example 1

**Input:** `nums = [2,2,2], target = 2`

**Output:** `3`

**Explanation:** There are 3 different ways to sum the input numbers to get a sum of 2.
`+2 +2 -2 = 2`
`+2 -2 +2 = 2`
`-2 +2 +2 = 2`

## Constraints

- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 1000`
- `-1000 <= target <= 1000`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See _TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
