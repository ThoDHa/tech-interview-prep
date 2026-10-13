# [Find Requests In Queue](https://www.fastprep.io/problems/amazon-find-requests-in-queue)

**Medium** | **NN minutes** | **Queue, Simulation**

Amazon Web Services (AWS) is a cloud computing platform with multiple servers. One of the servers is assigned to serve customer requests. There are n customer requests placed sequentially in a queue, where the ith request has a maximum waiting time denoted by wait[i]. That is, if the ith request is not served within wait[i] seconds, then the request expires and it is removed from the queue. The server processes the request following the First In First Out (FIFO) principle. The 1st request is processed first, and the nth request is served last. At each second, the first request in the queue is processed. At the next second, the processed request and any expired requests are removed from the queue.





Given the maximum waiting time of each request denoted by the array wait, find the number of requests present in the queue at every second until it is empty.





Note:

If a request is served at some time instant t, it will be counted for that instant and is removed at the next instant.
The first request is processed at time = 0. A request expires without being processed when time = wait[i]. It must be processed while time

## Examples

### Example 1

**Input:** `wait = [2, 2, 3, 1]`

**Output:** `[4, 2, 1, 0]`

**Explanation:** - time = 0 seconds, the 1st request is served. The number of requests in the queue is 4. queue = [1, 2, 3, 4].


- time = 1 second, request 1 is removed because it is processed, request 4 (wait[3] = 1) is removed because time = wait[3] = 1 which exceeds its maximum waiting time. Also, request 2 is served. The number of requests in the queue at time = 1 seconds is 2. queue = [2, 3].


- time = 2 seconds, request 2 is removed because it is processed, request 3 is served. The number of requests in the queue is 1. queue = [3].


- time = 3 seconds, request 3 is removed because it is processed. The number of requests in the queue is 0. queue = [empty].


The answer is [4, 2, 1, 0].

### Example 2

**Input:** `wait = [4, 4, 4]`

**Output:** `[3, 2, 1, 0]`

**Explanation:** time = 0 seconds, request 1 is served. queue = [1, 2, 3]

time = 1 second, request 1 is removed as it is processed, request 2 is served. queue = [2, 3]

time = 2 seconds, request 2 is removed as it is processed, request 3 is served. queue = [3]

time = 3 seconds, request 3 is removed as it is processed. queue = [empty]

so the answer is [3, 2, 1, 0]~~

### Example 3

**Input:** `wait = [3, 1, 2, 1]`

**Output:** `[4, 1, 0]`

**Explanation:** time = 0 secons, request 1 is served. The num of requests in queue is 4. queue = [3, 1, 2, 1]

time = 1 second, request 1 is removed as it is processed, request 2 and 4 are removed as time exceeds their max wating time 🥲, which is wait[1] = wait[3] = 1. Finally request 3 is served 🙌. The num of requests in the queue is 1. queue = [3]

time = 2 seconds, request 3 is removed as it is processed. The num of requests in the queue is 0, queue = [empty]

so the answer is [4, 1, 0]~

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ wait[i] ≤ 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
