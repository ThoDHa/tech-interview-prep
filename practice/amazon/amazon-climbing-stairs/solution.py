"""Climbing Stairs — https://www.fastprep.io/problems/amazon-climbing-stairs

Write-up & approaches: ../../../docs/amazon/amazon-climbing-stairs.md

You are climbing a staircase with n steps.

  uv run python amazon/amazon-climbing-stairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-climbing-stairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def climbStairs(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in climbStairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().climbStairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
