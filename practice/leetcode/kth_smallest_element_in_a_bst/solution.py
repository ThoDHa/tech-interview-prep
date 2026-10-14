"""Kth Smallest Element in a BST: https://leetcode.com/problems/kth-smallest-element-in-a-bst/

Write-up & approaches: ../../docs/problems/kth_smallest_element_in_a_bst.md

Given the `root` of a binary search tree and an integer `k`, return the `kth`
smallest value (1-indexed) of all the node values in the tree.

  uv run python kth_smallest_element_in_a_bst/solution.py   # debug one case (see CASE below)
  uv run pytest kth_smallest_element_in_a_bst/              # run the test sets
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
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in kthSmallest above, then run this file.
    # The case stores the tree as a level-order array; we marshal it to TreeNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    root = build_tree(case["args"][0])
    result = Solution().kthSmallest(root, case["args"][1])
    print(f"case {case['id']}: root = {case['args'][0]}, k = {case['args'][1]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
