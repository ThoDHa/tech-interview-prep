"""Parking Garage Allocator — https://www.fastprep.io/problems/amazon-parking-garage-allocator

Write-up & approaches: ../../../docs/amazon/amazon-parking-garage-allocator.md

Reference implementation of the write-up's recommended Free-Interval
First Fit solution, presented as the design class behind the page's
judged processParking form. Your own attempt lives in solution.py.

  uv run python amazon/amazon-parking-garage-allocator/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-parking-garage-allocator/              # run the test sets
"""

from typing import List, Tuple


class ParkingGarage:
    """A parking garage that parks every request in the leftmost run of
    free spaces large enough for it.

    The state is the list of maximal free runs, sorted by start, pairwise
    disjoint, and never adjacent, so a park reads the first run long
    enough and a leave re-inserts the freed range, merging with a free
    run that touches it on either side.
    """

    def __init__(self, space_count: int) -> None:
        """Open the garage with every space free: one run spanning all
        `space_count` spaces.

        Time:  O(1): one two-field run.
        Space: O(1): the run list grows only as fragmentation appears.
        """
        self.free_runs: List[Tuple[int, int]] = [(0, space_count)]

    def park(self, size: int) -> int:
        """Occupy the leftmost free run of at least `size` spaces and
        return its starting index, or -1 when no run fits.

        Time:  O(g): one left-to-right scan over the g live free runs,
            plus one in-place shrink or delete at the chosen run.
        Space: O(1): the chosen run shrinks or disappears.
        """
        for run_index, (run_start, run_end) in enumerate(self.free_runs):
            if run_end - run_start >= size:
                if run_end - run_start == size:
                    del self.free_runs[run_index]
                else:
                    self.free_runs[run_index] = (run_start + size, run_end)
                return run_start
        return -1

    def leave(self, freed_start: int, freed_size: int) -> None:
        """Free the occupied run of `freed_size` spaces beginning at
        `freed_start`, absorbing a free run that ends at its left edge
        and a free run that starts at its right edge.

        Time:  O(g): the binary search finds the insertion point in
            O(log g), and the list deletions and insertion around it
            move O(g) entries in the worst case.
        Space: O(1): at most one run is inserted and merges absorb its
            neighbors, so the run count rises by at most one.
        """
        freed_end = freed_start + freed_size
        low, high = 0, len(self.free_runs)
        while low < high:
            middle = (low + high) // 2
            if self.free_runs[middle][0] < freed_start:
                low = middle + 1
            else:
                high = middle
        insertion = low
        if insertion > 0 and self.free_runs[insertion - 1][1] == freed_start:
            freed_start = self.free_runs[insertion - 1][0]
            del self.free_runs[insertion - 1]
            insertion -= 1
        if insertion < len(self.free_runs) and self.free_runs[insertion][0] == freed_end:
            freed_end = self.free_runs[insertion][1]
            del self.free_runs[insertion]
        self.free_runs.insert(insertion, (freed_start, freed_end))


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    garage = ParkingGarage(6)
    print(garage.park(2))
    print(garage.park(3))
    garage.leave(0, 2)
    print(garage.park(1))
