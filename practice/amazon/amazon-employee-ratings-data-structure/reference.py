"""Employee Ratings Management System — https://www.fastprep.io/problems/amazon-employee-ratings-data-structure

Write-up & approaches: ../../../docs/amazon/amazon-employee-ratings-data-structure.md
Reference implementation of the write-up's recommended Lazy Heap + Fenwick
Index Mapping solution, kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.
"""

import heapq
from typing import List, Tuple


class EmployeeRatings:
    def __init__(self, operation_bound: int) -> None:
        """Size the slot arrays by `operation_bound`, an upper bound on
        the appends this structure will see. The write-up precounts the
        appends exactly; an upper bound leaves the fixed-array design
        untouched and only ever over-allocates, which costs nothing
        asymptotically.

        Time:  O(n) for n operations: one allocation pass.
        Space: O(n): the liveness arrays are sized by the bound.
        """
        self.append_count = operation_bound
        self.alive = [False] * (self.append_count + 1)
        self.live_prefix = [0] * (self.append_count + 1)
        self.highest_step = 1 << (self.append_count.bit_length() - 1)
        self.heap: List[Tuple[int, int]] = []
        self.sequence = 0

    def append(self, rating: int) -> None:
        """Claim the next slot, mark it live in the Fenwick tree, and push
        the negated rating keyed by slot number.

        Time:  O(log n): one Fenwick point update plus one heap push.
        Space: O(1) per call: one slot, one heap entry.
        """
        self.sequence += 1
        self.alive[self.sequence] = True
        self._add_live_prefix(self.sequence, 1)
        heapq.heappush(self.heap, (-rating, self.sequence))

    def delete(self, index: int) -> None:
        """Mark the live slot currently at `index` dead; its stale heap
        entry lingers until a query surfaces it.

        Time:  O(log n): one binary-lifting rank walk plus one Fenwick
            update.
        Space: O(1): no new retained state.
        """
        target_sequence = self._find_rank_live(index + 1)
        self.alive[target_sequence] = False
        self._add_live_prefix(target_sequence, -1)

    def query(self) -> List[int]:
        """Discard dead entries stranded at the heap top, then return
        [maximumRating, earliestIndex] for the live maximum.

        Time:  O(log n) amortized: each lazy pop discards one entry for
            good, so total pops are bounded by total pushes, and the
            index mapping is one Fenwick prefix read.
        Space: O(1) beyond the retained structures.
        """
        while not self.alive[self.heap[0][1]]:
            heapq.heappop(self.heap)
        negated_rating, max_sequence = self.heap[0]
        return [-negated_rating, self._count_live_through(max_sequence) - 1]

    def _add_live_prefix(self, sequence_number: int, delta: int) -> None:
        """Fenwick point update over the live counts.

        Time:  O(log n): one tail-hop chain.
        Space: O(1).
        """
        while sequence_number <= self.append_count:
            self.live_prefix[sequence_number] += delta
            sequence_number += sequence_number & -sequence_number

    def _count_live_through(self, sequence_number: int) -> int:
        """Fenwick prefix read: how many live slots sit at or before
        `sequence_number`.

        Time:  O(log n): one head-hop chain.
        Space: O(1).
        """
        live_total = 0
        while sequence_number > 0:
            live_total += self.live_prefix[sequence_number]
            sequence_number -= sequence_number & -sequence_number
        return live_total

    def _find_rank_live(self, rank: int) -> int:
        """Binary-lifting select: the slot number of the `rank`-th live
        slot.

        Time:  O(log n): one halving step walk.
        Space: O(1).
        """
        position = 0
        remaining = rank
        step = self.highest_step
        while step > 0:
            next_position = position + step
            if (next_position <= self.append_count
                    and self.live_prefix[next_position] < remaining):
                position = next_position
                remaining -= self.live_prefix[next_position]
            step //= 2
        return position + 1


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    ratings = EmployeeRatings(6)
    ratings.append(5)
    ratings.append(7)
    ratings.append(7)
    print(ratings.query())
    ratings.delete(1)
    print(ratings.query())
