"""Clone Graph: https://leetcode.com/problems/clone-graph/

Write-up & approaches: ../../docs/problems/clone_graph.md

Given a reference to a node in a connected undirected graph, return a deep copy
(clone) of the graph. Each node holds an `int` value and a list of its neighbors.

  uv run python clone_graph/solution.py   # debug one case (see CASE below)
  uv run pytest clone_graph/              # run the test sets
"""

from typing import Optional

from harness import (
    NotSolved,
    GraphNode as Node,
    build_graph,
    graph_to_adjacency,
    pick_case,
)


# Definition for a Node.
# class Node:
#     def __init__(self, val=0, neighbors=None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in cloneGraph above, then run this file.
    # The case stores the graph as an adjacency list; we marshal it to GraphNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    adj = case["args"][0]
    result = Solution().cloneGraph(build_graph(adj))
    print(f"case {case['id']}: adjList = {adj}")
    print(f"expected: {case['expected']}")
    print(f"got:      {graph_to_adjacency(result)}")
