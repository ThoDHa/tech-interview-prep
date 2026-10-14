"""Evaluate Reverse Polish Notation: https://leetcode.com/problems/evaluate-reverse-polish-notation/

Write-up & approaches: ../../docs/problems/evaluate_reverse_polish_notation.md

Evaluate an arithmetic expression given in Reverse Polish Notation and return its
integer value (division truncates toward zero).

  uv run python evaluate_reverse_polish_notation/solution.py   # debug one case (see CASE below)
  uv run pytest evaluate_reverse_polish_notation/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in evalRPN above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().evalRPN(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
