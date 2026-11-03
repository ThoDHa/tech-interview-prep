"""Detect Squares — https://leetcode.com/problems/detect-squares/

Write-up & approaches: ../../../docs/leetcode/detect_squares.md

You are given a stream of points consisting of x-y coordinates on a 2-D plane. Points can be added and queried as follows: * **Add** - new points can be added to the stream into a data structure. Dupl

  uv run python leetcode/detect_squares/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/detect_squares/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class CountSquares:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def add(self, point: List[int]) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def count(self, point: List[int]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a CountSquares method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "empty_count_is_zero"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(CountSquares, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement CountSquares's methods first")
