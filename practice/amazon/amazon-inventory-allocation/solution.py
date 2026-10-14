"""Inventory Allocation — https://www.fastprep.io/problems/amazon-inventory-allocation

Write-up & approaches: ../../../docs/amazon/amazon-inventory-allocation.md

You are given a list of inventory requests. Each request is represented as [customerId, quantity, bidAmount, timestamp].

  uv run python amazon_oa/amazon-inventory-allocation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-inventory-allocation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getUnfulfilledCustomers(self, requests, totalInventory):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getUnfulfilledCustomers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getUnfulfilledCustomers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
