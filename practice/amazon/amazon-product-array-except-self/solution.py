"""Product of Array Except Self — https://www.fastprep.io/problems/amazon-product-array-except-self

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-product-array-except-self.md

Given an integer array nums, return an array answer where answer[i] equals the product of every element of nums except nums[i].

  uv run python amazon_oa/amazon-product-array-except-self/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-product-array-except-self/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def productExceptSelf(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in productExceptSelf above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().productExceptSelf(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
