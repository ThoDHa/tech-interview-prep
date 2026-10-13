# [Get Largest Number](https://www.fastprep.io/problems/amazon-find-partition-cost)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

The database specialists at Amazon are engaged in segmenting their sequence of interconnected servers. There exists a consecutive sequence of m servers, labeled from 1 to m, where the expense metric linked to the j-th server is given in the list expense[j]. These servers must be divided into precisely p separate server segments.



The expense of dividing a server segment from servers[x : y] is established as expense[x] + expense[y]. The aggregate expense accounts for the sum of partitioning costs for all server segments.



Given m servers, a list expense, and an integer p, determine both the least and greatest achievable total expense of these operations and return them as a list of length 2: [minimum expense, maximum expense].



Note: Splitting a list means dividing it into consecutive subsequences where each item belongs strictly to one segment. For a list [10, 20, 30, 40, 50], a valid segmentation would be [[10], [20, 30], [40, 50]], while [[10, 20], [20, 30], [40, 50]] and [[10, 30], [20, 40, 50]] would be deemed incorrect 😭.

## Examples

### Example 1

**Input:** `expense = [1, 2, 3, 2, 5]`, `p = 3`

**Output:** `[14, 18]`

### Example 2

**Input:** `expense = [1, 2, 3, 4]`, `p = 2`

**Output:** `[12, 8]`

**Explanation:** Answer : Max = 12
[1+3,4+4] First Partition Is From Index 0 To 2 , second From 3 To 3

Min = 8
[1+1,2+4] First Partition From Index 0 to 0 , second From 1 To 3

PPS: This test case was added on 03-28-2025. Relevant source ss was included in the Problem Source section below.

## Constraints

- `👋😃👍`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
