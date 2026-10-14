"""Balanced Binary Tree: https://leetcode.com/problems/balanced-binary-tree/

Write-up & approaches: ../../docs/problems/balanced_binary_tree.md

Given a binary tree, determine if it is height-balanced (the left and right
subtrees of every node differ in height by no more than 1).

  uv run python balanced_binary_tree/solution.py   # debug one case (see CASE below)
  uv run pytest balanced_binary_tree/              # run the test sets
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
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isBalanced above, then run this file.
    # The case stores the tree as a level-order array; we marshal it to TreeNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().isBalanced(root)
    print(f"case {case['id']}: tree = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
