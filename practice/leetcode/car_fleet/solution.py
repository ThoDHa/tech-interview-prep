"""Car Fleet — https://leetcode.com/problems/car-fleet/

Write-up & approaches: ../../docs/problems/car_fleet.md

There are `n` cars traveling to the same destination on a one-lane highway. You are given two arrays of integers `position` and `speed`, both of length `n`. * `position[i]` is the position of the `ith

  uv run python car_fleet/solution.py   # debug one case (see CASE below)
  uv run pytest car_fleet/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def carFleet(self, target, position, speed):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in carFleet above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().carFleet(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
