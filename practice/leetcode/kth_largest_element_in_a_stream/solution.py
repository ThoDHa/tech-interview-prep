"""Kth Largest Element In a Stream — https://leetcode.com/problems/kth-largest-element-in-a-stream/

Write-up & approaches: ../../../docs/leetcode/kth_largest_element_in_a_stream.md

Design a class to find the `kth` largest integer in a stream of values, including duplicates. E.g. the `2nd` largest from [1, 2, 3, 3] is `3`. The stream is not necessarily sorted. Implement the follo

  uv run python leetcode/kth_largest_element_in_a_stream/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/kth_largest_element_in_a_stream/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class KthLargest:
    def __init__(self, k: int, nums: List[int]) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def add(self, val: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a KthLargest method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "classic_example"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(KthLargest, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement KthLargest's methods first")
