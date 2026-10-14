"""Binary Tree Right View — https://www.fastprep.io/problems/amazon-binary-tree-right-view

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-binary-tree-right-view.md

Given the root of a binary tree, imagine viewing the tree from its right side.

  uv run python amazon_oa/amazon-binary-tree-right-view/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-binary-tree-right-view/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def rightSideView(self, root):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in rightSideView above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().rightSideView(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
