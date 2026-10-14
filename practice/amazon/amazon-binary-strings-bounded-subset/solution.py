"""Largest Binary-String Subset Within Bit Budgets — https://www.fastprep.io/problems/amazon-binary-strings-bounded-subset

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-binary-strings-bounded-subset.md

Given an array of binary strings strs and two budgets, maxOnes and maxZeroes, return the maximum number of strings you can select.

  uv run python amazon_oa/amazon-binary-strings-bounded-subset/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-binary-strings-bounded-subset/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def largestBoundedSubset(self, strs, maxOnes, maxZeroes):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in largestBoundedSubset above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().largestBoundedSubset(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
