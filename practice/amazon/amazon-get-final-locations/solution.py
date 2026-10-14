"""Get Final Location — https://www.fastprep.io/problems/amazon-get-final-locations

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-final-locations.md

Amazon stores its data on different servers at different locations. From time to time, due to several factors, Amazon needs to move its data from one location to another. This challenge involves keepi

  uv run python amazon_oa/amazon-get-final-locations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-final-locations/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getFinalLocations(self, locations, movedFrom, movedTo):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getFinalLocations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getFinalLocations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
