"""Find Median from Data Stream: https://leetcode.com/problems/find-median-from-data-stream/

Write-up & approaches: ../../docs/problems/find_median_from_data_stream.md

Design a MedianFinder that supports adding integers from a stream and querying
the median of all elements added so far.

  uv run python find_median_from_data_stream/solution.py     # debug one case (see CASE below)
  uv run pytest find_median_from_data_stream/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class MedianFinder:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def addNum(self, num: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def findMedian(self) -> float:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a MedianFinder method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(MedianFinder, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement MedianFinder's methods first")
