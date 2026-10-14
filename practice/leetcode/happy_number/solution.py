"""Happy Number — https://leetcode.com/problems/happy-number/

Write-up & approaches: ../../docs/problems/happy_number.md

A **non-cyclical number** is an integer defined by the following algorithm: * Given a positive integer, replace it with the sum of the squares of its digits. * Repeat the above step until the number e

  uv run python happy_number/solution.py   # debug one case (see CASE below)
  uv run pytest happy_number/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isHappy(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isHappy above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isHappy(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
