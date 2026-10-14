"""Fare Between Stops on a Train Route — https://www.fastprep.io/problems/amazon-train-route-fare

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-train-route-fare.md

A train route is given as an ordered array of unique stop names. Traveling across one adjacent segment costs one fare unit in either direction.

  uv run python amazon_oa/amazon-train-route-fare/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-train-route-fare/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculateFare(self, route, start, stop):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculateFare above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculateFare(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
