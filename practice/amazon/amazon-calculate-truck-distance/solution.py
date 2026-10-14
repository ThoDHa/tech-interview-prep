"""Calculate Truck Distance — https://www.fastprep.io/problems/amazon-calculate-truck-distance

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-calculate-truck-distance.md

Trucks dispatch packages in a city. There are n trucks numbered 0, 1, ..., n - 1 used for dispatching goods. Assuming the trucks are parked along the x-coordinate axis, the coordinates of these trucks

  uv run python amazon_oa/amazon-calculate-truck-distance/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-calculate-truck-distance/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculateTruckDistanceAfterRefueling(self, position, extraGasStations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculateTruckDistanceAfterRefueling above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculateTruckDistanceAfterRefueling(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
