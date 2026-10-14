"""Best Time to Buy And Sell Stock With Cooldown — https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/

Write-up & approaches: ../../docs/problems/best_time_to_buy_and_sell_stock_with_cooldown.md
Reference implementation of the write-up's Bottom-Up State Machine solution.

You are given an integer array `prices` where `prices[i]` is the price of NeetCoin on the `ith` day. You may buy and sell one NeetCoin multiple times with a one-day cooldown after each sale, and you may own at most one NeetCoin at a time. Return the maximum profit you can achieve.

  uv run python best_time_to_buy_and_sell_stock_with_cooldown/reference.py   # debug one case (see CASE below)
  uv run pytest best_time_to_buy_and_sell_stock_with_cooldown/              # run the test sets
"""

from harness import pick_case


class Solution:
    def maxProfit(self, prices):
        """Return the maximum profit with a one-day cooldown after each sale.

        Rolls three states forward one day at a time: `hold` is the best
        profit while owning a share, `sold` the best profit having sold
        today, and `rest` the best profit free to act without having sold
        today. A purchase may only depart from `rest`, which is exactly the
        state a seller cannot occupy on the cooldown day.

        Args:
            prices: Daily prices, 1 <= len(prices) <= 5000, 0 <= prices[i] <= 1000.

        Returns:
            The maximum total profit over any number of cooldown-separated trades.

        Time:  O(n): one constant-work transition per day.
        Space: O(1): the three rolling scalars.
        """
        hold = float("-inf")
        sold = float("-inf")
        rest = 0
        for price in prices:
            prev_sold = sold
            sold = hold + price
            hold = max(hold, rest - price)
            rest = max(rest, prev_sold)
        return max(sold, rest)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxProfit above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxProfit(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
