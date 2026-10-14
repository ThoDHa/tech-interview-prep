"""Word Ladder: https://leetcode.com/problems/word-ladder/

Write-up & approaches: ../../../docs/leetcode/word_ladder.md

Given `beginWord`, `endWord`, and a dictionary `wordList`, return the number of
words in the shortest transformation sequence from `beginWord` to `endWord`
(changing one letter at a time, each intermediate word in `wordList`), or `0` if
no such sequence exists.

  uv run python word_ladder/solution.py     # debug one case (see CASE below)
  uv run pytest word_ladder/                # run the test sets
"""
from collections import deque

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        if endWord not in wordList:
            return 0

        word_set = set(wordList)

        visited = {beginWord}

        queue = deque([(beginWord, 1)])

        while queue:
            current_word, length  = queue.popleft()

            for i in range(len(current_word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c == current_word[i]:
                        continue

                    new_word = current_word[:i] + c + current_word[i+1:]

                    if new_word == endWord:
                        return length + 1

                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, length + 1))
        return 0

if __name__ == "__main__":
    # Debug playground: set a breakpoint in ladderLength above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().ladderLength(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
