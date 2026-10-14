# [Group Students](https://www.fastprep.io/problems/amazon-group-students)

**Easy** | **NN minutes** | **Sorting, Greedy**

Amazon Technical Academy (ATA) provides in-demand, technical training to current Amazon employees looking to broaden their skill sets. ATA has admitted a group of n prospective trainees with varying skill levels. To better accommodate the trainees, ATA has decided to create classes tailored to the skill levels. A placement examination will return a skill level that will be used to group the trainees into classes, where levels[i] represents the skill level of trainee i. All trainees within a class must have a skill level within maxSpread, a specified range of one another. Determine the minimum number of classes that must be formed.

## Examples

### Example 1

**Input:** `levels = [1, 4, 7, 3, 4]`, `maxSpread = 2`

**Output:** `3`

**Explanation:** The trainees in any class must be within maxSpread = 2 levels of each other. In this case, one optimal grouping is (1, 3), (4, 4), and (7). Another possible grouping is (1), (3, 4, 4), (7). There is no way to form fewer than 3 classes.

## Constraints

- `1 <= n <= 105
1 <- levels[i] <= 109 for every i (where 0 <= i <= n - 1)
0 <= maxSpread <= 109`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
