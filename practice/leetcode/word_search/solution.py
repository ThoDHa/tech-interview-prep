"""Word Search: https://leetcode.com/problems/word-search/

Write-up & approaches: ../../docs/problems/word_search.md

Given an `m x n` grid of characters `board` and a string `word`, return `True` if
`word` can be spelled out by a path of horizontally/vertically adjacent cells,
using each cell at most once.

  uv run python word_search/solution.py   # debug one case (see CASE below)
  uv run pytest word_search/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in exist above, then run this file.
    # exist mutates the board in place, so we hand it a fresh copy per run.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    board = [row[:] for row in case["args"][0]]
    word = case["args"][1]
    result = Solution().exist(board, word)
    print(f"case {case['id']}: board = {case['args'][0]}, word = {word!r}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
