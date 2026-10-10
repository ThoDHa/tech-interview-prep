"""Longest Subarray with K Distinct Values — https://www.fastprep.io/problems/amazon-longest-subarray-with-k-distinct

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-subarray-with-k-distinct.md

Given an integer array nums and an integer k, return the longest contiguous subarray containing exactly k distinct values.

  uv run python amazon_oa/amazon-longest-subarray-with-k-distinct/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-subarray-with-k-distinct/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestSubarrayWithKDistinct(self, nums, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestSubarrayWithKDistinct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestSubarrayWithKDistinct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
