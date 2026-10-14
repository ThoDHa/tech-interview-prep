"""Set Matrix Zeroes — https://leetcode.com/problems/set-matrix-zeroes/

Write-up & approaches: ../../docs/problems/set_matrix_zeroes.md

Given an `m x n` matrix of integers `matrix`, if an element is `0`, set its entire row and column to `0`'s. You must update the matrix *in-place*.

  uv run python set_matrix_zeroes/solution.py   # debug one case (see CASE below)
  uv run pytest set_matrix_zeroes/              # run the test sets
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
