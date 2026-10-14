"""Maximum Stock Profit with At Most Two Transactions — https://www.fastprep.io/problems/amazon-best-time-to-buy-and-sell-stock-iii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-best-time-to-buy-and-sell-stock-iii.md

You are given an array prices, where prices[i] is the price of one stock on day i. Return the maximum profit you can earn by completing at most two transactions.

  uv run python amazon_oa/amazon-best-time-to-buy-and-sell-stock-iii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-best-time-to-buy-and-sell-stock-iii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxProfitAtMostTwo(self, prices):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxProfitAtMostTwo above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxProfitAtMostTwo(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
