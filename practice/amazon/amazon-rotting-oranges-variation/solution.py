"""Minimum Time to Spread Through a Grid — https://www.fastprep.io/problems/amazon-rotting-oranges-variation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-rotting-oranges-variation.md

You are given a rectangular grid whose cells contain 0, 1, or 2. A zero is empty, a one is fresh, and a two is already active.

  uv run python amazon_oa/amazon-rotting-oranges-variation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-rotting-oranges-variation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minutesToSpread(self, grid):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minutesToSpread above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minutesToSpread(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
