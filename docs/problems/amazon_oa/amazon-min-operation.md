# [Min Operation](https://www.fastprep.io/problems/amazon-min-operation)

**Easy** | **NN minutes** | **Array, Greedy, Hash Table**

The manager of an Amazon warehouse needs to ship n products from different locations, the location of the ith product is represented by an array locations[i]. The manager is allowed to perform one operation at a time. Each operation is described below:


If the inventory has two or more products, the manager can pick two products x and y from the inventory if they have different locations (locations[x]!=locations[y]) and ship both of them.If the inventory has one or more products, the manager can pick one product x from the inventory and ship it.
Note: After shipping a product it gets removed from the inventory, and the rest of the products which are currently not shipped come together keeping the order the same as before.



Given n products and an array locations, find the minimum number of operations that the manager has to perform to ship all of the products.

## Examples

### Example 1

**Input:** `m = 5`, `locations = [1, 8, 6, 7, 7]`

**Output:** `3`

**Explanation:** One optimal sequence is to ship products from different locations together whenever possible. For [1, 8, 6, 7, 7], pair locations 1 and 8, then pair 6 and one 7, then ship the remaining 7 alone. This takes 3 operations.

### Example 2

**Input:** `m = 4`, `locations = [1, 3, 1, 2]`

**Output:** `2`

**Explanation:** Pair the products at locations 1 and 3, then pair the remaining products at locations 1 and 2. This ships all products in 2 operations.

## Constraints

- `1 <= m <= 105`
- `locations.length == m`
- `1 <= locations[i] <= 109`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
