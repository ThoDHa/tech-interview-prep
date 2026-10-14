"""Swim In Rising Water — https://leetcode.com/problems/swim-in-rising-water/

Write-up & approaches: ../../docs/problems/swim_in_rising_water.md

You are given a square 2-D matrix of distinct integers `grid` where each integer `grid[i][j]` represents the elevation at position `(i, j)`. Rain starts to fall at time = `0`, which causes the water l

  uv run python swim_in_rising_water/solution.py   # debug one case (see CASE below)
  uv run pytest swim_in_rising_water/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def swimInWater(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in swimInWater above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().swimInWater(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
