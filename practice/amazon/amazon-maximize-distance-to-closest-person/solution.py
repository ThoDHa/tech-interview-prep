"""Maximize Distance to the Closest Occupied Seat — https://www.fastprep.io/problems/amazon-maximize-distance-to-closest-person

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-distance-to-closest-person.md

You are given an array seats, where seats[i] = 1 means seat i is occupied and seats[i] = 0 means it is empty. At least one seat is empty and at least one seat is occupied.

  uv run python amazon_oa/amazon-maximize-distance-to-closest-person/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-distance-to-closest-person/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def bestSeat(self, seats):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in bestSeat above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().bestSeat(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
