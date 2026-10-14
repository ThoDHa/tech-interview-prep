"""Recent Advertisement Click Counts — https://www.fastprep.io/problems/amazon-ad-click-counts-sliding-window

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-ad-click-counts-sliding-window.md

You receive a finite sequence of advertisement click and count operations. Each operation is one of:

  uv run python amazon_oa/amazon-ad-click-counts-sliding-window/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-ad-click-counts-sliding-window/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countRecentAdClicks(self, operations, kMinutes):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countRecentAdClicks above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countRecentAdClicks(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
