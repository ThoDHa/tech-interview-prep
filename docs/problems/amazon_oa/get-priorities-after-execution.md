# [Get Priorities After Execution](https://www.fastprep.io/problems/get-priorities-after-execution)

**Hard** | **NN minutes** | **Heap, Hash Table, Simulation**

Several processes are scheduled for execution on an AWS server.



On one server, n processes are schedule where the ith process is assigned
a priority of priority[i]. The processes are placed sequentially in a queue
and are numbered 1, 2,..,n. The server schedules the processes per the following algorithm:


1. It finds the maximum priority shared by at least 2 processes. Let that be denoted by p. (if there is no such priority or p = 0, the algorithm is terminated)2. Otherwise, select the two of the processes with the lowest indexes and priority p, call them process1 and process2.3. The server executes process1 and removes it from the queue.4. To avoid starvation, it reduces the priority of process2 to floor(p/2).5. Start again from step 1.
Given the initial priority of the processes, find the final priority of the processes which remain after the algorithm terminates.



Note that relative the arrangement of remaining processes in the queue remains the same,only their priorities change.

## Examples

### Example 1

**Input:** `priority = [6, 6, 6, 1, 2, 2]`

**Output:** `[3, 6, 0]`

**Explanation:** The scheduler works as follows:

1. p = 6 at indices 1, 2 and 3. The indices used are process1 = 1, process2 = 2. Remove process 1 and update the priority of process 2 to floor(6/2) = 3.

2. p = 2 and process1 = 4, process2 = 5. So, update the priority = floor(2/2) = 1 of process2 and remove process1. Current set of process priorities, priority = [3, 6, 1, 1].

3. p = 1 and process 1 = 3, process2 = 4. So, update the priority = floor(1/2) = 0 of process2 and remove process1. Current set of process priorities, priority = [3, 6, 0].

4. There are no more matching process priorities so the algorithm ends.

The final priorities of the reamining processes are priority = [3, 6, 0].

### Example 2

**Input:** `priority = [4, 4, 2, 1]`

**Output:** `[0]`

**Explanation:** p = 4 and process1 = 1, process2 = 2. So, update the priority = floor(4/2) = 2 of process2 and remove process1. Current set of process priorities, priority = [2, 1, 1].

p = 2 and process1 = 1, process2 = 2. So, update the priority = floor(2/2) = 1 of process2 and remove process1. Current set of process priorities, priority = [1, 1].

p = 1 and process1 = 1, process2 = 2. So, update the priority = floor(1/2) = 0 of process2 and remove process1. Current set of process priorities, priority = [0].

### Example 3

**Input:** `priority = [2, 1, 5, 10, 10, 1]`

**Output:** `[0, 1]`

**Explanation:** p = 10 and process1 = 4, process2 = 5. So, update the priority = floor(10/2) = 5 of process2 and remove process1. Current set of process priorities, priority = [2, 1, 5, 5, 1].

p = 5 and process1 = 3, process2 = 4. So, update the priority = floor(5/2) = 2 of process2 and remove process1. Current set of process priorities, priority = [2, 1, 2, 1].

p = 2 and process1 = 1, process2 = 3. So, update the priority = floor(2/2) = 1 of process2 and remove process1. Current set of process priorities, priority = [1, 1, 1].

p = 1 and process1 = 1, process2 = 2. So, update the priority = floor(1/2) = 0 of process2 and remove process1. Current set of process priorities, priority = [0, 1].

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ priority[i] ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
