"""Rotting Oranges: https://leetcode.com/problems/rotting-oranges/

Write-up & approaches: ../../docs/problems/rotting_oranges.md

Given an `m x n` grid of cells (`0` empty, `1` fresh, `2` rotten), each minute
every fresh orange 4-directionally adjacent to a rotten one rots. Return the
minimum minutes until no fresh orange remains, or `-1` if some never rot.

  uv run python rotting_oranges/solution.py     # debug one case (see CASE below)
  uv run pytest rotting_oranges/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in orangesRotting above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().orangesRotting(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
