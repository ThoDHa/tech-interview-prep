"""Grid Reachability with a Forbidden Turn — https://www.fastprep.io/problems/amazon-grid-reachability-forbidden-turn

Write-up & approaches: ../../../docs/amazon/amazon-grid-reachability-forbidden-turn.md

Reference implementation of the write-up's recommended Turn-Constrained
Breadth-First Search solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-grid-reachability-forbidden-turn/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-grid-reachability-forbidden-turn/              # run the test sets
"""

from collections import deque
from typing import List

from harness import pick_case


class Solution:
    def canReachWithTurnRule(
        self, grid: List[str], start: List[int], destination: List[int],
        initialHeading: int, forbiddenTurn: str,
    ) -> bool:
        """Return whether any legal move sequence reaches the destination
        cell, where every move goes straight ahead or turns 90 degrees
        in the one un-forbidden direction.

        The walker's state is the cell plus the heading: the same cell
        offers different moves under different headings, so `4 * R * C`
        situations exist and each carries exactly two successors (the
        straight move and the one allowed turn). A breadth-first search
        over those situations, marking each visited once, answers
        reachability in linear time; the destination is a cell, so any
        heading arriving there succeeds, and the seed answering the
        start-equals-destination case pops before any move is made.

        Args:
            grid: Rows of '0' (open) and 'X' (blocked), equal lengths,
                `1 <= rows, columns <= 500`.
            start: Zero-based `[row, column]` of an open cell.
            destination: Zero-based `[row, column]` of an open cell.
            initialHeading: 0 north, 1 east, 2 south, or 3 west.
            forbiddenTurn: "left" or "right".

        Returns:
            Whether a valid path exists.

        Time:  O(R * C): each of the `4 * R * C` situations enters the
               queue once and expands two moves.
        Space: O(R * C): the visited table and the queue.
        """
        rows, columns = len(grid), len(grid[0])
        offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))
        allowed_turn = 1 if forbiddenTurn == "left" else 3

        visited = [[[False] * 4 for _ in range(columns)] for _ in range(rows)]
        visited[start[0]][start[1]][initialHeading] = True
        queue = deque([(start[0], start[1], initialHeading)])
        while queue:
            row, column, heading = queue.popleft()
            if (row, column) == (destination[0], destination[1]):
                return True
            for turned_heading in (heading, (heading + allowed_turn) % 4):
                dr, dc = offsets[turned_heading]
                next_row, next_column = row + dr, column + dc
                if (
                    0 <= next_row < rows
                    and 0 <= next_column < columns
                    and grid[next_row][next_column] == "0"
                    and not visited[next_row][next_column][turned_heading]
                ):
                    visited[next_row][next_column][turned_heading] = True
                    queue.append((next_row, next_column, turned_heading))
        return False


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canReachWithTurnRule above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().canReachWithTurnRule(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
