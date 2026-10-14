"""Number of Connected Components In An Undirected Graph — https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

Write-up & approaches: ../../docs/problems/number_of_connected_components_in_an_undirected_graph.md
Reference implementation of the write-up's Union-Find solution.

You have an undirected graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and an array `edges` where `edges[i] = [aᵢ, bᵢ]` indicates that there is an edge between `aᵢ` and `bᵢ` in the graph. Return the number of connected components in the graph.

  uv run python number_of_connected_components_in_an_undirected_graph/reference.py   # debug one case (see CASE below)
  uv run pytest number_of_connected_components_in_an_undirected_graph/              # run the test sets
"""

from harness import pick_case


class Solution:
    def countComponents(self, n, edges):
        """Count the connected components of an undirected graph by unioning.

        Starts from `n` singleton components and lets every edge merge the two
        components of its endpoints; each successful union lowers the count
        by one, and an edge whose endpoints already share a component lowers
        nothing because it closes a cycle.

        Args:
            n: Node count, nodes labeled 0..n-1, 1 <= n.
            edges: Undirected edges, each a pair of distinct labels.

        Returns:
            The number of connected components.

        Time:  O(n + e * alpha(n)): each edge pays two near-constant finds.
        Space: O(n): the parent and rank arrays.
        """
        parent = list(range(n))
        rank = [0] * n

        def find(node):
            while parent[node] != node:
                # Path halving: point the node at its grandparent to flatten
                # the tree as a side effect of every lookup.
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        components = n
        for a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                continue
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
            components -= 1
        return components


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countComponents above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countComponents(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
