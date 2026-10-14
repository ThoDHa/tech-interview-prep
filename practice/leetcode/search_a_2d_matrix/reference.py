"""Search a 2D Matrix — https://leetcode.com/problems/search-a-2d-matrix/

Write-up & approaches: ../../docs/problems/search_a_2d_matrix.md
Reference implementation of the write-up's Single Binary Search solution.

You are given an `m x n` 2-D integer array `matrix` and an integer `target`. Each row in `matrix` is sorted in non-decreasing order, and the first integer of every row is greater than the last integer of the previous row. Return `true` if `target` exists within `matrix` or `false` otherwise.

  uv run python search_a_2d_matrix/reference.py   # debug one case (see CASE below)
  uv run pytest search_a_2d_matrix/              # run the test sets
"""

from harness import pick_case


class Solution:
    def searchMatrix(self, matrix, target):
        """Report whether `target` occurs in the row-major-sorted `matrix`.

        Treats the matrix as one virtual sorted list of m * n entries and
        binary searches it, decoding a virtual position into
        matrix[position // n][position % n].

        Args:
            matrix: Rows sorted ascending; each row's first value exceeds
                the previous row's last value.
            target: The value to find.

        Returns:
            True when `target` is present, False otherwise.

        Time:  O(log(m * n)): one binary search over the virtual flat list.
        Space: O(1): only search-boundary variables.
        """
        rows, columns = len(matrix), len(matrix[0])
        left, right = 0, rows * columns - 1
        while left <= right:
            mid = (left + right) // 2
            value = matrix[mid // columns][mid % columns]
            if value == target:
                return True
            if value < target:
                left = mid + 1
            else:
                right = mid - 1
        return False


if __name__ == "__main__":
    # Debug playground: set a breakpoint in searchMatrix above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().searchMatrix(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
