"""Find Median from Data Stream — https://www.fastprep.io/problems/amazon-find-median-from-data-stream

Write-up & approaches: ../../../docs/amazon/amazon-find-median-from-data-stream.md
Reference implementation of the write-up's recommended Two Heaps solution,
kept next to the harness so authored cases stay falsifiable. Your own
attempt lives in solution.py.

  uv run python amazon-find-median-from-data-stream/reference.py   # replay the example
  uv run pytest amazon-find-median-from-data-stream/               # run the test sets
"""

import heapq
from typing import List


class MedianFinder:
    def __init__(self) -> None:
        """Start an empty stream with the two half-heaps empty.

        Time:  O(1): two empty lists and no work beyond that.
        Space: O(1): nothing stored yet beyond the heap lists themselves.
        """
        self.lower: List[int] = []
        self.upper: List[int] = []

    def add(self, num: int) -> None:
        """Funnel `num` through the lower heap into the upper heap, then
        rebalance so `lower` holds the extra element when counts are odd.

        Time:  O(log n): a constant number of heap pushes and pops, each
            logarithmic in the number of stored values.
        Space: O(1) per call: one entry retained in exactly one heap.
        """
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def median(self) -> float:
        """Return the current median as a float, read off the heap tops.

        Time:  O(1): the answer is one or two heap-top reads plus one
            division.
        Space: O(1): no retained state beyond the heaps themselves.
        """
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    stream = MedianFinder()
    for value in (5, 1, 9):
        stream.add(value)
        print(f"add {value} -> median {stream.median()}")
