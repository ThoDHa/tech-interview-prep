"""Find Minimum Days — https://www.fastprep.io/problems/amazon-find-minimum-days

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-minimum-days.md

A student is preparing for a scholarship test which is organized on the Amazon Academy platform and scheduled for next month.

  uv run python amazon_oa/amazon-find-minimum-days/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-minimum-days/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumDays(self, pages, k, p):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumDays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumDays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
