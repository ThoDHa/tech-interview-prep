"""Basic Calculator: https://leetcode.com/problems/basic-calculator/

Write-up & approaches: ../../docs/problems/basic_calculator.md

Given a string `s` representing a valid expression of integers, `+`, `-`,
parentheses, and spaces, evaluate it and return the result without using `eval`.

  uv run python basic_calculator/solution.py   # debug one case (see CASE below)
  uv run pytest basic_calculator/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculate(self, s: str) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculate above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
