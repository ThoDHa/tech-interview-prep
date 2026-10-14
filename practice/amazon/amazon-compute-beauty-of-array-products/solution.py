"""Compute Beauty of Array Products — https://www.fastprep.io/problems/amazon-compute-beauty-of-array-products

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-compute-beauty-of-array-products.md

The Amazon distribution center consists of arrays of products, each possessing unique attributes. The task at hand is to compute the beauty of these product arrays, with the goal of achieving an effic

  uv run python amazon_oa/amazon-compute-beauty-of-array-products/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-compute-beauty-of-array-products/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def computeBeauty(self, products, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in computeBeauty above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().computeBeauty(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
