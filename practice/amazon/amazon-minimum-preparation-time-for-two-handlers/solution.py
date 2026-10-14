"""Minimum Preparation Time for Two Handlers — https://www.fastprep.io/problems/amazon-minimum-preparation-time-for-two-handlers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-preparation-time-for-two-handlers.md

A work queue workList must be processed in order by two handlers. Each value in workList is a work type from 1 through m.

  uv run python amazon_oa/amazon-minimum-preparation-time-for-two-handlers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-preparation-time-for-two-handlers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minPreparationTime(self, workList, longPrepTime, shortPrepTime):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minPreparationTime above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minPreparationTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
