"""Jump Game — https://leetcode.com/problems/jump-game/

Write-up & approaches: ../../docs/problems/jump_game.md
Reference implementation of the write-up's Greedy solution, kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python jump_game/reference.py   # replay the example cases
  uv run pytest jump_game/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """Return whether the last index is reachable from index 0.

        Time:  O(n): one backward pass, one comparison per index.
        Space: O(1): one boundary integer.
        """
        target = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= target:
                target = i
        return target == 0


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().canJump(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
