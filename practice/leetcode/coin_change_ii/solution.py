"""Coin Change II — https://leetcode.com/problems/coin-change-ii/

Write-up & approaches: ../../docs/problems/coin_change_ii.md

You are given an integer array `coins` representing coins of different denominations (e.g. 1 dollar, 5 dollars, etc) and an integer `amount` representing a target amount of money. Return the number of

  uv run python coin_change_ii/solution.py   # debug one case (see CASE below)
  uv run pytest coin_change_ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def change(self, amount, coins):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in change above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().change(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
