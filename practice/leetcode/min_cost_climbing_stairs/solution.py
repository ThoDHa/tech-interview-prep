"""Min Cost Climbing Stairs — https://leetcode.com/problems/min-cost-climbing-stairs/

Write-up & approaches: ../../docs/problems/min_cost_climbing_stairs.md

You are given an array of integers `cost` where `cost[i]` is the cost of taking a step from the `ith` floor of a staircase. After paying the cost, you can step to either the `(i + 1)th` floor or the `

  uv run python min_cost_climbing_stairs/solution.py   # debug one case (see CASE below)
  uv run pytest min_cost_climbing_stairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minCostClimbingStairs(self, cost):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCostClimbingStairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCostClimbingStairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
