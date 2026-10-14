"""Largest Number With Digit Sum — https://www.fastprep.io/problems/amazon-largest-number-with-digit-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-largest-number-with-digit-sum.md

You are given three integers x, y, and n, where x and y are digits from 1 to 9.

  uv run python amazon_oa/amazon-largest-number-with-digit-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-largest-number-with-digit-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def largestNumberWithDigitSum(self, x, y, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in largestNumberWithDigitSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().largestNumberWithDigitSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
