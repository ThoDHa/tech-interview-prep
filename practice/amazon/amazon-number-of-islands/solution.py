"""Number of Islands — https://www.fastprep.io/problems/amazon-number-of-islands

Write-up & approaches: ../../../docs/amazon/amazon-number-of-islands.md

Given an array of equal-length strings grid, where '1' represents land and '0' represents water, return the number of islands.

  uv run python amazon_oa/amazon-number-of-islands/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-number-of-islands/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
