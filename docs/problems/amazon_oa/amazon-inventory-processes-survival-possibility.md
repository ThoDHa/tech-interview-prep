# [Inventory Processes Survival Possibility](https://www.fastprep.io/problems/amazon-inventory-processes-survival-possibility)

**Medium** | **NN minutes** | **Greedy, Math**

There are n inventory processes. Process i initially controls bots[i] bots.

In each round, choose any two remaining processes. The process with more bots defeats the other and absorbs all of its bots. If their bot counts are equal, either process may be chosen as the winner. Rounds continue until one process remains.

Return, in ascending order, the 1-based indices of all processes that can be the final survivor for at least one possible sequence of rounds.

## Examples

### Example 1

**Input:** `n = 5`, `bots = [1, 6, 2, 7, 2]`

**Output:** `[2, 4]`

**Explanation:** Process 2 can first absorb processes 1 and 3, growing from 6 to 9. It can then defeat process 4 and process 5, so it can finish with all 18 bots.

Process 4 can absorb processes 1 and 3, then defeat process 2 and process 5, so it can also finish with all 18 bots. No other process can survive every required matchup, so return [2, 4].

## Constraints

- `1 <= n <= 200000`
- `1 <= bots[i] <= 10^9`
- `bots.length = n`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
