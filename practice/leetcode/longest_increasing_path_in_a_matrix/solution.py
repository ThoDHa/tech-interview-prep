"""Longest Increasing Path In a Matrix — https://leetcode.com/problems/longest-increasing-path-in-a-matrix/

Write-up & approaches: ../../docs/problems/longest_increasing_path_in_a_matrix.md

You are given a 2-D grid of integers `matrix`, where each integer is greater than or equal to `0`. Return the length of the longest strictly increasing path within `matrix`. From each cell within the 

  uv run python longest_increasing_path_in_a_matrix/solution.py   # debug one case (see CASE below)
  uv run pytest longest_increasing_path_in_a_matrix/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestIncreasingPath(self, matrix):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestIncreasingPath above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestIncreasingPath(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
