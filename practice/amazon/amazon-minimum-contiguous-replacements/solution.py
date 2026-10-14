"""Minimum Contiguous Replacements — https://www.fastprep.io/problems/amazon-minimum-contiguous-replacements

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-contiguous-replacements.md

You are given an array arr of integers. In one operation, choose two distinct values x and y that currently appear in the array, then replace every occurrence of x with y.

  uv run python amazon_oa/amazon-minimum-contiguous-replacements/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-contiguous-replacements/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minOperations(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
