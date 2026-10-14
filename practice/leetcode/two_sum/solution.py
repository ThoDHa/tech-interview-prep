"""Two Sum: https://leetcode.com/problems/two-sum/

Write-up & approaches: ../../docs/problems/two_sum.md

Given an array of integers `nums` and an integer `target`, return indices of the
two numbers such that they add up to `target`. Exactly one solution exists; you
may not reuse an element. Return the answer in any order.

  uv run python two_sum/solution.py     # debug one case (see CASE below)
  uv run pytest two_sum/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in twoSum above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().twoSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
