"""Design Add And Search Words Data Structure — https://leetcode.com/problems/design-add-and-search-words-data-structure/

Write-up & approaches: ../../docs/problems/design_add_and_search_words_data_structure.md

Design a data structure that supports adding new words and searching for existing words. Implement the `WordDictionary` class: * `void addWord(word)` Adds `word` to the data structure. * `bool search(

  uv run python design_add_and_search_words_data_structure/solution.py   # debug one case (see CASE below)
  uv run pytest design_add_and_search_words_data_structure/              # run the test sets
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
