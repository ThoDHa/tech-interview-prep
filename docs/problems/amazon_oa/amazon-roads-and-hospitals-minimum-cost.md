# [Minimum Cost for Roads and Hospitals](https://www.fastprep.io/problems/amazon-roads-and-hospitals-minimum-cost)

**Medium** | **NN minutes** | **Graph, Union Find, Greedy**

Cities are labeled from 0 to cityCount - 1. A hospital can be built in any city for hospitalCost, and any listed undirected road can be built for roadCost.

Choose hospitals and roads at minimum total cost so every city can reach a hospital.

## Examples

### Example 1

**Input:** `cityCount = 3`, `possibleRoads = [[0,1],[1,2]]`, `hospitalCost = 3`, `roadCost = 2`

**Output:** `7`

**Explanation:** Case 1 exercises the documented deterministic contract.

### Example 2

**Input:** `cityCount = 3`, `possibleRoads = [[0,1]]`, `hospitalCost = 2`, `roadCost = 5`

**Output:** `6`

**Explanation:** Case 2 exercises the documented deterministic contract.

### Example 3

**Input:** `cityCount = 5`, `possibleRoads = [[0,1],[2,3]]`, `hospitalCost = 6`, `roadCost = 1`

**Output:** `20`

**Explanation:** Case 3 exercises the documented deterministic contract.

## Constraints

- `1 <= cityCount <= 200000.`
- `0 <= possibleRoads.length <= 200000.`
- `Costs are positive and the answer fits a signed 32-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
