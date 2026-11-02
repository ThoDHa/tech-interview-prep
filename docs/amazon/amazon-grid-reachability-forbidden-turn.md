# [Grid Reachability with a Forbidden Turn](https://www.fastprep.io/problems/amazon-grid-reachability-forbidden-turn)

**Medium** | **NN minutes** | **Breadth First Search, Graph**

Determine whether a destination can be reached on an obstacle grid while respecting movement direction.

For this exercise, assume grid contains 0 for open cells and X for blocked cells. start and destination are zero-based [row, column] coordinates of open cells.

initialHeading is 0 for north, 1 for east, 2 for south, or 3 for west. forbiddenTurn is left or right.

Each move advances exactly one adjacent cell. Relative to the current heading, you may continue straight or turn 90 degrees in the direction that is not forbidden. You cannot reverse direction, enter a blocked cell, or leave the grid. Your heading becomes the direction of the move. Reaching the destination with any heading succeeds. Starting at the destination succeeds with zero moves.

Return whether a valid path exists.

## Examples

### Example 1

**Input:** `grid = ["000","0X0","000"]`, `start = [0,0]`, `destination = [2,2]`, `initialHeading = 1`, `forbiddenTurn = "left"`

**Output:** `true`

**Explanation:** Move east along the top row, turn right, and continue south.

### Example 2

**Input:** `grid = ["000","0X0","000"]`, `start = [0,0]`, `destination = [2,2]`, `initialHeading = 1`, `forbiddenTurn = "right"`

**Output:** `false`

**Explanation:** The only open route from the top-left corner requires a right turn, which is forbidden.

## Constraints

- `For this exercise, assume 1 <= rows, columns <= 500; all rows have equal length.`
- `Every cell is 0 or X.`
- `Start and destination are valid open cells.`
- `0 <= initialHeading <= 3.`
- `forbiddenTurn is left or right.`

## Deriving the Solution

The trap is that plain grid BFS tracks cells, but here the same cell is not always the same place: standing in the middle of the grid heading east offers different moves than standing there heading north. The state of the walker is the cell plus the heading, and from every state exactly two moves exist, straight and the one allowed turn. Once the state is sized honestly, the question "does any valid move sequence reach the destination" is reachability in a small graph, and breadth-first search answers it.

1. **Start literal.** Try every move sequence by backtracking over simple paths; complete and correct, but exponential on open grids: see [Backtracking Path Enumeration](#backtracking-path-enumeration).
2. **Spot the waste.** The enumeration replays the same (cell, heading) situation along many different prefixes, and the answer from that situation onward never depends on how it was reached.
3. **Fix it with a queue.** Remember each (cell, heading) pair once, explore the two moves from each in first-in-first-out order, and stop when the destination cell pops: see [Turn-Constrained Breadth-First Search](#turn-constrained-breadth-first-search).

## Solutions

### Backtracking Path Enumeration

#### Derivation

The statement's most literal reading: a valid path exists if some sequence of legal moves lands on the destination, so enumerate sequences:

1. Walk from `(start, initialHeading)`; at every step try both moves, straight and the allowed 90-degree turn.
2. A move is legal when its target cell is inside the grid, open, and the walker has not already stood in that target state during the current path (heading included, so a corridor can be walked twice in opposite directions but a single state never repeats on one path).
3. Succeed the moment the walk stands on the destination cell; starting there succeeds immediately with zero moves.
4. If the enumeration exhausts every simple path without landing, return `False`.

Because a repeated state could be cut from any walk that contains it, a successful walk can always be shortened to a simple one; enumerating simple paths therefore misses nothing, which is what makes the enumeration a sound oracle for the queue version.

#### Walkthrough

Example 2 (`grid = ["000","0X0","000"]`, `start = [0,0]`, `initialHeading = 1` east, `forbiddenTurn = "right"`), the whole search tree:

```text
(0,0,east)   straight -> (0,1,east)   turn left -> (-1,0) off the grid
(0,1,east)   straight -> (0,2,east)   turn left -> (-1,1) off the grid
(0,2,east)   straight -> (0,3) off the grid   turn left -> (-1,2) off the grid: dead end
```

Forbidding right leaves the left turn, and left of an east heading is north: every turn from row 0 points off the grid, so straight is the only legal move and the walk dies at the top-right corner. The destination lies below the blocked center, behind a right turn the walker can never make, so every branch dies before touching `(2,2)`, matching the expected Output `false`.

#### Solution

```python
from typing import List


class Solution:
    def canReachWithTurnRule(self, grid: List[str], start: List[int], destination: List[int], initialHeading: int, forbiddenTurn: str) -> bool:
        rows, columns = len(grid), len(grid[0])
        offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))
        allowed_turn = 1 if forbiddenTurn == "left" else 3

        def walk(row: int, column: int, heading: int, walked: set) -> bool:
            if (row, column) == (destination[0], destination[1]):
                return True
            state = (row, column, heading)
            if state in walked:
                return False
            walked.add(state)
            for turned_heading in (heading, (heading + allowed_turn) % 4):
                dr, dc = offsets[turned_heading]
                next_row, next_column = row + dr, column + dc
                if (
                    0 <= next_row < rows
                    and 0 <= next_column < columns
                    and grid[next_row][next_column] == "0"
                    and walk(next_row, next_column, turned_heading, walked)
                ):
                    return True
            walked.remove(state)
            return False

        return walk(start[0], start[1], initialHeading, set())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^(4 * R * C))` worst case

Every state has at most two successors, and the recursion enumerates simple paths through the `4 * R * C` states; obstacle layouts cut this drastically.

##### Space Complexity: `O(R * C)`

The on-path set and the recursion stack.

#### Key Insights

- The enumeration needs no visited-ever table: cutting repeated states keeps at least one witness path, so simple-path enumeration is complete.
- The goal test runs on arrival at a cell, before the state check, so the zero-move start equals destination case exits immediately.
- Exponential branching makes this form a small-grid tool and an independent checker, not a production plan.

### Turn-Constrained Breadth-First Search

#### Derivation

The enumeration's flaw is replaying situations. A situation is `(row, column, heading)`: the cell plus the direction of travel, at most `4 * R * C` of them. From any situation exactly two moves exist: straight (same heading) and the one allowed turn. Since neither move's legality depends on history, collect situations in a queue and never process one twice:

1. Translate `forbiddenTurn` into the allowed turn's heading delta: forbidding left leaves the clockwise step, forbidding right leaves the counterclockwise step.
2. Seed the queue with `(start, initialHeading)`; if the start is the destination, the first pop answers `True` with zero moves.
3. Pop a situation; try straight and the allowed turn. A move landing inside the grid, on an open cell, in a never-seen situation enqueues that situation with its new heading.
4. The destination is a cell, not a heading: answer `True` the moment any situation on that cell pops, whichever heading it carries.
5. An empty queue means every reachable situation was seen and the destination never popped: return `False`.

#### Walkthrough

Example 1 (`grid = ["000","0X0","000"]`, `initialHeading = 1` east, `forbiddenTurn = "left"`, so the allowed turn is the clockwise right step), the queue's life:

```text
seed (0,0,east)
pop (0,0,east)   straight (0,1,east) enq   turn right (1,0,south) enq
pop (0,1,east)   straight (0,2,east) enq   turn right -> (1,1,south) blocked
pop (1,0,south)  straight (2,0,south) enq  turn right -> (1,-1) off the grid
pop (0,2,east)   straight -> (0,3) off the grid   turn right (1,2,south) enq
pop (2,0,south)  straight -> (3,0) off the grid   turn right -> (2,-1) off the grid
pop (1,2,south)  straight (2,2,south) enq  turn right -> (1,1,south) blocked
pop (2,2,south)  destination cell: return True
```

Matching the expected Output `true`: the straight-first expansion walks east along the top row and turns down the right side, hugging the ring around the blocked center.

#### Solution

```python
from collections import deque
from typing import List


class Solution:
    def canReachWithTurnRule(self, grid: List[str], start: List[int], destination: List[int], initialHeading: int, forbiddenTurn: str) -> bool:
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
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R * C)`

Each of the `4 * R * C` situations enters the queue once and expands two moves; the constant four hides in the bound.

##### Space Complexity: `O(R * C)`

The visited table and the queue.

#### Key Insights

- The heading is part of the state: dropping it merges situations with different move sets and can return `false` for a reachable destination, the one wrong answer this problem punishes.
- Exactly two moves per situation fall out of the rule's wording (straight, or the one un-forbidden turn); there is never a choice of two turns, so the transition table is tiny.
- The destination is a cell, not a state: any heading arriving there succeeds, so the goal test checks only the coordinates on pop.
- The start-equals-destination case needs no special code: the seed itself pops first and answers `True` with zero moves.

## Comparison of Solutions

### Time Complexity

- **Backtracking Path Enumeration**: `O(2^(4 * R * C))` worst case - every simple path through the state graph.
- **Turn-Constrained Breadth-First Search**: `O(R * C)` - each situation processed once.

### Space Complexity

- **Backtracking Path Enumeration**: `O(R * C)` - on-path set and recursion stack.
- **Turn-Constrained Breadth-First Search**: `O(R * C)` - visited table and queue.

### Trade-offs

- **Backtracking Path Enumeration**: the move rule transcribed into a recursion and the independent checker for the queue version; unusable on the 500-by-500 bound.
- **Turn-Constrained Breadth-First Search (Recommended)**: the same two-move transition table with the replay waste removed by a visited table.

### When to Use Each

- **Backtracking Path Enumeration**: tiny grids, and always as the oracle validating the queue version in tests.
- **Turn-Constrained Breadth-First Search (Recommended)**: the interview answer: state = cell plus heading, two moves per state, first-in-first-out.

### Optimization Notes

- **Turn-Constrained Breadth-First Search** is the recommended choice: linear in the grid with a two-successor transition table.
- `forbiddenTurn` folds into one heading delta before the search starts, so the loop body never reads the string.
- The 500 bound makes `4 * R * C` a million states, well within reach of the per-situation constant here; there is nothing left worth optimizing.
