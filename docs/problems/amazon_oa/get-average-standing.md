# [Get Average Standing](https://www.fastprep.io/problems/get-average-standing)

**Medium** | **NN minutes** | **Array, Sorting, Math**

As an aspiring developer, you are required to develop a result analysis service for a car game on Amazon games.



There are n even records of d players who participated in different events in form of [race id, player's id, player's time]. For some race id, a player's ranking id decided based on the increasing order of their finish time. If two players have the same finish time, the one with a lower id is ranked lower.



The average standing of any player is the average of their various positions in all the races they competed in, expressed in the form of a fraction p/q. If there are multiple possible such fractions, reduce them such that p is the minimum possible.



Return a 2-dimensional array where each element i contains the ith player's p and q as described above. If the player did not compete in any races, the player's p and q values are both -1.



Complete the function getAverageStanding which has the following parameters:



int d: the number of players
int records[n][3]: each record[i] contains [race id, player id, player time]

## Examples

### Example 1

**Input:** `d = 3`, `records = [[1, 1, 100], [1, 2, 200], [2, 1, 500]]`

**Output:** `[[-1, -1], [1, 1], [2, 1]]`

**Explanation:** There are a total of d = 3 players. 
- Player 0 did not compete in any race, so p0 = -1 and q0 = -1.

- Player 1 competed in 2 races and came first in both. Their average standing is (1+1)/2. Reduce as described so p1 = 1 and q1 = 1.

- Player 2 competed in 1 race and came second. Their average standing is (2)/1. Thus, p2 = 2 and q2 = 1.

## Constraints

- `N/A (If you know it, feel free to let us know ^^ tyvm!`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
