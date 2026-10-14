"""Redundant Connection — https://leetcode.com/problems/redundant-connection/

Write-up & approaches: ../../docs/problems/redundant_connection.md
Reference implementation of the write-up's Union-Find with Early Exit solution.

You are given a connected **undirected graph** with `n` nodes labeled from `1` to `n`. Initially, it contained no cycles and consisted of `n-1` edges. We have now added one additional edge to the graph. The edge has two **different** vertices chosen from `1` to `n`, and was not an edge that previously existed in the graph. The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` represents an edge between nodes `ai` and `bi` in the graph. Return an edge that can be removed so that the graph is still a connected non-cyclical graph. If there are multiple answers, return the edge that appears last in the input `edges`.

  uv run python redundant_connection/reference.py   # debug one case (see CASE below)
  uv run pytest redundant_connection/              # run the test sets
"""

from harness import pick_case


class Solution:
    def findRedundantConnection(self, edges):
        """Return the first edge that closes a cycle, scanning in input order.

        Unions each edge's endpoints into a growing forest: the tree-shaped
        input unions cleanly, and the one extra edge is exactly the first
        whose endpoints already share a component. Scanning in input order
        makes that first collision the last-listed removable edge.

        Args:
            edges: `n` edges of a tree plus one extra edge, nodes 1..n,
                each edge `[a, b]` with its endpoints in either order.

        Returns:
            The redundant edge as a `[a, b]` list.

        Time:  O(n * alpha(n)): one union with two finds per edge.
        Space: O(n): the parent and rank arrays.
        """
        n = len(edges)
        parent = list(range(n + 1))
        rank = [0] * (n + 1)

        def find(node):
            while parent[node] != node:
                # Path halving: point the node at its grandparent to flatten
                # the tree as a side effect of every lookup.
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                # Every earlier edge unioned cleanly, so this edge joins two
                # nodes a path already connects: it is the redundant one.
                return [a, b]
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
        return []


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findRedundantConnection above, then
    # run this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findRedundantConnection(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
