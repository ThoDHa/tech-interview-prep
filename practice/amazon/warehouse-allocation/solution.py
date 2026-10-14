"""Warehouse Distribution — https://www.fastprep.io/problems/warehouse-allocation

Write-up & approaches: ../../../docs/problems/amazon_oa/warehouse-allocation.md

Amazon has a warehouse that stores piles of boxes containing goods to be shipped. There are n piles numbered 1, 2, ..., n, where the i-th pile has boxes[i] boxes.

  uv run python amazon_oa/warehouse-allocation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/warehouse-allocation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumOperations(self, boxes):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
