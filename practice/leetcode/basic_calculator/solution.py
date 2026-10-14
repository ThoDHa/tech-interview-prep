"""Basic Calculator: https://leetcode.com/problems/basic-calculator/

Write-up & approaches: ../../../docs/leetcode/basic_calculator.md

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
        result = 0
        number = 0
        sign = 1
        signs = [1]

        for c in s:
            if c.isdigit():
                number = number * 10 + int(c)
            elif c == "+":
                result += sign * number
                number = 0
                sign = signs[-1]
            elif c == "-":
                result += sign * number
                number = 0
                sign = -signs[-1]
            elif c == "(":
                signs.append(sign)
                sign = signs[-1]
            elif c == ")":
                result += sign * number
                number = 0
                signs.pop()
                sign = signs[-1]

        result += sign * number
        return result

if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculate above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
