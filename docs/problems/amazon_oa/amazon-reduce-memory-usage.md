# [Reduce Memory Usage](https://www.fastprep.io/problems/amazon-reduce-memory-usage)

**Easy** | **NN minutes** | **Array, Prefix Sum, Sliding Window**

You are working on an Amazon Data Center where you are required to reduce the amount of main memory consumption by the processes.



Given list of processes where each value representing memory consumption by the processes and given one variable m representing number of processes to be removed. We need to delete m number of processes from the list in contiguous manner and return minimum amount of main memory used by all the processes running after deleting contiguous segment of processes.

## Examples

### Example 1

**Input:** `processes = [10, 4, 8, 13, 20]`, `m = 2`

**Output:** `22`

**Explanation:** Removing 13 and 20 as they are consuming large memory. The remaining processes consume 10 + 4 + 8 = 22 units of memory, which is the minimum possible.

## Constraints

- `1 < N < 1000000000 //size of the array`
- `1 < m < 100000 //contiguous segment of the array.`
- `1 < process[i] < 1000000000`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
