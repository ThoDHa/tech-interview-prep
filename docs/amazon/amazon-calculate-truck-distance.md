# [Calculate Truck Distance](https://www.fastprep.io/problems/amazon-calculate-truck-distance)

**Medium** | **NN minutes** | **Array, Prefix Sum**

Trucks dispatch packages in a city. There are n trucks numbered 0, 1, ..., n - 1 used for dispatching goods. Assuming the trucks are parked along the x-coordinate axis, the coordinates of these trucks can be represented as a non-decreasing array called position, where the truck numbered i is parked at position[i].



Each truck can move towards increasing positions of x-coordinates only. At the start of the day, each truck is refuelled. There is a gas station at the position of truck number n - 1, i.e., at position[n - 1], and all other trucks can travel to this position for refuelling. The total distance travelled is the sum of distances travelled by each truck to reach the last x-coordinate position. Thus, the total distance is:
(position[n - 1] - position[0]) + (position[n - 1] - position[1]) + ... + (position[n - 1] - position[n - 1])



Two additional gas stations are located at the positions of two trucks, positions a and b. Treat a and b as 1-based indexes into the position array. Given q queries of the form (a, b) where a < b, find the total distance travelled by all the trucks to refuel their tanks. Assume additional gas stations are installed at position[a - 1] and position[b - 1] for each query, and that each truck stops at the nearest gas station going in the forward direction (increasing position). Note that each query is independent, and there is always a gas station at the last position.

## Examples

### Example 1

**Input:** `position = [3, 6, 10, 15, 20]`, `extraGasStations = [[2, 4]]`

**Output:** `8`

**Explanation:** There are n = 5 trucks, and their positions are position = [3, 6, 10, 15, 20]. There is q = 1 query with extra gas stations at extraGasStations = [[2, 4]].



Once extra gas stations are installed at position[2 - 1] = 6 and position[4 - 1] = 15:



0th truck will move towards x = 6.
1st truck will not move since there is already a gas station installed.
2nd truck will move towards x = 15. Recall that trucks can move in increasing x-coordinate/position only.
3rd truck will not move since there is already a gas station installed.
4th truck will not move since there is already a gas station installed.
Total distance travelled:

(6 - 3) + (6 - 6) + (15 - 10) + (15 - 15) + (20 - 20) = 3 + 0 + 5 + 0 + 0 = 8.

## Constraints

- `:P`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
