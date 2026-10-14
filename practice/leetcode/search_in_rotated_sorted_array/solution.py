"""Search in Rotated Sorted Array: https://leetcode.com/problems/search-in-rotated-sorted-array/

Write-up & approaches: ../../docs/problems/search_in_rotated_sorted_array.md

An ascending array of distinct values is rotated at an unknown pivot. Given the
rotated `nums` and a `target`, return the index of `target`, or `-1` if it is
absent. The algorithm must run in `O(log n)` time.

  uv run python search_in_rotated_sorted_array/solution.py   # debug one case (see CASE below)
  uv run pytest search_in_rotated_sorted_array/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in search above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().search(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
