# [Count Pairs](https://www.fastprep.io/problems/amazon-count-pairs)

**Easy** | **NN minutes** | **Array, Hash Table**

You are given an integer array numbers and a nonnegative integer k. Count the number of distinct value pairs (a, b) for which both values occur in numbers and a + k = b.

Pairs are distinguished by their values, not by the indices or number of occurrences. Duplicate array elements therefore do not create duplicate pairs. When k = 0, each distinct value x contributes the pair (x, x); one occurrence of x is sufficient.

## Examples

### Example 1

**Input:** `numbers = [1, 1, 1, 2]`, `k = 1`

**Output:** `1`

**Explanation:** The only distinct value pair with difference 1 is (1, 2). The three occurrences of 1 do not create additional value pairs, so the answer is 1.

### Example 2

**Input:** `numbers = [1, 2]`, `k = 0`

**Output:** `2`

**Explanation:** Because k = 0, each distinct value forms one pair with itself. The values 1 and 2 contribute (1, 1) and (2, 2), so the answer is 2.

## Constraints

- `2 <= numbers.length <= 200000`
- `0 <= numbers[i] <= 1000000000`
- `0 <= k <= 1000000000`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
