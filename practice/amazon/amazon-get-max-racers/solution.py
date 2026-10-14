"""Get Max Racers — https://www.fastprep.io/problems/amazon-get-max-racers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-racers.md

HackerLand Sports Club wants to send a team for a relay race. There are n racers in the group indexed from 0 to n - 1. The ith racer has a speed of speed[i] units.

  uv run python amazon_oa/amazon-get-max-racers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-racers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxRacers(self, speed, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxRacers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxRacers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
