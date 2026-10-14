"""Word Search: https://leetcode.com/problems/word-search/

Write-up & approaches: ../../../docs/leetcode/word_search.md

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
        visited = set()
        (
            rows,
            cols,
        ) = len(
            board
        ), len(board[0])
        word_length = len(word)

        def dfs(r: int, c: int, found_length: int) -> bool:
            if found_length == word_length:
                return True
            if r < 0 or r >= rows:
                return False
            if c < 0 or c >= cols:
                return False
            if (r, c) in visited:
                return False

            if board[r][c] != word[found_length]:
                return False

            visited.add((r, c))

            found = (
                dfs(r + 1, c, found_length + 1)
                or dfs(r - 1, c, found_length + 1)
                or dfs(r, c + 1, found_length + 1)
                or dfs(r, c - 1, found_length + 1)
            )
            visited.remove((r, c))
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False


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
