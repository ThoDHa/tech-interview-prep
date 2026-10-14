"""Lowest Common Ancestor of a Binary Search Tree: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

Write-up & approaches: ../../docs/problems/lowest_common_ancestor_of_a_binary_search_tree.md

Given a binary search tree (BST) and two existing nodes `p` and `q`, return their
lowest common ancestor: the lowest node that has both `p` and `q` as descendants
(a node may be a descendant of itself).

  uv run python lowest_common_ancestor_of_a_binary_search_tree/solution.py   # debug one case (see CASE below)
  uv run pytest lowest_common_ancestor_of_a_binary_search_tree/              # run the test sets
"""

from harness import NotSolved, TreeNode, build_tree, find_tree_node, pick_case


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lowestCommonAncestor above, then run
    # this file. The case stores the tree as a level-order array plus p/q values;
    # we marshal it to TreeNodes here, the same way the test does.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    tree_array, p_val, q_val = case["args"]
    root = build_tree(tree_array)
    p_node = find_tree_node(root, p_val)
    q_node = find_tree_node(root, q_val)
    result = Solution().lowestCommonAncestor(root, p_node, q_node)
    print(f"case {case['id']}: tree = {tree_array}, p = {p_val}, q = {q_val}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result.val if result else None}")
