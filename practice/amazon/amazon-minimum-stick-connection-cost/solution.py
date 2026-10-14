"""Minimum Stick Connection Cost — https://www.fastprep.io/problems/amazon-minimum-stick-connection-cost

Write-up & approaches: ../../../docs/amazon/amazon-minimum-stick-connection-cost.md

You are given an integer array sticks, where each element is the length of a stick.

  uv run python amazon_oa/amazon-minimum-stick-connection-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-stick-connection-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumStickConnectionCost(self, sticks):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumStickConnectionCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumStickConnectionCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
