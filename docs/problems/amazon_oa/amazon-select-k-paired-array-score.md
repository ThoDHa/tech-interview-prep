# [Select K Paired Indices for Maximum Score](https://www.fastprep.io/problems/amazon-select-k-paired-array-score)

**Medium** | **NN minutes** | **Array, Sorting, Heap, Greedy**

Select exactly k shared indices from two equal-length arrays. The score is the sum of selected values from first multiplied by the minimum selected value from second.

Return the maximum score.

## Examples

### Example 1

**Input:** `first = [1,3,3,2]`, `second = [2,1,3,4]`, `k = 3`

**Output:** `12`

**Explanation:** Case 1 exercises the documented deterministic contract.

### Example 2

**Input:** `first = [4,2,3,1,1]`, `second = [7,5,10,9,6]`, `k = 1`

**Output:** `30`

**Explanation:** Case 2 exercises the documented deterministic contract.

### Example 3

**Input:** `first = [2,1,14,12]`, `second = [11,7,13,6]`, `k = 3`

**Output:** `168`

**Explanation:** Case 3 exercises the documented deterministic contract.

## Constraints

- `1 <= k <= first.length == second.length <= 100000.`
- `All values are positive integers.`
- `The answer fits a signed 32-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
