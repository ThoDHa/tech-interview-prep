# [Number of Suitable Locations](https://www.fastprep.io/problems/amazon-num-of-suitable-places)

**Medium** | **NN minutes** | **Sorting, Binary Search, Prefix Sum**

Amazon has multiple delivery centers across the world, represented by a number line from -10^9 to 10^9. There are n delivery centers, the ith one located at position center[i].

A point x on the number line is called a suitable location for a warehouse if it is possible to bring all the products from every delivery center to that point with a total travel distance of no more than d. At any one time, products can be brought from one delivery center and placed at point x; bringing products from a center at center[i] requires traveling to the center and returning, contributing a distance of 2 * |x - center[i]|. Thus the total travel distance to gather all products at x is the sum of 2 * |x - center[i]| over all centers.

Only integer points x on the number line (with -10^9 <= x <= 10^9) are considered. Given the positions of the delivery centers and the maximum total travel distance d, return the number of integer points x for which the total travel distance is less than or equal to d.

## Examples

### Example 1

**Input:** `center = [-2, 1, 0]`, `d = 8`

**Output:** `3`

**Explanation:** $24

### Example 2

**Input:** `center = [2, 0, 3, -4]`, `d = 22`

**Output:** `5`

**Explanation:** The suitable locations are {-1, 0, 1, 2, 3}, giving a count of 5.

At x = -1: total distance is 2*|-1-2| + 2*|-1-0| + 2*|-1-3| + 2*|-1-(-4)| = 22 <= d.At x = 0: total distance is 2*|0-2| + 2*|0-0| + 2*|0-3| + 2*|0-(-4)| = 18 <= d.At x = 1: total distance is 2*|1-2| + 2*|1-0| + 2*|1-3| + 2*|1-(-4)| = 18 <= d.At x = 2: total distance is 2*|2-2| + 2*|2-0| + 2*|2-3| + 2*|2-(-4)| = 18 <= d.At x = 3: total distance is 2*|3-2| + 2*|3-0| + 2*|3-3| + 2*|3-(-4)| = 22 <= d.Since there are 5 such points, the answer is 5.

### Example 3

**Input:** `center = [-3, 2, 2]`, `d = 8`

**Output:** `0`

**Explanation:** There are no suitable locations. For example, placing a warehouse at x = 2 gives a total distance of 2*|2-(-3)| + 2*|2-2| + 2*|2-2| = 10 > d. No integer point achieves a total distance of at most d = 8, so the answer is 0.

## Constraints

- `1 <= n <= 10^5`
- `-10^9 <= center[i] <= 10^9`
- `0 <= d <= 10^9`
- `Only integer locations x with -10^9 <= x <= 10^9 are counted.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
