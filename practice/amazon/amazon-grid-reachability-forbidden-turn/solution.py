"""Grid Reachability with a Forbidden Turn — https://www.fastprep.io/problems/amazon-grid-reachability-forbidden-turn

Write-up & approaches: ../../../docs/amazon/amazon-grid-reachability-forbidden-turn.md

Determine whether a destination can be reached on an obstacle grid while respecting movement direction.

  uv run python amazon/amazon-grid-reachability-forbidden-turn/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-grid-reachability-forbidden-turn/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def canReachWithTurnRule(self, grid, start, destination, initialHeading, forbiddenTurn):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canReachWithTurnRule above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canReachWithTurnRule(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
