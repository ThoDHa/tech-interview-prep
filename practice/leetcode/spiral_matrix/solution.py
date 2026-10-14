"""Spiral Matrix: https://leetcode.com/problems/spiral-matrix/

Write-up & approaches: ../../docs/problems/spiral_matrix.md

Given an `m x n` matrix, return all elements of the matrix in spiral order.

  uv run python spiral_matrix/solution.py   # debug one case (see CASE below)
  uv run pytest spiral_matrix/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in spiralOrder above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().spiralOrder(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
