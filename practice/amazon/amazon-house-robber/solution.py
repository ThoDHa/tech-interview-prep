"""House Robber — https://www.fastprep.io/problems/amazon-house-robber

Write-up & approaches: ../../../docs/amazon/amazon-house-robber.md

You are given an array nums, where nums[i] is the amount of money in house i.

  uv run python amazon_oa/amazon-house-robber/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-house-robber/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def rob(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in rob above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().rob(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
