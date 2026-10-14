"""Longest Substring Without Repeating Characters: https://leetcode.com/problems/longest-substring-without-repeating-characters/

Write-up & approaches: ../../docs/problems/longest_substring_without_repeating_characters.md

Given a string `s`, find the length of the longest substring without repeating
characters.

  uv run python longest_substring_without_repeating_characters/solution.py     # debug one case (see CASE below)
  uv run pytest longest_substring_without_repeating_characters/                # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lengthOfLongestSubstring above, then
    # run this file. Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().lengthOfLongestSubstring(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
