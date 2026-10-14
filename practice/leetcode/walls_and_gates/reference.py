"""Walls And Gates — https://leetcode.com/problems/walls-and-gates/

Write-up & approaches: ../../docs/problems/walls_and_gates.md
Reference implementation of the write-up's Multi-Source BFS solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python walls_and_gates/reference.py   # debug one case (see CASE below)
  uv run pytest walls_and_gates/               # run the test sets
"""

from collections import deque

INF = 2147483647


class Solution:
    def islandsAndTreasure(self, grid):
        """Fill each land cell with its shortest distance to a treasure chest.

        Seeds one BFS from every chest at once; because distance increases
        by exactly one per layer, the first wave to reach a land cell
        carries its nearest-chest distance, and the guard against re-entry
        makes the write idempotent.

        Args:
            grid: 2-D list mutated in place; -1 wall, 0 chest, INF land.

        Returns:
            None: the distances land in `grid` itself.

        Time:  O(rows · columns): every cell enters the queue at most once.
        Space: O(rows · columns): the queue in the worst case.
        """
        if not grid:
            return
        rows, columns = len(grid), len(grid[0])
        queue = deque()
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == 0:
                    queue.append((row, column))
        while queue:
            row, column = queue.popleft()
            for next_row, next_column in (
                (row + 1, column),
                (row - 1, column),
                (row, column + 1),
                (row, column - 1),
            ):
                if (
                    0 <= next_row < rows
                    and 0 <= next_column < columns
                    and grid[next_row][next_column] == INF
                ):
                    grid[next_row][next_column] = grid[row][column] + 1
                    queue.append((next_row, next_column))


if __name__ == "__main__":
    # Debug playground: set a breakpoint in islandsAndTreasure above, then
    # run this file. cases.json is empty (in-place mutation), so a literal
    # example stands in.
    grid = [
        [INF, -1, 0, INF],
        [INF, INF, INF, -1],
        [INF, -1, INF, -1],
        [0, -1, INF, INF],
    ]
    Solution().islandsAndTreasure(grid)
    print(f"args = {[[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]}")
    print(f"got: {grid}")
