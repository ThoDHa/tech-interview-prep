# [Lowest Common Ancestor in an Inserted BST](https://www.fastprep.io/problems/amazon-bst-lowest-common-ancestor)

**Easy** | **NN minutes** | **Tree, Binary Search**

Build a binary search tree by inserting the distinct values of insertionOrder from left to right. For each insertion, values smaller than the current node go left and larger values go right.

Return the value of the lowest common ancestor of the nodes containing p and q. A node may be an ancestor of itself.

## Examples

### Example 1

**Input:** `insertionOrder = [6,2,8,0,4,7,9,3,5]`, `p = 2`, `q = 8`

**Output:** `6`

**Explanation:** The two nodes lie on opposite sides of the root, so 6 is their lowest common ancestor.

### Example 2

**Input:** `insertionOrder = [6,2,8,0,4,7,9,3,5]`, `p = 2`, `q = 4`

**Output:** `2`

**Explanation:** The node containing 2 is an ancestor of the node containing 4.

### Example 3

**Input:** `insertionOrder = [5]`, `p = 5`, `q = 5`

**Output:** `5`

**Explanation:** A node is its own lowest common ancestor.

## Constraints

- `1 <= insertionOrder.length <= 100000.`
- `All values in insertionOrder are distinct integers.`
- `p and q both appear in insertionOrder.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
