"""Reverse Bits — https://leetcode.com/problems/reverse-bits/

Write-up & approaches: ../../docs/problems/reverse_bits.md

Given a 32-bit unsigned integer `n`, reverse the bits of the binary representation of `n` and return the result.

  uv run python reverse_bits/solution.py   # debug one case (see CASE below)
  uv run pytest reverse_bits/              # run the test sets
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
