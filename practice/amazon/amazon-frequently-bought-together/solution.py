"""Frequently Bought Together — https://www.fastprep.io/problems/amazon-frequently-bought-together

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-frequently-bought-together.md

Amazon's Retail Analytics team wants to discover which pairs of items are most often bought together so they can create Frequently Bought Together bundles.

  uv run python amazon_oa/amazon-frequently-bought-together/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-frequently-bought-together/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findFrequentBundlePair(self, orders):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findFrequentBundlePair above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findFrequentBundlePair(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
