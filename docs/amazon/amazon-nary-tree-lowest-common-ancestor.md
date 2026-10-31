# [Lowest Common Ancestor in an N-ary Tree](https://www.fastprep.io/problems/amazon-nary-tree-lowest-common-ancestor)

**Medium** | **NN minutes** | **Tree, Hash Table**

A rooted N-ary tree has nodes labeled from 0 through n - 1. It is encoded by parent, where parent[root] = -1 and every other value gives the node's direct parent.

Given two valid node labels p and q, return their lowest common ancestor: the deepest node that is an ancestor of both. A node is an ancestor of itself.

## Examples

### Example 1

**Input:** `parent = [-1,0,0,1,1,2,2,3]`, `p = 7`, `q = 4`

**Output:** `1`

**Explanation:** Node 1 is the deepest shared ancestor of nodes 7 and 4.

### Example 2

**Input:** `parent = [-1,0,0,1,1,2,2]`, `p = 5`, `q = 6`

**Output:** `2`

**Explanation:** Both queried nodes are direct children of node 2.

## Constraints

- `1 <= parent.length <= 200000.`
- `Exactly one entry is -1; every other entry is a valid node label.`
- `The parent relationships form one connected acyclic rooted tree.`
- `0 <= p, q < parent.length.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
