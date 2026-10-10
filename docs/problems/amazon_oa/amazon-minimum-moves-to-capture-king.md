# [Minimum Moves to Capture the King](https://www.fastprep.io/problems/amazon-minimum-moves-to-capture-king)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Matrix**

A piece starts at start on an empty rows-by-cols board and must capture the king at king.

## Examples

### Example 1

**Input:** `rows = 8`, `cols = 8`, `start = [0,0]`, `king = [7,7]`, `directions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]`

**Output:** `7`

**Explanation:** Seven diagonal moves reach the opposite corner.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-minimum-moves-to-capture-king; fill them in. -->

## Solutions

### List-Frontier BFS

#### Derivation

The most literal simulation expands the search ring by ring with the plainest containers the language offers: a list `frontier` of `(row, col, moves)` triples, popped from the head with `frontier.pop(0)`, and a list `seen` of cells already enqueued, tested with `not in`. The ring order is the algorithm; the lists are simply what a first draft reaches for:

1. Guard the trivial case: if `start` already equals `king`, return `0`.
2. Seed `frontier` with `(start_row, start_col, 0)` and `seen` with the start
   cell.
3. Pop the head `(row, col, moves)`; for every `(step_row, step_col)` in
   `directions`, when the neighbor `(next_row, next_col)` is on the board and
   not in `seen`: return `moves + 1` if it is the king's cell, otherwise
   append it to `seen` and `(next_row, next_col, moves + 1)` to `frontier`.
4. Return `-1` when the frontier drains, which happens only when no direction
   set can reach the king.

Nothing explodes: the `seen` guard gives every cell one enqueue, so the sweep touches each cell at most once and always terminates. What is wrong is the price of each operation. `frontier.pop(0)` shifts every remaining entry one slot toward the head, and every `not in seen` test walks the list end to end; both costs are bookkeeping rather than search, and together they square the cell count.

#### Walkthrough

Let us run the ring-by-ring sweep on Example 1: `rows = 8`, `cols = 8`, `start = [0,0]`, `king = [7,7]`, all eight directions. Cells fill in square rings around the corner, and the ring radius is the move count:

```text
frontier = [(0, 0, 0)]                 seen = [(0, 0)]
pop (0, 0, 0)   discover (0, 1), (1, 0), (1, 1)     frontier holds 3, seen holds 4
pop (0, 1, 1)   (0, 2), (1, 2) new; (1, 1) already in seen: skipped
pop (1, 0, 1)   (2, 0), (2, 1) new; earlier cells in seen: skipped
pop (1, 1, 1)   (2, 2) new
...             ring k fills the cells with max(row, col) = k at moves = k
pop (6, 6, 6)   neighbor (7, 7) is the king: return 6 + 1
-> 7
```

Every pop is the frontier's head removal, and every "already in seen" verdict is a linear scan of the list as it stands at that moment. The rings reach the cells with `max(row, col) = k` at `moves = k`; `(6, 6)` pops at `moves = 6`, its neighbor `(7, 7)` is the king, and the function returns `6 + 1 = 7`, matching the expected Output. The ring order is identical to the next solution's; what differs is what each head removal and each membership test costs.

#### Solution

The code is the walkthrough's pop-and-expand loop with plain lists carrying the bookkeeping.

```python
from typing import List, Tuple


class Solution:
    def solve(
        self,
        rows: int,
        cols: int,
        start: List[int],
        king: List[int],
        directions: List[List[int]],
    ) -> int:
        start_cell = (start[0], start[1])
        king_cell = (king[0], king[1])
        if start_cell == king_cell:
            return 0
        seen: List[Tuple[int, int]] = [start_cell]
        frontier = [(start_cell[0], start_cell[1], 0)]
        while frontier:
            row, col, moves = frontier.pop(0)
            for step_row, step_col in directions:
                next_row, next_col = row + step_row, col + step_col
                if (
                    0 <= next_row < rows
                    and 0 <= next_col < cols
                    and (next_row, next_col) not in seen
                ):
                    if (next_row, next_col) == king_cell:
                        return moves + 1
                    seen.append((next_row, next_col))
                    frontier.append((next_row, next_col, moves + 1))
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V² × len(directions))`

With `V = rows × cols` cells: each of the `V` cells pops once and tries every direction, but each `pop(0)` shifts up to `V` entries and each `not in seen` test scans up to `V` entries, so the bookkeeping squares the linear sweep.

##### Space Complexity: `O(V)`

The `seen` list and the frontier hold at most one entry per cell.

#### Key Insights

- The ring order is already the optimal algorithm: each cell is enqueued once
  and rings expand strictly in move order, so the answer is correct and the
  search always terminates.
- `frontier.pop(0)` is the classic list-queue pitfall: removing the head
  shifts every remaining entry one slot left, `O(V)` per pop.
- `(next_row, next_col) not in seen` walks the list; marking at enqueue time
  keeps `seen` to one entry per cell, but the scan itself still costs up to
  `O(V)` per test, which is what the set swap removes.

### Breadth-First Search

#### Derivation

The List-Frontier BFS is the right algorithm carrying the wrong containers: `frontier.pop(0)` shifts every remaining entry one slot toward the head, and every `not in seen` test scans the whole list, so the sweep's costs are bookkeeping rather than search. [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) bookkeeping repairs exactly that while the algorithm stays untouched: a `deque` removes from the head in constant time and a `set` tests membership in constant time, and the ring order survives verbatim: explore the board in rings around the start, every cell at `moves` steps before any cell at `moves + 1`, so the first arrival at any cell is necessarily by a shortest route. The king's cell never even needs to be enqueued; the first discovery carries the answer:

1. Guard the trivial case: if `start` already equals `king`, return `0`.
2. Seed the queue with `(start_row, start_col, 0)` and mark the start cell
   in `visited`.
3. Pop `(row, col, moves)`; for every `(step_row, step_col)` in
   `directions`, when the neighbor `(next_row, next_col)` is on the board
   and unvisited: return `moves + 1` if it is the king's cell, otherwise
   mark it visited and enqueue `(next_row, next_col, moves + 1)`.
4. Return `-1` if the queue empties, which happens only when no direction
   set can reach the king.

#### Walkthrough

Let us run the ring-by-ring sweep on Example 1: `rows = 8`, `cols = 8`, `start = [0,0]`, `king = [7,7]`, all eight directions. Cells fill in square rings around the corner, and the ring radius is the move count:

```text
moves = 0   ring holds 1 cell:     (0, 0)
moves = 1   ring holds 3 cells:    (0, 1), (1, 0), (1, 1)
moves = 2   ring holds 5 cells:    (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)
moves = 3   ring holds 7 cells:    ... through (3, 3)
moves = 4   ring holds 9 cells:    ... through (4, 4)
moves = 5   ring holds 11 cells:   ... through (5, 5)
moves = 6   ring holds 13 cells:   ... through (6, 6)
moves = 7   ring reaches (7, 7):   first pop of the king's cell
-> 7
```

Every cell at `moves = k` sits exactly `k` steps from the corner, because BFS pops rings in order and each cell is enqueued by its first discoverer only. The diagonal `(k, k)` cells are discovered at `moves = k`, so `(6, 6)` pops at `moves = 6` and its neighbor, the king at `(7, 7)`, returns `6 + 1 = 7`, matching the expected Output. The `visited` set is what keeps the count linear: the king's cell is discovered exactly once, by `(6, 6)`, its only ring-6 neighbor; its other on-board neighbors `(6, 7)` and `(7, 6)` sit on ring 7 and arrive later.

#### Solution

The code is the walkthrough's pop-and-expand loop with the early return on the king's cell.

```python
from collections import deque
from typing import List, Set, Tuple


class Solution:
    def solve(
        self,
        rows: int,
        cols: int,
        start: List[int],
        king: List[int],
        directions: List[List[int]],
    ) -> int:
        start_cell = (start[0], start[1])
        king_cell = (king[0], king[1])
        if start_cell == king_cell:
            return 0
        visited: Set[Tuple[int, int]] = {start_cell}
        queue = deque([(start_cell[0], start_cell[1], 0)])
        while queue:
            row, col, moves = queue.popleft()
            for step_row, step_col in directions:
                next_row, next_col = row + step_row, col + step_col
                if (
                    0 <= next_row < rows
                    and 0 <= next_col < cols
                    and (next_row, next_col) not in visited
                ):
                    if (next_row, next_col) == king_cell:
                        return moves + 1
                    visited.add((next_row, next_col))
                    queue.append((next_row, next_col, moves + 1))
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols × len(directions))`

Every cell is enqueued at most once and popped once, and each pop tries every direction once: linear in the board times the direction count.

##### Space Complexity: `O(rows × cols)`

The `visited` set and the queue each hold at most one entry per cell.

#### Key Insights

- Marking cells `visited` at enqueue time, not at pop time, is what bounds
  the queue: a cell discovered by two ring-`k` cells is enqueued once, by
  whichever saw it first.
- The first time the king's cell is discovered, the discoverer's `moves + 1`
  is the shortest distance, because BFS rings expand strictly in move order.
- Returning `-1` on queue exhaustion handles direction sets that cannot
  reach the king (for example, orthogonal-only directions on a diagonal
  target), keeping the function total.

## Comparison of Solutions

### Time Complexity

- **List-Frontier BFS**: `O(V² × len(directions))` - the ring sweep touches each of the `V = rows × cols` cells once, but every `pop(0)` shifts and every membership test scans up to `V` entries.
- **Breadth-First Search**: `O(rows × cols × len(directions))` - the same sweep with constant-time head removal and membership tests.

### Space Complexity

- **List-Frontier BFS**: `O(V)` - the `seen` list and frontier, one entry per cell at most.
- **Breadth-First Search**: `O(rows × cols)` - the `visited` set and queue, one entry per cell at most.

### Trade-offs

- The List-Frontier BFS shows the algorithm with nothing hidden: no imports beyond typing, and the queue and membership mechanics visible in the code, but its head removals and scans pay `V` per operation on large boards.
- The Breadth-First Search is linear in the board and settles every cell's shortest distance in one sweep, but it assumes every move costs exactly `1`, which is precisely the structure the ring order exploits; when costs vary, both give way to Dijkstra-style search.

### When to Use Each

- **List-Frontier BFS**: as the first draft to write and the teaching reference; the right call only when the board is small enough that the quadratic bookkeeping is irrelevant (or in a language where a list dequeues cheaply).
- **Breadth-First Search** (recommended): the default for any uniform-cost shortest-path question on a grid; linear, simple, and it reports every cell's distance, not just the king's.

### Optimization Notes

- The step from the first solution to the second changes containers, not algorithms: `deque` over `list.pop(0)` and `set` over `list` membership turn a `V`-per-operation bookkeeping cost into constant time, which is the whole speedup.
- Testing the king's cell at discovery time (when about to enqueue) rather than at pop time returns one ring-iteration earlier and skips enqueuing the goal; both variants are correct because BFS reaches cells in nondecreasing move order.
- The start-equals-king guard keeps the early-discovery return honest: without it, a start on the king would be skipped as already seen and the frontier would drain to `-1`.
- Marking `visited` at enqueue time instead of pop time caps the queue at one entry per cell; the pop-time variant can hold a cell once per discovering neighbor.
- If a follow-up adds blocked cells, the same loop gains one membership test against the blocker set; the complexity picks up only the blocker count.
