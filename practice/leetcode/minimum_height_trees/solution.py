"""Minimum Height Trees: https://leetcode.com/problems/minimum-height-trees/

Write-up & approaches: ../../../docs/leetcode/minimum_height_trees.md

Given a tree of `n` nodes labelled `0..n-1` and its `n - 1` undirected edges,
return the labels of every root that yields a tree of minimum height. Answer may
be returned in any order.

  uv run python minimum_height_trees/solution.py   # debug one case (see CASE below)
  uv run pytest minimum_height_trees/              # run the test sets
"""
from collections import deque

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """

        if n <= 2:
            return list(range(n))
        adj: List[List[int]] = [[] for _ in range(n)]

        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        leaves = deque(node for node in range(n) if len(adj[node]) == 1)

        remaining = n
        while remaining > 2:
            
            for _ in range(len(leaves)):
                node = leaves.popleft()
                remaining -= 1

                if adj[node]:
                    neighbor = adj[node].pop()
                    adj[neighbor].remove(node)
                    if len(adj[neighbor]) == 1:
                           leaves.append(neighbor)
        return list(leaves)
                

if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinHeightTrees above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinHeightTrees(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {sorted(case['expected'])}")
    print(f"got:      {sorted(result) if result is not None else result}")
