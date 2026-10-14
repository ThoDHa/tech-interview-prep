"""Maximize Sum of Array Multiplication — https://www.fastprep.io/problems/amazon-maximize-sum-of-array-multiplication

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-sum-of-array-multiplication.md

You have an array of data (index starting from 1)

  uv run python amazon_oa/amazon-maximize-sum-of-array-multiplication/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-sum-of-array-multiplication/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeSum(self, data):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
