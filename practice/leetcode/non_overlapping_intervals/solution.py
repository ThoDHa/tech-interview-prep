"""Non Overlapping Intervals — https://leetcode.com/problems/non-overlapping-intervals/

Write-up & approaches: ../../docs/problems/non_overlapping_intervals.md

Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping. Note: Inte

  uv run python non_overlapping_intervals/solution.py   # debug one case (see CASE below)
  uv run pytest non_overlapping_intervals/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def eraseOverlapIntervals(self, intervals):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in eraseOverlapIntervals above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().eraseOverlapIntervals(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
