"""Souvenir Shop Purchases — https://www.fastprep.io/problems/amazon-souvenir-shop-purchases

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-souvenir-shop-purchases.md

In an Amazon Souvenir Shop, a shopper visited a souvenir shop with items arranged on the shelf from left to right. The goal is to purchase as many items as possible within a given budget. Notably, the

  uv run python amazon_oa/amazon-souvenir-shop-purchases/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-souvenir-shop-purchases/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countPurchasedItems(self, cost, m):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countPurchasedItems above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countPurchasedItems(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
