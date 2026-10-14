"""Sort an Array with Rotate and Flip — https://www.fastprep.io/problems/amazon-sort-array-with-rotate-and-flip

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sort-array-with-rotate-and-flip.md

You are given an array values containing distinct integers. You may apply either of these operations:

  uv run python amazon_oa/amazon-sort-array-with-rotate-and-flip/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sort-array-with-rotate-and-flip/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minSortOperations(self, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minSortOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minSortOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
