"""Compute Encoded Product Name — https://www.fastprep.io/problems/amazon-compute-encoded-product-name

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-compute-encoded-product-name.md

Amazon's software team utilizes several algorithms to maintain data integrity, one of which targets the encoding of symmetrical names. Symmetrical names are unique in that they read identically in bot

  uv run python amazon_oa/amazon-compute-encoded-product-name/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-compute-encoded-product-name/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def computeEncodedProductName(self, nameString):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in computeEncodedProductName above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().computeEncodedProductName(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
