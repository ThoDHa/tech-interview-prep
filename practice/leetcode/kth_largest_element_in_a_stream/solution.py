"""Kth Largest Element In a Stream — https://leetcode.com/problems/kth-largest-element-in-a-stream/

Write-up & approaches: ../../docs/problems/kth_largest_element_in_a_stream.md

Design a class to find the `kth` largest integer in a stream of values, including duplicates. E.g. the `2nd` largest from [1, 2, 3, 3] is `3`. The stream is not necessarily sorted. Implement the follo

  uv run python kth_largest_element_in_a_stream/solution.py   # debug one case (see CASE below)
  uv run pytest kth_largest_element_in_a_stream/              # run the test sets
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
