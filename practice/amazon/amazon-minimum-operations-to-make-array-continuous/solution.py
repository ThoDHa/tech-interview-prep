"""Minimum Operations to Make an Array Continuous — https://www.fastprep.io/problems/amazon-minimum-operations-to-make-array-continuous

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-operations-to-make-array-continuous.md

You are given a non-empty integer array nums of length n. In one operation, you may replace any one element with any integer.

  uv run python amazon_oa/amazon-minimum-operations-to-make-array-continuous/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-operations-to-make-array-continuous/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minOperations(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
