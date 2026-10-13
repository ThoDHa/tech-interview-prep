# [Min Dock Bays](https://www.fastprep.io/problems/amazon-get-minimum-dock-bays)

**Medium** | **NN minutes** | **Array, Binary Search, Heap**

You are managing operations at a large Amazon warehouse. Loaded trucks arrive at the warehouse sequentially and must be unloaded within a specific timeframe to ensure timely delivery. Your task is to determine the minimum number of dock bays needed to unload all trucks within the given timeframe.

Formally, given a scheduling array truckCargoSize of length n, where each unit in the array represents the amount of time in minutes that a dock bay will take to unload the cargo from the i-th truck, and a second integer maxTurnaroundTime representing the total allowed time to unload all trucks, find the smallest number of dock bays d that will enable you to unload all trucks within maxTurnaroundTime minutes.

Notes:

As soon as a dock bay becomes available after unloading a truck, it can immediately start processing the next truck.It is guaranteed that unloading all trucks is possible with some number of dock bays.Only the start times of unloading need to be considered in order, not the finish times.Trucks are processed in their given arrival order. With d dock bays, the trucks are distributed among the bays in arrival order so that each bay's total processing time is the sum of the cargo times of the trucks assigned to it. The overall time to unload all trucks equals the maximum total processing time over all d dock bays.

## Examples

### Example 1

**Input:** `truckCargoSize = [3, 4, 3, 2, 3]`, `maxTurnaroundTime = 8`

**Output:** `3`

**Explanation:** Attempting with two dock bays (d = 2): the trucks are distributed in arrival order between the two bays. Dock bay 1 unloads trucks 1, 3, and 5 (3 + 3 + 3 = 9 minutes) and dock bay 2 unloads trucks 2 and 4 (4 + 2 = 6 minutes). All trucks are unloaded in 9 minutes, which exceeds the maxTurnaroundTime of 8 minutes. Attempting with three dock bays (d = 3): the bays finish in 5, 7, and 3 minutes respectively, so all trucks are unloaded in 7 minutes, which is within the maxTurnaroundTime of 8 minutes. Therefore, the minimum number of dock bays required is 3.

### Example 2

**Input:** `truckCargoSize = [2, 3, 1]`, `maxTurnaroundTime = 7`

**Output:** `1`

**Explanation:** With only one dock bay, all trucks can be unloaded in 2 + 3 + 1 = 6 minutes, which is within the maxTurnaroundTime of 7 minutes. Therefore, the minimum number of dock bays required is 1.

## Constraints

- `1 ≤ n ≤ 5 * 10^4`
- `1 ≤ maxTurnaroundTime ≤ 10^15`
- `1 ≤ truckCargoSize[i] ≤ min(maxTurnaroundTime, 10^9)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
