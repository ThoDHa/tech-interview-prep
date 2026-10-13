# [Schedule Tasks](https://www.fastprep.io/problems/amazon-schedule-tasks)

**Medium** | **NN minutes** | **Greedy, Sorting, Two Pointers**

In managing tasks at analytics platform, the goal is to efficiently schedule both primary and secondary tasks within specified time constraints.



There are n primary tasks and n secondary tasks. Two arrays, primary and secondary, provide information on task hours, where primary[i] represents the duration in hours of the ith primary task, and secondary[i] represents the duration in hours of the ith secondary task.



Each day on the platform has a time limit denoted as limit hours. One primary task must be scheduled each day. If time remains after the primary task, you can choose to schedule at most one secondary task on that day. It's essential to ensure that the total hours does not exceed the specified limit hours.



Determine the maximum number of secondary tasks that can be scheduled during these n days while adhering to the given constraints.

## Examples

### Example 1

**Input:** `limit = 7`, `primary = [4, 5, 2, 4]`, `secondary = [5, 6, 3, 4]`

**Output:** `2`

**Explanation:** One of the optimal scheduling can be:



Day 1: Schedule the first primary task and the third secondary task. Total time is 4 + 3 = 7.
Day 2: Schedule the second primary task. Total time is 5.
Day 3: Schedule the third primary task and first secondary task. Total time is 2 + 5 = 7.
Day 4: Schedule the fourth primary task. Total time is 4.

There is no other arrangement of secondary tasks for which more than 2 secondary tasks can be scheduled in 4 days.

## Constraints

- `🦦`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
