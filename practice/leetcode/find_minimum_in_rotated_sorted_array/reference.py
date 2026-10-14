"""Find Minimum In Rotated Sorted Array — https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Write-up & approaches: ../../docs/problems/find_minimum_in_rotated_sorted_array.md
Reference implementation of the write-up's Binary Search on Right Slope solution.

You are given an array of length `n` which was originally sorted in ascending order and has now been rotated between `1` and `n` times. Assuming all elements in the rotated sorted array `nums` are **unique**, return the minimum element of this array.

  uv run python find_minimum_in_rotated_sorted_array/reference.py   # debug one case (see CASE below)
  uv run pytest find_minimum_in_rotated_sorted_array/              # run the test sets
"""

from harness import pick_case


class Solution:
    def findMin(self, nums):
        """Return the minimum of a uniquely-valued rotated sorted array.

        Binary search over the closed interval [left, right]: comparing
        `nums[mid]` against the right sentinel `nums[right]` sorts mid into
        the unrotated segment (go right) or the rotated segment (go left);
        the loop converges on the segment boundary, the rotation point.

        Args:
            nums: Rotated ascending values, all unique, 1 <= len(nums).

        Returns:
            The smallest value in `nums`.

        Time:  O(log n): each probe halves the interval.
        Space: O(1): only search-boundary variables.
        """
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return nums[left]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMin above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMin(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
