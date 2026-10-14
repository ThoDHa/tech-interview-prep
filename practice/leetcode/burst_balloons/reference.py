"""Burst Balloons — https://leetcode.com/problems/burst-balloons/

Write-up & approaches: ../../docs/problems/burst_balloons.md
Reference implementation of the write-up's Top-Down Memoization solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python burst_balloons/reference.py   # replay the example cases
  uv run pytest burst_balloons/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """Return the most coins obtainable by bursting every balloon.

        Time:  O(n^3): O(n^2) intervals, each scanning up to n last-burst
            candidates once.
        Space: O(n^2): one memo entry per wall pair plus the recursion stack.
        """
        n = len(nums)
        nums2 = [1] + nums + [1]
        memo = {}

        def burst(l: int, r: int) -> int:
            if r - l < 2:
                return 0
            if (l, r) in memo:
                return memo[(l, r)]
            best_coins = 0
            for k in range(l + 1, r):
                coins = burst(l, k) + burst(k, r) + nums2[l] * nums2[k] * nums2[r]
                best_coins = max(best_coins, coins)
            memo[(l, r)] = best_coins
            return best_coins

        return burst(0, n + 1)


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1",):
        case = pick_case(__file__, case_id)
        result = Solution().maxCoins(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
