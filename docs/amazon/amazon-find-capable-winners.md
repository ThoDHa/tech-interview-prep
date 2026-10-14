# [Find Capable Winners](https://www.fastprep.io/problems/amazon-find-capable-winners)

**Hard** | **NN minutes** | **Sorting, Greedy, Array**

Amazon games have recently launched a new multi-player tournament on the platform. Each game of the tournament has 3 rounds. The players are provided with exactly three power boosters at the start of the game and each player is aware of the power boosters of their opponent. In each round, the player can choose to compete with any of the power boosters and any power booster can be used at most once in a particular game. In any particular round, the player with a higher power booster wins.



A player X is considered to be capable of defeating player Y if there exists a rearrangement of power boosters of X such that some rearrangement of power boosters of Y can be defeated in at least 2 out of the three rounds. For example, if power boosters of X = [9, 5, 11] and Y = [7, 12, 3], then


If Y uses the boosters in order [3, 7, 12] then X can use it in order [11, 9, 5] and X wins 2 out of the three games as 11 > 3 and 9 > 7. Thus X is capable of defeating Y.If X uses the boosters in order [5, 9, 11] then Y can use it in order [7, 12, 3] and Y wins 2 out of the three games as 7 > 5 and 12 > 9. Thus Y is also capable of defeating X.
Another example is if X = [1, 2, 3] and Y = [3, 4, 5]. Here X is not capable of defeating Y as any rearrangement of Y can not be defeated by X in at least two rounds.



Given the power boosters provided to n players where the three power boosters of the ith player are defined by (power_a[i], power_b[i], power_c[i]), find the number of players who are capable of defeating all other players in a game by using their power boosters optimally. It is guaranteed that all powers of each player's power boosters are distinct.

## Examples

### Example 1

**Input:** `power_a = [9, 4, 2]`, `power_b = [5, 12, 10]`, `power_c = [11, 3, 13]`

**Output:** `2`

**Explanation:** $24

## Constraints

- `2 ≤ n ≤ 10^5`
- `1 ≤ power_a[i], power_b[i], power_c[i] ≤ 10^9, where 0 ≤ i < n`
- `All power boosters of each player are pairwise distinct.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
