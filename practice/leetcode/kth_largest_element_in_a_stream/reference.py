"""Kth Largest Element In a Stream — https://leetcode.com/problems/kth-largest-element-in-a-stream/

Write-up & approaches: ../../docs/problems/kth_largest_element_in_a_stream.md
Reference implementation of the write-up's Min-Heap of Size K solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python kth_largest_element_in_a_stream/reference.py   # replay the example
  uv run pytest kth_largest_element_in_a_stream/               # run the test sets
"""

import heapq
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]) -> None:
        """Seed the heap with the top `k` values of the initial stream.

        Time:  O(n + (n - k) log n): heapify the initial stream in O(n), then
            pop the n - k values below the cutoff, each pop O(log n).
        Space: O(n) transient: the heap starts at the full initial stream and
            is trimmed to k entries before the first query.
        """
        self.k = k
        self.heap = list(nums)
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        """Add `val` to the stream and return its current kth largest.

        Time:  O(log k): one push plus at most one pop on a heap that never
            exceeds k + 1 entries.
        Space: O(1): no growth beyond the k entries held after construction.
        """
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


if __name__ == "__main__":
    # Debug playground: cases.json is empty (multi-method starter), so
    # Example 1's operation sequence stands in.
    stream = KthLargest(3, [1, 2, 3, 3])
    operations = [("add", 3), ("add", 5), ("add", 6), ("add", 7), ("add", 8)]
    print("KthLargest(k=3, nums=[1, 2, 3, 3])")
    print(f"operations = {operations}")
    for op, arg in operations:
        result = getattr(stream, op)(arg)
        print(f"{op}({arg}) -> {result}")
