"""Rotting Oranges: https://leetcode.com/problems/rotting-oranges/

Write-up & approaches: ../../../docs/leetcode/rotting_oranges.md

Given an `m x n` grid of cells (`0` empty, `1` fresh, `2` rotten), each minute
every fresh orange 4-directionally adjacent to a rotten one rots. Return the
minimum minutes until no fresh orange remains, or `-1` if some never rot.

  uv run python rotting_oranges/solution.py     # debug one case (see CASE below)
  uv run pytest rotting_oranges/                # run the test sets
"""
from collections import deque

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        """
            create a queue of all the rotton oranges, then go through the queue everytime.
            we can create two queues? and just cylcle, that's weird.


            we can do the same thing with the number of islands thing, where we go through and spread out every time.
            either keep track of fresh oranges, and at the end we will return back if fresh oranges is 0 etc.
        """
        rows, cols = len(grid), len(grid[0])
        fresh = 0
        minutes = 0
        queue = deque()
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    fresh += 1
                elif grid[row][col] == 2:
                    queue.append((row, col))
        directions = [(0, 1), (0,-1), (1, 0), (-1, 0)]
        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):
                row, col = queue.popleft()
                for nr, nc in directions:
                    r = row + nr
                    c = col + nc
                    if 0 <= r < rows and 0 <= c < cols:
                        if grid[r][c] == 1:
                            grid[r][c] = 2
                            fresh -= 1
                            queue.append((r, c))


        return minutes if fresh == 0 else -1

if __name__ == "__main__":
    # Debug playground: set a breakpoint in orangesRotting above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().orangesRotting(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
