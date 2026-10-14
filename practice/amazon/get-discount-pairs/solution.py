"""Get Discount Pairs — https://www.fastprep.io/problems/get-discount-pairs

Write-up & approaches: ../../../docs/problems/amazon_oa/get-discount-pairs.md

Amazon is offering a discount on every purchase of a pair of products whose price sum is divisible by x. Given the prices of n products, count the number of unordered index pairs (i, j) such that 0 <=

  uv run python amazon_oa/get-discount-pairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/get-discount-pairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getDiscountPairs(self, x, prices):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getDiscountPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getDiscountPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
