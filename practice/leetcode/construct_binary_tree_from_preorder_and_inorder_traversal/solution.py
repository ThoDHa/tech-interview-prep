"""Construct Binary Tree from Preorder and Inorder Traversal: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Write-up & approaches: ../../docs/problems/construct_binary_tree_from_preorder_and_inorder_traversal.md

Given preorder and inorder traversals of a binary tree (with unique values),
reconstruct and return the tree.

  uv run python construct_binary_tree_from_preorder_and_inorder_traversal/solution.py   # debug one case (see CASE below)
  uv run pytest construct_binary_tree_from_preorder_and_inorder_traversal/              # run the test sets
"""

from typing import List, Optional

from harness import NotSolved, TreeNode, build_tree, tree_to_list, pick_case


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in buildTree above, then run this file.
    # The case stores preorder/inorder as plain arrays; we marshal the expected
    # output to a level-order list for comparison.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    preorder, inorder = case["args"]
    result = Solution().buildTree(preorder, inorder)
    print(f"case {case['id']}: preorder = {preorder}, inorder = {inorder}")
    print(f"expected: {case['expected']}")
    print(f"got:      {tree_to_list(result)}")
