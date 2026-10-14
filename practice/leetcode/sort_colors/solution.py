"""Sort Colors: https://leetcode.com/problems/sort-colors/

Write-up & approaches: ../../docs/problems/sort_colors.md

Given an array `nums` with `n` objects colored red, white, or blue (encoded as
`0`, `1`, `2`), sort them in-place so the colors appear in the order red, white,
then blue. You may not use the library's sort function.

  uv run python sort_colors/solution.py   # debug one case (see CASE below)
  uv run pytest sort_colors/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in sortColors above, then run this file.
    # sortColors mutates nums in place and returns None; we compare the mutation.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    nums = list(case["args"][0])
    Solution().sortColors(nums)
    print(f"case {case['id']}: nums = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {nums}")
