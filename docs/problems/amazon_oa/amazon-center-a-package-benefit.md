# [Maximize Center A Package Benefit](https://www.fastprep.io/problems/amazon-center-a-package-benefit)

**Medium** | **NN minutes** | **Array, Greedy, Sorting**

Two distribution centers, A and B, must allocate n packages. Package i is worth benefitA[i] to Center A and benefitB[i] to Center B.

The array linkedPairs contains disjoint pairs [x, y]. For each linked pair, exactly one package goes to A and the other goes to B; A receives whichever of the two packages has the larger A-benefit. Packages that do not appear in any linked pair are independent.

Order the independent packages by decreasing benefitA[i] + benefitB[i], breaking a tie by smaller package index. Center A receives the first independent package in that order and then every other package; Center B receives the remaining independent packages.

## Examples

### Example 1

**Input:** `benefitA = [8,3,7,4]`, `benefitB = [1,9,2,6]`, `linkedPairs = [[0,1]]`

**Output:** `12`

**Explanation:** From linked pair [0,1], A takes package 0 for benefit 8. Independent packages 2 and 3 have combined benefits 9 and 10, so their order is 3,2. A receives package 3 for another 4, giving 12.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-center-a-package-benefit; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
