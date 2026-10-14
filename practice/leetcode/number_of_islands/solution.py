"""Number of Islands: https://leetcode.com/problems/number-of-islands/

Write-up & approaches: ../../../docs/leetcode/number_of_islands.md

Given an `m x n` 2D binary grid of `'1'`s (land) and `'0'`s (water), return the
number of islands. An island is formed by connecting adjacent lands horizontally
or vertically and is surrounded by water.

  uv run python number_of_islands/solution.py     # debug one case (see CASE below)
  uv run pytest number_of_islands/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        rows, cols = len(grid), len(grid[0])


        def dfs(row: int, col: int):
            if row < 0 or row >= rows or col < 0 or col >= cols or grid[row][col] == '0':
                return
            grid[row][col] = '0'
            directions = [[0,1],[0,-1],[1,0],[-1,0]]
            for direction in directions:
                dfs(row+direction[0], col+direction[1])

        islands = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1':
                    islands += 1
                    dfs(row, col)
        return islands
if __name__ == "__main__":
    # Debug playground: set a breakpoint in numIslands above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numIslands(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
