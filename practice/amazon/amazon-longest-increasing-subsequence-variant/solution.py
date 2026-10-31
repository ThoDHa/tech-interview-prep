"""Longest Increasing Subsequence — https://www.fastprep.io/problems/amazon-longest-increasing-subsequence-variant

Write-up & approaches: ../../../docs/amazon/amazon-longest-increasing-subsequence-variant.md

Given an integer array nums, return the length of its longest strictly increasing subsequence.

  uv run python amazon/amazon-longest-increasing-subsequence-variant/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-longest-increasing-subsequence-variant/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def lengthOfLIS(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lengthOfLIS above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().lengthOfLIS(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
