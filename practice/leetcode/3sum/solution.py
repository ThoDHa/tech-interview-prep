"""3Sum: https://leetcode.com/problems/3sum/

Write-up & approaches: ../../docs/problems/3sum.md

Given an integer array `nums`, return all unique triplets
`[nums[i], nums[j], nums[k]]` with distinct indices such that they sum to zero.
The solution set must not contain duplicate triplets; order does not matter.

  uv run python 3sum/solution.py     # debug one case (see CASE below)
  uv run pytest 3sum/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in threeSum above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().threeSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
