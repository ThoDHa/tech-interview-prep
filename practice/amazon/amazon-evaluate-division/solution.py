"""Evaluate Division — https://www.fastprep.io/problems/amazon-evaluate-division

Write-up & approaches: ../../../docs/amazon/amazon-evaluate-division.md

You are given variable pairs equations and positive real numbers values. For every index i, equations[i] = [a, b] and values[i] mean a / b = values[i].

  uv run python amazon_oa/amazon-evaluate-division/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-evaluate-division/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calcEquation(self, equations, values, queries):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calcEquation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calcEquation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
