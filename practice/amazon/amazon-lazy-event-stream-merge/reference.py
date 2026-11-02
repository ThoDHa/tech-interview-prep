"""Lazy Merge of Sorted Event Streams — https://www.fastprep.io/problems/amazon-lazy-event-stream-merge

Write-up & approaches: ../../../docs/amazon/amazon-lazy-event-stream-merge.md

Reference implementation of the write-up's recommended Min-Heap of
Stream Heads solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-lazy-event-stream-merge/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-lazy-event-stream-merge/              # run the test sets
"""

import heapq
from typing import List

from harness import pick_case


class Solution:
    def mergeEventStreams(self, streams: List[List[int]]) -> List[int]:
        """Merge sorted event streams into one nondecreasing timestamp list.

        The heap holds each nonempty stream's current event as
        `(timestamp, stream_index, cursor)`, the statement's one-event
        head per stream. Every pop emits the smallest head and advances
        only the stream that supplied it; empty rows are filtered at
        seeding, and a stream leaves the heap when its row runs out.

        Args:
            streams: Rows of integer timestamps, each row sorted in
                nondecreasing order and possibly empty; the page
                constraints allow 0 <= len(streams) <= 10000 with a
                total of at most 200000 events.

        Returns:
            Every timestamp from every row, in nondecreasing order,
            with duplicates preserved; `[]` for zero or all-empty rows.

        Time:  O(N log k): each of the N events pops once and pushes at
               most once from a heap of at most k heads.
        Space: O(k): one head per nonempty stream, plus the output.
        """
        stream_heads = [
            (stream[0], index, 0)
            for index, stream in enumerate(streams)
            if stream
        ]
        heapq.heapify(stream_heads)

        merged_events = []
        while stream_heads:
            timestamp, index, cursor = heapq.heappop(stream_heads)
            merged_events.append(timestamp)
            next_cursor = cursor + 1
            if next_cursor < len(streams[index]):
                heapq.heappush(
                    stream_heads, (streams[index][next_cursor], index, next_cursor)
                )
        return merged_events


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeEventStreams above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().mergeEventStreams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
