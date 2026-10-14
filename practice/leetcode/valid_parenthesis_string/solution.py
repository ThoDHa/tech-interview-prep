"""Valid Parenthesis String — https://leetcode.com/problems/valid-parenthesis-string/

Write-up & approaches: ../../docs/problems/valid_parenthesis_string.md

You are given a string `s` which contains only three types of characters: `'('`, `')'` and `'*'`. Return `true` if `s` is **valid**, otherwise return `false`. A string is valid if it follows all of th

  uv run python valid_parenthesis_string/solution.py   # debug one case (see CASE below)
  uv run pytest valid_parenthesis_string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def checkValidString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in checkValidString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().checkValidString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
