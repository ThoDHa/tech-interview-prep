"""Longest Repeating Character Replacement — https://leetcode.com/problems/longest-repeating-character-replacement/

Write-up & approaches: ../../docs/problems/longest_repeating_character_replacement.md

You are given a string `s` consisting of only uppercase english characters and an integer `k`. You can choose up to `k` characters of the string and replace them with any other uppercase English chara

  uv run python longest_repeating_character_replacement/solution.py   # debug one case (see CASE below)
  uv run pytest longest_repeating_character_replacement/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def characterReplacement(self, s, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in characterReplacement above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().characterReplacement(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
