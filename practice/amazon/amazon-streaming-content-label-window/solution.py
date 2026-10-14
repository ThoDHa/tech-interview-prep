"""Longest Content Window with Bounded Labels — https://www.fastprep.io/problems/amazon-streaming-content-label-window

Write-up & approaches: ../../../docs/amazon/amazon-streaming-content-label-window.md

A content stream arrives in order. Each item carries a non-empty set of labels. Given contentLabels and a limit k, find the longest contiguous window of items whose combined label set contains at most

  uv run python amazon_oa/amazon-streaming-content-label-window/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-streaming-content-label-window/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestContentWindow(self, contentLabels, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestContentWindow above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestContentWindow(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
