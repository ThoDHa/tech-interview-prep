"""Invert Binary Tree: https://leetcode.com/problems/invert-binary-tree/

Write-up & approaches: ../../docs/problems/invert_binary_tree.md

Given the `root` of a binary tree, invert it (swap every node's children) and
return the root.

  uv run python invert_binary_tree/solution.py   # debug one case (see CASE below)
  uv run pytest invert_binary_tree/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, TreeNode, build_tree, tree_to_list, pick_case


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in invertTree above, then run this file.
    # The case stores the tree as a level-order array; we marshal it to TreeNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().invertTree(root)
    print(f"case {case['id']}: tree = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {tree_to_list(result)}")
