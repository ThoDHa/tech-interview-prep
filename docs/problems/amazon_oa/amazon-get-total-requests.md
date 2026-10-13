# [Get Total Requests](https://www.fastprep.io/problems/amazon-get-total-requests)

**Easy** | **NN minutes** | **Array, Hash Table, Simulation**

Developers at Amazon have their applications deployed on n servers. Initially, the ith server has an id server[i] and can handle server[i] requests at a time.



For maintenance purposes, some servers are replaced periodically. On a jth day, all the servers with id equal to replaced[j] are replaced with servers with id newId[j] that can serve newId[j] requests. The total number of requests served on a jth day is the sum of the ids of the servers that the application is running on.



Given server, replaced, and newId, find the total number of requests served by the servers each day.



Note: The indices i and j are assumed to follow 1-based indexing.

## Examples

### Example 1

**Input:** `server = [20, 10]`, `replaced = [10, 20]`, `newId = [20, 1]`

**Output:** `[40, 2]`

**Explanation:** Day 1: The servers are [20, 10]. Server with id 10 is replaced by a server with id 20. New servers are [20, 20]. Total requests = 20 + 20 = 40.



Day 2: The servers are [20, 20]. Server with id 20 is replaced by a server with id 1. New servers are [1, 1]. Total requests = 1 + 1 = 2.



Hence the answer is [40, 2].

### Example 2

**Input:** `server = [3, 3]`, `replaced = [3, 1]`, `newId = [1, 5]`

**Output:** `[2, 10]`

**Explanation:** After the first day, the servers are [1, 1].

After the second day, the servers are [5, 5] :)

### Example 3

**Input:** `server = [2, 5, 2]`, `replaced = [2, 5, 3]`, `newId = [3, 1, 5]`

**Output:** `[11, 7, 11]`

**Explanation:** After the first day, the servers are [3, 5, 3].)

After the second day, the servers are [3, 1, 3] :)

After the third day,the servers are [5, 1, 5] :)

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ server[i], replaced[i], newId[i] < 10^4`
- `server, replaced, and newId each have exactly n elements.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
