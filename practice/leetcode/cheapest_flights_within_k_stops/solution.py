"""Cheapest Flights Within K Stops — https://leetcode.com/problems/cheapest-flights-within-k-stops/

Write-up & approaches: ../../docs/problems/cheapest_flights_within_k_stops.md

There are `n` airports, labeled from `0` to `n - 1`, which are connected by some flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]` represents a one-way flight from

  uv run python cheapest_flights_within_k_stops/solution.py   # debug one case (see CASE below)
  uv run pytest cheapest_flights_within_k_stops/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findCheapestPrice above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findCheapestPrice(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
