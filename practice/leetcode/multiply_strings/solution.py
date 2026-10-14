"""Multiply Strings — https://leetcode.com/problems/multiply-strings/

Write-up & approaches: ../../docs/problems/multiply_strings.md

You are given two strings `num1` and `num2` that represent non-negative integers. Return the product of `num1` and `num2` in the form of a string. Assume that neither `num1` nor `num2` contain any lea

  uv run python multiply_strings/solution.py   # debug one case (see CASE below)
  uv run pytest multiply_strings/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def multiply(self, num1, num2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in multiply above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().multiply(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
