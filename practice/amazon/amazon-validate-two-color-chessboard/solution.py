"""Validate a Two-Color Chessboard — https://www.fastprep.io/problems/amazon-validate-two-color-chessboard

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-validate-two-color-chessboard.md

You are given a nonempty rectangular integer matrix board. Every cell is one of two colors, encoded as 0 or 1.

  uv run python amazon_oa/amazon-validate-two-color-chessboard/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-validate-two-color-chessboard/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isValidChessboard(self, board):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isValidChessboard above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isValidChessboard(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
