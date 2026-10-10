"""Minimum Grid Inconvenience — https://www.fastprep.io/problems/amazon-minimum-grid-inconvenience

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-grid-inconvenience.md

A city is represented by a binary grid. A cell marked 1 is a delivery center, and a cell marked 0 is any other place.

  uv run python amazon_oa/amazon-minimum-grid-inconvenience/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-grid-inconvenience/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinInconvenience(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinInconvenience above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinInconvenience(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
