"""Longest Substring Without Repeating Characters — https://www.fastprep.io/problems/amazon-longest-substring-without-repeating-characters

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-longest-substring-without-repeating-characters.md

Given a string s, return the length of the longest contiguous substring whose characters are all distinct.

  uv run python amazon_oa/amazon-longest-substring-without-repeating-characters/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-longest-substring-without-repeating-characters/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def lengthOfLongestSubstring(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lengthOfLongestSubstring above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().lengthOfLongestSubstring(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
