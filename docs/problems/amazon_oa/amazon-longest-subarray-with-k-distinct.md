# [Longest Subarray with K Distinct Values](https://www.fastprep.io/problems/amazon-longest-subarray-with-k-distinct)

**Medium** | **NN minutes** | **Array, Hash Table, Sliding Window**

Given an integer array nums and an integer k, return the longest contiguous subarray containing exactly k distinct values.

If several subarrays have the same maximum length, return the one with the smallest starting index. Return an empty array when no subarray contains exactly k distinct values.

## Examples

### Example 1

**Input:** `nums = [1,2,1,2,3]`, `k = 2`

**Output:** `[1,2,1,2]`

**Explanation:** The prefix [1,2,1,2] has exactly two distinct values and is the longest valid subarray.

### Example 2

**Input:** `nums = [1,2,1,3,4]`, `k = 3`

**Output:** `[1,2,1,3]`

**Explanation:** Two length-four windows are valid. The earliest one starts at index 0.

### Example 3

**Input:** `nums = [1,1,1]`, `k = 2`

**Output:** `[]`

**Explanation:** No subarray contains two distinct values.

## Constraints

- `1 <= nums.length <= 100000.`
- `-10^9 <= nums[i] <= 10^9.`
- `1 <= k <= nums.length.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
