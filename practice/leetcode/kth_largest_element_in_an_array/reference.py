"""Kth Largest Element In An Array — https://leetcode.com/problems/kth-largest-element-in-an-array/

Write-up & approaches: ../../docs/problems/kth_largest_element_in_an_array.md
Reference implementation of the write-up's Quickselect solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

Given an unsorted array of integers `nums` and an integer `k`, return the `kth`
largest element in the array. By `kth` largest element, we mean the `kth`
largest element in the sorted order, not the `kth` distinct element.

  uv run python kth_largest_element_in_an_array/reference.py   # debug one case (see CASE below)
  uv run pytest kth_largest_element_in_an_array/               # run the test sets
"""

import random

from harness import pick_case


class Solution:
    def findKthLargest(self, nums, k):
        """Return the kth largest element of `nums` in sorted order.

        Runs randomized quickselect: each `partition` call places one
        pivot at its final ascending-sorted index, and the search narrows
        toward `target = len(nums) - k` (the kth largest's index) instead
        of sorting both sides. Partitions in place, so `nums` is reordered.

        Args:
            nums: Unsorted values, 1 <= len(nums) <= 10^4, each in
                [-1000, 1000]; mutated in place.
            k: Rank to select, 1 <= k <= len(nums).

        Returns:
            The value that would sit at index `len(nums) - k` if `nums`
            were sorted ascending.

        Time:  O(n) average, O(n^2) worst case: each partition is linear
            over its range and random pivots shrink it geometrically on
            average; adversarial pivots degrade to quadratic.
        Space: O(1): partitioning is in place; only indices are tracked.
        """

        def partition(left, right, pivot_idx):
            pivot = nums[pivot_idx]
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
            store = left
            for i in range(left, right):
                if nums[i] < pivot:
                    nums[store], nums[i] = nums[i], nums[store]
                    store += 1
            nums[right], nums[store] = nums[store], nums[right]
            return store

        left, right = 0, len(nums) - 1
        target = len(nums) - k
        while left < right:
            pivot_idx = random.randint(left, right)
            mid = partition(left, right, pivot_idx)
            if mid == target:
                break
            elif mid < target:
                left = mid + 1
            else:
                right = mid - 1
        return nums[target]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findKthLargest above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findKthLargest(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
