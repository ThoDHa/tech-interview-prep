# [Count Max Num Teams](https://www.fastprep.io/problems/count-max-num-teams)

**Easy** | **NN minutes** | **Array, Sorting, Sliding Window**

Amazon is hosting a team hackathon.



1. Each team will have exactly teamSize developers.
2. A developer's skill level is denoted by skill[i].
3. The difference between the maximum and minimum skill levels within a team cannot exceed a threshold, maxDiff.

Determine the maximum number of teams that can be formed from the contestants.



Complete the function countMaxNumTeams which has the following parameters



int skill[n]: the developers' skill levels
int teamSize: the number of developers to make up a team
int maxDiff: the threshold value.

int: the maximum number of teams that can be formed at one time

## Examples

### Example 1

**Input:** `skill = [3, 4, 3, 1, 6, 5]`, `teamSize = 3`, `maxDiff = 2`

**Output:** `2`

**Explanation:** At most, 2 teams can be formed: [3, 3, 1] and [4, 6, 5].The difference between the maximum and minimum skill levels is 2 in each case, which does not exceed the threshold value of 2

## Constraints

- `1 ≤ teamSize ≤ n ≤ 105`
- `1 ≤ maxDiff ≤ 109`
- `1 ≤ skill[i] ≤ 109`
- `Only one valid answer exists.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
