"""Climbing Stairs: https://leetcode.com/problems/climbing-stairs/

Write-up & approaches: ../../docs/problems/climbing_stairs.md

You climb `n` stairs, 1 or 2 steps at a time. Return how many distinct ways you
can reach the top.

  uv run python climbing_stairs/solution.py   # debug one case (see CASE below)
  uv run pytest climbing_stairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def climbStairs(self, n: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in climbStairs above, then run this file.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().climbStairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
