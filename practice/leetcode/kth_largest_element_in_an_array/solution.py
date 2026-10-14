"""Kth Largest Element In An Array — https://leetcode.com/problems/kth-largest-element-in-an-array/

Write-up & approaches: ../../docs/problems/kth_largest_element_in_an_array.md

Given an unsorted array of integers `nums` and an integer `k`, return the `kth` largest element in the array. By `kth` largest element, we mean the `kth` largest element in the sorted order, not the `

  uv run python kth_largest_element_in_an_array/solution.py   # debug one case (see CASE below)
  uv run pytest kth_largest_element_in_an_array/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findKthLargest(self, nums, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findKthLargest above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findKthLargest(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
