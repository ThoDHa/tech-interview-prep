"""Search a Row and Column Sorted Matrix — https://www.fastprep.io/problems/amazon-search-row-column-sorted-matrix

Write-up & approaches: ../../../docs/amazon/amazon-search-row-column-sorted-matrix.md

Reference implementation of the write-up's recommended Staircase
Search from the Top-Right Corner solution. Your own attempt lives in
solution.py.

  uv run python amazon/amazon-search-row-column-sorted-matrix/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-search-row-column-sorted-matrix/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """Return whether `target` occurs anywhere in the sorted matrix.

        The walk starts at the top-right corner, the one cell that is
        maximal in its row and minimal in its column. Each comparison
        eliminates a whole line: smaller than `target` discards the
        column's remainder above (move down), larger discards the row's
        remainder to the left (move left). Every step lands on the
        top-right corner of the surviving submatrix, so the argument
        repeats until the value is met or the grid is left.

        Args:
            matrix: Rectangular, nonempty; each row nondecreasing left
                to right, each column nondecreasing top to bottom; the
                page constraints give 1 <= m, n <= 300 and values in
                [-10^9, 10^9].
            target: The value to locate, in the same range.

        Returns:
            True when some cell equals `target`, False otherwise.

        Time:  O(m + n): every step discards one line, so the walk
               takes at most m + n - 1 steps.
        Space: O(1): the two walk indices.
        """
        row, column = 0, len(matrix[0]) - 1
        while row < len(matrix) and column >= 0:
            candidate = matrix[row][column]
            if candidate == target:
                return True
            if candidate < target:
                row += 1
            else:
                column -= 1
        return False


if __name__ == "__main__":
    # Debug playground: set a breakpoint in searchMatrix above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().searchMatrix(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
