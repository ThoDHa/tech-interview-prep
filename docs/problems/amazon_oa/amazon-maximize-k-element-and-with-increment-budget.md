# [Maximize K-Element AND with an Increment Budget](https://www.fastprep.io/problems/amazon-maximize-k-element-and-with-increment-budget)

**Hard** | **NN minutes** | **Array, Bit Manipulation, Greedy, Sorting**

You are given an array nums, an integer k, and a nonnegative increment budget budget. You may increase array elements by nonnegative integer amounts whose total is at most budget.

After applying the increments, choose exactly k distinct array positions. Return the maximum possible bitwise AND of the chosen values.

You do not need to return the chosen positions or the increment allocation.

## Examples

### Example 1

**Input:** `nums = [5,4,1,7,2]`, `k = 3`, `budget = 3`

**Output:** `6`

**Explanation:** Increase 4 to 6 and 5 to 6. Choosing 6, 6, 7 gives 6 & 6 & 7 = 6.

### Example 2

**Input:** `nums = [1,2,3]`, `k = 2`, `budget = 0`

**Output:** `2`

**Explanation:** Without increments, choose 2 and 3; their bitwise AND is 2.

### Example 3

**Input:** `nums = [0,0]`, `k = 2`, `budget = 2`

**Output:** `1`

**Explanation:** Increase both values to 1. Their bitwise AND is 1.

## Constraints

- `1 <= nums.length <= 200000.`
- `1 <= k <= nums.length.`
- `0 <= nums[i] <= 1000000000.`
- `0 <= budget <= 1000000000.`
- `All arithmetic fits in a signed 64-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
