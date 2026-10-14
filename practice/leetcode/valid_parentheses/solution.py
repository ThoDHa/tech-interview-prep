"""Valid Parentheses: https://leetcode.com/problems/valid-parentheses/

Write-up & approaches: ../../docs/problems/valid_parentheses.md

Given a string `s` of just `'()[]{}'`, determine whether every bracket is
closed by the same type in the correct order.

  uv run python valid_parentheses/solution.py   # debug one case (see CASE below)
  uv run pytest valid_parentheses/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isValid(self, s: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isValid above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isValid(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
