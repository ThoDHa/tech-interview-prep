# [Choose Warehouse Location](https://www.fastprep.io/problems/amazon-choose-warehouses-location)

**Medium** | **NN minutes** | **Array, Dynamic Programming, Prefix Sum**

Amazon has recently established n distribution centers in a new location. They want to set up 2 warehouses to serve these distribution centers. Note that the centers and warehouses are all built along a straight line. A distribution center has its demands met by the warehouse that is closest to it. A logistics team wants to choose the location of the warehouses such that the sum of the distances of the distribution centers to their closest warehouses is minimized.



Given an array dist_centers, that represent the positions of the distribution centers, return the minimum sum of distances to their closest warehouses if the warehouses are positioned optimally.

## Examples

### Example 1

**Input:** `dist_centers = [1, 6]`

**Output:** `0`

**Explanation:** Optimal solution: Place one warehouse at x1 = 1 and the other at x2 = 6. The sum of distances to the nearest warehouse is 0 + 0 = 0.

### Example 2

**Input:** `dist_centers = [1, 2, 5, 6]`

**Output:** `2`

**Explanation:** Optimal solution: Place one warehouse at x1 = 1 and the other at x2 = 6. The distances to the nearest warehouse are [0, 0, 1, 0], resulting in a total distance sum of 2.

## Constraints

- `⛈️`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
