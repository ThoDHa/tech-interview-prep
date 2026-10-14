"""Longest Increasing Subsequence With Bounded Adjacent Difference — https://www.fastprep.io/problems/amazon-longest-increasing-subsequence-bounded-difference

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-increasing-subsequence-bounded-difference.md

Given a non-empty integer array arr and a non-negative integer k, return the maximum length of a subsequence that satisfies all of the following:

  uv run python amazon_oa/amazon-longest-increasing-subsequence-bounded-difference/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-increasing-subsequence-bounded-difference/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestBoundedIncreasingSubsequence(self, arr, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestBoundedIncreasingSubsequence above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestBoundedIncreasingSubsequence(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
