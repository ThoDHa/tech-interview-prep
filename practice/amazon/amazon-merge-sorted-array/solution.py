"""Merge Sorted Array — https://www.fastprep.io/problems/amazon-merge-sorted-array

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-merge-sorted-array.md

You are given two integer arrays nums1 and nums2, each sorted in non-decreasing order, and two integers m and n representing the number of valid elements in the arrays.

  uv run python amazon_oa/amazon-merge-sorted-array/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-merge-sorted-array/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def mergeSortedArray(self, nums1, m, nums2, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeSortedArray above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().mergeSortedArray(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
