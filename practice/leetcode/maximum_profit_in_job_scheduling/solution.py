"""Maximum Profit in Job Scheduling: https://leetcode.com/problems/maximum-profit-in-job-scheduling/

Write-up & approaches: ../../docs/problems/maximum_profit_in_job_scheduling.md

Given `startTime`, `endTime`, and `profit` arrays describing `n` jobs, return the
maximum profit obtainable from a subset of non-overlapping jobs (a job ending at
time `X` may be followed by another starting at `X`).

  uv run python maximum_profit_in_job_scheduling/solution.py   # debug one case (see CASE below)
  uv run pytest maximum_profit_in_job_scheduling/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def jobScheduling(
        self, startTime: List[int], endTime: List[int], profit: List[int]
    ) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in jobScheduling above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().jobScheduling(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
