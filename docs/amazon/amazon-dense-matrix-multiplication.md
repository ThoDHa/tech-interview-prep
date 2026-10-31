# [Dense Matrix Multiplication](https://www.fastprep.io/problems/amazon-dense-matrix-multiplication)

**Medium** | **NN minutes** | **Matrix, Simulation**

You are given two rectangular integer matrices: left has m rows and k columns, and right has k rows and n columns. Return their matrix product, which has m rows and n columns.

Each output entry is the dot product of one left row and one right column: result[i][j] = sum(left[i][t] * right[t][j]) for 0 <= t < k.

Optimization follow-upAfter a correct simple implementation, explain how tiling reuses a small block of data and how contiguous memory access affects throughput. The interview report also asks about data coalescing. Discuss how adjacent GPU threads would access adjacent elements; no GPU API, kernel launch, timing target, or hardware-specific code is required by this portable exercise.

## Examples

### Example 1

**Input:** `left = [[1,2],[3,4]]`, `right = [[5,6],[7,8]]`

**Output:** `[[19,22],[43,50]]`

**Explanation:** Two-by-two dot products.

### Example 2

**Input:** `left = [[2],[3]]`, `right = [[4,5,6]]`

**Output:** `[[8,10,12],[12,15,18]]`

**Explanation:** Rectangular outer product.

### Example 3

**Input:** `left = [[1,0,-2]]`, `right = [[3],[4],[5]]`

**Output:** `[[-7]]`

**Explanation:** Signed row-column dot product.

## Constraints

- `1 <= m, k, n <= 64.`
- `Both matrices are rectangular and the inner dimensions agree.`
- `All elements are integers between -100 and 100.`
- `Every partial sum and result fits a signed 32-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
