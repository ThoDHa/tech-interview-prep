"""Permutations: https://leetcode.com/problems/permutations/

Write-up & approaches: ../../docs/problems/permutations.md

Given an array `nums` of distinct integers, return all the possible
permutations. You can return the answer in any order.

  uv run python permutations/solution.py     # debug one case (see CASE below)
  uv run pytest permutations/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in permute above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().permute(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
