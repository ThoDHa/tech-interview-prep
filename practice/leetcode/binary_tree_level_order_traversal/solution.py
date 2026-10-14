"""Binary Tree Level Order Traversal: https://leetcode.com/problems/binary-tree-level-order-traversal/

Write-up & approaches: ../../docs/problems/binary_tree_level_order_traversal.md

Given the `root` of a binary tree, return the level order traversal of its nodes'
values (from left to right, level by level).

  uv run python binary_tree_level_order_traversal/solution.py   # debug one case (see CASE below)
  uv run pytest binary_tree_level_order_traversal/              # run the test sets
"""

from typing import List, Optional

from harness import NotSolved, TreeNode, build_tree, pick_case


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in levelOrder above, then run this file.
    # The case stores the tree as a LeetCode level-order array; we marshal it here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().levelOrder(root)
    print(f"case {case['id']}: tree = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
