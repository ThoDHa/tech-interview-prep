"""Binary Search: https://leetcode.com/problems/binary-search/

Write-up & approaches: ../../docs/problems/binary_search.md

Given an array of integers `nums` sorted in ascending order and an integer
`target`, return the index of `target` in `nums`, or -1 if it is absent. The
algorithm must run in `O(log n)` time.

  uv run python binary_search/solution.py     # debug one case (see CASE below)
  uv run pytest binary_search/                # run the test sets
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
