"""Reverse Integer — https://leetcode.com/problems/reverse-integer/

Write-up & approaches: ../../docs/problems/reverse_integer.md

You are given a signed 32-bit integer `x`. Return `x` after reversing each of its digits. After reversing, if `x` goes outside the signed 32-bit integer range `[-2^31, 2^31 - 1]`, then return `0` inst

  uv run python reverse_integer/solution.py   # debug one case (see CASE below)
  uv run pytest reverse_integer/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def reverse(self, x):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in reverse above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().reverse(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
