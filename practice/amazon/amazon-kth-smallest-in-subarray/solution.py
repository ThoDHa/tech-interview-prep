"""Kth Smallest in Subarray — https://www.fastprep.io/problems/amazon-kth-smallest-in-subarray

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-kth-smallest-in-subarray.md

Given an array arr, return the kth smallest integer for each subarray of size m.

  uv run python amazon_oa/amazon-kth-smallest-in-subarray/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-kth-smallest-in-subarray/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def kthSmallestInSubarray(self, arr, k, m):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in kthSmallestInSubarray above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().kthSmallestInSubarray(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
