"""Dijkstra Shortest Paths in a Weighted Undirected Graph — https://www.fastprep.io/problems/amazon-shortest-path-weighted-graph

Write-up & approaches: ../../../docs/amazon/amazon-shortest-path-weighted-graph.md

You are given vertexCount vertices numbered from 0 to vertexCount - 1, an array of undirected weighted edges, and a source vertex. Each edge is [u, v, weight] with a nonnegative weight.

  uv run python amazon/amazon-shortest-path-weighted-graph/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-shortest-path-weighted-graph/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def shortestUndirectedDistances(self, vertexCount, edges, source):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in shortestUndirectedDistances above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().shortestUndirectedDistances(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
