"""Minimum Cost to Convert Products to Variant A — https://www.fastprep.io/problems/amazon-minimum-cost-to-convert-products-to-variant-a

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-cost-to-convert-products-to-variant-a.md

An inventory array product contains only 0 and 1, where 0 represents variant A and 1 represents variant B.

  uv run python amazon_oa/amazon-minimum-cost-to-convert-products-to-variant-a/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-cost-to-convert-products-to-variant-a/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minCostToConvertAllToVariantA(self, product, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCostToConvertAllToVariantA above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCostToConvertAllToVariantA(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
