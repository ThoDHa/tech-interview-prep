# [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/)

**Medium** | **30 minutes** | **Array, Matrix, Simulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Matrix](https://en.wikipedia.org/wiki/Matrix_(mathematics)) · [Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine) · [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/spiral_matrix/solution.py`](../../practice/spiral_matrix/solution.py)

Given an `m x n` matrix, return all elements of the `matrix` in spiral order.

## Examples

### Example 1

![Spiral Matrix Example 1](assets/spiral_matrix_example1.jpg)

**Input:** `matrix = [[1,2,3],[4,5,6],[7,8,9]]`

**Output:** `[1,2,3,6,9,8,7,4,5]`

### Example 2

![Spiral Matrix Example 2](assets/spiral_matrix_example2.jpg)

**Input:** `matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]`

**Output:** `[1,2,3,4,8,12,11,10,9,5,6,7]`

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 10`
- `-100 <= matrix[i][j] <= 100`

## Deriving the Solution

Spiral order visits all `m × n` cells by walking right, down, left, up, and turning inward each time the walk runs out of room. Every solution below is a different answer to one question: how does the walk know when to turn?

1. **Start literal.** Walk the grid the way a hand traces it: keep a current
   direction, mark cells as visited, and turn clockwise whenever the next step would leave the grid or land on a visited cell. That costs an `O(m×n)` visited array: see [Direction Vector Walk](#direction-vector-walk).
2. **Name the states.** The same walk can spell the turn rule out per
   direction as an explicit four-state machine, easier to extend but no cheaper: see [State Machine](#state-machine).
3. **Spot the waste.** The visited array only ever answers "is this cell
   inside the region still owed to the output?", and that region is always a rectangle. Four boundary indices describe it exactly.
4. **Track the boundaries.** Keep `top`, `bottom`, `left`, `right`, peel one
   edge at a time, and shrink the boundary just crossed: `O(1)` extra space: see [Boundary Simulation](#boundary-simulation).
5. **Reframe the rings.** The same ring-peeling can be phrased recursively
   (emit the outer ring, recurse on the inner rectangle), in [Layer-by-Layer Recursive](#layer-by-layer-recursive), or destructively with list pops on a working copy, in [Edge Peeling with Pop](#edge-peeling-with-pop).

## Solutions

### Direction Vector Walk

#### Derivation

The most intuitive way to discover the answer from scratch is to literally walk the spiral the way a person would trace it by hand. Carry a current direction drawn from the ordered list `right, down, left, up`, mark each cell as visited, then peek at the next cell in the current direction. If that step would leave the grid or land on a cell already visited, rotate the direction index clockwise by one and step that way instead. After exactly `m × n` steps every cell has been emitted in spiral order.

1. Allocate a `visited` grid and start at the top-left cell facing right.
2. Emit the current cell and mark it visited.
3. Compute the next cell in the current direction; if it is out of bounds or
   already visited, advance the direction index `(direction_idx + 1) % 4` and recompute.
4. Move to the next cell and repeat for `m × n` total steps.

#### Walkthrough

Let us watch the `Direction Vector Walk` run on Example 1: `matrix = [[1,2,3],[4,5,6],[7,8,9]]`, so `m = 3` and `n = 3`. We start at `row, col = 0, 0` facing `right` (`direction_idx = 0`), with `result = []` and every cell unvisited. The loop runs `m × n = 9` times. Each step: emit `matrix[row][col]`, mark it visited, then peek at the next cell in the current direction; if that peek leaves the grid or lands on a visited cell, turn clockwise (`direction_idx = (direction_idx + 1) % 4`) and recompute before moving.

The grid, for reference:

```text
1 2 3
4 5 6
7 8 9
```

Each row below shows the state right after the cell at `(row, col)` is emitted, the direction we end up moving, and the `next` cell we step to:

| Step | Emit `(row, col)` | Value | Turned? | Direction after | Next cell | `result` so far |
|------|-------------------|-------|---------|-----------------|-----------|-----------------|
| 0 | `(0, 0)` | `1` | no | right | `(0, 1)` | `[1]` |
| 1 | `(0, 1)` | `2` | no | right | `(0, 2)` | `[1, 2]` |
| 2 | `(0, 2)` | `3` | yes (col 3 is out of bounds) | down | `(1, 2)` | `[1, 2, 3]` |
| 3 | `(1, 2)` | `6` | no | down | `(2, 2)` | `[1, 2, 3, 6]` |
| 4 | `(2, 2)` | `9` | yes (row 3 is out of bounds) | left | `(2, 1)` | `[1, 2, 3, 6, 9]` |
| 5 | `(2, 1)` | `8` | no | left | `(2, 0)` | `[1, 2, 3, 6, 9, 8]` |
| 6 | `(2, 0)` | `7` | yes (col -1 is out of bounds) | up | `(1, 0)` | `[1, 2, 3, 6, 9, 8, 7]` |
| 7 | `(1, 0)` | `4` | yes (`(0, 0)` already visited) | right | `(1, 1)` | `[1, 2, 3, 6, 9, 8, 7, 4]` |
| 8 | `(1, 1)` | `5` | yes (`(1, 2)` already visited) | down | `(2, 1)` | `[1, 2, 3, 6, 9, 8, 7, 4, 5]` |

After step 8 the loop has run all `9` times, so it stops and the computed `next` cell is never used. Notice the turns at steps 6 through 8: the walk turns at the grid walls early on, then turns because of the `visited` marks once it spirals inward (the cell `4` turns because `(0, 0)` was already taken, and `5` turns because `(1, 2)` was already taken). The returned `result` is `[1, 2, 3, 6, 9, 8, 7, 4, 5]`, which matches the expected Output for Example 1.

#### Solution

The code is the walk from the walkthrough: emit, peek, turn on a wall or a visited cell, step.

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Use direction vectors and turn when hitting boundaries or visited cells
        """
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        result = []
        visited = [[False] * n for _ in range(m)]

        # Direction vectors: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_idx = 0

        row, col = 0, 0

        for _ in range(m * n):
            result.append(matrix[row][col])
            visited[row][col] = True

            # Calculate next position
            dr, dc = directions[direction_idx]
            next_row, next_col = row + dr, col + dc

            # Check if we need to turn (hit boundary or visited cell)
            if (next_row < 0 or next_row >= m or
                next_col < 0 or next_col >= n or
                visited[next_row][next_col]):
                # Turn clockwise to next direction
                direction_idx = (direction_idx + 1) % 4
                dr, dc = directions[direction_idx]
                next_row, next_col = row + dr, col + dc

            row, col = next_row, next_col

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Each of the `m × n` cells is processed once in the main loop.

##### Space Complexity: `O(m×n)`

A full `visited` matrix is allocated to track which cells have been consumed.

#### Key Insights

- The most self-derivable starting point: simulate the walk and turn whenever you hit a wall or a cell you have already seen.
- Encoding turns as a cyclic index into a direction vector list makes the rotation logic clean and systematic.
- The pattern generalizes well to other path-finding and grid-traversal problems.
- The visited array trades `O(m×n)` extra space for trivially simple turn detection, which later approaches eliminate.

### State Machine

#### Derivation

The direction-vector walk hides the turn rule inside one generic bounds check; this variant asks what the same walk looks like with the rule spelled out per direction. Hold the direction as an explicit state (`0=right, 1=down, 2=left, 3=up`) and give each state its own branch: continue in the current direction while the adjacent cell is in bounds and unvisited, otherwise advance to the next state and step that way instead. The mechanics are identical to the previous solution; only the organization changes, which pays off when a variation needs custom behavior in one particular direction.

1. Allocate a `visited` grid and start at the top-left cell in `state = 0`
   (right).
2. Emit the current cell and mark it visited.
3. In the current state's branch, inspect the adjacent cell in that
   direction; if it is in bounds and unvisited, step there, otherwise advance `state` to the next direction and step in the new direction.
4. Repeat for `m × n` total steps.

#### Walkthrough

Let us run the state machine on Example 2: `matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]`, so `m = 3` and `n = 4`. The grid:

```text
1  2  3  4
5  6  7  8
9 10 11 12
```

Starting at `row, col = 0, 0` in `state = 0` (right), each line shows the emitted value, the state that decided the move, and the cell stepped to. A `->` marks a transition firing:

```text
emit  1   right           step to (0,1)
emit  2   right           step to (0,2)
emit  3   right           step to (0,3)
emit  4   right -> down   col 4 out of bounds, so row += 1 to (1,3)
emit  8   down            step to (2,3)
emit 12   down -> left    row 3 out of bounds, so col -= 1 to (2,2)
emit 11   left            step to (2,1)
emit 10   left            step to (2,0)
emit  9   left -> up      col -1 out of bounds, so row -= 1 to (1,0)
emit  5   up -> right     (0,0) already visited, so col += 1 to (1,1)
emit  6   right           step to (1,2)
emit  7   right -> down   (1,3) already visited; loop ends after 12 emits
```

The first three transitions fire at the grid walls; the transitions at `5` and `7` fire because the neighbor was already visited, which is how the walk spirals inward. After `m × n = 12` iterations the loop stops (the final step computed toward `(2,2)` is never used). The returned `result` is `[1,2,3,4,8,12,11,10,9,5,6,7]`, matching the expected Output for Example 2.

#### Solution

The code is one branch per state from the walkthrough.

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        State machine with explicit state transitions
        """
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        result = []
        visited = [[False] * n for _ in range(m)]

        # States: 0=right, 1=down, 2=left, 3=up
        state = 0
        row, col = 0, 0

        for _ in range(m * n):
            result.append(matrix[row][col])
            visited[row][col] = True

            # Determine next position based on current state
            if state == 0:  # Moving right
                if col + 1 < n and not visited[row][col + 1]:
                    col += 1
                else:
                    state = 1  # Switch to moving down
                    row += 1
            elif state == 1:  # Moving down
                if row + 1 < m and not visited[row + 1][col]:
                    row += 1
                else:
                    state = 2  # Switch to moving left
                    col -= 1
            elif state == 2:  # Moving left
                if col - 1 >= 0 and not visited[row][col - 1]:
                    col -= 1
                else:
                    state = 3  # Switch to moving up
                    row -= 1
            else:  # state == 3, moving up
                if row - 1 >= 0 and not visited[row - 1][col]:
                    row -= 1
                else:
                    state = 0  # Switch to moving right
                    col += 1

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

The loop runs once per cell, performing constant work each iteration.

##### Space Complexity: `O(m×n)`

A `visited` matrix is maintained to decide when each state transition should fire.

#### Key Insights

- A refinement of the direction-vector walk that unrolls the turn rule into one explicit branch per direction.
- The explicit per-state transition logic makes the approach easy to extend when a problem variation needs custom behavior at each direction.
- It still relies on the same `O(m×n)` visited array, so it does not improve on the brute force's space cost.

### Boundary Simulation

#### Derivation

Both walks above spend `O(m×n)` space on the visited array, yet all it ever answers is "is this cell inside the region still owed to the output?", and that region is always a rectangle. Once you notice the walk only ever needs to know which ring it is on, the `visited` array becomes unnecessary. Maintain four boundaries (`top`, `bottom`, `left`, `right`) that mark the current outer ring, then peel that ring off one edge at a time. The unemitted cells are always exactly the rectangle `[top, bottom] x [left, right]`, and each traversal shrinks that rectangle by one row or column. The two inner traversals are guarded because the rectangle can empty part-way through an iteration, after the `while` test has already been checked, and without the guards a degenerate single remaining row or column would be emitted twice. The Invariant below states the property formally.

1. Initialize `top`, `bottom`, `left`, `right` to the matrix edges.
2. Emit the top row left to right, then increment `top`.
3. Emit the right column top to bottom, then decrement `right`.
4. If a row remains (`top <= bottom`), emit the bottom row right to left,
   then decrement `bottom`.
5. If a column remains (`left <= right`), emit the left column bottom to
   top, then increment `left`.
6. Repeat until the boundaries cross.

#### Invariant

The four boundaries describe exactly the part of the matrix still owed to the output. At the top of every `while` iteration:

$$ \{\,\text{cells not yet in } \textit{result}\,\} \;=\; [\,\textit{top},\ \textit{bottom}\,] \times [\,\textit{left},\ \textit{right}\,] $$

```text
cells not yet in result = { matrix[row][col] : top <= row <= bottom
                                              and left <= col <= right }
                          (holds at the top of every while iteration)
```

and `result` already holds every other cell, in spiral order. Call that rectangle \(R\). Each of the four traversals emits one full edge of \(R\) and then shrinks \(R\) past that edge: the top row followed by `top += 1`, the right column followed by `right -= 1`, the bottom row followed by `bottom -= 1`, and the left column followed by `left += 1`. Emitted cells leave \(R\), and nothing ever re-enters it.

The subtlety is that \(R\) shrinks *four times* per iteration while the `while` test is evaluated only once, at the top. By the time the third traversal runs, `top` and `right` have already moved, so \(R\) may have emptied in a dimension the `while` test cleared several lines earlier. Re-checking that is exactly what the two guards do, which is why they are not redundant:

- `if top <= bottom` asks whether \(R\) still has a row. On a single-row matrix
  the first traversal consumed that row and pushed `top` past `bottom`, yet `range(right, left - 1, -1)` is still non-empty and would emit part of row `bottom`, the very row already consumed, a second time.
- `if left <= right` asks whether \(R\) still has a column. On a single-column
  matrix the second traversal consumed that column and pulled `right` below `left`, yet `range(bottom, top - 1, -1)` would emit cells of column `left` again.

At loop exit `top > bottom` or `left > right`, so \(R\) is empty: every cell has been emitted, and by the invariant each of them exactly once.

#### Walkthrough

Let us peel Example 1 by hand: `matrix = [[1,2,3],[4,5,6],[7,8,9]]`, so the boundaries start at `top = 0`, `bottom = 2`, `left = 0`, `right = 2`.

First `while` iteration (`top <= bottom` and `left <= right` both hold):

```text
top row     emit 1, 2, 3    top    0 -> 1
right col   emit 6, 9       right  2 -> 1
guard: top(1) <= bottom(2), a row remains
bottom row  emit 8, 7       bottom 2 -> 1
guard: left(0) <= right(1), a column remains
left col    emit 4          left   0 -> 1
```

Second iteration: the remaining rectangle is the single cell `[1,1] x [1,1]`:

```text
top row     emit 5          top    1 -> 2
right col   emits nothing   right  1 -> 0   (range(2, 2) is empty)
guard: top(2) > bottom(1), bottom row SKIPPED
guard: left(1) > right(0), left col SKIPPED
```

This second iteration is where the guards earn their keep: after `5` is emitted as a "top row", the rectangle is empty, and without the two checks the bottom-row and left-column traversals would re-emit cells the Invariant says are already delivered. The `while` test then fails (`top > bottom`) and the loop exits with `result = [1,2,3,6,9,8,7,4,5]`, matching the expected Output for Example 1.

#### Solution

The code is the four edge traversals from the walkthrough, each followed by its boundary shrink.

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Traverse matrix using four boundaries that shrink inward
        """
        if not matrix or not matrix[0]:
            return []

        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Traverse right along top row
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            # Traverse down along right column
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            # Traverse left along bottom row (if row still exists)
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            # Traverse up along left column (if column still exists)
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Every cell of the matrix is appended to the result exactly once.

##### Space Complexity: `O(1)`

Only four integer boundaries are tracked; no auxiliary structure beyond the required output is used.

#### Key Insights

- The refinement that drops the visited array entirely: tracking the four shrinking boundaries is all the state the spiral needs.
- The guards `if top <= bottom` and `if left <= right` cleanly handle single-row and single-column corner cases.
- This is the classic interview answer, achieving `O(1)` auxiliary space without sacrificing clarity.

### Layer-by-Layer Recursive

#### Derivation

The boundary simulation peels rings inside one loop; the same decomposition can be phrased as [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)): treat the matrix as nested rings, emit the outer ring, and hand the inner rectangle to a recursive call. Each call owns exactly one ring, so the corner bookkeeping moves into the ranges (the down, left, and up traversals skip the corners the previous edge already emitted), and the degenerate shapes become base cases instead of guards: a single remaining row or column is emitted directly, and crossed boundaries return nothing.

1. `spiral_helper(top, bottom, left, right)` returns `[]` when the
   boundaries cross.
2. When `top == bottom`, return the single remaining row; when
   `left == right`, return the single remaining column.
3. Otherwise emit the top row, then the right column from `top + 1` down,
   then the bottom row from `right - 1` back, then the left column from `bottom - 1` up to just below `top`, skipping already-emitted corners.
4. Return that ring concatenated with
   `spiral_helper(top + 1, bottom - 1, left + 1, right - 1)`.

#### Walkthrough

Let us run the recursion on Example 1: `matrix = [[1,2,3],[4,5,6],[7,8,9]]`. The outer call receives the full matrix, `spiral_helper(0, 2, 0, 2)`:

```text
spiral_helper(0, 2, 0, 2)      not degenerate: walk the outer ring
  top row     cols 0..2  ->  1, 2, 3
  right col   rows 1..2  ->  6, 9       starts at top+1, corner 3 skipped
  bottom row  cols 1..0  ->  8, 7       starts at right-1, corner 9 skipped
  left col    row  1     ->  4          rows bottom-1 down to top+1
  ring = [1, 2, 3, 6, 9, 8, 7, 4], recurse on (1, 1, 1, 1)
  spiral_helper(1, 1, 1, 1)    top == bottom: single row base case
    returns [5]
returns [1, 2, 3, 6, 9, 8, 7, 4] + [5]
```

The inner rectangle collapses to the single cell `5`, which the single-row base case returns without walking a ring (a ring walk needs distinct corners for its corner-skipping ranges to be valid, and a lone cell has none). The concatenation is `[1,2,3,6,9,8,7,4,5]`, matching the expected Output for Example 1.

#### Solution

The code is the ring walk plus the two degenerate base cases from the walkthrough.

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Recursive approach - process outer layer then recurse on inner matrix
        """
        def spiral_helper(top: int, bottom: int, left: int, right: int) -> List[int]:
            if top > bottom or left > right:
                return []

            result = []

            # Single row case
            if top == bottom:
                return [matrix[top][col] for col in range(left, right + 1)]

            # Single column case
            if left == right:
                return [matrix[row][left] for row in range(top, bottom + 1)]

            # Traverse the outer layer
            # Right
            for col in range(left, right + 1):
                result.append(matrix[top][col])

            # Down (excluding corners already processed)
            for row in range(top + 1, bottom + 1):
                result.append(matrix[row][right])

            # Left (excluding corners)
            for col in range(right - 1, left - 1, -1):
                result.append(matrix[bottom][col])

            # Up (excluding corners)
            for row in range(bottom - 1, top, -1):
                result.append(matrix[row][left])

            # Recurse on inner matrix
            return result + spiral_helper(top + 1, bottom - 1, left + 1, right - 1)

        if not matrix or not matrix[0]:
            return []

        return spiral_helper(0, len(matrix) - 1, 0, len(matrix[0]) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n)`

Each cell belongs to exactly one ring and is visited a single time across all recursive calls.

##### Space Complexity: `O(min(m,n))`

The recursion depth equals the number of rings, which is bounded by `min(m, n) / 2`.

#### Key Insights

- Elegant divide-and-conquer decomposition: peel the outer ring, then solve the smaller inner matrix.
- Explicit single-row and single-column base cases handle corner cases cleanly.
- The recursive call stack makes execution harder to trace and debug than the iterative variants.

### Edge Peeling with Pop

#### Derivation

The rings can also be peeled physically instead of tracked with indices: Python lists can surrender their edges. Pop the first row and the result gains the top edge; pop the last element of every remaining row for the right column; pop the last row reversed for the bottom edge; pop the first element of each remaining row, bottom to top, for the left column. Each pass consumes one ring and the loop runs until nothing is left. The peeling is destructive, so the method first takes a row-by-row copy: the caller's input survives while the working copy is emptied.

1. Copy the input with `matrix = [list(row) for row in matrix]`.
2. `matrix.pop(0)` removes the top row; extend `result` with it.
3. If rows remain and are non-empty, `row.pop()` on each remaining row takes
   the right column top to bottom.
4. If rows remain, `matrix.pop()[::-1]` takes the bottom row right to left.
5. If rows remain and are non-empty, `row.pop(0)` on each remaining row in
   `reversed` order takes the left column bottom to top.
6. Repeat from step 2 until the working copy is empty.

#### Walkthrough

Let us peel Example 2: `matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]`. Each line shows one pop step and the working copy left behind:

```text
pop first row              emit 1, 2, 3, 4   copy = [[5,6,7,8], [9,10,11,12]]
pop last of each row       emit 8, 12        copy = [[5,6,7], [9,10,11]]
pop last row, reversed     emit 11, 10, 9    copy = [[5,6,7]]
pop first of each row      emit 5            copy = [[6,7]]
(in reversed row order)
pop first row              emit 6, 7         copy = []      loop ends
```

The first four steps consume the outer ring; what remains (`[[6,7]]`) is the inner ring, which the second `while` pass takes as a "first row" and empties. The guards `if matrix` and `if matrix and matrix[0]` are what stop a leftover single row or column from being processed by edge steps that no longer apply. The result is `[1,2,3,4,8,12,11,10,9,5,6,7]`, matching the expected Output for Example 2.

#### Solution

The code is the pop sequence from the walkthrough, applied to a protective copy.

```python
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Peel the outer edges off a working copy with list pops
        """
        if not matrix or not matrix[0]:
            return []

        # The peeling consumes rows and elements destructively, so work on a
        # copy and leave the caller's matrix intact.
        matrix = [list(row) for row in matrix]

        result = []

        while matrix:
            # Take the first row
            result.extend(matrix.pop(0))

            if matrix and matrix[0]:
                # Take the last element of each remaining row (right column)
                for row in matrix:
                    result.append(row.pop())

            if matrix:
                # Take the last row in reverse (bottom row, right to left)
                result.extend(matrix.pop()[::-1])

            if matrix and matrix[0]:
                # Take the first element of each remaining row in reverse order (left column, bottom to top)
                for row in reversed(matrix):
                    result.append(row.pop(0))

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m×n×min(m,n))`

Every element is appended once, but the front pops do hidden shifting work: `matrix.pop(0)` shifts every remaining row reference, and `row.pop(0)` shifts every remaining element of its row. Peeling one ring therefore costs up to `O(m × n)` in shifts, and with `O(min(m, n))` rings the total is `O(m × n × min(m, n))` rather than linear in the cell count.

##### Space Complexity: `O(m×n)`

The working copy duplicates the entire matrix. That copy is what keeps the approach non-destructive: without it, the peeling would empty the caller's matrix.

#### Key Insights

- Compact, pattern-based code that showcases Python list manipulation (`pop`, slicing, `reversed`).
- The peeling is inherently destructive, which is why the code takes a copy up front; peeling the input directly would leave the caller with an emptied matrix.
- The front pops (`matrix.pop(0)`, `row.pop(0)`) shift everything behind them, which is the hidden cost that breaks the `O(m×n)` time bound the other approaches share.
- The pop-based flow is less intuitive to read than explicit boundary tracking.

## Comparison of Solutions

### Time Complexity

- **Direction Vector Walk**: `O(m×n)` - one step per cell with constant-time turn checks.
- **State Machine**: `O(m×n)` - one loop iteration per cell.
- **Boundary Simulation**: `O(m×n)` - each cell is appended once as the boundaries shrink.
- **Layer-by-Layer Recursive**: `O(m×n)` - each cell belongs to exactly one ring.
- **Edge Peeling with Pop**: `O(m×n×min(m,n))` - the front pops shift rows and row elements on every ring.

### Space Complexity

- **Direction Vector Walk**: `O(m×n)` - a full visited matrix is allocated.
- **State Machine**: `O(m×n)` - a visited matrix drives the transitions.
- **Boundary Simulation**: `O(1)` - only four integer boundaries are tracked.
- **Layer-by-Layer Recursive**: `O(min(m,n))` - recursion depth equals the number of rings.
- **Edge Peeling with Pop**: `O(m×n)` - a working copy of the matrix is peeled so the input is preserved.

### Trade-offs

- **Direction Vector Walk** is the most self-derivable solution, simulating the walk and turning at walls or visited cells, paying for that simplicity with `O(m×n)` visited-array space.
- **State Machine** restates the same walk with explicit per-state transitions, which is easy to extend but more verbose and uses the same visited array.
- **Boundary Simulation** drops the visited array for `O(1)` space by tracking four shrinking boundaries, at the cost of careful single-row/column guard handling.
- **Layer-by-Layer Recursive** offers elegant divide-and-conquer decomposition with clean base cases, but spends `O(min(m,n))` stack space and is harder to trace when debugging.
- **Edge Peeling with Pop** is creative and compact, but the front pops add a `min(m,n)` factor to the time, the protective copy costs `O(m×n)` space, and the flow reads less intuitively.

### When to Use Each

- **Direction Vector Walk**: The intuitive starting point, and natural when the spiral is part of a broader grid/path-finding problem where direction vectors generalize.
- **State Machine**: When the traversal needs custom per-direction behavior or future state-specific extensions.
- **Boundary Simulation**: The recommended default for interviews and production: `O(1)` space, no visited array, and widely expected.
- **Layer-by-Layer Recursive**: When a divide-and-conquer framing or layer-wise reasoning is clearer for the audience.
- **Edge Peeling with Pop**: When code brevity is prized and the extra copy plus shifting cost are acceptable, which the small `1 <= m, n <= 10` constraint makes true here.

### Optimization Notes

- **Direction Vector Walk**: `O(m×n)` time, `O(m×n)` space, does not modify the input; its key advantage is being the most intuitive walk-and-turn simulation.
- **State Machine**: `O(m×n)` time, `O(m×n)` space, does not modify the input; its key advantage is explicit, extensible state management.
- **Boundary Simulation**: `O(m×n)` time, `O(1)` space, does not modify the input; its key advantage is eliminating the visited array entirely.
- **Layer-by-Layer Recursive**: `O(m×n)` time, `O(min(m,n))` space, does not modify the input; its key advantage is an elegant divide-and-conquer decomposition.
- **Edge Peeling with Pop**: `O(m×n×min(m,n))` time, `O(m×n)` space for the working copy it peels in place of the input; its key advantage is creative, compact pattern-based code.
- The first four solutions share the same `O(m×n)` time bound and differ in space usage; Edge Peeling with Pop pays an extra `min(m,n)` factor for its front pops.
- The ladder runs from the visited-array walk (Direction Vector Walk and State Machine) to boundary tracking (Boundary Simulation), which drops the `O(m×n)` visited array for `O(1)` space.
- Single-row and single-column matrices are the recurring corner case; boundary-based approaches need explicit guards to avoid double-counting them.
- Boundary Simulation is the most commonly expected interview answer and demonstrates clear algorithmic thinking.
- The spiral/layer-wise traversal pattern recurs across many matrix problems, so understanding multiple approaches builds a strong, generalizable foundation.
