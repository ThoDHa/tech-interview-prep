"""01 Matrix: https://leetcode.com/problems/01-matrix/

Write-up & approaches: ../../docs/problems/01_matrix.md

Given an `m x n` binary matrix `mat`, return a matrix of the same size where each
cell holds the distance to the nearest `0`. Adjacent cells are distance `1` apart.

  uv run python 01_matrix/solution.py   # debug one case (see CASE below)
  uv run pytest 01_matrix/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in updateMatrix above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().updateMatrix(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
