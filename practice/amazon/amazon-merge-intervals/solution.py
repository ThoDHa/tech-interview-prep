"""Merge Intervals — https://www.fastprep.io/problems/amazon-merge-intervals

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-merge-intervals.md

Given an array of closed intervals where intervals[i] = [start_i, end_i], merge every pair of overlapping intervals.

  uv run python amazon_oa/amazon-merge-intervals/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-merge-intervals/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def merge(self, intervals):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in merge above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().merge(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
