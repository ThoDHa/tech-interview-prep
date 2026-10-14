"""Maximize Product of Sizes of Subtrees — https://www.fastprep.io/problems/amazon-maximize-product-of-sizes-of-subtrees

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-product-of-sizes-of-subtrees.md

BREAKING! Its sister question was found --> Checkout LC 343. Integer Break <-- 

  uv run python amazon_oa/amazon-maximize-product-of-sizes-of-subtrees/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-product-of-sizes-of-subtrees/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeProductOfSubtreeSizes(self, w, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeProductOfSubtreeSizes above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeProductOfSubtreeSizes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
