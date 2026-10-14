"""Binary Tree Cameras — https://www.fastprep.io/problems/amazon-binary-tree-cameras

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-binary-tree-cameras.md

You are given the root of a binary tree. You may install cameras on its nodes.

  uv run python amazon_oa/amazon-binary-tree-cameras/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-binary-tree-cameras/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minCameraCover(self, root):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCameraCover above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCameraCover(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
