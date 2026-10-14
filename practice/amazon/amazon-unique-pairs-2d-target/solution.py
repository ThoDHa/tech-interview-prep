"""Unique Pairs in a 2D Matrix Summing to Target — https://www.fastprep.io/problems/amazon-unique-pairs-2d-target

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-unique-pairs-2d-target.md

Given a rectangular integer matrix matrix whose values are globally unique and an integer target, return the number of unordered pairs of values whose sum is target.

  uv run python amazon_oa/amazon-unique-pairs-2d-target/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-unique-pairs-2d-target/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countPairs(self, matrix, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
