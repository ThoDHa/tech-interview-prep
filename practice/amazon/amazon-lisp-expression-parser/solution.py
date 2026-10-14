"""Lisp Expression Parser — https://www.fastprep.io/problems/amazon-lisp-expression-parser

Write-up & approaches: ../../../docs/amazon/amazon-lisp-expression-parser.md

Source note: The reported task identifies this algorithmic exercise. The executable interface, bounds, deterministic tie rules, and examples are the documented practice contract.

  uv run python amazon_oa/amazon-lisp-expression-parser/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-lisp-expression-parser/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def parseLispExpression(self, expression):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in parseLispExpression above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().parseLispExpression(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
