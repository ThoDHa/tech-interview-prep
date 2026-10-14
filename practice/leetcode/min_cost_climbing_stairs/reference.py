"""Min Cost Climbing Stairs — https://leetcode.com/problems/min-cost-climbing-stairs/

Write-up & approaches: ../../docs/problems/min_cost_climbing_stairs.md
Reference implementation of the write-up's Space-Optimized DP solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

You are given an array of integers `cost` where `cost[i]` is the cost of taking a step from the `ith` floor of a staircase. After paying the cost, you can step to either the `(i + 1)th` floor or the `(i + 2)th` floor. You may choose to start at the index `0` or the index `1` floor. Return the minimum cost to reach the top of the staircase, i.e. just past the last index in `cost`.

  uv run python min_cost_climbing_stairs/reference.py   # debug one case (see CASE below)
  uv run pytest min_cost_climbing_stairs/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """Return the cheapest total payable on a climb from floor 0 or 1
        to the top, just past the last index.

        Sweeps the floors right to left holding the two cheapest finishes
        above the current floor: `one_above` is the cheapest finish from
        the next floor up, `two_above` from the one after that. Each floor
        pays its own cost and takes the cheaper leap, so after the floor 0
        update the registers hold dp[0] and dp[1], and the free choice of
        the starting floor is the min of the two.

        Args:
            cost: Per-floor step costs, 2 <= len(cost) <= 100, with each
                cost[i] in 0 <= cost[i] <= 100.

        Returns:
            The minimum total cost collectible on any legal climb to the top.

        Time:  O(n): one constant-work update per floor.
        Space: O(1): two rolling registers regardless of length.
        """
        one_above, two_above = 0, 0
        for i in range(len(cost) - 1, -1, -1):
            current = cost[i] + min(one_above, two_above)
            two_above = one_above
            one_above = current
        return min(one_above, two_above)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCostClimbingStairs above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCostClimbingStairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
