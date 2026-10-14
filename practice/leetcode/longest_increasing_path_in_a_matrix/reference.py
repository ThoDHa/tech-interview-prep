"""Longest Increasing Path In a Matrix — https://leetcode.com/problems/longest-increasing-path-in-a-matrix/

Write-up & approaches: ../../docs/problems/longest_increasing_path_in_a_matrix.md
Reference implementation of the write-up's DFS with Memoization solution.

You are given a 2-D grid of integers `matrix`, where each integer is greater than or equal to `0`. Return the length of the longest strictly increasing path within `matrix`; moves are horizontal or vertical only, never diagonal.

  uv run python longest_increasing_path_in_a_matrix/reference.py   # debug one case (see CASE below)
  uv run pytest longest_increasing_path_in_a_matrix/              # run the test sets
"""

import sys

from harness import pick_case

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def longestIncreasingPath(self, matrix):
        """Return the length of the longest strictly increasing path.

        Runs a memoized depth-first search from every cell: the memo stores
        the longest increasing path starting at each cell, so every cell's
        answer is computed once and every later visit is a lookup. Strict
        increase along each step keeps the search acyclic, which is what
        makes the plain memoization sound without a visited set.

        Args:
            matrix: Grid of non-negative integers,
                1 <= rows, cols <= 100.

        Returns:
            The number of cells on the longest strictly increasing path.

        Time:  O(rows * cols): four constant-work neighbor probes per cell.
        Space: O(rows * cols): the memo plus the recursion stack.
        """
        rows, cols = len(matrix), len(matrix[0])
        # One DFS frame per cell along the current path, up to rows * cols
        # deep (a snake grid reaches every cell), past CPython's default
        # recursion limit of 1000 on Python < 3.13.
        sys.setrecursionlimit(max(sys.getrecursionlimit(), rows * cols + 100))
        memo = [[0] * cols for _ in range(rows)]

        def dfs(r, c):
            if memo[r][c]:
                return memo[r][c]
            best = 1
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            memo[r][c] = best
            return best

        return max(dfs(r, c) for r in range(rows) for c in range(cols))


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestIncreasingPath above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestIncreasingPath(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
