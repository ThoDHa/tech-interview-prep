"""Largest Rectangle in Histogram: https://leetcode.com/problems/largest-rectangle-in-histogram/

Write-up & approaches: ../../docs/problems/largest_rectangle_in_histogram.md

Given an array of integers `heights` representing a histogram's bar heights where
each bar has width `1`, return the area of the largest rectangle in the histogram.

  uv run python largest_rectangle_in_histogram/solution.py     # debug one case (see CASE below)
  uv run pytest largest_rectangle_in_histogram/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in largestRectangleArea above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().largestRectangleArea(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
