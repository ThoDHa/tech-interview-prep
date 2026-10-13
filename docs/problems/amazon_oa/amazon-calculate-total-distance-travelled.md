# [Calculate Total Distrance Travelled](https://www.fastprep.io/problems/amazon-calculate-total-distance-travelled)

**Medium** | **NN minutes** | **Array, Binary Search, Prefix Sum**

Giving position of trucks and they are always moving towards end station as it is a gas station. 
Given a second array indicating extra gas station position in 1-indexing. Calculate the total distance 
travelled by all the trucks.



Example: Given trucks at positions [0,2,5,9,12,18] and extra gas stations at positions 
[[2,5],[3]], the answer to be returned is [12,18]. The solution can be 
solved in O(n^2) time complexity with one for loop for traversing gas station array and 
a second loop to calculate total distance travelled. However, there are test cases where this approach 
may not be optimal.

## Examples

### Example 1

**Input:** `trucks = [0,2,5,9,12,18]`, `extraGasStations = [[2,5],[1, 3]]`

**Output:** `[12,18]`

**Explanation:** Heads up ~~> explanation is not from the official

The trucks at positions 0, 2, and 5 will travel to the gas station at position 5. The trucks at positions 9 and 12 will travel to the gas station at position 12. The truck at position 18 does not need to travel as it is already at the end station. Therefore, the total distance travelled by all the trucks is 5 + 3 + 0 + 3 + 0 + 0 = 12 for the first gas station and 0 + 0 + 0 + 0 + 0 + 0 = 0 for the second gas station, resulting in the answer [12, 18].

## Constraints

- `🍇🍇`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
