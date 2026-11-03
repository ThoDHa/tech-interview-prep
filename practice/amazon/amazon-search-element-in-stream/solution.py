"""Search for an Element in a Stream — https://www.fastprep.io/problems/amazon-search-element-in-stream

Write-up & approaches: ../../../docs/amazon/amazon-search-element-in-stream.md

Values arrive one at a time in a stream. At any moment, you may be asked whether a given value has already arrived.

  uv run python amazon/amazon-search-element-in-stream/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-search-element-in-stream/              # run the test sets
"""
from harness import NotSolved, pick_case, run_operations


class StreamSearch:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def add(self, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def search(self, value: int) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a StreamSearch method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(StreamSearch, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement StreamSearch's methods first")
