"""Minimum Moves to Capture the King — https://www.fastprep.io/problems/amazon-minimum-moves-to-capture-king

Write-up & approaches: ../../../docs/amazon/amazon-minimum-moves-to-capture-king.md

A piece starts at start on an empty rows-by-cols board and must capture the king at king.

  uv run python amazon/amazon-minimum-moves-to-capture-king/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-minimum-moves-to-capture-king/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumMovesToCaptureKing(self, rows, cols, start, king, directions):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumMovesToCaptureKing above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumMovesToCaptureKing(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
