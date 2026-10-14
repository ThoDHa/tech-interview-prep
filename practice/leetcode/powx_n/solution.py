"""Pow(x, n) — https://leetcode.com/problems/powx-n/

Write-up & approaches: ../../docs/problems/powx_n.md

`Pow(x, n)` is a mathematical function to calculate the value of `x` raised to the power of `n` (i.e., `x^n`). Given a floating-point value `x` and an integer value `n`, implement the `myPow(x, n)` fu

  uv run python powx_n/solution.py   # debug one case (see CASE below)
  uv run pytest powx_n/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def myPow(self, x, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in myPow above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().myPow(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
