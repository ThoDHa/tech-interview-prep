"""Maximum Product Subarray — https://leetcode.com/problems/maximum-product-subarray/

Write-up & approaches: ../../docs/problems/maximum_product_subarray.md

Given an integer array `nums`, find a **subarray** that has the largest product, and return the product. A **subarray** is a contiguous non-empty sequence of elements within an array. You can assume t

  uv run python maximum_product_subarray/solution.py   # debug one case (see CASE below)
  uv run pytest maximum_product_subarray/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxProduct(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxProduct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxProduct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
