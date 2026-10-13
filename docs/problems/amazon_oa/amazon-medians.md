# [All About Medians](https://www.fastprep.io/problems/amazon-medians)

**Easy** | **NN minutes** | **Array, Sorting**

A new Amazon intern encountered a challenging task. Currently, the intern has n integers, where the value of the ith element is represented by the array element nums[i]. The intern is curious to play with arrays and subsequences and thus asks you to join him.

Given an array nums of n integers and an integer k, the intern needs to find the maximum and minimum median over all subsequences of length k.

The median of a subsequence of length k is defined as follows: sort the k chosen elements in non-decreasing order, then the median is the element at 0-indexed position floor((k-1)/2). In other words, for odd k it is the middle element, and for even k it is the lower-middle element.

## Examples

### Example 1

**Input:** `nums = [1, 2, 3]`, `k = 2`

**Output:** `[2, 1]`

**Explanation:** The subsequences of length k = 2 and their medians (using the lower-middle element of the sorted pair) are:

[1, 2] → median 1[1, 3] → median 1[2, 3] → median 2The maximum median is 2 and the minimum median is 1.

### Example 2

**Input:** `nums = [56, 21]`, `k = 1`

**Output:** `[56, 21]`

**Explanation:** The subsequences of length k = 1 and their medians are:

[56] → median 56[21] → median 21The maximum median is 56 and the minimum median is 21.

### Example 3

**Input:** `nums = [16, 21, 9, 2, 78]`, `k = 5`

**Output:** `[16, 16]`

**Explanation:** There is only one subsequence of length k = 5:

[16, 21, 9, 2, 78] → sorted [2, 9, 16, 21, 78], median at index floor((5-1)/2) = 2 is 16Since there is only one subsequence, both the maximum and minimum median are 16.

## Constraints

- `1 ≤ n ≤ 10^5`
- `0 ≤ nums[i] ≤ 10^9`
- `1 ≤ k ≤ n`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
