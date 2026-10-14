"""Coin Change II — https://leetcode.com/problems/coin-change-ii/

Write-up & approaches: ../../docs/problems/coin_change_ii.md
Reference implementation of the write-up's Space-Optimized 1-D DP solution.

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a target amount of money. Return the number of distinct combinations that total up to `amount`, or `0` when it is impossible. You have an unlimited number of each coin and each value in `coins` is unique.

  uv run python coin_change_ii/reference.py   # debug one case (see CASE below)
  uv run pytest coin_change_ii/              # run the test sets
"""

from harness import pick_case


class Solution:
    def change(self, amount, coins):
        """Count the coin combinations summing to `amount`.

        Processes one denomination at a time over a single row `dp`, where
        `dp[a]` is the number of combinations of the coins seen so far that
        sum to `a`. Sweeping `a` left to right lets `dp[a - coin]` already
        include the current coin, so each combination is counted once, in
        exactly one coin order (unordered combinations, not permutations).

        Args:
            amount: Target total, 0 <= amount <= 5000.
            coins: Unique denominations, 1 <= len(coins) <= 100,
                1 <= coins[i] <= 5000.

        Returns:
            The number of distinct combinations making `amount`, 0 if none.

        Time:  O(len(coins) * amount): one row sweep per denomination.
        Space: O(amount): the single row.
        """
        dp = [0] * (amount + 1)
        dp[0] = 1
        for coin in coins:
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]
        return dp[amount]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in change above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().change(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
