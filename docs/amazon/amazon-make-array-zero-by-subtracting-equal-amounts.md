# [Min Operations](https://www.fastprep.io/problems/amazon-make-array-zero-by-subtracting-equal-amounts)

**Easy** | **NN minutes** | **Array, Hash Table**

You are given a non-negative integer array nums. In one operation, you must:



Choose a positive integer x such that x is less than or equal to the smallest non-zero element in nums.
Subtract x from every positive element in nums.

Return the minimum number of operations to make every element in nums equal to 0.

## Examples

### Example 1

**Input:** `nums = [1,5,0,3,5]`

**Output:** `3`

**Explanation:** In the first operation, choose x = 1. Now, nums = [0,4,0,2,4]

In the second operation, choose x = 2. Now, nums = [0,2,0,0,2]

In the third operation, choose x = 2. Now, nums = [0,0,0,0,0]

### Example 2

**Input:** `nums = [0]`

**Output:** `0`

**Explanation:** Each element in nums is already 0 so no operations are needed.

## Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
