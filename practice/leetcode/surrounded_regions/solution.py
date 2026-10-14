"""Surrounded Regions — https://leetcode.com/problems/surrounded-regions/

Write-up & approaches: ../../docs/problems/surrounded_regions.md

You are given an `m x n` matrix `board` containing letters `'X'` and `'O'`, capture regions that are surrounded: * **Connect:** A cell is connected to adjacent cells horizontally or vertically. * **Re

  uv run python surrounded_regions/solution.py   # debug one case (see CASE below)
  uv run pytest surrounded_regions/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
