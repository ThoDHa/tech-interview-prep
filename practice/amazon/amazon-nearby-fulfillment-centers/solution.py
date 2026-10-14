"""Nearby Fulfillment Centers with Inventory — https://www.fastprep.io/problems/amazon-nearby-fulfillment-centers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-nearby-fulfillment-centers.md

A delivery must be fulfilled near a destination center. The fulfillment network is an undirected graph whose edges are given by connections. Each row [u, v] connects centers u and v in both directions

  uv run python amazon_oa/amazon-nearby-fulfillment-centers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-nearby-fulfillment-centers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findFulfillmentCenters(self, connections, destination, maxStep, inventory):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findFulfillmentCenters above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findFulfillmentCenters(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
