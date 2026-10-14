"""Loyal Customers Across Two Days — https://www.fastprep.io/problems/amazon-loyal-customers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-loyal-customers.md

You are given two arrays of website logs, dayOneLogs and dayTwoLogs. Each log entry contains exactly three strings in this order: timestamp, customerId, and pageId.

  uv run python amazon_oa/amazon-loyal-customers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-loyal-customers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findLoyalCustomers(self, dayOneLogs, dayTwoLogs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findLoyalCustomers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findLoyalCustomers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
