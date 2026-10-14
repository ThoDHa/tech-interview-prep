"""About Mortgage — https://www.fastprep.io/problems/amazon-maximum-number-of-days-to-survive

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-number-of-days-to-survive.md

A lender lent money to a borrower, each day a different lender lent the money to the borrower.

  uv run python amazon_oa/amazon-maximum-number-of-days-to-survive/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-number-of-days-to-survive/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumNumberOfDaysToSurvive(self, lender, payback):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumNumberOfDaysToSurvive above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumNumberOfDaysToSurvive(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
