"""Dynamic Kth Largest Queries — https://www.fastprep.io/problems/amazon-dynamic-kth-largest-queries

Write-up & approaches: ../../../docs/amazon/amazon-dynamic-kth-largest-queries.md

You are given an initial list of integer values and a stream of operations. The list changes over time as values are inserted.

  uv run python amazon/amazon-dynamic-kth-largest-queries/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-dynamic-kth-largest-queries/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class DynamicKthLargest:
    def __init__(self, initial_values: List[int]) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def insert(self, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def find(self, k: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a DynamicKthLargest method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(DynamicKthLargest, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement DynamicKthLargest's methods first")
