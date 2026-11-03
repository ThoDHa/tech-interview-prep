"""Meeting Rooms II — https://leetcode.com/problems/meeting-rooms-ii/

Write-up & approaches: ../../../docs/leetcode/meeting_rooms_ii.md

Given an array of meeting time interval objects consisting of start and end times `[[start_1,end_1],[start_2,end_2],...] (start_i < end_i)`, find the minimum number of rooms required to schedule all m

  uv run python leetcode/meeting_rooms_ii/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/meeting_rooms_ii/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minMeetingRooms, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "classic_two_rooms"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(Solution, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement minMeetingRooms first")
