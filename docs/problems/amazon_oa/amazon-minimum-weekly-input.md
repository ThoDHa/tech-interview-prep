# [Planning the Campaign](https://www.fastprep.io/problems/amazon-minimum-weekly-input)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

A company will launch a series of marketing campaigns over several weeks. Each campaign has a certain cost. They want to launch at least one campaign every week, and to plan the campaigns in a way that minimizes the total weekly input. The weekly input is the maximum cost of any campaign planned in that week. Given the cost of the campaigns in a list, costs, and the number of weeks, find the minimum sum of weekly inputs that can be achieved with optimal planning. The campaigns must be organized in the same order in which they appear in the list costs.

## Examples

### Example 1

**Input:** `costs = [1000, 500, 2000, 8000, 1500]`, `weeks = 3`

**Output:** `9500`

**Explanation:** The company can organize the first campaign in the first week, the second campaign in the second week, and the remaining campaigns in the third week. The sum of weekly inputs in this planning is 1000 + 500 + max(2000, 8000, 1500) = 9500, which is the minimum possible input. Return 9500.

## Constraints

- `1 ≤ n ≤ 300`
- `1 ≤ weeks ≤ n ≤ 300`
- `1 ≤ costs[i] ≤ 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
