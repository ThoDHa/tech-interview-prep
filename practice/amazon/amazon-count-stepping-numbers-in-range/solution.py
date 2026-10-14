"""Count Stepping Numbers In Range — https://www.fastprep.io/problems/amazon-count-stepping-numbers-in-range

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-stepping-numbers-in-range.md

A stepping number is an integer whose adjacent digits differ by exactly 1. Every one-digit integer, including 0, is a stepping number.

  uv run python amazon_oa/amazon-count-stepping-numbers-in-range/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-stepping-numbers-in-range/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countSteppingNumbers(self, low, high):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countSteppingNumbers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countSteppingNumbers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
