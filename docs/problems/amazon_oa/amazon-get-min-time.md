# [Get Min Time](https://www.fastprep.io/problems/amazon-get-min-time)

**Medium** | **NN minutes** | **Array, Sorting, Greedy**

Developers at Amazon have deployed an application with a distributed database. It is stored on total_servers different servers numbered from 1 to total_servers that are connected in a circular fashion, i.e. 1 is connected to 2, 2 is connected to 3, and so on until total_servers connects back to 1.



There is a subset of servers represented by an array servers of integers. They need to transfer the data to each other to be synchronized. Data transfer from one server to one it is directly connected to takes 1 unit of time. Starting from any server, find the minimum amount of time to transfer the data to all the other servers.

## Examples

### Example 1

**Input:** `total_servers = 8`, `servers = [2, 6, 8]`

**Output:** `4`

**Explanation:** Two possible paths are shown, but there can be many more. One path goes from 2 to 6 to 8 taking 6 units of time. The other path goes from 2 to 8 to 6 and takes 4 units of time. Return the shorter path length, 4.

### Example 2

**Input:** `total_servers = 5`, `servers = [1, 5]`

**Output:** `1`

**Explanation:** The two servers are directly connected so it will take only 1 unit of time to share the data.

### Example 3

**Input:** `total_servers = 10`, `servers = [4, 6, 2, 9]`

**Output:** `7`

**Explanation:** An optimal strategy is to start from server 2 and go to 4, then 6, then 9. It takes 2 + 2 + 3 = 7 units of time.

## Constraints

- `1 ≤ total_servers ≤ 109`
- `1 ≤ n ≤ 105`
- `1 ≤ servers[i] ≤ n`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
