# [Find Subarray with Minimum Distinct Integers](https://www.fastprep.io/problems/amazon-find-subarray-with-minimum-distinct-integers)

**Medium** | **NN minutes** | **Sliding Window, Hash Table, Array**

Given an array of integers and two specified numbers, find a subarray from the original array that contains both of these specified numbers, with the requirement that the subarray contains the minimum number of distinct numbers. Return the count of distinct numbers in this subarray.



If the two specified numbers are the same, simply return 1 if the array contains this number, otherwise return 0.

## Examples

### Example 1

**Input:** `array = [1, 2, 2, 2, 5, 2]`, `series1 = 1`, `series2 = 5`

**Output:** `3`

**Explanation:** The subarray must contain the series1 and series2 and having the smallest number of distinct values is [1, 2, 2, 2, 5], so return 3, the number of distinct integers in this subarray.

### Example 2

**Input:** `array = [1, 3, 2, 1, 4]`, `series1 = 1`, `series2 = 2`

**Output:** `2`

**Explanation:** The shortest subarray contains both series1 and series2 is [2, 1], so we return 2, the number of distinct values in this subarray.

### Example 3

**Input:** `array = [3, 1, 2]`, `series1 = 1`, `series2 = 1`

**Output:** `1`

**Explanation:** Because series1 and series2 are the same, so if the array contains series1, that would be good. This array contains series1, so we return 1.

### Example 4

**Input:** `array = [2, 4, 9]`, `series1 = 1`, `series2 = 1`

**Output:** `0`

**Explanation:** Because series1 and series2 are the same, but this array doesn't contain series1, so we return 0.

## Constraints

- `🍍🍍`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
