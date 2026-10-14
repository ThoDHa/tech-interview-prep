"""Get Minimal Cost — https://www.fastprep.io/problems/amazon-get-minimal-cost

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-minimal-cost.md

An online retailer offers products in n different dimensions as specified in the array dimensions. The category supervisor notices that several dimensions are redundant and do not offer a favorable cu

  uv run python amazon_oa/amazon-get-minimal-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-minimal-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinimalCost(self, dimensions, adjustmentCosts):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinimalCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinimalCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
