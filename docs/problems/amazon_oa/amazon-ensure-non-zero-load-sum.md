# [Ensure Non Zero Load Sum](https://www.fastprep.io/problems/amazon-ensure-non-zero-load-sum)

**Hard** | **NN minutes** | **Prefix Sum, Hash Table, Greedy**

You are given an integer array queueMessages. Positive values represent messages sent by producers, and negative values represent messages retrieved by consumers. The processing load of a contiguous subarray is the sum of its values.

You may insert messages with any integer value at any positions in the array. Return the minimum number of insertions needed so that no non-empty contiguous subarray of the resulting array has a processing load of 0.

Every original message is nonzero. Inserted values may be chosen freely, so the task is to place the fewest separators needed to break every zero-sum subarray formed by original adjacent messages.

## Examples

### Example 1

**Input:** `queueMessages = [1, -5, 3, 2, -5]`

**Output:** `1`

**Explanation:** The original values at zero-based indices 2 through 4 are [3, 2, -5], whose sum is 0. Insert 100 between 3 and 2 to obtain [1, -5, 3, 100, 2, -5]. This array has no zero-sum subarray, so one insertion is sufficient. Zero insertions cannot work because the original zero-sum subarray would remain.

## Constraints

- `1 <= queueMessages.length <= 200000`
- `-1000000000 <= queueMessages[i] <= 1000000000`
- `queueMessages[i] != 0`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
