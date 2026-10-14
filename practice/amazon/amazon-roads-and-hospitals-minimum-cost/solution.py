"""Minimum Cost for Roads and Hospitals — https://www.fastprep.io/problems/amazon-roads-and-hospitals-minimum-cost

Write-up & approaches: ../../../docs/amazon/amazon-roads-and-hospitals-minimum-cost.md

Cities are labeled from 0 to cityCount - 1. A hospital can be built in any city for hospitalCost, and any listed undirected road can be built for roadCost.

  uv run python amazon_oa/amazon-roads-and-hospitals-minimum-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-roads-and-hospitals-minimum-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumInfrastructureCost(self, cityCount, possibleRoads, hospitalCost, roadCost):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumInfrastructureCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumInfrastructureCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
