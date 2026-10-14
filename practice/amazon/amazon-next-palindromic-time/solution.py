"""Next Palindromic Time — https://www.fastprep.io/problems/amazon-next-palindromic-time

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-next-palindromic-time.md

Given a valid 24-hour time time in HH:MM format, return the first strictly later time whose four digits form a palindrome.

  uv run python amazon_oa/amazon-next-palindromic-time/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-next-palindromic-time/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def nextPalindromicTime(self, time):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in nextPalindromicTime above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().nextPalindromicTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
