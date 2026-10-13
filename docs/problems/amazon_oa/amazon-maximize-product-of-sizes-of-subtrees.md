# [Maximize Product of Sizes of Subtrees](https://www.fastprep.io/problems/amazon-maximize-product-of-sizes-of-subtrees)

**Hard** | **NN minutes** | **Tree, Dynamic Programming, Greedy**

BREAKING! Its sister question was found --> Checkout LC 343. Integer Break <-- 



You are given a mystical tree with w nodes. Each node is connected to at least one other node by an edge. Your task is to sever one or more edges in the tree to split it into subtrees. The goal is to maximize the product of the sizes of these subtrees. The size of a subtree is defined as the number of nodes it contains. The product of subtree sizes is calculated by multiplying the sizes of all subtrees together.



Write a program that takes as input the number of nodes in the tree and the edges between them, and outputs the maximum product of subtree sizes achievable after severing edges in the tree.



Input Format



The first line of input contains an integer N, representing the number of nodes in the mystical tree.
The next N-1 lines each contain two space-separated integers U and V, signifying an edge between the respective nodes.



Output Format



Print a number X, representing the maximum product of subtree sizes achievable after edge deletions.

## Examples

### Example 1

**Input:** `w = 5`, `edges = [[1, 2], [2, 3], [3, 4], [4, 5]]`

**Output:** `6`

**Explanation:** Cut the 3-4 edge. Subtrees formed are 1-2-3 and 4-5, so the product is 3 * 2 = 6.

## Constraints

- `:)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
