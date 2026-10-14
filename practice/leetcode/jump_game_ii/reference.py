"""Jump Game II — https://leetcode.com/problems/jump-game-ii/

Write-up & approaches: ../../docs/problems/jump_game_ii.md
Reference implementation of the write-up's Greedy solution, kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python jump_game_ii/reference.py   # replay the example cases
  uv run pytest jump_game_ii/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def jump(self, nums: List[int]) -> int:
        """Return the minimum number of jumps to reach the last index.

        Time:  O(n): one forward pass, constant work per index.
        Space: O(1): three integers.
        """
        jumps = 0
        current_end = 0
        farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == current_end:
                jumps += 1
                current_end = farthest
        return jumps


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().jump(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
