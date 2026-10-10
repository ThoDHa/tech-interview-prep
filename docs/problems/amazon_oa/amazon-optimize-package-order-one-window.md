# [Optimize Package Order by Sorting One Window](https://www.fastprep.io/problems/amazon-optimize-package-order-one-window)

**Medium** | **NN minutes** | **Array, Sorting, Simulation**

Given an integer array of package priorities and a window size k, choose exactly one contiguous window of length k and sort only that window in ascending order.

Return the lexicographically smallest complete array obtainable by that operation.

## Examples

### Example 1

**Input:** `packages = [3,2,1,4]`, `k = 3`

**Output:** `[1,2,3,4]`

**Explanation:** Sorting the first three values produces the smallest possible first element.

### Example 2

**Input:** `packages = [1,4,3,2]`, `k = 2`

**Output:** `[1,3,4,2]`

**Explanation:** The window [4,3] is the first choice that improves the array lexicographically.

## Constraints

- `1 <= packages.length <= 200`
- `1 <= k <= packages.length`
- `Package priorities fit in signed 32-bit integers.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
