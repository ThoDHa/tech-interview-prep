"""Minimum Operations to Sort a Permutation — https://www.fastprep.io/problems/amazon-minimum-operations-to-sort-permutation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-operations-to-sort-permutation.md

You are given a permutation arr of size n, containing each integer from 1 to n exactly once.

  uv run python amazon_oa/amazon-minimum-operations-to-sort-permutation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-operations-to-sort-permutation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minOperationsToSortPermutation(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minOperationsToSortPermutation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minOperationsToSortPermutation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
