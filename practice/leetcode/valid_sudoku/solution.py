"""Valid Sudoku — https://leetcode.com/problems/valid-sudoku/

Write-up & approaches: ../../docs/problems/valid_sudoku.md

You are given a `9 x 9` Sudoku board `board`. A Sudoku board is valid if the following rules are followed: 1. Each row must contain the digits `1-9` without duplicates. 2. Each column must contain the

  uv run python valid_sudoku/solution.py   # debug one case (see CASE below)
  uv run pytest valid_sudoku/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isValidSudoku(self, board):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isValidSudoku above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isValidSudoku(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
