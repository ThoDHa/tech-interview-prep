"""Palindromic Substrings — https://leetcode.com/problems/palindromic-substrings/

Write-up & approaches: ../../docs/problems/palindromic_substrings.md

Given a string `s`, return the number of substrings within `s` that are palindromes. A **palindrome** is a string that reads the same forward and backward.

  uv run python palindromic_substrings/solution.py   # debug one case (see CASE below)
  uv run pytest palindromic_substrings/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countSubstrings(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countSubstrings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countSubstrings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
