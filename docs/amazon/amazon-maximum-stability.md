# [Maximum Stability](https://www.fastprep.io/problems/amazon-maximum-stability)

**Medium** | **NN minutes** | **Sorting, Greedy**

AWS provides servers for client deployments. Each server has an availability factor and a reliability factor. You are given two arrays, availability and reliability, where availability[i] and reliability[i] describe the i-th server.

For any non-empty subset of servers, its stability is defined as the minimum availability in that subset multiplied by the sum of reliabilities in that subset.

Find the maximum true stability value over all non-empty subsets. Because the answer can be large, return this maximum value modulo 10^9 + 7. The subset must be chosen by comparing the true stability values before applying the modulo.

## Examples

### Example 1

**Input:** `reliability = [1, 2, 2]`, `availability = [1, 1, 3]`

**Output:** `6`

**Explanation:** Consider reliability = [1, 2, 2] and availability = [1, 1, 3]. The stability of each non-empty subset of servers (by indices) is:

{0}: 1 * 1 = 1{1}: 1 * 2 = 2{2}: 3 * 2 = 6{0, 1}: min(1, 1) * (1 + 2) = 3{0, 2}: min(1, 3) * (1 + 2) = 3{1, 2}: min(1, 3) * (2 + 2) = 4{0, 1, 2}: min(1, 1, 3) * (1 + 2 + 2) = 5The maximum stability is achieved by the subset with index {2}, so the answer is 6 % 1000000007 = 6.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ reliability[i], availability[i] ≤ 10^6`
- `It is guaranteed that lengths of reliability and availability are the same.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
