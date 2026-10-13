# [Get Max Skill Sum](https://www.fastprep.io/problems/amazon-get-max-skill-sum)

**Medium** | **NN minutes** | **Prefix Sum, Hash Table**

A manager at Amazon is managing a team of n employees with IDs numbered from 0 to n - 1. Some employees are marketing experts and others are developers. The employee with id i has a skill level of skill[i]. The employee is a marketing expert if expertise[i] is 0 and a developer if expertise[i] is 1.



The manager wants to select a team to work on a project with some contiguous set of ids [i, i + 1, i + 2, ..., j] such that there is an equal number of marketing experts and developers and the total sum of skills is maximized.



Given two arrays, skill and expertise, find the maximum possible sum of skills of any team that can be formed respecting the above conditions.



Note:



It is always possible to form a team consisting of zero employees with a total skill of zero.A contiguous set of elements is a sequence where each element is adjacent to the next, with no gaps between them. Each element in the set is directly next to the previous one.

## Examples

### Example 1

**Input:** `expertise = [0, 0, 0, 1]`, `skill = [10, 2, 3, 4]`

**Output:** `7`

**Explanation:** The optimal selection is [3, 4] with 1 marketing expert and 1 developer. The sum of skills is 3 + 4 = 7. Hence the answer is 7.

## Constraints

- `:)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
