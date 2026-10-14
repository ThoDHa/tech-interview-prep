# [Count Games Won By Group1 (AMZ CN)](https://www.fastprep.io/problems/amazon-how-many-games-did-the-team-win)

**Medium** | **NN minutes** | **Sorting, Binary Search**

Amazon Games is organizing a tournament of pair games. There are two groups, firstTeam and secondTeam, each containing n players. The skill level of the i-th player in each group is firstTeam[i] and secondTeam[i].

For each pair of indices (i, j) with 0 <= i < j < n, the pair (firstTeam[i], firstTeam[j]) competes against (secondTeam[i], secondTeam[j]). The first team wins that game if firstTeam[i] + firstTeam[j] > secondTeam[i] + secondTeam[j].

Return the number of games won by the first team, modulo 10^9 + 7.

## Examples

### Example 1

**Input:** `n = 3`, `firstTeam = [1, 2, 3]`, `secondTeam = [3, 2, 1]`

**Output:** `1`

**Explanation:** The possible index pairs are (0, 1), (0, 2), and (1, 2).

(0, 1): 1 + 2 = 3 and 3 + 2 = 5, so the first team loses.(0, 2): 1 + 3 = 4 and 3 + 1 = 4, so the first team does not win.(1, 2): 2 + 3 = 5 and 2 + 1 = 3, so the first team wins.There is 1 winning game.

## Constraints

- `2 <= n <= 10^5`
- `firstTeam.length == secondTeam.length == n`
- `1 <= firstTeam[i], secondTeam[i] <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
