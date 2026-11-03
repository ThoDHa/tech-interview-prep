"""Word Dictionary with Wildcard Find — https://www.fastprep.io/problems/amazon-wildcard-word-dictionary

Write-up & approaches: ../../../docs/amazon/amazon-wildcard-word-dictionary.md

Build a word dictionary that supports inserting words and finding words with wildcards. Process the rows of operations from left to right. The dictionary starts empty, and each row has one of these fo

  uv run python amazon/amazon-wildcard-word-dictionary/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-wildcard-word-dictionary/              # run the test sets
"""
from harness import NotSolved, pick_case, run_operations


class WordDictionary:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def insert(self, word: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def find(self, pattern: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a WordDictionary method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(WordDictionary, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement WordDictionary's methods first")
