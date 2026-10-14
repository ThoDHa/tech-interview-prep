"""Meeting Room Scheduler — https://www.fastprep.io/problems/amazon-meeting-room-scheduler

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-meeting-room-scheduler.md

Implement a scheduler for roomCount meeting rooms numbered from 0 to roomCount - 1.

  uv run python amazon_oa/amazon-meeting-room-scheduler/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-meeting-room-scheduler/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def scheduleMeetings(self, roomCount, meetings):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in scheduleMeetings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().scheduleMeetings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
