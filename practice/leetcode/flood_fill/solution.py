"""Flood Fill: https://leetcode.com/problems/flood-fill/

Write-up & approaches: ../../docs/problems/flood_fill.md

You are given an `m x n` grid `image` of pixel values plus a start pixel
`(sr, sc)` and a new `color`. Recolor the start pixel and every pixel
4-directionally connected to it that shares the start pixel's original color.
Return the modified image.

  uv run python flood_fill/solution.py     # debug one case (see CASE below)
  uv run pytest flood_fill/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def floodFill(
        self, image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in floodFill above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().floodFill(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
