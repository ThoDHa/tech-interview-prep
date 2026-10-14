"""Sliding Window Maximum — https://www.fastprep.io/problems/amazon-sliding-window-maximum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sliding-window-maximum.md

Given an integer array nums and a window size k, return the maximum value in every contiguous window of length k, from left to right.

  uv run python amazon_oa/amazon-sliding-window-maximum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sliding-window-maximum/              # run the test sets
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
