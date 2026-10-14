"""N Queens — https://leetcode.com/problems/n-queens/

Write-up & approaches: ../../docs/problems/n_queens.md
Canonical reference implementation of the write-up's Row-by-Row Backtracking
solution, kept next to the harness so authored cases stay falsifiable. Your
own attempt lives in solution.py.

  uv run python n_queens/reference.py   # debug one case (see below)
  uv run pytest n_queens/               # run the test sets
"""

from typing import List, Set


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """Return every distinct n-queens board as rows of '.' and 'Q' strings.

        Places one queen per row from top to bottom, tracking the occupied
        columns and both diagonal families in sets so each candidate cell is
        rejected or accepted in constant time; a full placement is rendered
        into the board strings and recorded.

        Args:
            n: Board edge length; also the number of queens (1 <= n <= 8-ish).

        Returns:
            All distinct solutions, each a list of `n` strings of length `n`.

        Time:  O(n!): row 0 has n candidates, row 1 at most n - 1, and the
            pruning only trims, never adds.
        Space: O(n): the three sets and the `queens` stack, plus the output.
        """
        columns: Set[int] = set()
        positive_diagonals: Set[int] = set()  # row + col is constant on a "/" diagonal
        negative_diagonals: Set[int] = set()  # row - col is constant on a "\" diagonal
        queens: List[int] = []
        boards: List[List[str]] = []

        def backtrack(row: int) -> None:
            if row == n:
                boards.append(["." * col + "Q" + "." * (n - col - 1) for col in queens])
                return
            for col in range(n):
                attacked = (
                    col in columns
                    or row + col in positive_diagonals
                    or row - col in negative_diagonals
                )
                if attacked:
                    continue
                columns.add(col)
                positive_diagonals.add(row + col)
                negative_diagonals.add(row - col)
                queens.append(col)
                backtrack(row + 1)
                columns.remove(col)
                positive_diagonals.remove(row + col)
                negative_diagonals.remove(row - col)
                queens.pop()

        backtrack(0)
        return boards


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solveNQueens above, then run this
    # file. cases.json is empty (any-order output), so a literal example
    # stands in.
    n = 4
    boards = Solution().solveNQueens(n)
    print(f"args = {n}")
    print(f"got: {boards}")
