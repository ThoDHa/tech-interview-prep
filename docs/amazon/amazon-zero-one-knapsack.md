# [0/1 Knapsack](https://www.fastprep.io/problems/amazon-zero-one-knapsack)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

You are given two arrays, weights and values, describing n items. Item i has weight weights[i] and value values[i].

Choose a subset of the items whose total weight is at most capacity. Each item may be chosen at most once. Return the maximum total value achievable.

## Examples

### Example 1

**Input:** `weights = [1,3,4,5]`, `values = [1,4,5,7]`, `capacity = 7`

**Output:** `9`

**Explanation:** Choosing the items with weights 3 and 4 uses the full capacity and yields value 4 + 5 = 9.

### Example 2

**Input:** `weights = [2,2,3]`, `values = [6,10,12]`, `capacity = 5`

**Output:** `22`

**Explanation:** The second and third items fit together and yield value 22.

### Example 3

**Input:** `weights = [4,5]`, `values = [8,9]`, `capacity = 3`

**Output:** `0`

**Explanation:** No item fits, so the empty subset is optimal.

## Constraints

- `0 <= weights.length = values.length <= 200`
- `1 <= weights[i] <= 10000`
- `0 <= values[i] <= 1000000`
- `0 <= capacity <= 10000`
- `The maximum answer fits in a signed 32-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
