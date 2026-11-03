"""Dynamic Prefix Search Collection — https://www.fastprep.io/problems/amazon-prefix-search-collection

Write-up & approaches: ../../../docs/amazon/amazon-prefix-search-collection.md

Implement a dynamic collection of lowercase words. Process the finite array operations from left to right.

  uv run python amazon/amazon-prefix-search-collection/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-prefix-search-collection/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class PrefixSearchCollection:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def insert(self, word: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def search(self, prefix: str) -> List[str]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a PrefixSearchCollection method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(PrefixSearchCollection, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement PrefixSearchCollection's methods first")
