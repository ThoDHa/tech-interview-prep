"""Dynamic Kth Largest Queries — https://www.fastprep.io/problems/amazon-dynamic-kth-largest-queries

Write-up & approaches: ../../../docs/amazon/amazon-dynamic-kth-largest-queries.md
Reference implementation of the write-up's recommended Sorted List with
Binary Search Insertion solution, kept next to the harness so authored
cases stay falsifiable. Your own attempt lives in solution.py.
"""

from bisect import insort
from typing import List


class DynamicKthLargest:
    def __init__(self, initial_values: List[int]) -> None:
        """Sort the initial values once; the list stays sorted forever.

        Time:  O(m log m) for m initial values.
        Space: O(m): every initial value is retained.
        """
        self.sorted_values = sorted(initial_values)

    def insert(self, value: int) -> None:
        """Splice `value` into its sorted slot: O(log m) comparisons to
        find the slot, an O(m) tail shift to make room.

        Time:  O(m) worst case, dominated by the list splice.
        Space: O(1) amortized per call beyond the list's growth.
        """
        insort(self.sorted_values, value)

    def find(self, k: int) -> int:
        """Return the current kth largest by negative indexing from the
        sorted end.

        Time:  O(1): one index read.
        Space: O(1): no retained state.
        """
        return self.sorted_values[-k]


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    tracker = DynamicKthLargest([3, 7, 1])
    print(tracker.find(3))
    tracker.insert(4)
    tracker.insert(9)
    print(tracker.find(2))
    print(tracker.find(4))
