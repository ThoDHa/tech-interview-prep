"""Trapping Rain Water — https://www.fastprep.io/problems/amazon-trapping-rain-water

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-trapping-rain-water.md

You are given an integer array height of length n. n vertical bars stand on the x-axis. The i-th bar has width 1 and height height[i].

  uv run python amazon_oa/amazon-trapping-rain-water/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-trapping-rain-water/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def trap(self, height):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in trap above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().trap(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
