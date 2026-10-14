"""Remove K Digits — https://www.fastprep.io/problems/amazon-remove-k-digits

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-remove-k-digits.md

You are given a string num that represents a non-negative integer, and an integer k.

  uv run python amazon_oa/amazon-remove-k-digits/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-remove-k-digits/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def removeKdigits(self, num, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in removeKdigits above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().removeKdigits(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
