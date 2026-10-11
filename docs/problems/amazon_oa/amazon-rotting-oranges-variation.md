# [Minimum Time to Spread Through a Grid](https://www.fastprep.io/problems/amazon-rotting-oranges-variation)

**Medium** | **NN minutes** | **Array, Breadth First Search, Matrix**

You are given a rectangular grid whose cells contain 0, 1, or 2. A zero is empty, a one is fresh, and a two is already active.

After each minute, every active cell makes each orthogonally adjacent fresh cell active. Return the minimum number of minutes until no fresh cell remains. Return -1 when this is impossible.

## Examples

### Example 1

**Input:** `grid = [[2,1,1],[1,1,0],[0,1,1]]`

**Output:** `4`

**Explanation:** The wave reaches the lower-right fresh cell after four minutes.

### Example 2

**Input:** `grid = [[2,1,1],[0,1,1],[1,0,1]]`

**Output:** `-1`

**Explanation:** The isolated fresh cell in the lower-left corner is unreachable.

### Example 3

**Input:** `grid = [[0,2]]`

**Output:** `0`

**Explanation:** There are no fresh cells, so no minute needs to pass.

## Constraints

- `1 <= grid.length, grid[r].length <= 200`
- `Every row has the same length.`
- `grid[r][c] is 0, 1, or 2.`

## Solutions

### Round-by-Round Simulation

#### Derivation

The most literal reading of the statement plays the minutes one at a time. A fresh cell turns active in a minute exactly when at least one of its four orthogonal neighbors was already active when the minute began, so a minute is one pass: collect the fresh cells, test each against its neighbors, and activate the whole set simultaneously. Simultaneity is the one trap: the cells turning active in minute `t` must not cause further spreading until minute `t + 1`, which is why the set to activate is collected completely before any cell is written:

1. Copy the integer rows into `cells` so the simulation can mark cells
   without touching the caller's grid.
2. Each round, list `fresh_cells`, the positions still holding `1`.
3. If `fresh_cells` is empty, return `minutes`: no fresh cell remains.
4. Otherwise list `spreading`, the fresh cells with at least one active
   neighbor (checked by `borders_active` over the four `directions`).
5. If `spreading` is empty while fresh cells remain, the spread is blocked:
   return `-1`.
6. Activate every cell in `spreading`, increment `minutes`, and loop.

#### Walkthrough

Let us run the rounds by hand on a small tailored 2 × 2 grid, `grid = [[2,1],[1,0]]`, chosen so a single round finishes the spread:

```text
grid          2 1
              1 0

minute 0 scan fresh_cells = [(0,1), (1,0)]
             borders_active(0,1): neighbor (0,0) is 2 -> yes
             borders_active(1,0): neighbor (0,0) is 2 -> yes
             spreading = [(0,1), (1,0)]  -> activate both, minutes = 1
minute 1 scan fresh_cells = []  -> return 1
```

Both fresh cells bordered the original active cell, so one round empties the fresh list and the function returns `1`. The same loop on Example 1 needs four rounds (the wave crosses the grid diagonally to the lower-right corner) and returns `4`, matching its expected Output; on Example 2 the lower-left fresh cell never borders an active cell, `spreading` comes back empty with `fresh_cells` still non-empty, and the function returns `-1`.

#### Solution

The code is the walkthrough's round loop written down: collect, test, activate, repeat.

```python
from typing import List


class Solution:
    def minutesToSpread(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        cells = [list(row) for row in grid]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def borders_active(row: int, col: int) -> bool:
            return any(
                0 <= row + row_offset < rows
                and 0 <= col + col_offset < cols
                and cells[row + row_offset][col + col_offset] == 2
                for row_offset, col_offset in directions
            )

        minutes = 0
        while True:
            fresh_cells = [
                (row, col)
                for row in range(rows)
                for col in range(cols)
                if cells[row][col] == 1
            ]
            if not fresh_cells:
                return minutes
            spreading = [
                (row, col) for row, col in fresh_cells if borders_active(row, col)
            ]
            if not spreading:
                return -1
            for row, col in spreading:
                cells[row][col] = 2
            minutes += 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m × n)²)`

Each round costs a full `O(m × n)` scan to list the fresh cells and test their neighbors, and on a winding path of fresh cells the spread takes `O(m × n)` rounds to finish, so the rounds multiply the scan.

##### Space Complexity: `O(m × n)`

The element-for-element copy `cells`, plus the per-round lists `fresh_cells` and `spreading`, which together never exceed the cell count.

#### Key Insights

- Collecting `spreading` completely before writing any cell is what makes a round simultaneous; activating during the test would let minute `t`'s converts spread within the same round and inflate the count.
- The `-1` exit falls out of the loop for free: a full round with no conversions means the remaining fresh cells are sealed off behind empty cells forever.
- Correct and easy to trust, but the full-grid rescan every minute repeats work the frontier already knew about, which is exactly what the queue version removes.

### Multi-Source BFS

#### Derivation

The simulation's waste is the rescan: every minute it re-reads cells the frontier will never touch again. The frontier is all the information a minute needs, and [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) is the traversal that holds exactly a frontier, one layer per minute. The only twist over single-source flood fill is that spreading starts everywhere at once: every already-active cell is a source, so all of them seed the queue before the first minute. A running `fresh_cells` tally answers both exit conditions without ever rescanning:

1. Seed `queue` with every cell holding `2` and count every cell holding `1`
   into `fresh_cells`, in one pass over the copy `cells`.
2. While the queue is non-empty and `fresh_cells > 0`, spend one minute:
   increment `minutes`, then process the whole current queue level.
3. Processing a level pops each cell and inspects its four neighbors; every
   in-bounds neighbor still holding `1` is flipped to `2`, decrements
   `fresh_cells`, and is appended to the next level.
4. Flipping at enqueue time (not dequeue time) stops a cell from entering
   the queue twice.
5. When the loop ends, `fresh_cells == 0` means every fresh cell was reached:
   return `minutes`. Otherwise the queue drained with fresh cells stranded:
   return `-1`.
6. The `fresh_cells > 0` loop guard also handles Example 3: with no fresh
   cells the loop never runs and `minutes` stays `0`.

#### Walkthrough

Let us spread over Example 1, `grid = [[2,1,1],[1,1,0],[0,1,1]]`, by hand. The scan seeds `queue = [(0,0)]` and counts `fresh_cells = 6`. Each line below is one minute; the queue shown is the level being consumed, and neighbors are checked right, down, left, up:

```text
minute 1  pop (0,0): right (0,1) fresh -> flip, fresh 5; down (1,0) fresh -> flip, fresh 4
          next level [(0,1), (1,0)]
minute 2  pop (0,1): right (0,2) fresh -> flip, fresh 3; down (1,1) fresh -> flip, fresh 2
          pop (1,0): right (1,1) already flipped; down (2,0) empty
          next level [(0,2), (1,1)]
minute 3  pop (0,2): down (1,2) empty
          pop (1,1): down (2,1) fresh -> flip, fresh 1
          next level [(2,1)]
minute 4  pop (2,1): right (2,2) fresh -> flip, fresh 0
          next level [(2,2)]
          fresh_cells == 0 -> loop exits
```

The lower-right fresh cell `(2, 2)` was converted during minute 4, which is exactly the value the loop reports, matching the expected Output for Example 1. The queue held at most two cells at a time, and the grid was never rescanned: each cell entered and left the queue once.

#### Solution

The code is the walkthrough's minute loop: one level of the queue per minute, one flip per fresh neighbor.

```python
from collections import deque
from typing import List


class Solution:
    def minutesToSpread(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        cells = [list(row) for row in grid]
        queue = deque()
        fresh_cells = 0
        for row in range(rows):
            for col in range(cols):
                if cells[row][col] == 2:
                    queue.append((row, col))
                elif cells[row][col] == 1:
                    fresh_cells += 1

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        minutes = 0
        while queue and fresh_cells > 0:
            minutes += 1
            for _ in range(len(queue)):
                row, col = queue.popleft()
                for row_offset, col_offset in directions:
                    new_row, new_col = row + row_offset, col + col_offset
                    if (
                        0 <= new_row < rows
                        and 0 <= new_col < cols
                        and cells[new_row][new_col] == 1
                    ):
                        cells[new_row][new_col] = 2
                        fresh_cells -= 1
                        queue.append((new_row, new_col))
        return minutes if fresh_cells == 0 else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One pass seeds the queue and the fresh tally, and every cell is appended to the queue at most once, so the minute loop does constant work per cell across all levels.

##### Space Complexity: `O(m × n)`

The copy `cells` dominates; the queue itself never holds more than one wavefront, whose width is bounded by `O(min(m, n))`.

#### Key Insights

- Multi-source seeding is the whole generalization: starting every active cell in the queue at layer zero makes layer count equal elapsed minutes, with no per-source restart.
- The level-for-minute correspondence (`for _ in range(len(queue))` per minute) is what converts BFS depth into the time value the problem asks for; a plain flat traversal would only give reachability.
- Flipping a fresh cell when it is enqueued, not when it is popped, keeps each cell in the queue once and keeps the level boundaries honest.
- The two exits live in the loop condition and the return line: no fresh cells at start yields `0`, a drained queue with a positive tally yields `-1`, and neither needs a special-case branch.

## Comparison of Solutions

### Time Complexity

- **Round-by-Round Simulation**: `O((m × n)²)` - every minute rescans the whole grid, and a winding spread can last `O(m × n)` minutes.
- **Multi-Source BFS**: `O(m × n)` - one seeding pass, then constant work per cell across all queue levels.

### Space Complexity

- **Round-by-Round Simulation**: `O(m × n)` - the working copy plus the per-round fresh and spreading lists.
- **Multi-Source BFS**: `O(m × n)` - the working copy dominates; the queue holds one wavefront at a time.

### Trade-offs

- The simulation is the statement translated line by line, so its correctness is visible by inspection, but its per-minute rescan re-does work on every cell of the grid for every minute of the spread.
- The multi-source BFS pays for a queue and a fresh tally and returns the same numbers in one visit per cell; the extra care is the level-per-minute loop and the enqueue-time flip.

### When to Use Each

- **Round-by-Round Simulation**: tiny grids, or as the reference oracle when testing the BFS version's minute counts.
- **Multi-Source BFS (Recommended)**: the interview answer, and the only one of the two that survives the stated limits of a 200 × 200 grid under adversarial spreads.

### Optimization Notes

- Both solutions copy the grid once; keeping the caller's input intact costs one `O(m × n)` pass and does not change either asymptotic bound. Mutating the input in place is a legal shortcut when the caller does not reuse it.
- The BFS converts a reachability traversal into a timed one purely through level discipline; the same trick answers any "minimum number of simultaneous expansion steps" question (word ladders, knight moves, wire routing).
- If the grid arrived as strings, the copy step becomes mandatory (string rows are immutable in Python); with integer rows the copy is a cleanliness choice, not a correctness one.
