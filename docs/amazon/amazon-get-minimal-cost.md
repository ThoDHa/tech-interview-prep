# [Get Minimal Cost](https://www.fastprep.io/problems/amazon-get-minimal-cost)

**Medium** | **NN minutes** | **Array, Sorting, Greedy**

An online retailer offers products in n different dimensions as specified in the array dimensions. The category supervisor notices that several dimensions are redundant and do not offer a favorable customer experience. To optimize the available stock, the product should be offered in unique dimensions. The dimension of the i-th product, dimensions[i], can be augmented by one unit for a fee given in the adjustmentCosts array, adjustmentCosts[i].



Determine the minimal total fee required to ensure that all product dimensions are unique.



dimensions === size, cost === adjustmentCosts

## Examples

### Example 1

**Input:** `dimensions = [3, 7, 9, 7, 8]`, `adjustmentCosts = [5, 2, 5, 7, 5]`

**Output:** `6`

**Explanation:** Increase the second value in size from 7 to 10 at a cost of 3 * 2 = 6.

### Example 2

**Input:** `dimensions = [3, 3, 4, 5]`, `adjustmentCosts = [5, 2, 2, 1]`

**Output:** `5`

**Explanation:** • Increase the second 3 to 5 at a cost of 2 * 2 = 4.

• Increase 5 to 6 at a cost of 1.

• Total cost = 5.

### Example 3

**Input:** `dimensions = [2, 3, 3, 2]`, `adjustmentCosts = [2, 4, 5, 1]`

**Output:** `7`

**Explanation:** Process:

The array size contains duplicate values.

Adjust size[3] from 2 to 3 at a cost of 1 × 1 = 1.

Adjust size[2] from 3 to 4 at a cost of 1 × 4 = 4.

The total cost is 7.

Alternatively,

• Adjust size[1] to 5, which costs cost[1] * (5 - size[1]) = 8, and

• Adjust size[3] to 4, which costs cost[3] * (4 - size[3]) = 2.

• Therefore, the total cost = 8 + 2 = 10.

Thus, 7 is the minimum cost required to make all sizes distinct.

## Constraints

- `1 ≤ n ≤ 2 * 10^5`
- `1 ≤ size[i] ≤ 10^9`
- `1 ≤ cost[i] ≤ 10^4`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
