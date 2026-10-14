"""Median of Two Sorted Arrays — https://leetcode.com/problems/median-of-two-sorted-arrays/

Write-up & approaches: ../../docs/problems/median_of_two_sorted_arrays.md
Reference implementation of the write-up's Partition Binary Search solution.

You are given two integer arrays `nums1` and `nums2` of size `m` and `n` respectively, where each is sorted in ascending order. Return the median value among all elements of the two arrays.

  uv run python median_of_two_sorted_arrays/reference.py   # debug one case (see CASE below)
  uv run pytest median_of_two_sorted_arrays/              # run the test sets
"""

from harness import pick_case


class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """Return the median of two sorted arrays in logarithmic time.

        Binary searches a cut through the shorter array such that every
        element left of the cut in both arrays is <= every element right of
        it; the combined halves then hold exactly half the elements, and the
        boundary values give the median directly.

        Args:
            nums1: Sorted ascending, 0 <= len(nums1).
            nums2: Sorted ascending, 1 <= len(nums1) + len(nums2).

        Returns:
            The middle value for odd combined length, the mean of the two
            middle values for even combined length.

        Time:  O(log(min(m, n))): the search always runs over the shorter
            array, so it halves the smaller of m and n.
        Space: O(1): only boundary variables.
        """
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        half = (m + n + 1) // 2
        left, right = 0, m
        while left <= right:
            take1 = (left + right) // 2
            take2 = half - take1
            left1 = nums1[take1 - 1] if take1 > 0 else float("-inf")
            right1 = nums1[take1] if take1 < m else float("inf")
            left2 = nums2[take2 - 1] if take2 > 0 else float("-inf")
            right2 = nums2[take2] if take2 < n else float("inf")
            if left1 <= right2 and left2 <= right1:
                if (m + n) % 2 == 1:
                    return float(max(left1, left2))
                return (max(left1, left2) + min(right1, right2)) / 2
            if left1 > right2:
                right = take1 - 1
            else:
                left = take1 + 1
        raise ValueError("unreachable: sorted inputs always admit a valid cut")


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMedianSortedArrays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMedianSortedArrays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
