"""Single Element in a Sorted Array — https://www.fastprep.io/problems/amazon-single-element-in-sorted-array

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-single-element-in-sorted-array.md

Given a sorted integer array nums, every value appears exactly twice except for one value that appears exactly once.

  uv run python amazon_oa/amazon-single-element-in-sorted-array/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-single-element-in-sorted-array/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def singleNonDuplicate(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in singleNonDuplicate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().singleNonDuplicate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
