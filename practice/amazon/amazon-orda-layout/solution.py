"""Ordered Confirguration — https://www.fastprep.io/problems/amazon-orda-layout

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-orda-layout.md

Note - Feel free to checkout the source image for the original statement :) 🐳

  uv run python amazon_oa/amazon-orda-layout/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-orda-layout/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def ordaLayout(self, layout):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in ordaLayout above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().ordaLayout(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
