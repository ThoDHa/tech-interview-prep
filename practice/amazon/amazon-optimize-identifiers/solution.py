"""Optimize Identifiers — https://www.fastprep.io/problems/amazon-optimize-identifiers

Write-up & approaches: ../../../docs/amazon/amazon-optimize-identifiers.md

In an Amazon inventory management, an operations analyst is dealing with a set of initial product identifiers represented by strings. The type of a product identifier is determined by the first and la

  uv run python amazon/amazon-optimize-identifiers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-optimize-identifiers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def optimizeIdentifiers(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in optimizeIdentifiers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().optimizeIdentifiers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
