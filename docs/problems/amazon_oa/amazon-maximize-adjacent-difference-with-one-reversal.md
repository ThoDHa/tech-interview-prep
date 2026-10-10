# [Maximize Adjacent Difference With One Reversal](https://www.fastprep.io/problems/amazon-maximize-adjacent-difference-with-one-reversal)

**Hard** | **NN minutes** | **Array, Greedy, Math**

Given an integer array values, define its score as the sum of abs(values[i] - values[i + 1]) over every adjacent pair.

You may reverse at most one contiguous subarray. Return the maximum score obtainable after the optional reversal.

## Examples

### Example 1

**Input:** `values = [2,3,1,5,4]`

**Output:** `10`

**Explanation:** The original score is 8. Reversing the subarray [3,1,5] produces [2,5,1,3,4], whose score is 10.

### Example 2

**Input:** `values = [1,2,3,4]`

**Output:** `5`

**Explanation:** Reversing [2,3] produces [1,3,2,4], with score 2 + 1 + 2 = 5.

## Constraints

- `1 <= values.length <= 10^5`
- `-10^9 <= values[i] <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
