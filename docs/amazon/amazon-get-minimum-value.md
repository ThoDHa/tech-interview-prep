# [Get Min Value](https://www.fastprep.io/problems/amazon-get-minimum-value)

**Easy** | **NN minutes** | **Array, Greedy**

Amazon Prime Games is designing a game. The player needs to pass n rounds sequentially in this game. Rules of play are as follows:


The player loses power[i] health to complete round i.The player's health must be greater than 0 at all times.The player can choose to use armor in any one round. The armor will prevent damage of min(armor, power[i]).
Determine the minimum starting health for a player to win the game.

## Examples

### Example 1

**Input:** `power = [1, 2, 6, 7]`, `armor = 5`

**Output:** `12`

**Explanation:** Give the player 12 units of health at the beginning of the game. One of the optimal strategies is to use the armor in the third round and only lose 1 unit instead of 6. The health of the player after each round is:



Round 1: 12
Round 2: 11
Round 3: 9
Round 4: 8
Final: 1

Round, health



0. 12
1. 12 - power[0] = 12 - 1 = 11
2. 11 - power[1] = 11 - 2 = 9
3. 9 - power[2] + armor = 9 - 6 + 5 = 8
4. 8 - power[3] = 8 - 7 = 1
No lower starting health will allow a win.

## Constraints

- `power contains the per-round health cost for each of the n rounds, played sequentially.`
- `The armor may be applied to at most one round, reducing that round's damage by min(armor, power[i]).`
- `The player's health must remain strictly greater than 0 at all times.`
- `Return the minimum starting health that allows the player to complete all rounds.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
