"""Min Cost to Connect All Points — https://leetcode.com/problems/min-cost-to-connect-all-points/

Write-up & approaches: ../../docs/problems/min_cost_to_connect_all_points.md
Reference implementation of the write-up's Prim's Algorithm solution.

You are given a 2-D integer array `points`, where `points[i] = [xi, yi]`. Each `points[i]` represents a distinct point on a 2-D plane. The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the manhattan distance between them: `|xi - xj| + |yi - yj|`. Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

  uv run python min_cost_to_connect_all_points/reference.py   # debug one case (see CASE below)
  uv run pytest min_cost_to_connect_all_points/              # run the test sets
"""

import heapq

from harness import pick_case


class Solution:
    def minCostConnectPoints(self, points):
        """Grow a minimum spanning tree from the first point with Prim's.

        Builds the complete implicit graph lazily: a min-heap holds the cost
        of reaching every not-yet-connected point from the tree grown so far,
        seeded with point 0 at cost 0. Each pop either lands on an already
        connected point (a stale entry, skipped) or claims a new point, and
        claims its Manhattan distances to the remaining points.

        Args:
            points: Distinct 2-D points, `2 <= len(points) <= 1000`.

        Returns:
            The minimum total Manhattan cost of a tree spanning all points.

        Time:  O(n^2 * log n): each of the n claims relaxes n edges into the heap.
        Space: O(n^2): the heap can hold one entry per pair.
        """
        total = 0
        connected = 0
        in_tree = [False] * len(points)
        # (cost_to_reach, point_index), seeded with the first point free.
        heap = [(0, 0)]
        while connected < len(points):
            cost, index = heapq.heappop(heap)
            if in_tree[index]:
                continue
            in_tree[index] = True
            connected += 1
            total += cost
            x, y = points[index]
            for other in range(len(points)):
                if not in_tree[other]:
                    ox, oy = points[other]
                    distance = abs(x - ox) + abs(y - oy)
                    heapq.heappush(heap, (distance, other))
        return total


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCostConnectPoints above, then
    # run this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCostConnectPoints(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
