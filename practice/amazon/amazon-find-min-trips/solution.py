"""Find Min Trips — https://www.fastprep.io/problems/amazon-find-min-trips

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-min-trips.md

There were a large number of orders placed on Amazon Prime Day. The orders are packed and are at the warehouse ready to be delivered. The delivery agent needs to deliver them in as few trips as possib

  uv run python amazon_oa/amazon-find-min-trips/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-min-trips/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinTrips(self, packageweight):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinTrips above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinTrips(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
