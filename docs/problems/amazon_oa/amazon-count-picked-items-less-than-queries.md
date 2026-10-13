# [Count Picked Items Less Than Queries](https://www.fastprep.io/problems/amazon-count-picked-items-less-than-queries)

**unknown difficulty** | **NN minutes** | **unknown categories**

A warehouse has items represented by an array items, where items[i] is the value of the i-th item.

There are several orders. The i-th order picks every item in the inclusive index range startIndex[i] through endIndex[i]. Across all orders, this creates one combined multiset of picked item values.

For each value query[i], return how many picked items have value strictly less than query[i].

## Examples

### Example 1

**Input:** `items = [1,2,5,4,5]`, `startIndex = [0,0,1]`, `endIndex = [1,2,2]`, `query = [2,4]`

**Output:** `[2,5]`

**Explanation:** The orders pick values [1,2], [1,2,5], and [2,5]. Two picked values are less than 2, and five are less than 4.

## Constraints

- `1 <= items.length`
- `startIndex.length == endIndex.length`
- `0 <= startIndex[i] <= endIndex[i] < items.length`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
