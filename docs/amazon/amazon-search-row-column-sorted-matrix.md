# [Search a Row and Column Sorted Matrix](https://www.fastprep.io/problems/amazon-search-row-column-sorted-matrix)

**Medium** | **NN minutes** | **Matrix, Binary Search**

Given a nonempty rectangular integer matrix matrix and an integer target, return true if the target occurs anywhere in the matrix, or false otherwise.

Each row is sorted in nondecreasing order from left to right. Each column is sorted in nondecreasing order from top to bottom. Duplicate values are allowed. The first value of a row need not be greater than the last value of the preceding row: the matrix is not necessarily sorted in row-major order.

## Examples

### Example 1

**Input:** `matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 6`

**Output:** `true`

**Explanation:** The target 6 is in the third row and second column (using one-based positions).

### Example 2

**Input:** `matrix = [[1,4,7],[2,5,9],[3,6,12]]`, `target = 8`

**Output:** `false`

**Explanation:** The matrix values are 1, 4, 7, 2, 5, 9, 3, 6, 12. None equals 8.

## Constraints

- `1 <= matrix.length <= 300.`
- `1 <= matrix[i].length <= 300.`
- `-1000000000 <= matrix[i][j] <= 1000000000.`
- `-1000000000 <= target <= 1000000000.`
- `The matrix is rectangular.`
- `Each row is nondecreasing from left to right, and each column is nondecreasing from top to bottom.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
