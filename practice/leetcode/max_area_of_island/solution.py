"""Max Area of Island — https://leetcode.com/problems/max-area-of-island/

Write-up & approaches: ../../docs/problems/max_area_of_island.md

You are given a matrix `grid` where `grid[i]` is either a `0` (representing water) or `1` (representing land). An island is defined as a group of `1`'s connected horizontally or vertically. You may as

  uv run python max_area_of_island/solution.py   # debug one case (see CASE below)
  uv run pytest max_area_of_island/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxAreaOfIsland(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxAreaOfIsland above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxAreaOfIsland(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
