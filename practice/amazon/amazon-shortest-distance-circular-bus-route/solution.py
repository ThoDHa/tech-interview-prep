"""Shortest Distance on a Circular Bus Route — https://www.fastprep.io/problems/amazon-shortest-distance-circular-bus-route

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-shortest-distance-circular-bus-route.md

For this exercise, assume a bus route has n stops arranged in a circle. The array distance contains the distance from stop i to stop (i + 1) mod n.

  uv run python amazon_oa/amazon-shortest-distance-circular-bus-route/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-shortest-distance-circular-bus-route/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def shortestBusRouteDistance(self, distance, start, destination):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in shortestBusRouteDistance above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().shortestBusRouteDistance(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
