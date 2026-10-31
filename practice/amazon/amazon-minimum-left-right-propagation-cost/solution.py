"""Minimum Cost of Left and Right Propagation — https://www.fastprep.io/problems/amazon-minimum-left-right-propagation-cost

Write-up & approaches: ../../../docs/amazon/amazon-minimum-left-right-propagation-cost.md

You are given a positive integer array values. You may perform either propagation operation any number of times and in any order:

  uv run python amazon/amazon-minimum-left-right-propagation-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-minimum-left-right-propagation-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumPropagationCost(self, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumPropagationCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumPropagationCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
