"""Squirrel Nut Collection Shortest Path — https://www.fastprep.io/problems/amazon-squirrel-nut-collection-shortest-path

Write-up & approaches: ../../../docs/amazon/amazon-squirrel-nut-collection-shortest-path.md

A squirrel, a tree, and several nuts occupy distinct cells on a rectangular Manhattan grid. The squirrel can carry one nut at a time. Every nut must be delivered to the tree.

  uv run python amazon_oa/amazon-squirrel-nut-collection-shortest-path/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-squirrel-nut-collection-shortest-path/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, tree, squirrel, nuts):
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
