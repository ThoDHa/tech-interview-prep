"""Reconstruct Itinerary — https://leetcode.com/problems/reconstruct-itinerary/

Write-up & approaches: ../../docs/problems/reconstruct_itinerary.md
Reference implementation of the write-up's Hierholzer's Algorithm solution.

You are given a list of flight tickets `tickets` where `tickets[i] = [from_i, to_i]` represent the source airport and the destination airport. Each `from_i` and `to_i` consists of three uppercase English letters. Reconstruct the itinerary in order and return it. All of the tickets belong to someone who originally departed from `"JFK"`. Your objective is to reconstruct the flight path that this person took, assuming each ticket was used exactly once. If there are multiple valid flight paths, return the lexicographically smallest one. You may assume all the tickets form at least one valid flight path.

  uv run python reconstruct_itinerary/reference.py   # debug one case (see CASE below)
  uv run pytest reconstruct_itinerary/              # run the test sets
"""

import heapq

from harness import pick_case


class Solution:
    def findItinerary(self, tickets):
        """Return the lexicographically smallest Eulerian path via Hierholzer.

        Sorts each departure's destinations smallest-first, then walks greedily
        to the smallest untried destination, pushing airports on a stack when
        stuck. The itinerary is the stack read bottom-up: the walk consumes
        every ticket exactly once, and dead ends pop out in reverse, splicing
        the smallest valid tour into the path.

        Args:
            tickets: Pairs `[from, to]` of three-letter airport codes forming
                at least one Eulerian path from "JFK".

        Returns:
            The lexicographically smallest itinerary as a list of airport
            codes, one more entry than `tickets`.

        Time:  O(e log e): the destination sorts dominate the linear walk.
        Space: O(e): the adjacency map and the stack.
        """
        adjacency = {}
        for src, dst in tickets:
            heapq.heappush(adjacency.setdefault(src, []), dst)

        route = []
        stack = ["JFK"]
        while stack:
            while adjacency.get(stack[-1]):
                # Move to the smallest untried destination, consuming the
                # ticket so it can never be taken twice.
                stack.append(heapq.heappop(adjacency[stack[-1]]))
            # The top airport has no untried tickets left: it is the next
            # airport from the end of the final itinerary.
            route.append(stack.pop())
        route.reverse()
        return route


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findItinerary above, then run this
    # file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findItinerary(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
