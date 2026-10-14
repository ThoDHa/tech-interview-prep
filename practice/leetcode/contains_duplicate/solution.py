"""Contains Duplicate: https://leetcode.com/problems/contains-duplicate/

Write-up & approaches: ../../docs/problems/contains_duplicate.md

Given an integer array `nums`, return `true` if any value appears at least
twice in the array, and `false` if every element is distinct.

  uv run python contains_duplicate/solution.py     # debug one case (see CASE below)
  uv run pytest contains_duplicate/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in containsDuplicate above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().containsDuplicate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
