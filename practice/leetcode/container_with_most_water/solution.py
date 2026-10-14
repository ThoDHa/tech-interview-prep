"""Container With Most Water: https://leetcode.com/problems/container-with-most-water/

Write-up & approaches: ../../docs/problems/container_with_most_water.md

Given an integer array `height` of `n` vertical lines, find two lines that with
the x-axis form a container holding the most water, and return that maximum area.

  uv run python container_with_most_water/solution.py     # debug one case (see CASE below)
  uv run pytest container_with_most_water/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxArea above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxArea(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
