"""Determine the Best Skipping Strategy — https://www.fastprep.io/problems/amazon-determine-the-best-skipping-strategy

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-determine-the-best-skipping-strategy.md

A company operates numerous warehouses, with each warehouse i holding inventory[i] units of a particular product. You and your co-worker are responsible for dispatching these items to fulfill customer

  uv run python amazon_oa/amazon-determine-the-best-skipping-strategy/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-determine-the-best-skipping-strategy/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxPoints(self, inventory, dispatch1, dispatch2, skips):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxPoints above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxPoints(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
