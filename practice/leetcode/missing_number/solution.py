"""Missing Number — https://leetcode.com/problems/missing-number/

Write-up & approaches: ../../docs/problems/missing_number.md

Given an array `nums` containing `n` integers in the range `[0, n]` without any duplicates, return the single number in the range that is missing from `nums`. **Follow-up**: Could you implement a solu

  uv run python missing_number/solution.py   # debug one case (see CASE below)
  uv run pytest missing_number/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def missingNumber(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in missingNumber above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().missingNumber(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
