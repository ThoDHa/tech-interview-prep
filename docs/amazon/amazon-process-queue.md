# [Process Queue](https://www.fastprep.io/problems/amazon-process-queue)

**Medium** | **NN minutes** | **Queue, Simulation**

You are given an array wait with elements that represent processes where each element in the array denotes the amount on time that process can wait before needing to be removed. Each second, the next process in the queue is processed and removed from the queue. Additionally, at each second, every process that had a wait time less than or equal to the time passed, needs to be removed. You need to write a function that takes the array wait and returns an array where each element of the array represents the number of processes currently in the queue.

## Examples

### Example 1

**Input:** `wait = [2,2,3,1]`

**Output:** `[3,1,0]`

**Explanation:** If wait = [2,2,3,1]



At time 0:
First process is processed and therefore removed, no other processes have a wait time of 0 so nothing else is removed.
Now wait = [2,3,1]. Num of processes = 3. answer = [3]



At time 1:
First process is removed. The process with 1 second wait time is also removed.
Now wait = [3]. Num of processes = 1 answer = [3,1]



At time 2:
First process is removed. No more processes in queue.
Now wait = []. Num of processes = 0. answer = [3,1,0]



Return [3,1,0]

### Example 2

**Input:** `wait = [4,3,1,2,1]`

**Output:** `[4,1,0]`

**Explanation:** n/a for now. If you happen to know about it, pls feel free to lmk!! Manyy thanks in advance! 👍

### Example 3

**Input:** `wait = [3,4,4,4]`

**Output:** `[3,2,1,0]`

**Explanation:** n/a for now. If you happen to know about it, pls feel free to lmk!! Manyy thanks in advance! 🍻

## Constraints

- `N/A`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
