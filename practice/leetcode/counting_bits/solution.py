"""Counting Bits — https://leetcode.com/problems/counting-bits/

Write-up & approaches: ../../docs/problems/counting_bits.md

Given an integer `n`, count the number of `1`'s in the binary representation of every number in the range `[0, n]`. Return an array `output` where `output[i]` is the number of `1`'s in the binary repr

  uv run python counting_bits/solution.py   # debug one case (see CASE below)
  uv run pytest counting_bits/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countBits(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countBits above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countBits(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
