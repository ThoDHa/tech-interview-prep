"""Jump Game II — https://leetcode.com/problems/jump-game-ii/

Write-up & approaches: ../../docs/problems/jump_game_ii.md

You are given an array of integers `nums`, where `nums[i]` represents the maximum length of a jump towards the right from index `i`. For example, if you are at `nums[i]`, you can jump to any index `i 

  uv run python jump_game_ii/solution.py   # debug one case (see CASE below)
  uv run pytest jump_game_ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def jump(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in jump above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().jump(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
