"""Minimum Window Substring: https://leetcode.com/problems/minimum-window-substring/

Write-up & approaches: ../../docs/problems/minimum_window_substring.md

Given two strings `s` and `t`, return the shortest substring of `s` that contains
every character of `t` (including duplicates), or `""` if no such window exists.

  uv run python minimum_window_substring/solution.py   # debug one case (see CASE below)
  uv run pytest minimum_window_substring/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minWindow above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minWindow(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
