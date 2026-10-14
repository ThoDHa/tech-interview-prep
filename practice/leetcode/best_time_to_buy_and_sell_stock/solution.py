"""Best Time to Buy and Sell Stock: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

Write-up & approaches: ../../docs/problems/best_time_to_buy_and_sell_stock.md

Given an array `prices` where `prices[i]` is the stock price on day `i`, choose a
single day to buy and a later day to sell to maximize profit. Return the maximum
profit achievable, or `0` if no profitable transaction exists.

  uv run python best_time_to_buy_and_sell_stock/solution.py     # debug one case (see CASE below)
  uv run pytest best_time_to_buy_and_sell_stock/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxProfit above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxProfit(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
