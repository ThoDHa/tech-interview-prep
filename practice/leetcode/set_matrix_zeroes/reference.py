"""Set Matrix Zeroes — https://leetcode.com/problems/set-matrix-zeroes/

Write-up & approaches: ../../docs/problems/set_matrix_zeroes.md
Canonical reference implementation: the write-up's First Row and Column as
Flags solution (in place, O(1) extra space). Your own attempt lives in
solution.py.

Given an `m x n` matrix of integers `matrix`, if an element is `0`, set its
entire row and column to `0`'s, in place.

  uv run python set_matrix_zeroes/reference.py   # replay the example cases
  uv run pytest set_matrix_zeroes/               # run the test sets
"""

from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """Zero every row and column containing an original 0, in place.

        Reads both border verdicts up front, writes row flags into column 0
        and column flags into row 0 during an interior scan, applies the
        flags to the interior, then zeroes the two borders from their
        verdicts.

        Args:
            matrix: Row-major m x n matrix; mutated in place, returns None.

        Time:  O(m * n): interior record and apply sweeps plus three
            linear border passes.
        Space: O(1): two border booleans; all other flags live in the
            matrix's own first row and column.
        """
        m, n = len(matrix), len(matrix[0])

        # Both verdicts read before any flag write buries the originals
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    # Row i's flag in column 0, column j's flag in row 0
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0
        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0


if __name__ == "__main__":
    # Debug playground: cases.json is empty (in-place mutation is not
    # `==`-assertable), so the statement's examples stand in.
    examples = {
        "example_1": [[0, 1], [1, 0]],
        "example_2": [[1, 2, 3], [4, 0, 5], [6, 7, 8]],
    }
    expected = {
        "example_1": [[0, 0], [0, 0]],
        "example_2": [[1, 0, 3], [0, 0, 0], [6, 0, 8]],
    }
    for case_id, matrix in examples.items():
        Solution().setZeroes(matrix)
        print(f"case {case_id}: expected {expected[case_id]}")
        print(f"got:      {matrix}")
