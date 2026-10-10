# [Lowest Common Ancestor Implemented with Stack](https://www.fastprep.io/problems/amazon-lowest-common-ancestor-implemented-with-stack)

**Medium** | **NN minutes** | **Tree, Stack, Hash Table**

This question was reported for Amazon Fall Intern onsite.

Given the root of a binary tree and two distinct nodes p and q in that tree, return their lowest common ancestor.

In this FastPrep version, the binary tree is provided as root, a level-order representation of the tree. Each non-null entry is an integer stored as a string, and "null" marks a missing child. The values p and q identify the two target nodes.

The lowest common ancestor of two nodes is the deepest node in the tree that has both p and q as descendants. A node may be considered a descendant of itself.

You should solve this problem iteratively. In particular, use a stack to traverse the tree and build a parent mapping for each visited node. Then use that parent information to find the first common ancestor of p and q.

A Note From OP

The original OP mentioned that the interviewer specifically required a stack-based solution. The approach they described was to use a stack to traverse the tree and build a parent map for every node. Then, starting from p, move upward to the root and store all ancestors in a set. Finally, starting from q, move upward toward the root; the first node that already appears in p's ancestor set is the lowest common ancestor.

Reference Choice

There are 3 "find lowest common ancestor" questions on LeetCode. 236 was selected as the reference because this source describes the LCA of exactly two existing nodes, p and q, in a normal binary tree.

It does not match 1644, because that variant changes the contract by allowing one or both target nodes to be missing from the tree. It also does not match 1676, because that variant asks for the LCA of multiple nodes, not just p and q.

Additional Practice Note

A super tiny interviewer-pattern prediction:::) if you are interested, you can also try solving the other two Lowest Common Ancestor variants with a stack-based approach. Given that this interviewer seems to be a fan of stacks, they may ask one LCA problem as the main interview question and use the other two LCA variants as follow-ups if time allows 😉

## Examples

### Example 1

**Input:** `root = ["10","5","15","3","7","12","18","null","4","6","8"]`, `p = 3`, `q = 8`

**Output:** `5`

**Explanation:** Node 5 is the lowest node that has both 3 and 8 in its subtree.

### Example 2

**Input:** `root = ["10","5","15","3","7","12","18","null","4","6","8"]`, `p = 5`, `q = 8`

**Output:** `5`

**Explanation:** A node can be an ancestor of itself. Since 5 is an ancestor of 8, the lowest common ancestor is 5.

## Constraints

- `2 <= root.length <= 10^5`
- `Each non-null entry in root is an integer in the range [-10^9, 10^9].`
- `All non-null node values are unique.`
- `p and q are distinct.`
- `Both p and q exist in the tree.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
