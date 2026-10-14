"""Minimum Moves for Two Knights to Meet — https://www.fastprep.io/problems/amazon-two-knights-minimum-meeting-moves

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-two-knights-minimum-meeting-moves.md

Two knights start at coordinates first = [x1, y1] and second = [x2, y2] on an infinite chessboard. They take turns, with the first knight moving first. On a turn, the chosen knight must make one stand

  uv run python amazon_oa/amazon-two-knights-minimum-meeting-moves/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-two-knights-minimum-meeting-moves/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumKnightMeetingMoves(self, first, second):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumKnightMeetingMoves above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumKnightMeetingMoves(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
