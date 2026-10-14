"""Apply a Reversi Move — https://www.fastprep.io/problems/amazon-reversi-move-simulation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-reversi-move-simulation.md

Given a Reversi board board, a zero-based target cell row, col, and a player player equal to B or W, apply exactly one move.

  uv run python amazon_oa/amazon-reversi-move-simulation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-reversi-move-simulation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def applyReversiMove(self, board, row, col, player):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in applyReversiMove above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().applyReversiMove(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
