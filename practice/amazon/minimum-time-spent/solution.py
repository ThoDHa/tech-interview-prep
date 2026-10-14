"""Minimum Time Spent — https://www.fastprep.io/problems/minimum-time-spent

Write-up & approaches: ../../../docs/problems/amazon_oa/minimum-time-spent.md

Amazon Prime Video has movies in category 'comedy' or 'drama'. Determine the earliest time you can finish at least one movie from each category. The release schedule and duration of the movies are pro

  uv run python amazon_oa/minimum-time-spent/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/minimum-time-spent/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumTimeSpent(self, comedyReleaseTime, comedyDuration, dramaReleaseTime, dramaDuration):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumTimeSpent above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumTimeSpent(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
