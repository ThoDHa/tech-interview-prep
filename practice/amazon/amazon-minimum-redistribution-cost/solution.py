"""Minimum Redistribution Cost — https://www.fastprep.io/problems/amazon-minimum-redistribution-cost

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-redistribution-cost.md

There are n warehouses arranged in a circle. Warehouse i initially stores products[i] items.

  uv run python amazon_oa/amazon-minimum-redistribution-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-redistribution-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinimumRedistributionCost(self, products):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinimumRedistributionCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinimumRedistributionCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
