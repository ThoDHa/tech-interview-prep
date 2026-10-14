"""Package Delivery System — https://www.fastprep.io/problems/amazon-package-delivery-system

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-package-delivery-system.md

Each shipment scenario has a list of truck capacities and a list of package weights.

  uv run python amazon_oa/amazon-package-delivery-system/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-package-delivery-system/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def canDeliverAllPackages(self, truckCapacities, packageWeights):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canDeliverAllPackages above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canDeliverAllPackages(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
