"""Kth Smallest Sum from Sorted Matrix Rows — https://www.fastprep.io/problems/amazon-kth-smallest-row-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-kth-smallest-row-sum.md

Given an integer matrix mat whose rows are sorted in nondecreasing order, choose exactly one value from each row and add the chosen values.

  uv run python amazon_oa/amazon-kth-smallest-row-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-kth-smallest-row-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def kthSmallestRowSum(self, mat, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in kthSmallestRowSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().kthSmallestRowSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
