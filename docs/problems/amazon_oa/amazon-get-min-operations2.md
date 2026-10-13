# [Min Operations](https://www.fastprep.io/problems/amazon-get-min-operations2)

**Medium** | **NN minutes** | **Sorting, Greedy**

🍊 Following is the original prompt - 🥑



Devs at AMZ are working on a new sorting algorithm for points on the x-axis of the coordinate system.



There are n points. The i^th point initially has a weight of weight[i] and is located at position i on the x-axis.
In a single position, the i^th point can be moved to the right by a distance of dist[i].



Given weight and dist, find the minimum number of operations required to sort the points by their weights.



Function Description 🥑



Complete the function getMinOperations2 in the editor - 



GetMinOperations2 has the following arguments - 


int weights[n]: the weights of the pointsint dist[n]: the distances the points can moveReturns 
long int: the min num of operations to sort the points. Here long int represents a 64 bit integer. :)

## Examples

### Example 1

**Input:** `weight = [3, 6, 5, 2]`, `dist = [4, 3, 2, 1]`

**Output:** `5`

**Explanation:** Thus, the number of operations required are 1 + 2 + 2 = 5.

### Example 2

**Input:** `weight = [2, 4, 3, 1]`, `dist = [2, 6, 3, 5]`

**Output:** `4`

**Explanation:** Perform the ops on the first point twice and the second and the third points once. The final points are [4, 7, 3, 5] :)

## Constraints

- `2 <= n <= 2 * 10^5`
- `1 <= weights[i] <= 10^9`
- `1 <= dist[i] <= 10^3`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
