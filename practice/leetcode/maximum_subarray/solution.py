"""Maximum Subarray: https://leetcode.com/problems/maximum-subarray/

Write-up & approaches: ../../docs/problems/maximum_subarray.md

Given an integer array `nums`, find the contiguous subarray (containing at least
one number) which has the largest sum and return its sum.

  uv run python maximum_subarray/solution.py     # debug one case (see CASE below)
  uv run pytest maximum_subarray/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSubArray above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSubArray(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
