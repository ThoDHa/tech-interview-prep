"""Dijkstra Shortest Paths in a Weighted Undirected Graph — https://www.fastprep.io/problems/amazon-shortest-path-weighted-graph

Write-up & approaches: ../../../docs/amazon/amazon-shortest-path-weighted-graph.md

Reference implementation of the write-up's recommended Dijkstra with a
Min-Heap solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-shortest-path-weighted-graph/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-shortest-path-weighted-graph/              # run the test sets
"""

import heapq
from typing import List

from harness import pick_case


class Solution:
    def shortestUndirectedDistances(self, vertexCount: int, edges: List[List[int]], source: int) -> List[int]:
        """Return the shortest distance from `source` to every vertex, in
        vertex order, with -1 for unreachable vertices.

        Nonnegative weights make cheapest-first settlement safe: when a
        vertex pops with its current best distance, no future route can
        beat it, because any route would leave the frontier through an
        entry that is already no cheaper. The adjacency list registers
        both orientations of every edge, so parallel edges and
        self-loops are ordinary entries that a strict improvement test
        ignores. The heap holds lazy duplicates (an improvement pushes a
        fresh entry rather than decreasing a key); a popped entry older
        than the vertex's current best is discarded. Distances reach
        `(V - 1) * 1e9 ~ 1e14`, which needs the statement's 64-bit
        arithmetic.

        Args:
            vertexCount: Vertices numbered `0 .. vertexCount - 1`.
            edges: Undirected `[u, v, weight]` triples, weights in
                `[0, 1e9]`; parallel edges and self-loops allowed.
            source: The start vertex, `0 <= source < vertexCount`.

        Returns:
            Length-`vertexCount` distances, `-1` where unreachable.

        Time:  O(E log V): each edge pushes at most one entry and each
               pop costs a logarithm.
        Space: O(V + E): adjacency list, distance table, frontier.
        """
        adjacency = [[] for _ in range(vertexCount)]
        for u, v, w in edges:
            adjacency[u].append((v, w))
            adjacency[v].append((u, w))

        unreached = -1
        distances = [unreached] * vertexCount
        distances[source] = 0
        frontier = [(0, source)]
        while frontier:
            distance, vertex = heapq.heappop(frontier)
            if distance > distances[vertex]:
                continue
            for next_vertex, weight in adjacency[vertex]:
                arrival = distance + weight
                if distances[next_vertex] == unreached or arrival < distances[next_vertex]:
                    distances[next_vertex] = arrival
                    heapq.heappush(frontier, (arrival, next_vertex))
        return distances


if __name__ == "__main__":
    # Debug playground: set a breakpoint in shortestUndirectedDistances above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().shortestUndirectedDistances(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
