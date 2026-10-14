"""Capacity To Ship Packages Within D Days — https://www.fastprep.io/problems/amazon-capacity-to-ship-packages-within-d-days

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-capacity-to-ship-packages-within-d-days.md

A conveyor belt has packages that must be shipped from one port to another within days days.

  uv run python amazon_oa/amazon-capacity-to-ship-packages-within-d-days/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-capacity-to-ship-packages-within-d-days/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def shipWithinDays(self, weights, days):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in shipWithinDays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().shipWithinDays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
