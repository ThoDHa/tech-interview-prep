# [Use Minimum Tokens](https://www.fastprep.io/problems/amazon-use-minimum-tokens)

**Hard** | **NN minutes** | **Sorting, Prefix Sum, Binary Search**

Amazon operates a system of n warehouses, each represented by warehouse[i], where warehouse[i] indicates the maximum number of items that particular warehouse can hold. Additionally, there are q shipments to process, represented by a 2D array catalog[i][2]. Each shipment has specific requirements:


catalog[i][0] denotes the minimum capacity that the selected warehouse must have to accommodate the shipment.catalog[i][1] denotes the minimum combined capacity required from the other warehouses to fulfill backup storage needs.
Amazon can increase the capacity of any warehouse by spending 1 token per unit of capacity.



The task is to determine the optimal strategy for allocating capacity for each shipment such that the fewest number of tokens are expended. This strategy must ensure that the selected warehouse meets the required capacity for the shipment and that the combined capacity of the other warehouses is sufficient for backup storage.



Note



The tokens are spent independently for each shipmentIf warehouse i is selected to accommodate the shipment and if there are some left over capacity (i.e., warehouse[i] - catalog[i][0] > 0) then it cannot be used for backup storage.

## Examples

### Example 1

**Input:** `warehouse = [2, 4, 1, 3]`, `catalog = [[5, 7]]`

**Output:** `[2]`

**Explanation:** $24

### Example 2

**Input:** `warehouse = [5, 1, 1, 4]`, `catalog = [[5, 7], [4, 10], [7, 9]]`

**Output:** `[1, 3, 5]`

**Explanation:** For the first shipment, the optimal selection is warehouse number four. You’ll need to spend one token to extend the capacity of the fourth warehouse to accommodate the shipment and no tokens on the other warehouses. The total tokens spent equal one for capacity augmentation + zero for backup storage = 1.

For the second shipment, the optimal selection is either the second or third warehouse. You’ll spend three tokens to extend the capacity of the selected warehouse and no tokens on the remaining warehouses. Hence, the total tokens spent equal three for augmentation + zero for backup storage = 3.

This explanation is incomplete. Will enhance it later.

## Constraints

- `2 ≤ n ≤ 10^5`
- `1 ≤ warehouse[i] ≤ 10^9`
- `1 ≤ q ≤ 10^5`
- `1 ≤ catalog[i][0] ≤ 10^9`
- `1 ≤ catalog[i][1] ≤ 10^15`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
