"""Choose Warehouse Location — https://www.fastprep.io/problems/amazon-choose-warehouses-location

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-choose-warehouses-location.md

Amazon has recently established n distribution centers in a new location. They want to set up 2 warehouses to serve these distribution centers. Note that the centers and warehouses are all built along

  uv run python amazon_oa/amazon-choose-warehouses-location/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-choose-warehouses-location/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minSumDistancesToWarehouses(self, dist_centers):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minSumDistancesToWarehouses above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minSumDistancesToWarehouses(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
