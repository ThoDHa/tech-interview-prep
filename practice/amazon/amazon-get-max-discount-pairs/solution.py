"""Get Max Discount Pairs — https://www.fastprep.io/problems/amazon-get-max-discount-pairs

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-discount-pairs.md

It is the third anniversary of Amazon Prime Day, and they have come up with amazing offers yet again! Customers who purchase a pair of products whose prices sum to a power of three receive a 50% disco

  uv run python amazon_oa/amazon-get-max-discount-pairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-discount-pairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxDiscountPairs(self, price):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxDiscountPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxDiscountPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
