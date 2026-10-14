"""VM Rental Revenue — https://www.fastprep.io/problems/amazon-vm-rental-revenue

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-vm-rental-revenue.md

There are multiple VM types, each with an initial stock count. A sequence of customers rent one VM at a time.

  uv run python amazon_oa/amazon-vm-rental-revenue/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-vm-rental-revenue/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculateVmRentalRevenue(self, vmStock, customerRequests):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculateVmRentalRevenue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculateVmRentalRevenue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
