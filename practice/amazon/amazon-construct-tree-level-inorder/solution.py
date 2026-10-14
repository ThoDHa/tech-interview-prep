"""Construct a Tree from Level-Order and Inorder Traversals — https://www.fastprep.io/problems/amazon-construct-tree-level-inorder

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-construct-tree-level-inorder.md

Given the levelOrder and inorder traversals of the same binary tree, reconstruct and return its root.

  uv run python amazon_oa/amazon-construct-tree-level-inorder/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-construct-tree-level-inorder/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def buildTree(self, levelOrder, inorder):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in buildTree above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().buildTree(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
