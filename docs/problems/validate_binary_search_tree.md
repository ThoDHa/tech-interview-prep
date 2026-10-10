# [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)

**Medium** | **30 minutes** | **Tree, Depth-First Search, Binary Search Tree, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal)

**Practice:** [`practice/validate_binary_search_tree/solution.py`](../../practice/validate_binary_search_tree/solution.py)

Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A **valid BST** is defined as follows:

- The left subtree of a node contains only nodes with keys **less than** the node's key.
- The right subtree of a node contains only nodes with keys **greater than** the node's key.
- Both the left and right subtrees must also be binary search trees.

## Examples

### Example 1

![BST](assets/validate_binary_search_tree_example1.jpg)

**Input:** `root = [2,1,3]`

**Output:** `true`

### Example 2

![Invalid BST](assets/validate_binary_search_tree_example2.jpg)

**Input:** `root = [5,1,4,null,null,3,6]`

**Output:** `false`

**Explanation:** The root node's value is 5 but its right child's value is 4.

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

