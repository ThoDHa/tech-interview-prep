# [Calculate Warehouse Efficiency](https://www.fastprep.io/problems/amazon-calculate-warehouse-efficiency)

**Medium** | **NN minutes** | **Array, Greedy, Prefix Sum**

The supply chain manager at one of Amazon's warehouses wants to measure the efficiency of the way parcels are shipped. The volume of each parcel is represented in the array parcelWeights. Each day, the first and last parcels in the array parcelWeights are shipped until all of them are dispatched.



The manager comes up with metrics to calculate warehouse efficiency. Each day before shipping, any parcel in the warehouse is chosen and its volume is added to the sum of total efficiency. A parcel can only be chosen once.



Given the array parcelWeights, find the maximum possible efficiency of the warehouse.

## Examples

### Example 1

**Input:** `parcelWeights = [4, 4, 8, 5, 3, 2]`

**Output:** `17`

**Explanation:** The parcels have selection deadlines [1, 2, 3, 3, 2, 1]. Select a weight-4 parcel by day 1, the weight-5 parcel by day 2, and the weight-8 parcel by day 3, for total efficiency 4 + 5 + 8 = 17.

### Example 2

**Input:** `parcelWeights = [2, 1, 8, 5, 6, 2, 4]`

**Output:** `23`

**Explanation:** Select weights 4, 6, 8, and 5 on the four shipping days. Their deadlines are compatible, and their sum is 23, which is the maximum possible.

## Constraints

- `1 <= n <= 2 * 10^5`
- `0 <= parcelWeights[i] <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
