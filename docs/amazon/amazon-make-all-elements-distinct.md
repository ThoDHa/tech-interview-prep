# [Make All Elements Distinct](https://www.fastprep.io/problems/amazon-make-all-elements-distinct)

**Easy** | **NN minutes** | **Array, Hash Table**

An Amazon warehouse manager is responsible for managing inventory and ensuring that each product has a unique identifier. There are n products in the warehouse, where the identifier of the i-th item is represented by the array identifier[i]. However, in the inventory management system, some items have the same identifier.



To make all items in the inventory distinct, the following operation can be used:



Remove the first (leftmost) item from the inventory sequence.

Given n products and the array identifier, find the minimum number of operations required to make all items in the inventory distinct.

## Examples

### Example 1

**Input:** `n = 6`, `identifier = [2, 3, 2, 1, 5, 2]`

**Output:** `3`

**Explanation:** Operations:



Remove the first 2, resulting in [3, 2, 1, 5, 2]
Remove the next 3, resulting in [2, 1, 5, 2]
Remove the next 2, resulting in [1, 5, 2]

After 3 operations, identifier = [1, 5, 2], and all the elements of identifier are distinct.



Hence, the minimum number of operations required to make all the elements of the array distinct is 3.

## Constraints

- `🍑🍑`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
