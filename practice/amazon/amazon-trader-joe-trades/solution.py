"""Trader Joe Trades — https://www.fastprep.io/problems/amazon-trader-joe-trades

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-trader-joe-trades.md

In the Amazon Trade Optimization System, a financial strategist named Joe the trader is assigned the task of maximizing revenue while following the execution rules for trade operations. The trading sy

  uv run python amazon_oa/amazon-trader-joe-trades/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-trader-joe-trades/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def traderTrades(self, tasks, rewards, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in traderTrades above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().traderTrades(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
