# [Ways to Group Parcels](https://www.fastprep.io/problems/amazon-find-number-of-ways-to-group-parcels)

**Medium** | **NN minutes** | **Hash Table, Math, Combinatorics**

In one of the warehouses of Amazon, a pan balance is used to weigh and load the parcels for delivery.



A pan balance has 2 pans, and each of the pans can contain one parcel. Due to some defect, one of the pans shows an extra erroneous weight wt. A pair of parcels is said to be balanced if they show the same weight on the pan balance. Since one of the pans is heavier by the amount wt, the absolute difference in weight of the parcels has to be wt.



Given the weights of n parcels, weight[n], and the erroneous weight wt, find the number of ways to group these parcels into pairs such that every pair of the group is balanced. Since the answer can be large, compute it modulo (10^9 + 7). Technically, the task is to find out the number of pairs that can be formed from the weight array which have an absolute difference equal to wt.
If there are no such pairs, you have to return 0.



Note:



A parcel cannot be present in more than one pair in a group.
Two groups are different if at least one of their pairs contains a different pair of parcels. The pairs at indices (i, j) and (j, i) are considered the same.
If there are no such pair, you have to return 0.

## Examples

### Example 1

**Input:** `weight = [4, 5, 5, 4, 4, 5, 2, 3]`, `wt = 1`

**Output:** `6`

**Explanation:** Pairs will contain either 4 and 5 or 2 and 3 with an absolute difference of 1.

All possible ways of grouping the parcels into pairs are, {(1, 2), (4, 3), (5, 6), (7, 8)}, {(1, 3), (4, 2), (5, 6), (7, 8)}, {(1, 6), (4, 3), (5, 2), (7, 8)}, {(1, 2), (4, 6), (5, 3), (7, 8)}, {(1, 3), (4, 6), (5, 2), (7, 8)} and {(1, 6), (4, 2), (5, 3), (7, 8)}. In all these groups, the absolute difference of the weights of each pair of parcels is equal to the given extra weight wt = 1. For example, consider the group {(1, 6), (4, 2), (5, 3), (7, 8)}.



|weight[1] - weight[6]| = |4 - 5| = 1|weight[4] - weight[2]| = |4 - 5| = 1|weight[3] - weight[5]| = |5 - 4| = 1|weight[7] - weight[8]| = |2 - 3| = 1

## Constraints

- `Unknown for now 🙉`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
