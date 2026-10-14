"""Word Search II — https://www.fastprep.io/problems/amazon-word-search-ii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-word-search-ii.md

Given an m x n board of lowercase English letters and an array of distinct lowercase words, return every word that can be formed on the board.

  uv run python amazon_oa/amazon-word-search-ii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-word-search-ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findWords(self, board, words):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findWords above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findWords(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
