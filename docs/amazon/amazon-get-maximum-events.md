# [Get Max Events](https://www.fastprep.io/problems/amazon-get-maximum-events)

**Hard** | **NN minutes** | **Dynamic Programming, Sorting, Greedy**

You are given an array payload of size n, where payload[i] represents the size of the (i)-th event payload. The task is to select a subset of events and rearrange them into a new array optimizedPayload that satisfies the following conditions:


The first segment is strictly increasing.The second segment is strictly decreasing.The third segment is strictly increasing.
The goal is to maximize the number of events included in optimizedPayload.



Function Specification:



Complete the function getMaximumEvents in the editor.



getMaximumEvents has the following parameter:



int payload[n]: Array of payload sizes.

Output:



int: Maximum number of events that can be selected.

## Examples

### Example 1

**Input:** `payload = [1, 3, 5, 4, 2, 6, 8, 7, 9]`

**Output:** `9`

**Explanation:** The subset optimizedPayload = [1, 3, 5, 4, 2, 6, 7, 8, 9] satisfies the increasing-decreasing-increasing sequence configuration.

## Constraints

- `2 ≤ n ≤ 2×10^5`
- `1 ≤ payload[i] ≤ 10^9`
- `payload contains at least 2 distinct elements.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
