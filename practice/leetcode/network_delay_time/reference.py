"""Network Delay Time — https://leetcode.com/problems/network-delay-time/

Write-up & approaches: ../../docs/problems/network_delay_time.md
Reference implementation of the write-up's Dijkstra's Algorithm solution.

You are given a network of `n` directed nodes, labeled from `1` to `n`. You are also given `times`, a list of directed edges where `times[i] = (ui, vi, ti)`. * `ui` is the source node (an integer from `1` to `n`) * `vi` is the target node (an integer from `1` to `n`) * `ti` is the time it takes for a signal to travel from the source to the target node (an integer greater than or equal to `0`). You are also given an integer `k`, representing the node that we will send a signal from. Return the **minimum** time it takes for all of the `n` nodes to receive the signal. If it is impossible for all the nodes to receive the signal, return `-1` instead.

  uv run python network_delay_time/reference.py   # debug one case (see CASE below)
  uv run pytest network_delay_time/              # run the test sets
"""

import heapq

from harness import pick_case


class Solution:
    def networkDelayTime(self, times, n, k):
        """Return the signal's furthest shortest-path arrival time via Dijkstra.

        Runs Dijkstra from the signal source `k` over an adjacency list,
        popping the not-yet-settled node with the smallest known distance
        from a min-heap and relaxing its outgoing edges. The answer is the
        largest settled distance, or -1 when some node never settles.

        Args:
            times: Directed weighted edges `[u, v, t]`, labels 1..n, t >= 0.
            n: Node count, 1 <= n.
            k: Source node label, 1 <= k <= n.

        Returns:
            The minimum time after which every node has received the signal,
            or -1 when at least one node is unreachable from `k`.

        Time:  O(n + e * log e): each edge may push one heap entry.
        Space: O(n + e): adjacency lists, distances, heap.
        """
        adjacency = [[] for _ in range(n + 1)]
        for u, v, t in times:
            adjacency[u].append((v, t))

        distances = [-1] * (n + 1)
        distances[k] = 0
        heap = [(0, k)]
        settled = 0

        while heap:
            distance, node = heapq.heappop(heap)
            if distance > distances[node]:
                # A shorter path to `node` was settled after this stale entry
                # was pushed; skip it.
                continue
            settled += 1
            for neighbor, weight in adjacency[node]:
                candidate = distance + weight
                if distances[neighbor] == -1 or candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))

        if settled < n:
            return -1
        return max(distances[1:])


if __name__ == "__main__":
    # Debug playground: set a breakpoint in networkDelayTime above, then run
    # this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().networkDelayTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
