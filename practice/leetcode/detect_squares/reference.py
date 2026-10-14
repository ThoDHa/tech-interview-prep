"""Detect Squares — https://leetcode.com/problems/detect-squares/

Write-up & approaches: ../../docs/problems/detect_squares.md
Canonical reference implementation: the write-up's Count Map with Diagonal
Scan solution. Your own attempt lives in solution.py.

You are given a stream of points on a 2-D plane. `add` stores a point
(duplicates allowed and counted separately); `count` returns the number of
axis-aligned squares having the query point as one corner, formed with three
stored points.

  uv run python detect_squares/reference.py   # replay the example stream
  uv run pytest detect_squares/               # run the test sets
"""

from typing import Dict, List, Tuple


class CountSquares:
    """Count axis-aligned squares through a query point, over a point stream."""

    def __init__(self) -> None:
        """Start an empty structure with no stored points.

        Time:  O(1): one empty dict.
        Space: O(1): nothing stored yet.
        """
        self.counts: Dict[Tuple[int, int], int] = {}

    def add(self, point: List[int]) -> None:
        """Record one copy of `point` in the stream.

        Args:
            point: `[x, y]` with 0 <= x, y <= 1000; duplicates accumulate.

        Time:  O(1) average: one dict lookup and one increment.
        Space: O(1) amortized: one entry per distinct point.
        """
        self.counts[(point[0], point[1])] = self.counts.get((point[0], point[1]), 0) + 1

    def count(self, point: List[int]) -> int:
        """Count squares with `point` as a corner, diagonals enumerated.

        A stored point `p` forms a square with query `q` exactly when
        `abs(px - qx) == abs(py - qy) != 0`; its two side corners are then
        `[px, qy]` and `[qx, py]`. Each valid diagonal contributes the
        product of the three multiplicities.

        Args:
            point: The query corner `[x, y]`.

        Returns:
            The number of square choices, counting duplicate points
            separately.

        Time:  O(U) average over the U distinct stored points: one test
            and two dict lookups per entry.
        Space: O(1): no per-query allocations beyond scalars.
        """
        qx, qy = point
        total = 0
        for (px, py), copies in self.counts.items():
            dx, dy = px - qx, py - qy
            if abs(dx) != abs(dy) or dx == 0:
                continue
            total += (
                copies
                * self.counts.get((px, qy), 0)
                * self.counts.get((qx, py), 0)
            )
        return total


if __name__ == "__main__":
    # Debug playground: cases.json is empty (multi-method starter), so
    # Example 1's operation sequence stands in.
    operations = [
        ("add", (1, 1)),
        ("add", (2, 2)),
        ("add", (1, 2)),
        ("count", (2, 1)),
        ("count", (3, 3)),
        ("add", (2, 2)),
        ("count", (2, 1)),
    ]
    expected = [None, None, None, 1, 0, None, 2]
    detector = CountSquares()
    print("CountSquares()")
    for (method, args), want in zip(operations, expected):
        result = getattr(detector, method)(list(args))
        print(f"{method}{list(args)} -> {result} (expected {want})")
