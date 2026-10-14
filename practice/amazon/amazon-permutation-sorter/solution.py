"""Permutation Sorter — https://www.fastprep.io/problems/amazon-permutation-sorter

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-permutation-sorter.md

Amazon engineers are testing a new tool, the Permutation Sorter, built to reorder sequences using limited operations.

  uv run python amazon_oa/amazon-permutation-sorter/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-permutation-sorter/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumOperations(self, arr):
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
