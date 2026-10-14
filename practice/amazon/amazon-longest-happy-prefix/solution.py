"""Longest Happy Prefix — https://www.fastprep.io/problems/amazon-longest-happy-prefix

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-happy-prefix.md

A string is a happy prefix of s when it is a non-empty proper prefix of s and is also a suffix of s.

  uv run python amazon_oa/amazon-longest-happy-prefix/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-happy-prefix/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestPrefix(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestPrefix above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestPrefix(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
