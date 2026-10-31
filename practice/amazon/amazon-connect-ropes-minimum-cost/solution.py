"""Connect N Ropes With Minimum Cost — https://www.fastprep.io/problems/amazon-connect-ropes-minimum-cost

Write-up & approaches: ../../../docs/amazon/amazon-connect-ropes-minimum-cost.md

You are given an integer array ropes, where ropes[i] is the length of one rope.

  uv run python amazon/amazon-connect-ropes-minimum-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-connect-ropes-minimum-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumRopeConnectionCost(self, ropes):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumRopeConnectionCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumRopeConnectionCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
