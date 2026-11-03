"""Meeting Rooms — https://leetcode.com/problems/meeting-rooms/

Write-up & approaches: ../../../docs/leetcode/meeting_rooms.md

Given an array of meeting time interval objects consisting of start and end times `[[start_1,end_1],[start_2,end_2],...] (start_i < end_i)`, determine if a person could add all meetings to their sched

  uv run python leetcode/meeting_rooms/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/meeting_rooms/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canAttendMeetings, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "classic_overlap"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(Solution, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement canAttendMeetings first")
