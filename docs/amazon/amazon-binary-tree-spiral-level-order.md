# [Binary Tree Spiral Level Order](https://www.fastprep.io/problems/amazon-binary-tree-spiral-level-order)

**Medium** | **NN minutes** | **Tree, Breadth First Search, Depth First Search**

Return the values of a binary tree one level at a time in alternating directions.

For this exercise, assume the root level is traversed left to right, the next level right to left, and directions alternate thereafter. Group values by their distance from the root and omit missing children. Preserve node positions even when values repeat. An empty tree returns an empty list.

## Examples

### Example 1

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `[[3],[20,9],[15,7]]`

**Explanation:** The root is left-to-right, the second level is right-to-left, and the third returns to left-to-right.

### Example 2

**Input:** `root = [1,2,3,4,null,null,5]`

**Output:** `[[1],[3,2],[4,5]]`

**Explanation:** Null links are skipped; the second level is [3,2] and the third is [4,5].

### Example 3

**Input:** `root = []`

**Output:** `[]`

**Explanation:** An empty tree has no levels.

## Constraints

- `For this exercise, assume a finite acyclic binary tree with 0 through 500 nodes.`
- `-10^6 <= node.val <= 10^6.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
