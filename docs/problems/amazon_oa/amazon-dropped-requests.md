# [Dropped Requests](https://www.fastprep.io/problems/amazon-dropped-requests)

**Medium** | **NN minutes** | **Sliding Window, Array**

Special thanks: 🥝 1003 thanks to the real MVP spike! 🍉

enigma contributed this example.


On Amazon Prime Day, non-critical requests for a transaction system are routed through a throttling gateway to ensure that the network is not choked by non-essential requests. The gateway has the following limits:


The number of transactions in any given second cannot exceed 3.The number of transactions in any given 10 second period cannot exceed 20. A ten-second period includes all requests arriving from time T to T-9 (inclusive of both) for any valid time T.The number of transactions in any given minute cannot exceed 60. Similar to above, 1 minute is from max(T, T-59) to T.
Any request that exceeds any of the above limits will be dropped by the gateway. Given the times at which different requests arrive sorted ascending, find how many requests will be dropped.



Note: Even if a request is dropped it is still considered for future calculations. Although, if a request is to be dropped due to multiple violations, it is still counted only once.

## Examples

### Example 1

**Input:** `requestTime = [1, 1, 1, 1, 2]`

**Output:** `1`

**Explanation:** Request 1 - Not Dropped.Request 1 - Not Dropped.Request 1 - Not Dropped.Request 1 - Dropped. At most 3 requests are allowed in one second.Request 2 - Not Dropped.

### Example 2

**Input:** `requestTime = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7]`

**Output:** `2`

**Explanation:** Request 1 - Not Dropped.Request 1 - Not Dropped.Request 1 - Not Dropped.Request 1 - Dropped. At most 3 requsts are allowed in one second.Request 2 - Not Dropped.Request 2 - Not Dropped.Request 2 - Not Dropped.Request 3 - Not Dropped.Request 3 - Not Dropped.Request 3 - Not Dropped.Request 4 - Not Dropped.Request 4 - Not Dropped.Request 4 - Not Dropped.Request 5 - Not Dropped.Request 5 - Not Dropped.Request 5 - Not Dropped.Request 6 - Not Dropped.Request 6 - Not Dropped.Request 6 - Not Dropped.Request 7 - Not Dropped.

The total count of requests in the 10-second period from the first to the seventh second is 21, which exceeds the limit (21 > 20), so 1 request is dropped.Request 7 - Dropped.

### Example 3

**Input:** `requestTime = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 11, 11, 11, 11]`

**Output:** `7`

**Explanation:** $24

## Constraints

- `1 ≤ n ≤ 10^6`
- `1 ≤ requestTime[i] ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
