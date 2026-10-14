"""Regular Expression Matching — https://leetcode.com/problems/regular-expression-matching/

Write-up & approaches: ../../docs/problems/regular_expression_matching.md

You are given an input string `s` consisting of lowercase english letters, and a pattern `p` consisting of lowercase english letters, as well as `'.'`, and `'*'` characters. Return `true` if the patte

  uv run python regular_expression_matching/solution.py   # debug one case (see CASE below)
  uv run pytest regular_expression_matching/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isMatch(self, s, p):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isMatch above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isMatch(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
