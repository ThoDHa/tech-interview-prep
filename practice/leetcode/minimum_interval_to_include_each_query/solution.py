"""Minimum Interval to Include Each Query — https://leetcode.com/problems/minimum-interval-to-include-each-query/

Write-up & approaches: ../../docs/problems/minimum_interval_to_include_each_query.md

You are given a 2D integer array `intervals`, where `intervals[i] = [left_i, right_i]` represents the `ith` interval starting at `left_i` and ending at `right_i` **(inclusive)**. You are also given an

  uv run python minimum_interval_to_include_each_query/solution.py   # debug one case (see CASE below)
  uv run pytest minimum_interval_to_include_each_query/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minInterval(self, intervals, queries):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minInterval above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minInterval(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
