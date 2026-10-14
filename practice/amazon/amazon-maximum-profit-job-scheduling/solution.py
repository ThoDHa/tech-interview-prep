"""Maximum Profit in Job Scheduling — https://www.fastprep.io/problems/amazon-maximum-profit-job-scheduling

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-profit-job-scheduling.md

You are given equal-length arrays startTime, endTime, and profit. Job i runs on the half-open interval from its start time to its end time and earns its profit.

  uv run python amazon_oa/amazon-maximum-profit-job-scheduling/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-profit-job-scheduling/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def jobScheduling(self, startTime, endTime, profit):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in jobScheduling above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().jobScheduling(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
