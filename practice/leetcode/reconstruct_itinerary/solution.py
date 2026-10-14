"""Reconstruct Itinerary — https://leetcode.com/problems/reconstruct-itinerary/

Write-up & approaches: ../../docs/problems/reconstruct_itinerary.md

You are given a list of flight tickets `tickets` where `tickets[i] = [from_i, to_i]` represent the source airport and the destination airport. Each `from_i` and `to_i` consists of three uppercase Engl

  uv run python reconstruct_itinerary/solution.py   # debug one case (see CASE below)
  uv run pytest reconstruct_itinerary/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findItinerary(self, tickets):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findItinerary above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findItinerary(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
