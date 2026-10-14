"""Longest Increasing Subsequence — https://leetcode.com/problems/longest-increasing-subsequence/

Write-up & approaches: ../../docs/problems/longest_increasing_subsequence.md

Given an integer array `nums`, return the *length* of the longest strictly *increasing* subsequence. A **subsequence** is a sequence that can be derived from the given sequence by deleting some or no 

  uv run python longest_increasing_subsequence/solution.py   # debug one case (see CASE below)
  uv run pytest longest_increasing_subsequence/              # run the test sets
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
