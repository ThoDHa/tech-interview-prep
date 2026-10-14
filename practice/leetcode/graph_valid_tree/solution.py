"""Graph Valid Tree — https://leetcode.com/problems/graph-valid-tree/

Write-up & approaches: ../../docs/problems/graph_valid_tree.md

Given `n` nodes labeled from `0` to `n - 1` and a list of **undirected** edges (each edge is a pair of nodes), write a function to check whether these edges make up a valid tree.

  uv run python graph_valid_tree/solution.py   # debug one case (see CASE below)
  uv run pytest graph_valid_tree/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def validTree(self, n, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in validTree above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().validTree(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
