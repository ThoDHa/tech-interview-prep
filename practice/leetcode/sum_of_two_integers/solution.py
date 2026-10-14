"""Sum of Two Integers — https://leetcode.com/problems/sum-of-two-integers/

Write-up & approaches: ../../docs/problems/sum_of_two_integers.md

Given two integers `a` and `b`, return the sum of the two integers without using the `+` and `-` operators.

  uv run python sum_of_two_integers/solution.py   # debug one case (see CASE below)
  uv run pytest sum_of_two_integers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getSum(self, a, b):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
