"""Graph Valid Tree — https://leetcode.com/problems/graph-valid-tree/

Write-up & approaches: ../../docs/problems/graph_valid_tree.md
Reference implementation of the write-up's Union-Find solution.

Given `n` nodes labeled from `0` to `n - 1` and a list of **undirected** edges (each edge is a pair of nodes), write a function to check whether these edges make up a valid tree.

  uv run python graph_valid_tree/reference.py   # debug one case (see CASE below)
  uv run pytest graph_valid_tree/              # run the test sets
"""

from harness import pick_case


class Solution:
    def validTree(self, n, edges):
        """Decide whether `edges` form a tree on nodes 0..n-1 by unioning.

        A tree on `n` nodes holds exactly `n - 1` edges and no cycle; `n - 1`
        acyclic edges already force connectivity, so the edge-count check plus
        a cycle check settles the question. Each edge unions its endpoints'
        components; an edge whose endpoints already share a component closes
        a cycle and rejects the graph.

        Args:
            n: Node count, nodes labeled 0..n-1, 1 <= n.
            edges: Distinct undirected edges without self-loops.

        Returns:
            True when the edges make up a valid tree, False otherwise.

        Time:  O(n + e * alpha(n)): each edge pays two near-constant finds.
        Space: O(n): the parent and rank arrays.
        """
        if len(edges) != n - 1:
            return False

        parent = list(range(n))
        rank = [0] * n

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
                # Both endpoints already sit in one component: this edge
                # closes a cycle.
                return False
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
        return True


if __name__ == "__main__":
    # Debug playground: set a breakpoint in validTree above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().validTree(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
