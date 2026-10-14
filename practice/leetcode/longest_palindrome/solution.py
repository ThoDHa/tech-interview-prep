"""Longest Palindrome: https://leetcode.com/problems/longest-palindrome/

Write-up & approaches: ../../docs/problems/longest_palindrome.md

Given a string `s` of lowercase and/or uppercase letters, return the length of
the longest palindrome that can be built with those letters. Letters are case
sensitive, so "Aa" is not a palindrome here.

  uv run python longest_palindrome/solution.py     # debug one case (see CASE below)
  uv run pytest longest_palindrome/                # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestPalindrome(self, s: str) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestPalindrome above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestPalindrome(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
