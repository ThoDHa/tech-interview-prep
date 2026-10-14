"""Sliding Window Maximum — https://leetcode.com/problems/sliding-window-maximum/

Write-up & approaches: ../../docs/problems/sliding_window_maximum.md

You are given an array of integers `nums` and an integer `k`. There is a sliding window of size `k` that starts at the left edge of the array. The window slides one position to the right until it reac

  uv run python sliding_window_maximum/solution.py   # debug one case (see CASE below)
  uv run pytest sliding_window_maximum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxSlidingWindow(self, nums, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSlidingWindow above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSlidingWindow(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
