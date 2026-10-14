"""Count Promotional Periods — https://www.fastprep.io/problems/amazon-count-promotional-periods

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-promotional-periods.md

Data analysts at Amazon are studying product order patterns. They classify a period of at least three consecutive days as a promotional period when the order counts on the first and last days are both

  uv run python amazon_oa/amazon-count-promotional-periods/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-promotional-periods/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countPromotionalPeriods(self, orders):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countPromotionalPeriods above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countPromotionalPeriods(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
