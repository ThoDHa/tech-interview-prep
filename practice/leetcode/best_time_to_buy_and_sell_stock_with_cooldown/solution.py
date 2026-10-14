"""Best Time to Buy And Sell Stock With Cooldown — https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/

Write-up & approaches: ../../docs/problems/best_time_to_buy_and_sell_stock_with_cooldown.md

You are given an integer array `prices` where `prices[i]` is the price of NeetCoin on the `ith` day. You may buy and sell one NeetCoin multiple times with the following restrictions: * After you sell 

  uv run python best_time_to_buy_and_sell_stock_with_cooldown/solution.py   # debug one case (see CASE below)
  uv run pytest best_time_to_buy_and_sell_stock_with_cooldown/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxProfit(self, prices):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxProfit above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxProfit(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
