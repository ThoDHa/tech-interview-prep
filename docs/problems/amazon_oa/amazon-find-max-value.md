# [Find Max Value](https://www.fastprep.io/problems/amazon-find-max-value)

**Medium** | **NN minutes** | **Matrix, Dynamic Programming, Greedy**

Amazon’s engineering team is developing a tool designed to minimize the size of an n x n grid named matrix, based on a compression ratio described by the array limit. Their challenge is to compute the highest possible sum of exactly x elements from the matrix while adhering to the following conditions:




For every row i (where 0 ≤ i

## Examples

### Example 1

**Input:** `limit = [1, 2, 1]`, `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`, `x = 2`

**Output:** `15`

**Explanation:** The top selections from each row, respecting the limit constraints, are as follows:

Row 0: Choose 3 (since limit[0] = 1 allows only one pick)
Row 1: Pick 5 and 6 (as limit[1] = 2 permits two selections)
Row 2: Choose 9 (since limit[2] = 1 restricts to a single selection)

However, only x = 2 items can be chosen in total.

The most optimal selection strategy is to pick 6 from Row 1 and 9 from Row 2, maximizing the sum.

## Constraints

- `1 ≤ n ≤ 50`
- `1 ≤ limit[i] ≤ n`
- `1 ≤ matrix[i][j] ≤ 10^4`
- `1 ≤ x ≤ n * n`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
