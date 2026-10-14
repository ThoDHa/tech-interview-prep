"""Optimal Interval Difference — https://www.fastprep.io/problems/amazon-optimal-interval-difference

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-optimal-interval-difference.md

AMZ Interval Collection (A group of problems focused on operations involving intervals :) - 

  uv run python amazon_oa/amazon-optimal-interval-difference/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-optimal-interval-difference/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def optimalIntervalDifference(self, intervals):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in optimalIntervalDifference above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().optimalIntervalDifference(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
