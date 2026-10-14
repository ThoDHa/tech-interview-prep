"""House Robber II — https://leetcode.com/problems/house-robber-ii/

Write-up & approaches: ../../docs/problems/house_robber_ii.md

You are given an integer array `nums` where `nums[i]` represents the amount of money the `i`th house has. The houses are arranged in a circle, i.e. the first house and the last house are neighbors. Yo

  uv run python house_robber_ii/solution.py   # debug one case (see CASE below)
  uv run pytest house_robber_ii/              # run the test sets
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
