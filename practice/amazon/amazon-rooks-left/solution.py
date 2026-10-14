"""Rooks Left — https://www.fastprep.io/problems/amazon-rooks-left

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-rooks-left.md

You are given a 2D grid board that represents a chessboard. The board contains multiple cells, where:

  uv run python amazon_oa/amazon-rooks-left/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-rooks-left/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def rooksLeft(self, board):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in rooksLeft above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().rooksLeft(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
