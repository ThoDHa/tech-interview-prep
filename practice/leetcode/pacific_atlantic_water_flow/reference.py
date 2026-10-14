"""Pacific Atlantic Water Flow — https://leetcode.com/problems/pacific-atlantic-water-flow/

Write-up & approaches: ../../docs/problems/pacific_atlantic_water_flow.md
Reference implementation of the write-up's Reverse Two-Ocean DFS solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python pacific_atlantic_water_flow/reference.py   # debug one case (see CASE below)
  uv run pytest pacific_atlantic_water_flow/               # run the test sets
"""

from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """Return the cells whose water can reach both oceans.

        Runs one reachability flood inland from each ocean's border cells
        (water flows uphill in this reversed view: a neighbor is reachable
        when its height is >= the current cell's), then reports the cells
        reachable from both floods.

        Args:
            heights: Rectangular grid of cell heights.

        Returns:
            The `[row, column]` pairs reachable from both oceans, in scan
            order.

        Time:  O(rows · columns): each flood visits every cell at most once.
        Space: O(rows · columns): the two visited grids and the DFS stack.
        """
        if not heights:
            return []
        rows, columns = len(heights), len(heights[0])

        pacific = set()
        atlantic = set()

        def flood(row: int, column: int, reachable: set) -> None:
            if (row, column) in reachable:
                return
            reachable.add((row, column))
            for next_row, next_column in (
                (row + 1, column),
                (row - 1, column),
                (row, column + 1),
                (row, column - 1),
            ):
                if (
                    0 <= next_row < rows
                    and 0 <= next_column < columns
                    and heights[next_row][next_column] >= heights[row][column]
                ):
                    flood(next_row, next_column, reachable)

        for row in range(rows):
            flood(row, 0, pacific)
            flood(row, columns - 1, atlantic)
        for column in range(columns):
            flood(0, column, pacific)
            flood(rows - 1, column, atlantic)

        return [
            [row, column]
            for row in range(rows)
            for column in range(columns)
            if (row, column) in pacific and (row, column) in atlantic
        ]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in pacificAtlantic above, then run
    # this file. cases.json is empty (any-order output), so a literal
    # example stands in.
    heights = [
        [4, 2, 7, 3, 4],
        [7, 4, 6, 4, 7],
        [6, 3, 5, 3, 6],
    ]
    result = Solution().pacificAtlantic(heights)
    print(f"args = {heights}")
    print(f"got: {result}")
