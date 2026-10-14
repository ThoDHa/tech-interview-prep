"""Validate Binary Search Tree: https://leetcode.com/problems/validate-binary-search-tree/

Write-up & approaches: ../../docs/problems/validate_binary_search_tree.md

Given the `root` of a binary tree, determine whether it is a valid binary search
tree: every node's value must exceed all values in its left subtree and be less
than all values in its right subtree, recursively.

  uv run python validate_binary_search_tree/solution.py   # debug one case (see CASE below)
  uv run pytest validate_binary_search_tree/              # run the test sets
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
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isValidBST above, then run this file.
    # The case stores the tree as a level-order array; we marshal it to TreeNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().isValidBST(root)
    print(f"case {case['id']}: tree = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
