"""Find Word-Multiset Windows — https://www.fastprep.io/problems/amazon-word-multiset-window-search

Write-up & approaches: ../../../docs/amazon/amazon-word-multiset-window-search.md

You are given a tokenized text textWords and a nonempty list targetWords. Return every word index at which a consecutive window contains exactly the same multiset of words as targetWords.

  uv run python amazon/amazon-word-multiset-window-search/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-word-multiset-window-search/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def wordWindowStarts(self, textWords, targetWords):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in wordWindowStarts above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().wordWindowStarts(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
