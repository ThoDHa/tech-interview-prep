"""Product of Array Except Self: https://leetcode.com/problems/product-of-array-except-self/

Write-up & approaches: ../../../docs/leetcode/product_of_array_except_self.md

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
        length = len(nums)
        prefix = [1] * length
        suffix = [1] * length
        result = [1] * length

        for i in range(1, length):
            prefix[i] = prefix[i-1] * nums[i-1]

        for i in range(length-2, -1, -1):
            suffix[i] = suffix[i+1] * nums[i+1]

        for i in range(length):
            result[i] = prefix[i] * suffix[i]
        return result

if __name__ == "__main__":
    # Debug playground: set a breakpoint in productExceptSelf above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().productExceptSelf(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
