"""Binary Tree Maximum Path Sum: https://leetcode.com/problems/binary-tree-maximum-path-sum/

Write-up & approaches: ../../docs/problems/binary_tree_maximum_path_sum.md

Given the `root` of a binary tree, return the maximum path sum of any non-empty
path. A path is a sequence of nodes connected by edges, each node used at most
once, and it need not pass through the root.

  uv run python binary_tree_maximum_path_sum/solution.py     # debug one case (see CASE below)
  uv run pytest binary_tree_maximum_path_sum/                # run the test sets
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
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxPathSum above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().maxPathSum(root)
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
