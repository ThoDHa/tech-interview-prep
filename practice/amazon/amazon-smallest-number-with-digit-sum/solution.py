"""Smallest Number With a Given Digit Sum — https://www.fastprep.io/problems/amazon-smallest-number-with-digit-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-smallest-number-with-digit-sum.md

Given integers digitSum and numberOfDigits, construct the smallest non-negative decimal number that:

  uv run python amazon_oa/amazon-smallest-number-with-digit-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-smallest-number-with-digit-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def smallestNumberWithDigitSum(self, digitSum, numberOfDigits):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in smallestNumberWithDigitSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().smallestNumberWithDigitSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
