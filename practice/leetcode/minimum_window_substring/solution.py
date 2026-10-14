"""Minimum Window Substring: https://leetcode.com/problems/minimum-window-substring/

Write-up & approaches: ../../../docs/leetcode/minimum_window_substring.md

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
        if len(s) < len(t):
            return ""

        t_count = {}

        for c in t:
            t_count[c] = t_count.get(c, 0) + 1
        required = len(t_count)
        formed = 0
        left = right = 0
        min_left = 0
        min_len = float("inf")

        window_count = {}
        while right < len(s):
            c = s[right]
            window_count[c] = window_count.get(c, 0) + 1

            if c in t_count and t_count[c] == window_count[c]:
                formed += 1

            while left <= right and formed == required:
                c = s[left]
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left

                # Remove character at left from window
                window_count[c] -= 1
                if c in t_count and window_count[c] < t_count[c]:
                    formed -= 1

                left += 1
            right += 1

        return "" if min_len == float("inf") else s[min_left : min_left + min_len]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minWindow above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minWindow(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
