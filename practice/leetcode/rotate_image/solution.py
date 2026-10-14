"""Rotate Image — https://leetcode.com/problems/rotate-image/

Write-up & approaches: ../../docs/problems/rotate_image.md

Given a square `n x n` matrix of integers `matrix`, rotate it by 90 degrees *clockwise*. You must rotate the matrix *in-place*. Do not allocate another 2D matrix and do the rotation.

  uv run python rotate_image/solution.py   # debug one case (see CASE below)
  uv run pytest rotate_image/              # run the test sets
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
