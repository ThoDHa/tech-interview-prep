"""Longest Perfect Anagrams — https://www.fastprep.io/problems/amazon-longest-perfect-anagrams

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-perfect-anagrams.md

Developers at Amazon continuously develop algorithms to ensure the security of users' accounts through strong passwords.

  uv run python amazon_oa/amazon-longest-perfect-anagrams/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-perfect-anagrams/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestPerfectAnagrams(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestPerfectAnagrams above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestPerfectAnagrams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
