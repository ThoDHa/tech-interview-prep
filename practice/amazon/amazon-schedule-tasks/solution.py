"""Schedule Tasks — https://www.fastprep.io/problems/amazon-schedule-tasks

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-schedule-tasks.md

In managing tasks at analytics platform, the goal is to efficiently schedule both primary and secondary tasks within specified time constraints.

  uv run python amazon_oa/amazon-schedule-tasks/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-schedule-tasks/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxSecondaryTasks(self, limit, primary, secondary):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSecondaryTasks above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSecondaryTasks(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
