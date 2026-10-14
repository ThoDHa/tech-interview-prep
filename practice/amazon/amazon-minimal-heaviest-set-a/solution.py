"""Optimizing Box Weights — https://www.fastprep.io/problems/amazon-minimal-heaviest-set-a

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimal-heaviest-set-a.md

An Amazon Fulfillment Associate has a set of items that need to be packed into two boxes. Given an integer array of the item weights (arr) to be packed, divide the item weights into two subsets, A and

  uv run python amazon_oa/amazon-minimal-heaviest-set-a/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimal-heaviest-set-a/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimalHeaviestSetA(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimalHeaviestSetA above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimalHeaviestSetA(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
