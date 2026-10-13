# [Determine the Best Skipping Strategy](https://www.fastprep.io/problems/amazon-determine-the-best-skipping-strategy)

**Hard** | **NN minutes** | **Dynamic Programming, Greedy**

A company operates numerous warehouses, with each warehouse i holding inventory[i] units of a particular product. You and your co-worker are responsible for dispatching these items to fulfill customer orders, following a specific process:

When dispatching from warehouse i, you begin by reducing the inventory of the i-th warehouse by dispatch1 units.After your dispatch, your co-worker reduces the inventory by dispatch2 units.This process repeats until the inventory of the i-th warehouse reaches zero or becomes negative (i.e., inventory[i] <= 0).For every warehouse that is emptied during your dispatch (i.e., the inventory reaches zero or below on your turn), you and your co-worker collectively earn 1 credit.Your co-worker has the option to skip their turn, but they can only do this a limited number of times in total, defined by skips (across all warehouses).

The two of you alternate turns until the warehouse is emptied, then move on to the next warehouse.

Your task is to determine the best strategy to maximize the total credits that both you and your co-worker can earn together. Return the maximum number of credits that can be obtained.

## Examples

### Example 1

**Input:** `inventory = [10, 6, 12, 8, 15, 1]`, `dispatch1 = 2`, `dispatch2 = 3`, `skips = 3`

**Output:** `5`

**Explanation:** $24

## Constraints

- `1 <= n <= 10^5`
- `1 <= inventory[i] <= 10^9`
- `1 <= dispatch1, dispatch2, skips <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
