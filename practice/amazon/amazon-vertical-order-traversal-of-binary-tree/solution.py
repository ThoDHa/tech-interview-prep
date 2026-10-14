"""Vertical Order Traversal of a Binary Tree — https://www.fastprep.io/problems/amazon-vertical-order-traversal-of-binary-tree

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-vertical-order-traversal-of-binary-tree.md

You are given a binary tree serialized as a level-order array levelOrder. Each non-null token is a signed decimal integer, and the token "null" denotes a missing child.

  uv run python amazon_oa/amazon-vertical-order-traversal-of-binary-tree/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-vertical-order-traversal-of-binary-tree/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def verticalOrder(self, levelOrder):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in verticalOrder above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().verticalOrder(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
