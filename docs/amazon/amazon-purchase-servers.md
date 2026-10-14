# [Buy Servers](https://www.fastprep.io/problems/amazon-purchase-servers)

**Medium** | **NN minutes** | **Greedy, Sorting**

AWS provides a range of servers to meet their clients' deployment and computation needs. One AWS client wants to purchase servers to deploy their application.

You are given a description of n servers in the form of two arrays, efficiency and cost. Here efficiency is a hypothetical integer metric that represents the computational power of the server, and cost is the number of AWS credits required to purchase the server. For simplicity, the servers have cost = 1 or cost = 2. Find the minimum possible total cost to purchase a set of servers with the total sum of efficiency greater than or equal to a given integer k.

If it is not possible to get a total efficiency of greater than or equal to k, report -1 as the answer.

Note: A server can only be purchased once.

## Examples

### Example 1

**Input:** `power = [4, 4, 6, 7]`, `cost = [1, 1, 2, 2]`, `target = 7`

**Output:** `2`

**Explanation:** Given efficiency = [4, 4, 6, 7], cost = [1, 1, 2, 2], k = 7. Choosing server indices [0, 1] gives cost 1 + 1 = 2 and efficiency 4 + 4 = 8 >= 7. Choosing [0, 2] gives cost 1 + 2 = 3 and efficiency 4 + 6 = 10. Choosing [1, 2] gives cost 1 + 2 = 3 and efficiency 4 + 6 = 10, and so on. Among all valid selections, indices [0, 1] yield the minimum total cost of 2 while satisfying total efficiency >= k (=7).

## Constraints

- `Each server's cost is either 1 or 2.`
- `Each server can be purchased at most once.`
- `If no selection of servers achieves a total efficiency greater than or equal to k, the answer is -1.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
