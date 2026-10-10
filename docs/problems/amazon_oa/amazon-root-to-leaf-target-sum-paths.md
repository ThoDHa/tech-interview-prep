# [Root-to-Leaf Paths with a Target Sum](https://www.fastprep.io/problems/amazon-root-to-leaf-target-sum-paths)

**Medium** | **NN minutes** | **Tree, Depth First Search, Backtracking**

Given the root of a binary tree and an integer targetSum, return every root-to-leaf path whose node values add up to targetSum.

A leaf has no children. Return paths in left-to-right depth-first order, with each path listed from the root to its leaf.

## Examples

### Example 1

**Input:** `root = [5,4,8,11,null,13,4,7,2,null,null,5,1]`, `targetSum = 22`

**Output:** `[[5,4,11,2],[5,8,4,5]]`

**Explanation:** Both listed root-to-leaf paths sum to 22, and the left path is visited first.

### Example 2

**Input:** `root = [1,2,3]`, `targetSum = 5`

**Output:** `[]`

**Explanation:** Neither root-to-leaf path sums to 5.

### Example 3

**Input:** `root = []`, `targetSum = 0`

**Output:** `[]`

**Explanation:** An empty tree has no root-to-leaf path.

## Constraints

- `The tree contains between 0 and 500 nodes.`
- `-1000 ≤ Node.val ≤ 1000.`
- `-10^9 ≤ targetSum ≤ 10^9.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
