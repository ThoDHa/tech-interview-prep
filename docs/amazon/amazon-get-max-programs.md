# [Get Max Programs](https://www.fastprep.io/problems/amazon-get-max-programs)

**Medium** | **NN minutes** | **Array, Binary Search, Greedy**

Within an Amazon software management tool, there's a collection of software programs and time slots. Each time slot lasts k seconds, and within that time the slots do not overlap. The software programs are required to sequentially from 1 to n, and cannot be interrupted. Each program has a specific execution time denoted as time[i].



The objective is to execute the software programs following a specific algorithm:


Start with the first time slot.Proceed sequentially through the software programs from left to right.Execute a program if it can be completed within the current time slot (i.e., the remaining time in the time slot is greater than or equal to the execution time of the program).If a program cannot be completed in the current time slot, move it to the next available time slot (if one is available).Continue this process until the available time slot.If there are no available time slots and some software programs remain to be executed, then the goal is to determine the maximum number of software programs that can be executed using this algorithm.
The goal is to determine the maximum number of software programs that can be executed using this algorithm. This can be done by moving to the last program executed within the set of software programs and removing the software programs from the leftmost of the list until the remaining set of software programs can be executed with the available time slots.



Find the maximum number of software programs from the suffix that can be executed efficiently using this algorithm. In other words, you are looking for the longest sequence of consecutive software programs from the end of the list that can be successfully scheduled within the given time slots when scheduled according to the rules provided.

## Examples

### Example 1

**Input:** `time = [5, 2, 1, 4, 2]`, `m = 2`, `k = 6`

**Output:** `4`

**Explanation:** $24

### Example 2

**Input:** `time = [4, 2, 3, 4, 1]`, `m = 1`, `k = 4`

**Output:** `1`

**Explanation:** Since there is only one time slot, of length 4, we can not start from the 1st, 2nd, 3rd, or 4th software program. Only the last software program will be executed. Hence the answer is 1.

### Example 3

**Input:** `time = [1, 2, 3, 1, 1]`, `m = 3`, `k = 3`

**Output:** `5`

**Explanation:** All the software programs will be executed in the following manner:



1st and 2nd software programs in the first time slot.3rd software program in the second time slot.4th and 5th software programs in the third time slot.

Hence the answer is 5.

## Constraints

- `1 ≤ n, m ≤ 2*105`
- `1 ≤ k ≤ 109`
- `1 <= time[i] <= k/li>`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
