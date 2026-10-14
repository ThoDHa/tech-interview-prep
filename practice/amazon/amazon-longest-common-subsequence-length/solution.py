"""Longest Common Subsequence Length — https://www.fastprep.io/problems/amazon-longest-common-subsequence-length

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-common-subsequence-length.md

Given two lowercase strings first and second, return the length of their longest common subsequence.

  uv run python amazon_oa/amazon-longest-common-subsequence-length/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-common-subsequence-length/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestCommonSubsequence(self, first, second):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestCommonSubsequence above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestCommonSubsequence(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
