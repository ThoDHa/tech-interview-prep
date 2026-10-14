"""Max Area of Island — https://leetcode.com/problems/max-area-of-island/

Write-up & approaches: ../../docs/problems/max_area_of_island.md
Reference implementation of the write-up's Recursive DFS solution, kept next
to the harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python max_area_of_island/reference.py   # debug one case (see CASE below)
  uv run pytest max_area_of_island/               # run the test sets
"""

from harness import pick_case


class Solution:
    def maxAreaOfIsland(self, grid):
        """Return the largest island area, sinking each visited island to 0.

        Scans every cell; each unvisited land cell starts a DFS that counts
        the island's cells by flipping them to water as they are visited, so
        every cell is entered by the scan or the DFS exactly once.

        Args:
            grid: 2-D list of 0/1 ints, modified in place (islands sunk).

        Returns:
            The maximum island area, 0 when the grid holds no land.

        Time:  O(rows · columns): every cell is visited a constant number
            of times (once by the scan, once by the DFS at most).
        Space: O(rows · columns): the DFS recursion depth on a snake island
            that fills the grid.
        """
        if not grid:
            return 0
        rows, columns = len(grid), len(grid[0])

        def sink_island(row: int, column: int) -> int:
            if not (0 <= row < rows and 0 <= column < columns):
                return 0
            if grid[row][column] != 1:
                return 0
            grid[row][column] = 0
            return (
                1
                + sink_island(row + 1, column)
                + sink_island(row - 1, column)
                + sink_island(row, column + 1)
                + sink_island(row, column - 1)
            )

        largest = 0
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == 1:
                    largest = max(largest, sink_island(row, column))
        return largest


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxAreaOfIsland above, then run
    # this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxAreaOfIsland(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
