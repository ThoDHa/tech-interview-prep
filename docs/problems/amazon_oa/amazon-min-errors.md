# [Minimum Total Errors](https://www.fastprep.io/problems/amazon-min-errors)

**Medium** | **NN minutes** | **String, Dynamic Programming, Greedy**

See the Image Source section for the original statement :)



In a vast digital database, numbers were carefully stored as strings of binary characters—'0' and '1'. But something went wrong. In place of some digits, mysterious '!' marks appeared, casting doubt on what those digits should be. Should they be '0's or '1's? To make matters worse, whenever a '0' and '1' pair appeared together, they caused glitches—small errors that multiplied throughout the system. Some combinations triggered more glitches than others. The challenge now is to replace all the '!' marks in a way that minimizes the total glitches, while keeping the system stable and efficient.

## Examples

### Example 1

**Input:** `errorString = "101!1"`, `x = 2`, `y = 3`

**Output:** `9`

**Explanation:** For example, given the string errorString = "101!1" with two different error costs:

If the '!' is replaced with '0', the string becomes "10101". In this case, the sequence '01' appears multiple times, and so does the sequence '10'. The total number of errors is calculated based on how often these sequences appear and their associated error costs, resulting in a higher error count.

If the '!' is replaced with '1', the string changes to "10111". While '01' still occurs several times, '10' appears far less frequently, leading to a lower total error count.

Therefore, the goal is to choose the replacement that results in fewer errors. In this case, the option with the lowest error count is the better choice.

## Constraints

- `Unknown for now`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
