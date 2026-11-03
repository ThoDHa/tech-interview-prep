"""Design Add And Search Words Data Structure — https://leetcode.com/problems/design-add-and-search-words-data-structure/

Write-up & approaches: ../../../docs/leetcode/design_add_and_search_words_data_structure.md

Design a data structure that supports adding new words and searching for existing words. Implement the `WordDictionary` class: * `void addWord(word)` Adds `word` to the data structure. * `bool search(

  uv run python leetcode/design_add_and_search_words_data_structure/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/design_add_and_search_words_data_structure/              # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class WordDictionary:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def addWord(self, word: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def search(self, word: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a WordDictionary method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "empty_search_literal"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(WordDictionary, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement WordDictionary's methods first")
