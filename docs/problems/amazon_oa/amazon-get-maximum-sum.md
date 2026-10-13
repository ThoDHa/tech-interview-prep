# [Get Maximum Sum](https://www.fastprep.io/problems/amazon-get-maximum-sum)

**Easy** | **NN minutes** | **Hash Table, Sorting, Greedy**

Note 📝 - might be a sister problem of  🦥 Get Max Sum



Amazon is building a new data center with n servers of different types. The health and type of each server are represented in the arrays health and serverType. The developers need to build a server facility with a maximum of k distinct types of servers and the sum of their health should be maximized.



Given arrays health and serverType, find the maximum sum of the health for up to k types of servers.



Complete the function getMaximumSum in the editor.



getMaximumSum has the following parameters:



int health[n]: the health of each server
int serverType[n]: the type of each server
int k: the maximum number of distinct types

long int: the maximum sum of health of the selected servers



Thanks a lot to Spike — our trusted authority! 🥰

## Examples

### Example 1

**Input:** `health = [4, 5, 5, 6]`, `serverType = [1, 2, 1, 2]`, `k = 1`

**Output:** `11`

**Explanation:** Since k = 1, all selected servers must be the same type. The better option is to select type 2 servers. The maximum sum of health for type 2 servers is 5 + 6 = 11. Return 11.

### Example 2

**Input:** `health = [1, 2, 3, 10, 10]`, `serverType = [3, 3, 1, 2, 5]`, `k = 2`

**Output:** `20`

**Explanation:** With k = 2, the best option is to select servers of types 1 and 5. The maximum sum of health for these types is 2 + 3 + 10 = 15 for type 1 and 10 for type 5, which adds up to 20. Return 20.

## Constraints

- `1 ≤ k ≤ n ≤ 10^5`
- `1 ≤ health[i] ≤ 10^9`
- `1 ≤ serverType[i] ≤ n`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
