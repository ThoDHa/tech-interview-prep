"""Maximum Depth of Binary Tree: https://leetcode.com/problems/maximum-depth-of-binary-tree/

Write-up & approaches: ../../docs/problems/maximum_depth_of_binary_tree.md

Given the `root` of a binary tree, return its maximum depth (the number of nodes
along the longest path from the root down to the farthest leaf).

  uv run python maximum_depth_of_binary_tree/solution.py   # debug one case (see CASE below)
  uv run pytest maximum_depth_of_binary_tree/              # run the test sets
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
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxDepth above, then run this file.
    # The case stores the tree as a LeetCode level-order array; we marshal it here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().maxDepth(root)
    print(f"case {case['id']}: tree = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
