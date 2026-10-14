"""Meeting Rooms II — https://leetcode.com/problems/meeting-rooms-ii/

Write-up & approaches: ../../docs/problems/meeting_rooms_ii.md
Reference implementation of the write-up's Min-Heap of End Times solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python meeting_rooms_ii/reference.py   # replay the example
  uv run pytest meeting_rooms_ii/               # run the test sets
"""

import heapq
from typing import List


class Interval:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        """Return the minimum rooms covering every meeting without overlap.

        Time:  O(n log n): start-sort plus one heap pop and push per meeting.
        Space: O(n): one heap entry per open room.
        """
        intervals.sort(key=lambda interval: interval.start)

        heap: List[int] = []
        for interval in intervals:
            if heap and heap[0] <= interval.start:
                # The room freeing soonest is free for this meeting.
                heapq.heappop(heap)
            heapq.heappush(heap, interval.end)
        return len(heap)


if __name__ == "__main__":
    # Debug playground: cases.json is empty (multi-method starter), so
    # Example 1's intervals stand in.
    example = [(0, 40), (5, 10), (15, 20)]
    intervals = [Interval(start, end) for start, end in example]
    result = Solution().minMeetingRooms(intervals)
    print(f"intervals = {example}")
    print(f"expected: 2")
    print(f"got:      {result}")
