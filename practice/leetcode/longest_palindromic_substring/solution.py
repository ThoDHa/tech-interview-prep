"""Longest Palindromic Substring: https://leetcode.com/problems/longest-palindromic-substring/

Write-up & approaches: ../../docs/problems/longest_palindromic_substring.md

Given a string `s`, return the longest palindromic substring in `s`. The answer
may not be unique; any longest palindromic substring is accepted.

  uv run python longest_palindromic_substring/solution.py   # debug one case (see CASE below)
  uv run pytest longest_palindromic_substring/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestPalindrome(self, s: str) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestPalindrome above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    # The answer can be non-unique, so the case stores the expected LENGTH; we
    # report whether the returned string is a valid longest palindromic substring.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    s = case["args"][0]
    result = Solution().longestPalindrome(s)
    expected_len = case["expected"]
    is_palindrome = result == result[::-1]
    is_substring = result in s
    ok = len(result) == expected_len and is_palindrome and is_substring
    print(f"case {case['id']}: s = {s!r}")
    print(f"expected: a palindromic substring of length {expected_len}")
    print(f"got:      {result!r} (len={len(result)}, palindrome={is_palindrome}, substring={is_substring})")
    print(f"valid:    {ok}")
