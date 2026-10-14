"""Validate Binary Search Tree: https://leetcode.com/problems/validate-binary-search-tree/

Write-up & approaches: ../../../docs/leetcode/validate_binary_search_tree.md

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
        self.previous = None
        return self.inNode(root)

    def inNode(self, root: Optional[TreeNode]) -> bool:
        """Visit very node in order in the tree, if the last node is always greater than
            the current node, then it's a valid BST
        """
        if root is None:
            return True
        if not self.inNode(root.left):
            return False

        if self.previous and root.val <= self.previous:
            return False
        self.previous = root.val

        return self.inNode(root.right)

    def isBST(self, root: Optional[TreeNode], min: int, max: int) -> bool:
        if root is None:
            return True

        if min >= root.val:
            return False
        if max <= root.val:
            return False
        return self.isBST(root.left, min, root.val) and self.isBST(root.right, root.val, max)

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
