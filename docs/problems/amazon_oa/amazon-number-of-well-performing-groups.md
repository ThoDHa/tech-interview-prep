# [Number Of Well Performing Groups](https://www.fastprep.io/problems/amazon-number-of-well-performing-groups)

**Medium** | **NN minutes** | **Array, Sliding Window**

Amazon aims to review its network of m servers deployed across different regions globally. The workloads on these servers are stored in the array workloads. A collection of servers is labeled as performing optimally when the difference between the highest and lowest workloads in that collection equals difference.



A collection is termed a consecutive group if there are two positions x and y such that 1 ≤ x ≤ y ≤ m, where all servers from position x to y are included in the group, with none from outside.



A group of servers is called contiguous servers when there exists x, y such that 1 ≤ x ≤ y ≤ m and all the servers between i and j are in the group and no other should be in the group.



Given the integer array workloads and integer difference, determine how many consecutive groups of servers meet the optimal performance criteria.

## Examples

### Example 1

**Input:** `load = [2, 4, 6]`, `k = 2`

**Output:** `2`

**Explanation:** We return 2 based on the part highlighted in orange.

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
