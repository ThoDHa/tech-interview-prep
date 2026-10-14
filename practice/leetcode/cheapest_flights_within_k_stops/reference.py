"""Cheapest Flights Within K Stops — https://leetcode.com/problems/cheapest-flights-within-k-stops/

Write-up & approaches: ../../docs/problems/cheapest_flights_within_k_stops.md
Reference implementation of the write-up's Bellman-Ford Relaxation Sweeps solution.

There are `n` airports, labeled from `0` to `n - 1`, which are connected by some flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]` represents a one-way flight from airport `from_i` to airport `to_i` with cost `price_i`. You may assume there are no duplicate flights and no flights from an airport to itself.

You are also given three integers `src`, `dst`, and `k` where `src` is the starting airport, `dst` is the destination airport, `src != dst`, and `k` is the maximum number of stops you can make (not including `src` and `dst`). Return **the cheapest price** from `src` to `dst` with at most `k` stops, or return `-1` if it is impossible.

  uv run python cheapest_flights_within_k_stops/reference.py   # debug one case (see CASE below)
  uv run pytest cheapest_flights_within_k_stops/               # run the test sets
"""

from harness import pick_case


class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        """Return the cheapest src -> dst price using at most k stops (k + 1 flights).

        Runs Bellman-Ford limited to k + 1 sweeps over a frozen previous
        layer: each sweep reads only the previous layer (at most t flights
        used) while writing the current one (at most t + 1), so a route can
        gain at most one flight per sweep and the stop budget is enforced
        structurally by the sweep count.

        Args:
            n: Airport count, 1 <= n; airports are labeled 0..n - 1.
            flights: Directed edges `[u, v, price]`, 1 <= price, no duplicate
                flights, no self loops.
            src: Starting airport, 0 <= src < n.
            dst: Destination airport, 0 <= dst < n, dst != src.
            k: Maximum number of intermediate stops, 0 <= k < n.

        Returns:
            The cheapest price of any route with at most k stops, or -1 when
            every route to dst needs more than k stops.

        Time:  O(k * e): k + 1 sweeps over all e flights.
        Space: O(n): two distance arrays; the flight list is swept directly.
        """
        distances = [None] * n
        distances[src] = 0

        # One sweep per additional flight the budget allows: k stops = k + 1 flights.
        for _ in range(k + 1):
            previous = distances[:]
            for u, v, price in flights:
                if previous[u] is not None and (
                    distances[v] is None or previous[u] + price < distances[v]
                ):
                    distances[v] = previous[u] + price

        return -1 if distances[dst] is None else distances[dst]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findCheapestPrice above, then run
    # this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findCheapestPrice(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
