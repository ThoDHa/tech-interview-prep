# [Bring Servers Down](https://www.fastprep.io/problems/amazon-bring-servers-down)

**Hard** | **NN minutes** | **Greedy, Math, Simulation**

The developers at Amazon want to perform a reliability drill on some servers. There are n servers where the ith server can serve request[i] number of requests and has an initial health of health[i] units.



Each second, the developers send the maximum possible number of requests that can be served by all the available servers. With the request, the developers can also send a virus to one of the servers that can decrease the health of a particular server by k units. The developers can choose the server where the virus should be sent. A server goes down when its health is less than or equal to 0.



After all the servers are down, the developers must send one more request to conclude the failure of the application.



Find the minimum total number of requests that the developers must use to bring all the servers down.

## Examples

### Example 1

**Input:** `request = [3, 4]`, `health = [4, 6]`, `k = 3`

**Output:** `21`

**Explanation:** The minimum number of requests required is 21.



Explanation image was added on 06-13-2025

## Constraints

- `n == request.length == health.length`
- `n >= 1`
- `request[i] >= 1 for each server i`
- `health[i] >= 1 for each server i`
- `k >= 1`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
