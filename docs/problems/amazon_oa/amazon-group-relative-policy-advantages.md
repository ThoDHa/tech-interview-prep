# [Group-Relative Policy Advantages](https://www.fastprep.io/problems/amazon-group-relative-policy-advantages)

**Medium** | **NN minutes** | **Array, Hash Table, Math, Simulation**

Compute group-relative advantages for sampled policy responses. Response i belongs to groupIds[i] and receives the integer reward correctnessRewards[i] + formatRewards[i].

Within each group, compute the population mean and population standard deviation of the combined rewards. The advantage of a response is (reward - mean) / standardDeviation. When a group's standard deviation is zero, every response in that group has advantage zero.

Return the advantages in original response order, formatted to exactly six decimal places.

## Examples

### Example 1

**Input:** `groupIds = [0,0,1,1,1]`, `correctnessRewards = [1,0,1,1,0]`, `formatRewards = [1,0,0,1,0]`

**Output:** `["1.000000","-1.000000","0.000000","1.224745","-1.224745"]`

**Explanation:** Each prompt group is normalized independently after correctness and format rewards are combined.

### Example 2

**Input:** `groupIds = [7,7]`, `correctnessRewards = [1,1]`, `formatRewards = [0,0]`

**Output:** `["0.000000","0.000000"]`

**Explanation:** Equal rewards have zero variance, so both normalized advantages are zero.

## Constraints

- `2 <= groupIds.length <= 100000`
- `All three arrays have the same length.`
- `Each group ID appears at least twice.`
- `-100 <= correctnessRewards[i], formatRewards[i] <= 100`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
