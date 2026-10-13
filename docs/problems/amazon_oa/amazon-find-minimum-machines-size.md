# [Find Minimum Machine Sizes](https://www.fastprep.io/problems/amazon-find-minimum-machines-size)

**Medium** | **NN minutes** | **Array, Greedy**

A sequence of n machines is tasked with stocking or retrieving items. You are given the individual stocking/retrieving capacity values of each machine as an integer array, machineCapacity.

The Efficiency of a sequence is defined as the sum of the absolute differences between consecutive machine capacities. For a sequence a of length k, the efficiency is |a[0]-a[1]| + |a[1]-a[2]| + ... + |a[k-2]-a[k-1]|. The efficiency of a sequence consisting of a single machine is 0.

Your task is to remove zero or more machines from the sequence so that the remaining sequence has the same efficiency as the original sequence. When machines are removed, the relative order of the remaining machines must be preserved (the result must be a subsequence of the original array, not a reordering).

Among all subsequences whose efficiency equals the original efficiency, return the minimum possible number of machines (the smallest subsequence length). The remaining sequence must contain at least one machine. If the original array already has all equal elements (efficiency 0), the minimum is 1, since a single machine also has efficiency 0.

If it is impossible to remove any machine while preserving the original efficiency, return n, the original number of machines.

## Examples

### Example 1

**Input:** `machineCapacity = [1, 2, 2, 1, 1]`

**Output:** `3`

**Explanation:** Efficiency initially for [1, 2, 2, 1, 1]: |1-2| + |2-2| + |2-1| + |1-1| = 1 + 0 + 1 + 0 = 2. After removing the machines at positions [2] and [3] (0-indexed), the remaining subsequence is [1, 2, 1] (relative order preserved), whose efficiency is |1-2| + |2-1| = 1 + 1 = 2, which equals the original efficiency. No smaller efficiency-preserving subsequence exists, so the minimum number of machines is 3.

## Constraints

- `1 ≤ n ≤ 2×10^5`
- `0 ≤ machineCapacity[i] ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
