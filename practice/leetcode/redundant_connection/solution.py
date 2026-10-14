"""Redundant Connection — https://leetcode.com/problems/redundant-connection/

Write-up & approaches: ../../docs/problems/redundant_connection.md

You are given a connected **undirected graph** with `n` nodes labeled from `1` to `n`. Initially, it contained no cycles and consisted of `n-1` edges. We have now added one additional edge to the grap

  uv run python redundant_connection/solution.py   # debug one case (see CASE below)
  uv run pytest redundant_connection/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findRedundantConnection(self, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findRedundantConnection above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findRedundantConnection(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
