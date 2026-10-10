# [Find Minimum Cost](https://www.fastprep.io/problems/amazon-find-minimum-cost)

**Hard** | **NN minutes** | **Array, Prefix Sum, Greedy**

A warehouse has n identical containers arranged in a circle. Adjacent containers are one unit apart, and the goal is to make every container hold the same number of products.

Choose either clockwise or counterclockwise movement; all transfers must use that same direction.Products may be collected from containers with excess units and delivered to containers with deficits.Moving one product across one edge costs 1.Return the minimum total transfer cost. It is guaranteed that equal redistribution is possible.

## Examples

### Example 1

**Input:** `products = [3, 4, 6, 6, 6]`

**Output:** `7`

**Explanation:** $23

### Example 2

**Input:** `products = [1, 11, 1, 1, 1]`

**Output:** `20`

**Explanation:** The final average is 3. One container has 8 extra products. Moving in either fixed direction, send 2 products to each of the other four containers, for total cost 2*1 + 2*2 + 2*3 + 2*4 = 20.

## Constraints

- `1 <= products.length <= 2 * 10^50 <= products[i] <= 10^9The answer may exceed the 32-bit integer range.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
