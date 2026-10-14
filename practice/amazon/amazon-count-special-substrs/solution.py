"""Count Special Substrings — https://www.fastprep.io/problems/amazon-count-special-substrs

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-special-substrs.md

Imagine you're working with Amazon's data analysis team, specifically focusing on analyzing customer behavior through clickstream data. This data consists of sequences of user actions on the website, 

  uv run python amazon_oa/amazon-count-special-substrs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-special-substrs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countSpecialSubstrings(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countSpecialSubstrings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countSpecialSubstrings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
