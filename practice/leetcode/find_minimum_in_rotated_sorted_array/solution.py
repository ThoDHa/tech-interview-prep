"""Find Minimum In Rotated Sorted Array — https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Write-up & approaches: ../../docs/problems/find_minimum_in_rotated_sorted_array.md

You are given an array of length `n` which was originally sorted in ascending order. It has now been **rotated** between `1` and `n` times. For example, the array `nums = [1,2,3,4,5,6]` might become: 

  uv run python find_minimum_in_rotated_sorted_array/solution.py   # debug one case (see CASE below)
  uv run pytest find_minimum_in_rotated_sorted_array/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMin(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMin above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMin(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
