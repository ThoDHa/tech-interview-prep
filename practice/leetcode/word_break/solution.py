"""Word Break: https://leetcode.com/problems/word-break/

Write-up & approaches: ../../docs/problems/word_break.md

Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s`
can be segmented into a space-separated sequence of one or more dictionary
words. The same word may be reused multiple times.

  uv run python word_break/solution.py     # debug one case (see CASE below)
  uv run pytest word_break/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in wordBreak above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().wordBreak(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
