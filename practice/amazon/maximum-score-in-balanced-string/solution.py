"""Maximum Score in Balanced String — https://www.fastprep.io/problems/maximum-score-in-balanced-string

Write-up & approaches: ../../../docs/problems/amazon_oa/maximum-score-in-balanced-string.md

Given a string s consisting of parentheses, you need to find the maximum score possible in a balanced substring of s. The score of a substring is calculated by choosing two indices i and j (0 <= i < j

  uv run python amazon_oa/maximum-score-in-balanced-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/maximum-score-in-balanced-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumScoreInBalancedString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumScoreInBalancedString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumScoreInBalancedString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
