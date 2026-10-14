"""Cheapest Flights Within K Stops — https://www.fastprep.io/problems/amazon-cheapest-flights-within-k-stops

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-cheapest-flights-within-k-stops.md

There are n cities numbered from 0 to n - 1. You are given an array flights where flights[i] = [from_i, to_i, price_i] means there is a directed flight from city from_i to city to_i with cost price_i.

  uv run python amazon_oa/amazon-cheapest-flights-within-k-stops/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-cheapest-flights-within-k-stops/              # run the test sets
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
