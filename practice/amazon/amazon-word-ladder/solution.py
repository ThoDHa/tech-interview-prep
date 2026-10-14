"""Word Ladder — https://www.fastprep.io/problems/amazon-word-ladder

Write-up & approaches: ../../../docs/amazon/amazon-word-ladder.md

You are given beginWord, endWord, and a dictionary wordList. A transformation changes exactly one character, and every transformed word—including endWord—must appear in the dictionary.

  uv run python amazon_oa/amazon-word-ladder/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-word-ladder/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def ladderLength(self, beginWord, endWord, wordList):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in ladderLength above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().ladderLength(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
