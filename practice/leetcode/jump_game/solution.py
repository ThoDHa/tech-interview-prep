"""Jump Game — https://leetcode.com/problems/jump-game/

Write-up & approaches: ../../docs/problems/jump_game.md

You are given an integer array `nums` where each element `nums[i]` indicates your maximum jump length at that position. Return `true` if you can reach the last index starting from index `0`, or `false

  uv run python jump_game/solution.py   # debug one case (see CASE below)
  uv run pytest jump_game/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def canJump(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canJump above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canJump(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
