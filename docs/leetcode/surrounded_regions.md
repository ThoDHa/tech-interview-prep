# [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

**Medium** | **25 minutes** | **Array, Depth-First Search, Breadth-First Search, Union Find, Matrix**

**Pattern:** [Multi-Source BFS](../patterns/grid_bfs_multi_source/intuition.md), [Graph Traversal](../patterns/graph/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Flood fill](https://en.wikipedia.org/wiki/Flood_fill)

**Practice:** [`practice/surrounded_regions/solution.py`](../../practice/surrounded_regions/solution.py)

You are given an `m x n` matrix `board` containing letters `'X'` and `'O'`, capture regions that are surrounded:

* **Connect:** A cell is connected to adjacent cells horizontally or vertically.

* **Region:** To form a region connect every `'O'` cell. Regions can have any shape; they do not need to be squares or rectangles.

* **Surround:** A region is surrounded if none of the `'O'` cells in that region are on the edge of the board. Such regions are **completely enclosed** by `'X'` cells.

To capture a **surrounded region**, replace all `'O'`s with `'X'`s **in-place** within the original board. You do not need to return anything.

## Examples

### Example 1

**Input:**

```text
board = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"]
]
```

**Output:**

```text
[
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","O","X","X"]
]
```

**Explanation:** The bottom `'O'` region is not captured because it touches the edge of the board, so it cannot be surrounded.

### Example 2

**Input:** `board = [["X"]]`

**Output:** `[["X"]]`

## Constraints

- `1 <= board.length, board[i].length <= 200`
- `board[i][j]` is `'X'` or `'O'`.

## Deriving the Solution

Deciding whether one `'O'` region is surrounded means asking whether it can walk to the board's edge, which is a flood-fill reachability question. Reading the definition again reframes the whole problem: a region is captured exactly when it is *not* connected to any border `'O'`, so the safe regions are precisely those touching the border, and everything else dies. Every solution below finds the border-connected `'O'` cells first and captures the rest; they differ in where the search starts and how the intermediate state is carried.

1. **Start literal.** For each `'O'` region, flood-fill it and check whether
   it touched the border; capture the ones that did not: see
   [Per-Region Flood Fill](#per-region-flood-fill).
2. **Invert the search.** Instead of testing every region, seed the flood
   from the border `'O'` cells only: whatever the flood reaches is safe,
   whatever it never reaches is captured. A sentinel mark carries the
   "safe" state through one extra sweep: see
   [Border DFS + Capture](#border-dfs-capture).

## Solutions

### Per-Region Flood Fill

#### Derivation

The most literal reading walks the board, finds each unvisited `'O'` cell, flood-fills its whole region, and asks during the fill whether the region touched the border. If it did, the region survives; if not, the region is captured by rewriting its cells to `'X'`:

1. Keep a `visited` set; scan every cell.
2. On an unvisited `'O'`, run a flood fill collecting the region's cells
   and a flag recording any border contact.
3. After the fill: write `X` over every collected cell when the flag is
   clear; otherwise leave the region alone and record its cells visited.
4. Continue the scan.

#### Walkthrough

Trace the scan on Example 1: the first unvisited `'O'` is `(1,1)`, whose region fills to `(1,1)`, `(1,2)`, `(2,2)` with no border contact; the second is `(3,1)`, which sits in the last row:

```text
region A  fill from (1,1)  collects {(1,1), (1,2), (2,2)}   border? no
          -> capture: all three cells become 'X'
region B  fill from (3,1)  collects {(3,1)}                 border? row 3 = last row, yes
          -> safe: leave as 'O'
```

Capturing region A and sparing region B yields the expected output: only the bottom `'O'` remains. The explanation matches: the bottom region is not captured because it touches the edge.

#### Solution

The code is the scan, the full-region fill, and the conditional rewrite.

```python
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board:
            return
        rows, columns = len(board), len(board[0])
        visited = set()

        def fill(row: int, column: int, region: list) -> None:
            if not (0 <= row < rows and 0 <= column < columns):
                return
            if (row, column) in visited or board[row][column] != "O":
                return
            visited.add((row, column))
            region.append((row, column))
            fill(row + 1, column, region)
            fill(row - 1, column, region)
            fill(row, column + 1, region)
            fill(row, column - 1, region)

        for row in range(rows):
            for column in range(columns):
                if board[row][column] == "O" and (row, column) not in visited:
                    region = []
                    fill(row, column, region)
                    touches_border = any(
                        r in (0, rows - 1) or c in (0, columns - 1)
                        for r, c in region
                    )
                    if not touches_border:
                        for r, c in region:
                            board[r][c] = "X"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * columns)`

Every cell enters exactly one region's fill (or none), and the scan plus rewrites are linear.

##### Space Complexity: `O(rows * columns)`

The `visited` set, the recursion, and one region's cell list.

#### Key Insights

- The fill must finish before any capture decision: a region cannot be
  rewritten cell by cell while it is being explored, because border
  contact might still be found later in the fill.
- Correct but bookkeeping-heavy: the region list and the flag exist only
  to defer the decision the border-first versions never need to make.

### Border DFS + Capture

#### Derivation

The per-region version pays for a deferred decision per region. Flip it: instead of finding each region and testing border contact, start from the border and find every region that could never be captured. A flood from the border `'O'` cells marks exactly the safe cells; everything still reading `'O'` afterward is interior by construction and can be captured in one sweep. The temporary state rides in the board itself: a `'B'` sentinel marks the border-connected cells so the sweep can restore them:

1. Run `mark_safe` from every border cell; it writes `'B'` over each
   border-connected `'O'` it reaches.
2. Sweep the board: `'O'` (never reached by the flood) becomes `'X'`;
   `'B'` (safe) is restored to `'O'`.
3. `'X'` cells pass through untouched.

The board needs no copy: the mark pass never destroys information (`O -> B` is reversible, and the sweep resolves every cell to a final value).

#### Walkthrough

Trace Example 1: the border `'O'` scan seeds only `(3,1)` (the other border cells are all `'X'`), and its flood dies immediately at the surrounding `'X'`s:

```text
mark_safe(3,1)  'O' -> 'B'   neighbors: (2,1)='X', (4,1) off, (3,0)='X', (3,2)='X'
board now       [["X","X","X","X"], ["X","O","O","X"], ["X","X","O","X"], ["X","B","X","X"]]

sweep  (1,1) 'O' -> 'X'   (1,2) 'O' -> 'X'   (2,2) 'O' -> 'X'   (3,1) 'B' -> 'O'
```

The final board is all `'X'` except the restored `'O'` at `(3,1)`, matching Example 1's expected output. Example 2 (`board = [["X"]]`) never seeds a flood and its sweep flips nothing.

#### Solution

The code is the border-seeded mark pass and the two-way sweep.

```python
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board:
            return
        rows, columns = len(board), len(board[0])

        def mark_safe(row: int, column: int) -> None:
            if not (0 <= row < rows and 0 <= column < columns):
                return
            if board[row][column] != "O":
                return
            board[row][column] = "B"
            mark_safe(row + 1, column)
            mark_safe(row - 1, column)
            mark_safe(row, column + 1)
            mark_safe(row, column - 1)

        for row in range(rows):
            mark_safe(row, 0)
            mark_safe(row, columns - 1)
        for column in range(columns):
            mark_safe(0, column)
            mark_safe(rows - 1, column)

        for row in range(rows):
            for column in range(columns):
                if board[row][column] == "O":
                    board[row][column] = "X"
                elif board[row][column] == "B":
                    board[row][column] = "O"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * columns)`

The mark pass visits each cell at most once (the `'O'`-only guard rejects re-entry), and the sweep is one pass.

##### Space Complexity: `O(rows * columns)`

The DFS recursion depth; an `'O'`-filled board drives it to the full grid.

#### Key Insights

- "Surrounded" is a negative-space property: searching from the border
  finds the uncapturable cells directly, so no per-region test remains.
- The `'B'` sentinel carries two rounds of information through the board
  itself: border-connected `'O'` cells are distinguishable from both
  capturable `'O'` and wall `'X'` in the sweep.
- Seeding the flood from all border cells at once is the same multi-source
  idea as [Walls And Gates](walls_and_gates.md), applied to reachability
  instead of distance.

## Comparison of Solutions

### Time Complexity

- **Per-Region Flood Fill**: `O(rows * columns)` - one fill per region, each cell once.
- **Border DFS + Capture**: `O(rows * columns)` - one flood from the border, one sweep.

### Space Complexity

- **Per-Region Flood Fill**: `O(rows * columns)` - `visited` set, region lists, recursion.
- **Border DFS + Capture**: `O(rows * columns)` - recursion only; the board holds the state.

### Trade-offs

- The per-region fill defers each capture until its region is fully
  explored, needing a region buffer and a border flag per region.
- The border version decides nothing per region: the flood marks safe
  cells, and one unconditional sweep finishes. No auxiliary container
  beyond the call stack.

### When to Use Each

- **Per-Region Flood Fill**: when a rule other than border contact decides
  capture (anything the flood can test), the collect-then-decide shape
  generalizes.
- **Border DFS + Capture**: the intended solution for this problem and
  the pattern to reach for whenever "surrounded by" means "cannot reach
  the boundary" (recommended here).

### Optimization Notes

- An explicit stack or BFS queue in `mark_safe` removes the recursion
  depth limit for huge boards, at identical bounds.
- The two-way sweep handles the `'B'` restoration in the same pass as the
  capture; splitting it into two sweeps only re-touches cells.
- Non-rectangular or ragged inputs need the bounds check kept per
  neighbor; the `rows`/`columns` precompute assumes a rectangular grid,
  which the constraints guarantee.
