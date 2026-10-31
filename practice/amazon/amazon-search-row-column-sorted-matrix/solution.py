"""Search a Row and Column Sorted Matrix — https://www.fastprep.io/problems/amazon-search-row-column-sorted-matrix

Write-up & approaches: ../../../docs/amazon/amazon-search-row-column-sorted-matrix.md

Given a nonempty rectangular integer matrix matrix and an integer target, return true if the target occurs anywhere in the matrix, or false otherwise.

  uv run python amazon/amazon-search-row-column-sorted-matrix/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-search-row-column-sorted-matrix/              # run the test sets
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
