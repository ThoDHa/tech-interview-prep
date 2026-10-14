"""Closest Version Date — https://www.fastprep.io/problems/amazon-closest-version-date

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-closest-version-date.md

2026-07-02 •ᴗ• Practice note: This version should match the core of the reported interview question by about 85%-90%. It was reported for SDE II. It may not be word-for-word identical, but the main id

  uv run python amazon_oa/amazon-closest-version-date/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-closest-version-date/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findClosestVersionDate(self, targetDate, versions):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findClosestVersionDate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findClosestVersionDate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
