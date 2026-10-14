"""Min Cost to Connect All Points — https://leetcode.com/problems/min-cost-to-connect-all-points/

Write-up & approaches: ../../docs/problems/min_cost_to_connect_all_points.md

You are given a 2-D integer array `points`, where `points[i] = [xi, yi]`. Each `points[i]` represents a distinct point on a 2-D plane. The cost of connecting two points `[xi, yi]` and `[xj, yj]` is th

  uv run python min_cost_to_connect_all_points/solution.py   # debug one case (see CASE below)
  uv run pytest min_cost_to_connect_all_points/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minCostConnectPoints(self, points):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCostConnectPoints above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCostConnectPoints(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
