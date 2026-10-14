"""Longest Common Subsequence — https://leetcode.com/problems/longest-common-subsequence/

Write-up & approaches: ../../docs/problems/longest_common_subsequence.md

Given two strings `text1` and `text2`, return the length of the *longest common subsequence* between the two strings if one exists, otherwise return `0`. A **subsequence** is a sequence that can be de

  uv run python longest_common_subsequence/solution.py   # debug one case (see CASE below)
  uv run pytest longest_common_subsequence/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestCommonSubsequence(self, text1, text2):
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
