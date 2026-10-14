"""Trapping Rain Water — https://leetcode.com/problems/trapping-rain-water/

Write-up & approaches: ../../docs/problems/trapping_rain_water.md

Given `n` non-negative integers representing an elevation map where the width of
each bar is `1`, compute how much water it can trap after raining.

  uv run python trapping_rain_water/solution.py     # debug one case (see CASE below)
  uv run pytest trapping_rain_water/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def trap(self, height: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in trap above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().trap(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
