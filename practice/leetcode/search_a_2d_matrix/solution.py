"""Search a 2D Matrix — https://leetcode.com/problems/search-a-2d-matrix/

Write-up & approaches: ../../docs/problems/search_a_2d_matrix.md

You are given an `m x n` 2-D integer array `matrix` and an integer `target`. * Each row in `matrix` is sorted in *non-decreasing* order. * The first integer of every row is greater than the last integ

  uv run python search_a_2d_matrix/solution.py   # debug one case (see CASE below)
  uv run pytest search_a_2d_matrix/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def searchMatrix(self, matrix, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in searchMatrix above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().searchMatrix(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
