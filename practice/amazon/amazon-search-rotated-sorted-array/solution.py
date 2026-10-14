"""Search in a Rotated Sorted Array — https://www.fastprep.io/problems/amazon-search-rotated-sorted-array

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-search-rotated-sorted-array.md

Given an integer array nums that was sorted in strictly increasing order and then rotated at an unknown pivot, and an integer target, return the index of target.

  uv run python amazon_oa/amazon-search-rotated-sorted-array/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-search-rotated-sorted-array/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def searchRotatedArray(self, nums, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in searchRotatedArray above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().searchRotatedArray(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
