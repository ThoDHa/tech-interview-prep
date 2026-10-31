# [Next Greater Element I](https://www.fastprep.io/problems/amazon-next-greater-element-i)

**Easy** | **NN minutes** | **Stack, Hash Table**

You are given two arrays of distinct integers, query and reference, where every query value appears in reference.

For each query value, return the first greater value to its right in reference, or -1 when none exists.

## Examples

### Example 1

**Input:** `query = [4,1,2]`, `reference = [1,3,4,2]`

**Output:** `[-1,3,-1]`

**Explanation:** Four and two have no greater value to their right; one is followed by three.

### Example 2

**Input:** `query = [2,4]`, `reference = [1,2,3,4]`

**Output:** `[3,-1]`

**Explanation:** Three is the next greater value after two, while four has none.

## Constraints

- `1 <= query.length <= reference.length <= 10^5.`
- `All values in each array are distinct.`
- `Every value in query appears in reference.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
