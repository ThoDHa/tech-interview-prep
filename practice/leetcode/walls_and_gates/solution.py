"""Walls And Gates — https://leetcode.com/problems/walls-and-gates/

Write-up & approaches: ../../docs/problems/walls_and_gates.md

You are given a $m \times n$ 2D `grid` initialized with these three possible values: 1. `-1` - A water cell that *can not* be traversed. 2. `0` - A treasure chest. 3. `INF` - A land cell that *can* be

  uv run python walls_and_gates/solution.py   # debug one case (see CASE below)
  uv run pytest walls_and_gates/              # run the test sets
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
