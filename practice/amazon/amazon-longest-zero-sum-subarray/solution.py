"""Longest Zero Sum Subarray — https://www.fastprep.io/problems/amazon-longest-zero-sum-subarray

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-zero-sum-subarray.md

You are given an integer array nums containing positive and negative integers.

  uv run python amazon_oa/amazon-longest-zero-sum-subarray/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-zero-sum-subarray/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestZeroSumSubarray(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestZeroSumSubarray above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestZeroSumSubarray(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
