"""Meeting Rooms — https://leetcode.com/problems/meeting-rooms/

Write-up & approaches: ../../docs/problems/meeting_rooms.md
Reference implementation of the write-up's Sort and Adjacent Scan solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python meeting_rooms/reference.py   # replay the example cases
  uv run pytest meeting_rooms/               # run the test sets
"""

from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        """Return whether every meeting fits one person's schedule.

        Time:  O(n log n): sorting by start dominates; the adjacency sweep is
            one linear pass of one comparison per meeting.
        Space: O(1): the sort is in-place and the scan keeps one index.
        """
        intervals.sort(key=lambda interval: interval.start)
        for i in range(1, len(intervals)):
            # A meeting may start exactly when the previous one ends.
            if intervals[i].start < intervals[i - 1].end:
                return False
        return True


if __name__ == "__main__":
    # Debug playground: cases.json is empty (multi-method starter), so
    # the two examples stand in.
    for intervals in ([Interval(0, 30), Interval(5, 10), Interval(15, 20)],
                      [Interval(5, 8), Interval(9, 15)]):
        result = Solution().canAttendMeetings(intervals)
        print(f"intervals = {[(i.start, i.end) for i in intervals]}")
        print(f"canAttendMeetings -> {result}")
