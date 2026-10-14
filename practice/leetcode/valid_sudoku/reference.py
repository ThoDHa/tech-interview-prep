"""Valid Sudoku — https://leetcode.com/problems/valid-sudoku/

Write-up & approaches: ../../docs/problems/valid_sudoku.md

Canonical reference implementation: the write-up's optimal approach (one
pass with per-row, per-column, and per-box seen sets), kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python valid_sudoku/reference.py   # debug one case (see CASE below)
  uv run pytest valid_sudoku/               # run the test sets
"""

from harness import pick_case


class Solution:
    def isValidSudoku(self, board):
        """Check each digit against its row, column, and box seen sets.

        A board is valid exactly when no digit repeats in any unit, so one
        pass recording every digit in three sets per unit decides it.

        Time:  O(81) = O(1): a fixed 9 x 9 board, each cell visited once.
        Space: O(1): at most 27 sets bounded by 9 entries each.
        """
        rows = [set() for _ in range(9)]
        columns = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                value = board[r][c]
                if value == ".":
                    continue
                box = (r // 3) * 3 + c // 3
                if (
                    value in rows[r]
                    or value in columns[c]
                    or value in boxes[box]
                ):
                    return False
                rows[r].add(value)
                columns[c].add(value)
                boxes[box].add(value)
        return True


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isValidSudoku above, then run this
    # file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isValidSudoku(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
