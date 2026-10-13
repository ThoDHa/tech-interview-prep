# [Channel Max Quality](https://www.fastprep.io/problems/amazon-calculate-median-sum)

**Medium** | **NN minutes** | **Sorting, Greedy**

You are given a list of packets of varying sizes and there are n channels.


Each of the n channel must have a single packetEach packet can only be on a single channel
The quality of a channel is described as the median of the packet sizes on that channel. The total quality
is defined as sum of the quality of all channels (round to integer in case of float).



Given the packet sizes and num of channels, find the maximum quality.


Function Description 
Complete the function calculateMedianSum in the editor.



calculateMedianSum has the following parameters:



int[] packets: an array of integers
int n: the number of channels
Returns 
int: the sum of the medians of each channel

## Examples

### Example 1

**Input:** `packets = [1, 2, 3, 4, 5]`, `n = 2`

**Output:** `8`

**Explanation:** If packet {1, 2, 3, 4} is sent to channel 1, the median of that channel would be 2.5

If packet {5} is sent to channel 2, its median would be 5

Max total quality is 2.5 + 5 = 7.5 ~ 8

### Example 2

**Input:** `packets = [5, 2, 2, 1, 5, 3]`, `n = 2`

**Output:** `7`

**Explanation:** channel 1 -> {2, 2, 1, 3,}, median = 2

channel 2 -> {5, 5}, median = 5

total quality 2 + 5 = 7

## Constraints

- `Unknown for now`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
