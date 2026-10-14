"""Surrounded Regions — https://leetcode.com/problems/surrounded-regions/

Write-up & approaches: ../../docs/problems/surrounded_regions.md
Reference implementation of the write-up's Border DFS + Capture solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python surrounded_regions/reference.py   # debug one case (see CASE below)
  uv run pytest surrounded_regions/               # run the test sets
"""


class Solution:
    def solve(self, board):
        """Capture every 'O' region that does not touch the board's border.

        Marks every border-connected 'O' as 'B' (safe), then sweeps the
        board: remaining 'O' cells are captured to 'X', and the marked
        cells are restored to 'O'.

        Args:
            board: 2-D list of single-character strings, mutated in place.

        Returns:
            None: the capture happens inside `board`.

        Time:  O(rows · columns): every cell is visited a constant number
            of times (mark pass, sweep pass).
        Space: O(rows · columns): DFS recursion depth on an 'O'-filled
            board.
        """
        if not board:
            return
        rows, columns = len(board), len(board[0])

        def mark_safe(row: int, column: int) -> None:
            if not (0 <= row < rows and 0 <= column < columns):
                return
            if board[row][column] != "O":
                return
            board[row][column] = "B"
            mark_safe(row + 1, column)
            mark_safe(row - 1, column)
            mark_safe(row, column + 1)
            mark_safe(row, column - 1)

        for row in range(rows):
            mark_safe(row, 0)
            mark_safe(row, columns - 1)
        for column in range(columns):
            mark_safe(0, column)
            mark_safe(rows - 1, column)

        for row in range(rows):
            for column in range(columns):
                if board[row][column] == "O":
                    board[row][column] = "X"
                elif board[row][column] == "B":
                    board[row][column] = "O"


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # cases.json is empty (in-place mutation), so a literal example stands in.
    board = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    Solution().solve(board)
    print(f"args = {board}")
    print(f"got: {board}")
