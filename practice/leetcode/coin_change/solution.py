"""Coin Change: https://leetcode.com/problems/coin-change/

Write-up & approaches: ../../../docs/leetcode/coin_change.md

Given an integer array `coins` of different denominations and an integer
`amount`, return the fewest number of coins needed to make up that amount, or
`-1` if it cannot be made. You have an infinite supply of each coin.

  uv run python coin_change/solution.py     # debug one case (see CASE below)
  uv run pytest coin_change/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        dp: list[int] = [amount+1] * (amount+1)
        dp[0] = 0

        for i in range(1, amount+1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i-coin] + 1)
        return dp[amount] if dp[amount] != amount+1 else -1

if __name__ == "__main__":
    # Debug playground: set a breakpoint in coinChange above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().coinChange(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
