"""Generate Parentheses — https://leetcode.com/problems/generate-parentheses/

Write-up & approaches: ../../docs/problems/generate_parentheses.md

You are given an integer `n`. Return all well-formed parentheses strings that you can generate with `n` pairs of parentheses.

  uv run python generate_parentheses/solution.py   # debug one case (see CASE below)
  uv run pytest generate_parentheses/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def generateParenthesis(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in generateParenthesis above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().generateParenthesis(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
