"""Find the Safest Path in a Grid — https://www.fastprep.io/problems/amazon-find-safest-path-in-grid

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-safest-path-in-grid.md

You are given an n x n binary matrix grid. A cell containing 1 contains a thief, and a cell containing 0 is empty.

  uv run python amazon_oa/amazon-find-safest-path-in-grid/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-safest-path-in-grid/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumSafenessFactor(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumSafenessFactor above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumSafenessFactor(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
