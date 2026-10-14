"""K Closest Points to Origin: https://leetcode.com/problems/k-closest-points-to-origin/

Write-up & approaches: ../../docs/problems/k_closest_points_to_origin.md

Given an array of points `points[i] = [xi, yi]` and an integer `k`, return the
`k` points closest to the origin `(0, 0)` by Euclidean distance, in any order.

  uv run python k_closest_points_to_origin/solution.py     # debug one case (see CASE below)
  uv run pytest k_closest_points_to_origin/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in kClosest above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().kClosest(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
