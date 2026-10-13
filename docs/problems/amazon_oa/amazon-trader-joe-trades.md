# [Trader Joe Trades](https://www.fastprep.io/problems/amazon-trader-joe-trades)

**Hard** | **NN minutes** | **Dynamic Programming, Greedy**

In the Amazon Trade Optimization System, a financial strategist named Joe the trader is assigned the task of maximizing revenue while following the execution rules for trade operations. The trading system includes 26 distinct operation types, labeled from 'A' to 'Z'. The strategist is provided with n operations to perform, where the i-th operation is denoted by the string element task[i], and the related revenue is specified by the array reward[i].



According to the trade rules, no more than k identical operations can be executed consecutively. For instance, if k = 2 and the operation sequence is "bccc", this is invalid because 'c' is repeated three times in succession. On the other hand, if the sequence is "bcbcc", the trade is considered valid.



To maintain a valid sequence, the trader might need to skip certain operations. Determine the maximum possible revenue the trader can earn by omitting specific operations while keeping the sequence valid.

## Examples

### Example 1

**Input:** `tasks = "BAAAB"`, `rewards = [1, 4, 2, 10, 3]`, `k = 2`

**Output:** `18`

**Explanation:** The best strategy is to skip the task at index 2 (tasks[2] = 'A'). The sequence then becomes "BAAB", leading to a total gain of 1 + 4 + 10 + 3 = 18.

## Constraints

- `:O`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
