"""Lexicographically Smallest Palindrome Possible — https://www.fastprep.io/problems/amazon-lexicographically-smallest-palindrome-possible

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-lexicographically-smallest-palindrome-possible.md

Given a String, return the lexicographically smallest palindrome possible or -1.

  uv run python amazon_oa/amazon-lexicographically-smallest-palindrome-possible/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-lexicographically-smallest-palindrome-possible/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getSmallestPalindrome(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getSmallestPalindrome above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getSmallestPalindrome(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
