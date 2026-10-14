"""Basic Calculator — https://www.fastprep.io/problems/amazon-basic-calculator

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-basic-calculator.md

Given a valid arithmetic expression s, return its evaluated integer value.

  uv run python amazon_oa/amazon-basic-calculator/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-basic-calculator/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculate(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
