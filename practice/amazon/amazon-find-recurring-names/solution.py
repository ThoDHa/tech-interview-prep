"""Find Recurring Name — https://www.fastprep.io/problems/amazon-find-recurring-names

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-recurring-names.md

Amazon rewards its new users with a discount coupon that can be applied to their first purchase. Some users create more than one account in order to receive the offer multiple times. It was found that

  uv run python amazon_oa/amazon-find-recurring-names/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-recurring-names/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findRecurringNames(self, realNames, allNames):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findRecurringNames above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findRecurringNames(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
