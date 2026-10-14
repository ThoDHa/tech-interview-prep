# [Maximum Quality Sum](https://www.fastprep.io/problems/amazon-maximum-quality-sum)

**Hard** | **NN minutes** | **Greedy, Sorting, Heap**

Amazon's AWS provides fast and efficient server solutions. The developers want to stress-test the quality of the servers' channels. They must ensure the following:


Each of the packets must be sent via a single channel.Each of the channels must transfer at least one packet.
The quality of the transfer for a channel is defined by the median of the sizes of all the data packets sent through that channel.



Note: The median of an array is the middle element if the array is sorted in non-decreasing order. If the number of elements in the array is even, the median is the average of the two middle elements.



Find the maximum possible sum of the qualities of all channels. If the answer is a floating-point value, round it to the next higher integer.

## Examples

### Example 1

**Input:** `packets = [1, 2, 3, 4, 5]`, `channels = 2`

**Output:** `8`

**Explanation:** At least one packet has to go through each of the 2 channels. One maximal solution is to transfer packets {1, 2, 3, 4) through channel 1 and packet {5} through channel 2.



The quality of transfer for channel 1 is (2 + 3)/2 = 2.5 and that of channel 2 is 5. Their sum is 2.5 + 5 = 7.5 which rounds up to 8.

### Example 2

**Input:** `packets = [2, 2, 1, 5, 3]`, `channels = 2`

**Output:** `7`

**Explanation:** One solution is to send packet {5} through one channel and {2, 2, 1, 3} through the other. The sum of quality is 5 + (2 + 2)/2 = 7

### Example 3

**Input:** `packets = [89, 48, 14]`, `channels = 3`

**Output:** `151`

**Explanation:** There are 3 channels for 3 packets. Each channel carries one, so the overall sum of quality is 89 + 48 + 14 = 151

## Constraints

- `1 ≤ len(packets) ≤ 5×10^5`
- `1 ≤ packets[i] ≤ 10^9`
- `1 ≤ channels ≤ len(packets)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
