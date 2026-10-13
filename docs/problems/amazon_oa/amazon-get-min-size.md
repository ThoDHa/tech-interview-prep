# [Get Min Size](https://www.fastprep.io/problems/amazon-get-min-size)

**Medium** | **NN minutes** | **Binary Search, Greedy, Sorting**

Within the Amazon Gaming Distribution System, a logistics coordinator is faced with the task of efficiently distributing n games among k different children. Each game is characterized by its size, denoted by gameSize[i] for 1 ≤ i ≤ n.



To facilitate the distribution process, the coordinator opts to utilize pen drives, ordering k pen drives with identical storage capacity. Each pen drive can receive a maximum of 2 games, and every child must receive at least one game, also no game should be left unassigned.



Considering the impracticality of transferring large game files over the internet, the strategy involves determining the minimum storage capacity required for the pen drives. A pen drive can only store games if the sum of their sizes does not exceed the pen drive's storage capacity.



What is the minimum storage capacity of pen drives that you must order to be able to give these games to the children?

## Examples

### Example 1

**Input:** `gameSize = [9, 2, 4, 6]`, `k = 3`

**Output:** `9`

**Explanation:** We note that we will need pen drives of the size of at least 9 units, to store the first game.

This also turns out to be the minimum size of pen drives that should be ordered to give the games to these children.

We can use the first pen drive to store the game of size 9, the 2nd one to store the second and third games, and the 3rd pen drive to store the fourth game.

Hence, the minimum capacity of pen drives required is 9 units.

## Constraints

- `1 ≤ k ≤ n ≤ 2 * 10^5`
- `1 ≤ gameSize[i] ≤ 10^9`
- `n ≤ 2*k`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
