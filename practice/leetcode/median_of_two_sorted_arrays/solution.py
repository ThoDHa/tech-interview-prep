"""Median of Two Sorted Arrays — https://leetcode.com/problems/median-of-two-sorted-arrays/

Write-up & approaches: ../../docs/problems/median_of_two_sorted_arrays.md

You are given two integer arrays `nums1` and `nums2` of size `m` and `n` respectively, where each is sorted in ascending order. Return the [median](https://en.wikipedia.org/wiki/Median) value among al

  uv run python median_of_two_sorted_arrays/solution.py   # debug one case (see CASE below)
  uv run pytest median_of_two_sorted_arrays/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMedianSortedArrays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMedianSortedArrays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
