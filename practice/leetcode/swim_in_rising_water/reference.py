"""Swim In Rising Water — https://leetcode.com/problems/swim-in-rising-water/

Write-up & approaches: ../../docs/problems/swim_in_rising_water.md
Reference implementation of the write-up's Modified Dijkstra's Algorithm solution.

You are given a square 2-D matrix of distinct integers `grid` where each integer `grid[i][j]` represents the elevation at position `(i, j)`. Rain starts to fall at time = `0`, which causes the water level to rise. At time `t`, the water level across the entire grid is `t`. You may swim either horizontally or vertically in the grid between two adjacent squares if the original elevation of both squares is less than or equal to the water level at time `t`. Starting from the top left square `(0, 0)`, return the minimum amount of time it will take until it is possible to reach the bottom right square `(n - 1, n - 1)`.

  uv run python swim_in_rising_water/reference.py   # debug one case (see CASE below)
  uv run pytest swim_in_rising_water/              # run the test sets
"""

import heapq

from harness import pick_case


class Solution:
    def swimInWater(self, grid):
        """Return the least water level reaching the far corner via Dijkstra.

        The cost of a path is its maximum cell elevation, not a sum, so
        Dijkstra relaxes with `max(distance, elevation)` instead of addition:
        popping the reachable cell with the smallest such bottleneck first is
        optimal because all other frontiers can only demand a higher level.

        Args:
            grid: Square matrix of distinct elevations, `grid[0][0]` = minimum.

        Returns:
            The minimum water level that allows a swim from the top-left to
            the bottom-right cell.

        Time:  O(n^2 * log n): each cell may push one heap entry.
        Space: O(n^2): the heap and the best-known bottleneck grid.
        """
        size = len(grid)
        best = [[None] * size for _ in range(size)]
        best[0][0] = grid[0][0]
        heap = [(grid[0][0], 0, 0)]
        while heap:
            level, row, col = heapq.heappop(heap)
            if (row, col) == (size - 1, size - 1):
                return level
            if level > best[row][col]:
                continue
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row, next_col = row + dr, col + dc
                if not (0 <= next_row < size and 0 <= next_col < size):
                    continue
                candidate = max(level, grid[next_row][next_col])
                if best[next_row][next_col] is None or candidate < best[next_row][next_col]:
                    best[next_row][next_col] = candidate
                    heapq.heappush(heap, (candidate, next_row, next_col))
        raise AssertionError("bottom-right cell is always reachable on a square grid")


if __name__ == "__main__":
    # Debug playground: set a breakpoint in swimInWater above, then run this
    # file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().swimInWater(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
