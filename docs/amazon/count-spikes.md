# [Count Spikes](https://www.fastprep.io/problems/count-spikes)

**Medium** | **NN minutes** | **Array, Sorting**

A k-Spike is an element that satisfies both the following conditions: 

There are at least k elements from indices (0, i-1) that are less than prices[i].

There are at least k  elements from indices (i+1, n-1) that are less than prices[i].

Count the number of k-Spikes in the given array.

## Examples

### Example 1

**Input:** `prices = [1, 2, 8, 5, 3, 4]`, `k = 2`

**Output:** `2`

**Explanation:** 8 at index 2 has (1, 2) to the left and (5, 3, 4) to the right that are less than 8. 5 at index 3 has (1, 2) to the left and (3, 4) to the right that are less than 5.

## Constraints

- `N/A (If you know about it, feel free to contact us :P tysm!)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
