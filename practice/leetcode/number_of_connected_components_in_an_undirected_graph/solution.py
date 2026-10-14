"""Number of Connected Components In An Undirected Graph — https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

Write-up & approaches: ../../docs/problems/number_of_connected_components_in_an_undirected_graph.md

You have an undirected graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and an array `edges` where `edges[i] = [aᵢ, bᵢ]` indicates that there is an edge between `aᵢ` and `b

  uv run python number_of_connected_components_in_an_undirected_graph/solution.py   # debug one case (see CASE below)
  uv run pytest number_of_connected_components_in_an_undirected_graph/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countComponents(self, n, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countComponents above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countComponents(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
