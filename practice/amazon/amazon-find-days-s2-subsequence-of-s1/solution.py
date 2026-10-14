"""Find Days S2 Subsequence of S1 — https://www.fastprep.io/problems/amazon-find-days-s2-subsequence-of-s1

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-days-s2-subsequence-of-s1.md

Given two strings s1 and s2, find till how many days is s2 a subsequence of s1 if on every day we delete all the strings in s1 from start to end inclusive.

  uv run python amazon_oa/amazon-find-days-s2-subsequence-of-s1/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-days-s2-subsequence-of-s1/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findDaysS2SubsequenceOfS1(self, s1, s2, start, end):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findDaysS2SubsequenceOfS1 above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findDaysS2SubsequenceOfS1(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
