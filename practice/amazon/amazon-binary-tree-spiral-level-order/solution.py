"""Binary Tree Spiral Level Order — https://www.fastprep.io/problems/amazon-binary-tree-spiral-level-order

Write-up & approaches: ../../../docs/amazon/amazon-binary-tree-spiral-level-order.md

Return the values of a binary tree one level at a time in alternating directions.

  uv run python amazon/amazon-binary-tree-spiral-level-order/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-binary-tree-spiral-level-order/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def zigzagLevels(self, root):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in zigzagLevels above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().zigzagLevels(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
