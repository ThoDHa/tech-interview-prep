"""Subsets: https://leetcode.com/problems/subsets/

Write-up & approaches: ../../docs/problems/subsets.md

Given an integer array `nums` of unique elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets, and may be
returned in any order.

  uv run python subsets/solution.py     # debug one case (see CASE below)
  uv run pytest subsets/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in subsets above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().subsets(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
