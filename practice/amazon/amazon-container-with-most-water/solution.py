"""Container With Most Water — https://www.fastprep.io/problems/amazon-container-with-most-water

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-container-with-most-water.md

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).

  uv run python amazon_oa/amazon-container-with-most-water/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-container-with-most-water/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxArea(self, height):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxArea above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxArea(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
