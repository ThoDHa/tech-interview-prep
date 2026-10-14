"""Longest Consecutive Sequence — https://leetcode.com/problems/longest-consecutive-sequence/

Write-up & approaches: ../../docs/problems/longest_consecutive_sequence.md

Given an array of integers `nums`, return *the length* of the longest consecutive sequence of elements that can be formed. A *consecutive sequence* is a sequence of elements in which each element is e

  uv run python longest_consecutive_sequence/solution.py   # debug one case (see CASE below)
  uv run pytest longest_consecutive_sequence/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestConsecutive(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestConsecutive above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestConsecutive(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
