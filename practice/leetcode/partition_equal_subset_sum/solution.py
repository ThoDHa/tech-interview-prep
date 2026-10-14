"""Partition Equal Subset Sum: https://leetcode.com/problems/partition-equal-subset-sum/

Write-up & approaches: ../../docs/problems/partition_equal_subset_sum.md

Given an integer array `nums`, return `True` if it can be partitioned into two
subsets with equal sum.

  uv run python partition_equal_subset_sum/solution.py   # debug one case (see CASE below)
  uv run pytest partition_equal_subset_sum/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canPartition above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canPartition(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
