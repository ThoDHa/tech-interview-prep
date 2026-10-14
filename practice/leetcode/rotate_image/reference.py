"""Rotate Image — https://leetcode.com/problems/rotate-image/

Write-up & approaches: ../../docs/problems/rotate_image.md
Canonical reference implementation: the write-up's Transpose then Reverse
Rows solution (in-place, two passes). Your own attempt lives in solution.py.

Given a square `n x n` matrix of integers `matrix`, rotate it by 90 degrees
clockwise, in place: column `i` read bottom-up becomes row `i`.

  uv run python rotate_image/reference.py   # replay the example cases
  uv run pytest rotate_image/               # run the test sets
"""

from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """Rotate the square matrix 90 degrees clockwise, in place.

        Transposes the matrix across the main diagonal (each off-diagonal
        pair swapped exactly once), then reverses every row so the former
        bottom-up column order reads left to right.

        Args:
            matrix: Square row-major matrix; mutated in place, returns None.

        Time:  O(n^2): the transpose performs n(n-1)/2 swaps and the row
            reversals at most n/2 swaps per row, together constant work
            per cell.
        Space: O(1): index variables and pairwise swap handoffs only.
        """
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                # j > i swaps each off-diagonal pair exactly once
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            left, right = 0, n - 1
            while left < right:
                row[left], row[right] = row[right], row[left]
                left += 1
                right -= 1


if __name__ == "__main__":
    # Debug playground: cases.json is empty (in-place mutation is not
    # `==`-assertable), so the statement's examples stand in.
    examples = {
        "example_1": [[1, 2], [3, 4]],
        "example_2": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    }
    expected = {
        "example_1": [[3, 1], [4, 2]],
        "example_2": [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
    }
    for case_id, matrix in examples.items():
        Solution().rotate(matrix)
        print(f"case {case_id}: expected {expected[case_id]}")
        print(f"got:      {matrix}")
