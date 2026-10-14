"""Merge Intervals: https://leetcode.com/problems/merge-intervals/

Write-up & approaches: ../../docs/problems/merge_intervals.md

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all
overlapping intervals and return an array of the non-overlapping intervals that
cover all the intervals in the input. The answer may be returned in any order.

  uv run python merge_intervals/solution.py     # debug one case (see CASE below)
  uv run pytest merge_intervals/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in merge above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().merge(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
