# [Maximize Negative Signs](https://www.fastprep.io/problems/maximize-negative-signs)

**Medium** | **NN minutes** | **Array, Greedy**

Given a sequence of n natural numbers a_1, a_2, ..., a_n, you are to assign a sign (+ or -) to each a_i such that the cumulative sum of the signed a_1 + a_2 + ... + a_i remains positive for each i in 1 <= i <= n. Your task is to maximize the number of assigned negative signs, while still satisfying the above condition.



Input



The input consists of a single line containing n natural numbers separated by spaces, representing the sequence a_1, a_2, ..., a_n.



Output



Output a single integer, the maximum number of negative signs that can be assigned to the elements of the sequence, while ensuring that all partial cumulative sums a_1 + a_2 + ... + a_i are positive.

## Examples

### Example 1

**Input:** `sequence = [3, 2, 1, 1, 1, 1]`

**Output:** `4`

**Explanation:** In the given example, an optimal way to assign the signs could be: +3 +2 -1 -1 -1 -1. This assignment keeps all prefix sums positive, while still maximizing the number of negative signs.

## Constraints

- `1 <= n <= 100000`
- `1 <= a_i <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
