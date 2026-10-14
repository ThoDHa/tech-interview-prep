"""Target Sum — https://leetcode.com/problems/target-sum/

Write-up & approaches: ../../docs/problems/target_sum.md

You are given an array of integers `nums` and an integer `target`. For each number in the array, you can choose to either add or subtract it to a total sum. * For example, if `nums = [1, 2]`, one poss

  uv run python target_sum/solution.py   # debug one case (see CASE below)
  uv run pytest target_sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findTargetSumWays(self, nums, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findTargetSumWays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findTargetSumWays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
