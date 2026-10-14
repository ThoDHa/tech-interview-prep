"""Word Ladder: https://leetcode.com/problems/word-ladder/

Write-up & approaches: ../../docs/problems/word_ladder.md

Given `beginWord`, `endWord`, and a dictionary `wordList`, return the number of
words in the shortest transformation sequence from `beginWord` to `endWord`
(changing one letter at a time, each intermediate word in `wordList`), or `0` if
no such sequence exists.

  uv run python word_ladder/solution.py     # debug one case (see CASE below)
  uv run pytest word_ladder/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in ladderLength above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().ladderLength(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
