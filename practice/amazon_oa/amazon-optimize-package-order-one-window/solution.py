"""Optimize Package Order by Sorting One Window — https://www.fastprep.io/problems/amazon-optimize-package-order-one-window

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-optimize-package-order-one-window.md

Given an integer array of package priorities and a window size k, choose exactly one contiguous window of length k and sort only that window in ascending order.

  uv run python amazon_oa/amazon-optimize-package-order-one-window/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-optimize-package-order-one-window/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def optimizePackageOrder(self, packages, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in optimizePackageOrder above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().optimizePackageOrder(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
