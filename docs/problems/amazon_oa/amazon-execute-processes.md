# [Execute Processes](https://www.fastprep.io/problems/amazon-execute-processes)

**Medium** | **NN minutes** | **Array, Hash Table, Simulation**

Amazon Web Services (AWS) has several processors for executing processes scheduled on its servers.



There are n processes to be executed, where the i^th process takes 
execution[i] amount of time to execute. Two processes are cohesive if and only if 
their original execution times are equal. When a process with execution time execution[i] 
is executed, it takes execution[i] time to complete and simultaneously reduces the 
execution time of all its cohesive processes to ceil(execution[i] / 2).



Given the execution time of n processes, find the total amount of time the processor 
takes to execute all the processes if you execute the processes in the given order, i.e. from left 
to right.



Notes



The ceil() function returns the smallest integer that is bigger or equal to its argument. For example, ceil(1.1) = 2, ceil(2.5) = 3, ceil(5) = 5, etc.If the execution time of some process i is reduced and becomes equal to the execution time of any other process j, then the two processes i and j are not considered cohesive.
Complete the function totalExecutionTime in the editor.



totalExecutionTime has the following parameter:



int execution[n]: an array of integers representing the execution timesint: the total amount of time to execute all processes

## Examples

### Example 1

**Input:** `execution = [5, 5, 3, 6, 5, 3]`

**Output:** `21`

**Explanation:** processes 1, 2, 5 are cohesive
processes 3, 6 are cohesive
process 4 is cohesive

Excuting Process 1 results in [0, 3, 3, 6, 3, 3] // total_execution = 5
Excuting Process 2 results in [0, 0, 3, 6, 2, 3] // total_execution = 8
Excuting Process 3 results in [0, 0, 0, 6, 2, 2] // total_execution = 11
Excuting Process 4 results in [0, 0, 0, 0, 2, 2] // total_execution = 17
Excuting Process 5 results in [0, 0, 0, 0, 0, 2] // total_execution = 19
Excuting Process 6 results in [0, 0, 0, 0, 0, 0] // total_execution = 21

Hence, total excution time is 21.

## Constraints

- `Unknown for now 🐰`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
