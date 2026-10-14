"""Unique Paths: https://leetcode.com/problems/unique-paths/

Write-up & approaches: ../../docs/problems/unique_paths.md

A robot starts at the top-left of an `m x n` grid and may move only down or
right. Return the number of unique paths to reach the bottom-right corner.

  uv run python unique_paths/solution.py     # debug one case (see CASE below)
  uv run pytest unique_paths/                # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in uniquePaths above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().uniquePaths(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
