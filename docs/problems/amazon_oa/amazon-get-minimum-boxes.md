# [Get Minimum Boxes](https://www.fastprep.io/problems/amazon-get-minimum-boxes)

**Medium** | **NN minutes** | **Array, Sorting, Sliding Window**

The supply chain manager at one of Amazon's warehouses is shipping the last container of the day. All n boxes have been loaded into the truck with their sizes represented in the array boxes. The truck may not have enough capacity to store all the boxes though, so some of the boxes may have to be unloaded. Any boxes may be unloaded, and the order of the boxes does not matter; only the sizes of the remaining boxes are considered. The remaining boxes must satisfy the condition max(boxes) ≤ capacity * min(boxes).

Given the array boxes and the value capacity, find the minimum number of boxes that need to be unloaded so that the remaining boxes satisfy the condition.

## Examples

### Example 1

**Input:** `boxes = [1, 4, 3, 2]`, `capacity = 2`

**Output:** `1`

**Explanation:** Here boxes = [1, 4, 3, 2] and capacity = 2.

With all boxes loaded, max = 4 and min = 1, so max ≤ capacity * min becomes 4 ≤ 2 * 1 = 2, which is false.

Unload the box of size 1. The remaining boxes are [4, 3, 2] with max = 4 and min = 2, so 4 ≤ 2 * 2 = 4, which is true.

Only one box must be unloaded, so the answer is 1.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ boxes[i] ≤ 5 * 10^5`
- `1 ≤ capacity`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
