"""Minimum Edge Moves to Connect a Network — https://www.fastprep.io/problems/amazon-minimum-edge-moves-to-connect-graph

Write-up & approaches: ../../../docs/amazon/amazon-minimum-edge-moves-to-connect-graph.md

You manage an undirected network with nodes 0 through n - 1. In one move, you may remove one existing cable and reconnect that cable between any two nodes.

  uv run python amazon_oa/amazon-minimum-edge-moves-to-connect-graph/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-edge-moves-to-connect-graph/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumEdgeMoves(self, n, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumEdgeMoves above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumEdgeMoves(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
