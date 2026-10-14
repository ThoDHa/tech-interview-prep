"""Word Search II — https://leetcode.com/problems/word-search-ii/

Write-up & approaches: ../../docs/problems/word_search_ii.md

Given a 2-D grid of characters `board` and a list of strings `words`, return all words that are present in the grid. For a word to be present it must be possible to form the word with a path in the bo

  uv run python word_search_ii/solution.py   # debug one case (see CASE below)
  uv run pytest word_search_ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
