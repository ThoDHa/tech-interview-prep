# [Optimal Utilization](https://www.fastprep.io/problems/amazon-optimal-utilization)

**Medium** | **NN minutes** | **Two Pointers, Sorting**

You are given a device with a limited amount of memory. Each device must run two applications at the same time: one foreground application and one background application. Each application is identified by a unique integer ID (unique within its type), requires a fixed non-zero amount of memory to execute, and is classified as either foreground or background.



A pair of applications (one foreground and one background) is considered optimal if:



Their combined memory usage is less than or equal to the device's capacity.There is no other valid pair with a higher combined memory usage without exceeding the device's capacity.
Your task is to write an algorithm that finds all pairs of foreground and background applications that optimally utilize the device memory.



The function should return a list of pairs [foregroundAppID, backgroundAppID] representing the IDs of applications that optimally utilize the device. If no valid pair exists, return a list with an empty pair.



Input Format



An integer deviceCapacity representing the device's memory.A list of pairs for foreground applications.A list of pairs for background applications.
Output Format



A list of pairs of integers [foregroundAppID, backgroundAppID] for each optimal application pair.If no valid pair exists, return a list containing an empty pair.

## Examples

### Example 1

**Input:** `deviceCapacity = 7`, `foregroundAppList = [[1, 2], [2, 4], [3, 6]]`, `backgroundAppList = [[1, 2]]`

**Output:** `[[2, 1]]`

**Explanation:** The possible pairs are:

[1, 1] uses 2 + 2 = 4 memory.
[2, 1] uses 4 + 2 = 6 memory.
[3, 1] uses 6 + 2 = 8 memory (exceeds the device capacity).

Since 6 is the largest usage within capacity, [2, 1] is the only optimal pair.

### Example 2

**Input:** `deviceCapacity = 10`, `foregroundAppList = [[1, 3], [2, 5], [3, 7], [4, 10]]`, `backgroundAppList = [[1, 2], [2, 3], [3, 4], [4, 5]]`

**Output:** `[[2, 4], [3, 2]]`

**Explanation:** There are two optimal pairs:

Pair [2, 4]: Foreground app 2 uses 5 memory, background app 4 uses 5 memory; combined = 10.

Pair [3, 2]: Foreground app 3 uses 7 memory, background app 2 uses 3 memory; combined = 10.

### Example 3

**Input:** `deviceCapacity = 16`, `foregroundAppList = [[2, 7], [3, 14]]`, `backgroundAppList = [[2, 10], [3, 14]]`

**Output:** `[[]]`

**Explanation:** No combination of one foreground and one background application fits within the device capacity. Hence, the output is a list with an empty pair.

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
