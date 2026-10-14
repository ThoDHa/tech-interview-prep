"""Product of Array Except Self: https://leetcode.com/problems/product-of-array-except-self/

Write-up & approaches: ../../docs/problems/product_of_array_except_self.md

Given an integer array `nums`, return an array `answer` such that `answer[i]` is
the product of all elements of `nums` except `nums[i]`. Solve it in `O(n)` time
without using division.

  uv run python product_of_array_except_self/solution.py     # debug one case (see CASE below)
  uv run pytest product_of_array_except_self/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in productExceptSelf above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().productExceptSelf(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
