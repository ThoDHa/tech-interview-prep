"""Diameter of Binary Tree: https://leetcode.com/problems/diameter-of-binary-tree/

Write-up & approaches: ../../docs/problems/diameter_of_binary_tree.md

Given the `root` of a binary tree, return the length of the diameter of the tree:
the number of edges on the longest path between any two nodes, which may or may
not pass through the root.

  uv run python diameter_of_binary_tree/solution.py     # debug one case (see CASE below)
  uv run pytest diameter_of_binary_tree/                # run the test sets
"""

from typing import Optional

from harness import NotSolved, TreeNode, build_tree, pick_case


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in diameterOfBinaryTree above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().diameterOfBinaryTree(root)
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
