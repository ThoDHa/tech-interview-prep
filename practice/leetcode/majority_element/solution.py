"""Majority Element: https://leetcode.com/problems/majority-element/

Write-up & approaches: ../../docs/problems/majority_element.md

Given an array `nums` of size `n`, return the majority element: the element that
appears more than `⌊n / 2⌋` times. You may assume it always exists.

  uv run python majority_element/solution.py   # debug one case (see CASE below)
  uv run pytest majority_element/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in majorityElement above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().majorityElement(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
