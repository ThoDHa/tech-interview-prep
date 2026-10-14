"""Cousins in Binary Tree II — https://www.fastprep.io/problems/amazon-cousins-in-binary-tree-ii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-cousins-in-binary-tree-ii.md

You are given a non-empty binary tree serialized as a level-order string array levelOrder. Each non-null token is a decimal integer, and "null" denotes a missing child.

  uv run python amazon_oa/amazon-cousins-in-binary-tree-ii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-cousins-in-binary-tree-ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def replaceValueInTree(self, levelOrder):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in replaceValueInTree above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().replaceValueInTree(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
