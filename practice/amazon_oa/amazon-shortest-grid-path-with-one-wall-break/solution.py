"""Shortest Grid Path With One Wall Break — https://www.fastprep.io/problems/amazon-shortest-grid-path-with-one-wall-break

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-shortest-grid-path-with-one-wall-break.md

Given a rectangular binary matrix grid, a cell containing 1 is open and a cell containing 0 is a wall.

  uv run python amazon_oa/amazon-shortest-grid-path-with-one-wall-break/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-shortest-grid-path-with-one-wall-break/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumMovesWithOneWallBreak(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumMovesWithOneWallBreak above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumMovesWithOneWallBreak(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
