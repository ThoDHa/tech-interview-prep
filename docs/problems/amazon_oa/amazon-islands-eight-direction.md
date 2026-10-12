# [Count Islands with Eight-Direction Adjacency](https://www.fastprep.io/problems/amazon-islands-eight-direction)

**Medium** | **NN minutes** | **Array, Matrix, Depth First Search, Breadth First Search**

Given a rectangular binary matrix grid, return the number of islands.

An island is a maximal group of cells containing 1. Two land cells belong to the same island when they share an edge or a corner, so each cell can connect in any of the eight horizontal, vertical, or diagonal directions.

## Examples

### Example 1

**Input:** `grid = [[1,0,1],[0,1,0],[1,0,1]]`

**Output:** `1`

**Explanation:** Every land cell connects to the center diagonally, so all five cells form one island.

### Example 2

**Input:** `grid = [[1,1,0],[0,0,0],[0,1,1]]`

**Output:** `2`

**Explanation:** The upper-left and lower-right land groups do not touch, even at a corner.

### Example 3

**Input:** `grid = [[0,0],[0,0]]`

**Output:** `0`

**Explanation:** There are no land cells.

## Constraints

- `1 <= grid.length, grid[i].length <= 500.`
- `Every row has the same length.`
- `grid[i][j] is either 0 or 1.`
- `The matrix contains at most 100000 cells.`

## Solutions

### DFS with Grid Modification

#### Derivation

The question to ask first is the literal one: how many times does a scan of the grid step onto land that belongs to no island counted so far? Each such cell is the seed of exactly one new island, so the problem reduces to two duties: detect a fresh land cell, then mark the rest of its island as seen before the scan continues. This is the classic islands problem with one changed rule: each cell connects in all eight directions, so the flood fill recurses into eight neighbors instead of four. [DFS](https://en.wikipedia.org/wiki/Depth-first_search) naturally explores an entire connected component before returning, and sinking every visited cell to `0` turns the grid itself into the visited marker (this grid arrives as integer lists, so no copy is needed before sinking):

1. Scan every cell with a double loop over `rows` and `cols`.
2. When `grid[row][col] == 1`, a new island starts: increment `islands` and
   call `dfs(row, col)`.
3. `dfs` returns immediately when the cell is out of bounds or `0`; otherwise
   it sinks the cell (`grid[row][col] = 0`) and recurses into all eight
   neighbors from `EIGHT_DIRECTIONS` (right, down-right, down, down-left,
   left, up-left, up, up-right).
4. After the scan completes, return `islands`.

#### Walkthrough

Example 1 is the five-cell X-shaped grid whose cells all connect diagonally through the center, a compact grid but already the full eight-direction story, so it is traced directly. The scan reaches `(0, 0)`, finds `1`, sets `islands = 1`, and calls `dfs(0, 0)`. Neighbors are checked in the order right, down-right, down, down-left, left, up-left, up, up-right; the trace compresses each immediate `return` onto its caller's line:

```text
dfs(0,0): 1 -> sink, explore 8 neighbors
  dfs(0,1): 0 -> return
  dfs(1,1): 1 -> sink, explore
    dfs(1,2): 0 -> return
    dfs(2,2): 1 -> sink, all neighbors out/water/sunk -> return
    dfs(2,1): 0 -> return
    dfs(2,0): 1 -> sink, all neighbors out/water/sunk -> return
    dfs(1,0): 0 -> return
    dfs(0,0): sunk -> return
    dfs(0,1): 0 -> return
    dfs(0,2): 1 -> sink, all neighbors out/water/sunk -> return
  dfs(1,0): 0 -> return
  down-left (1,-1), left (0,-1), up-left (-1,-1), up (-1,0), up-right (-1,1): out -> return
```

The single call sank all five land cells: `(0,0)` first, then `(1,1)`, which reached `(2,2)` and `(2,0)` down its diagonals and `(0,2)` up its up-right diagonal. When the scan resumes, every cell is `0` and no second island starts, so the function returns `islands = 1`, matching the expected Output. Under the four-direction rule of the classic problem the same grid yields three islands; the diagonal rule is the whole difference. For Example 3 the scan finds no `1` at all and returns `0`.

#### Solution

The code is the walkthrough's scan and flood fill with the eight-direction list:

```python
from typing import List

EIGHT_DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1),
                    (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        """Return the number of islands under eight-direction adjacency.

        Time:  O(rows × cols): every cell is visited at most once across the
            main loop and the flood fill.
        Space: O(rows × cols) for the recursion stack in the worst case of a
            snake-shaped island through every cell.
        """
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def dfs(row: int, col: int) -> None:
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                    grid[row][col] == 0):
                return

            grid[row][col] = 0

            for dr, dc in EIGHT_DIRECTIONS:
                dfs(row + dr, col + dc)

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    islands += 1
                    dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Every cell is visited at most once across the main loop and the flood fill; the eight-neighbor fan-out is a constant factor per cell.

##### Space Complexity: `O(rows × cols)`

The recursion stack can hold all cells of a snake-shaped island threading the whole grid.

#### Key Insights

- The eight-direction change is one line of data: the neighbor list grows from four offsets to eight, and everything else about the flood fill is unchanged.
- Diagonal adjacency merges grids the four-direction rule keeps separate: Example 1's X-shape is three islands with four directions and one with eight.
- Sinking visited land to `0` doubles as the visited marker, and the integer matrix (unlike string rows) can be modified in place with no copy.

### BFS with Grid Modification

#### Derivation

The recursive fill has one weakness: its memory is the call stack. The grid can hold `100000` cells, so a snake-shaped island threading the whole grid could recurse tens of thousands of frames deep, past the interpreter's recursion limit. The repair is to change the exploration order: instead of following one path as deep as it goes, expand the island as a widening frontier with a [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) queue. The neighborhood grows to eight directions; the queue discipline does not:

1. The main scan is unchanged: every unvisited `1` increments `islands` and
   starts a fill, now `bfs(row, col)`.
2. `bfs` seeds a `queue` with `(start_row, start_col)` and sinks that cell to
   `0` immediately.
3. While the queue is non-empty, `popleft` a cell and inspect its eight
   neighbors; every in-bounds neighbor still holding `1` is sunk and appended.
4. Sinking at enqueue time (not at dequeue time) guarantees no cell enters the
   queue twice.

#### Walkthrough

Example 2, `grid = [[1,1,0],[0,0,0],[0,1,1]]`, shows both islands. The scan reaches `(0, 0)`, sets `islands = 1`, and starts `bfs(0, 0)`, which sinks the seed and enqueues it. Each line is one queue event; the eight neighbors are checked in walkthrough order and only land survivors are listed:

```text
seed (0,0)   sink, queue = [(0,0)]
pop (0,0)    right (0,1)='1' -> sink+enqueue      queue = [(0,1)]
             down (1,1) water; down-right (1,2) water; all others sunk/out
pop (0,1)    all eight neighbors water, sunk, or out of bounds
             queue = []  -> bfs returns, island one = {(0,0), (0,1)}
```

The scan continues across the empty middle row and reaches `(2, 1)`: `islands = 2`, and `bfs(2, 1)` sinks `(2, 1)` and its right neighbor `(2, 2)` the same way, giving island two. The two islands never touch, even diagonally: the down-diagonal cells `(1, 1)` and `(1, 2)` beneath the island pair are water, so nothing bridges the gap, which is exactly what Example 2's Explanation asserts, and the function returns `2`. The decisive eight-direction beat sits in that check: had `(1, 1)` held `1`, it would be diagonally adjacent to both `(0, 0)` and `(0, 1)` and the count would collapse to one island.

#### Solution

The code is the queue discipline from the walkthrough: sink at enqueue time, expand at dequeue time, eight neighbors per cell:

```python
from collections import deque
from typing import List

EIGHT_DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1),
                    (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        """Return the number of islands under eight-direction adjacency.

        Time:  O(rows × cols): every cell is enqueued at most once.
        Space: O(rows × cols) for the queue's worst-case wavefront.
        """
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def bfs(start_row: int, start_col: int) -> None:
            queue = deque([(start_row, start_col)])
            grid[start_row][start_col] = 0

            while queue:
                row, col = queue.popleft()
                for dr, dc in EIGHT_DIRECTIONS:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                            grid[new_row][new_col] == 1):
                        grid[new_row][new_col] = 0
                        queue.append((new_row, new_col))

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    islands += 1
                    bfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Every cell is enqueued at most once and each dequeue inspects a constant eight neighbors.

##### Space Complexity: `O(rows × cols)`

Sinking at enqueue time caps the queue at the active wavefront, `O(min(rows, cols))` on a diagonal island, plus at most a constant number of guard-rejected duplicates per wavefront cell; the bound is quoted against the cell count because adversarial shapes can push the wavefront toward a full grid row.

#### Key Insights

- BFS removes the recursion-depth hazard the DFS variants inherit; on a `100000`-cell grid the interpreter's default recursion limit is a real risk.
- Sinking at enqueue time (not dequeue time) is what guarantees each cell enters the queue at most once, even with eight directions feeding the frontier.
- With eight directions the wavefront on a diagonal island spans `min(rows, cols)` cells, wider than the four-direction frontier bound but still far below the cell count in practice.

### Iterative DFS with Stack

#### Derivation

The BFS queue fixed the recursion depth by holding the to-do list explicitly. The same fix works without changing the exploration order: the call stack contributes nothing but that to-do list, so DFS only needs *some* stack, not the interpreter's. Replace it with an explicit list used as a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) and the depth-first fill survives, recursion-free, still over eight directions:

1. `iterative_dfs` seeds `stack` with the starting cell.
2. Loop while the stack is non-empty: `pop` a cell, and skip it when it is out
   of bounds or `0` (water or already sunk).
3. Otherwise sink it and push all eight neighbors unconditionally; invalid
   ones are filtered when they are popped.
4. The main scan is unchanged: each unvisited `1` increments `islands` and
   runs one fill.

#### Walkthrough

Example 2's first island again, now by stack. The scan finds `(0, 0)`, sets `islands = 1`, and starts the fill. Each line is one pop; pushes go right, down-right, down, down-left, left, up-left, up, up-right, so the last-pushed neighbor pops first:

```text
seed (0,0)    stack = [(0,0)]
pop (0,0)     '1' -> sink, push 8 neighbors
pop (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)   out of bounds -> skip
pop (1,0), (1,1)   water -> skip
pop (0,1)     '1' -> sink, push 8 neighbors
pop (-1,2), (-1,1), (-1,0)   out of bounds -> skip
pop (0,0)     sunk -> skip            (duplicate entry, guard rejects it)
pop (1,0), (1,1), (1,2)      water -> skip
pop (0,2)     water -> skip           stack drains -> fill done
```

The fill sank `(0,0)` and `(0,1)` and nothing else: every diagonal neighbor of the pair is water or out of bounds, so the island is exactly the pair. The pop order shows the LIFO discipline: after `(0, 0)` sinks, the last-pushed neighbor `(-1, 1)` pops first, and `(0, 1)` waits behind the whole push batch. The scan later seeds the second fill at `(2, 1)`, which sinks `(2, 1)` and `(2, 2)`, and the function returns `islands = 2`, matching the expected Output. Duplicate entries appear because neighbors are pushed before validation; the sink-then-guard discipline is what keeps them harmless.

#### Solution

The code is the pop, guard, sink, push loop from the walkthrough, wrapped in the usual scan:

```python
from typing import List

EIGHT_DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1),
                    (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        """Return the number of islands under eight-direction adjacency.

        Time:  O(rows × cols): each cell is sunk at most once and inspected a
            constant number of times across stack operations.
        Space: O(rows × cols) for the explicit stack in the worst case.
        """
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def iterative_dfs(start_row: int, start_col: int) -> None:
            stack = [(start_row, start_col)]
            while stack:
                row, col = stack.pop()
                if (row < 0 or row >= rows or
                    col < 0 or col >= cols or
                        grid[row][col] == 0):
                    continue

                grid[row][col] = 0

                for dr, dc in EIGHT_DIRECTIONS:
                    stack.append((row + dr, col + dc))

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    islands += 1
                    iterative_dfs(row, col)

        return islands
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Each cell is sunk at most once and can sit on the stack at most once per sunk neighbor, a constant eight.

##### Space Complexity: `O(rows × cols)`

The explicit stack may hold all cells for a snake-shaped island, plus duplicates that the guard later rejects.

#### Key Insights

- The explicit stack keeps DFS's exploration order while removing the interpreter recursion limit, which matters at this problem's `100000`-cell scale.
- Pushing neighbors first and validating on pop keeps the inner loop branch-free, at the cost of stacking cells the guard later discards.
- A cell can appear on the stack once per sunk neighbor, so the bounds-and-water guard on pop, not the push, is what guarantees each cell is sunk exactly once.

### Union-Find

#### Derivation

Every approach so far answers "how many islands?" by walking each island. [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) asks a different question: if every cell starts as its own component, how many components remain after gluing all adjacent land together? With eight directions the gluing must include the diagonal pairs, and the right, down, down-right, and down-left offsets from each cell cover all eight pairwise adjacencies exactly once per unordered pair (the remaining four directions are their mirrors, seen from the neighbor's scan):

1. Build `uf = UnionFind(rows * cols)` over all cells, flattening coordinates
   with `get_index(row, col) = row * cols + col`; `components` starts at the
   total cell count.
2. Scan the grid. Count each `0` in `water_cells`; for each `1`, union it with
   its right, down, down-right, and down-left land neighbors only.
3. Each `union` of two different roots decrements `components`; `find` applies
   path compression and `union` applies union by rank to keep both operations
   nearly constant.
4. Water cells never union with anything, so each stays a singleton;
   `uf.components - water_cells` is the island count.

#### Walkthrough

Example 2, `grid = [[1,1,0],[0,0,0],[0,1,1]]`, keeps the arithmetic small: 9 cells indexed `0` to `8` by `get_index(row, col) = row * 3 + col`, land at indices `0`, `1`, `7`, `8`. `components` starts at `9`, and the scan visits cells in row-major order (trace legend: `idx` is the flattened `get_index` value shown only where the union arithmetic needs it):

```text
(0,0) idx 0   land: right (0,1) land      -> union(0, 1), components 9 -> 8
              down (1,0) water; down-right (1,1) water; down-left out
(0,1) idx 1   land: right (0,2) water; down (1,1) water
              down-right (1,2) water; down-left (1,0) water -> no unions
(0,2)         water, water_cells = 1
row 1         all water, water_cells = 2, 3, 4
(2,0) idx 6   water, water_cells = 5
(2,1) idx 7   land: right (2,2) land      -> union(7, 8), components 8 -> 7
              down, down-right, down-left: out of bounds
(2,2) idx 8   land: all four forward neighbors out of bounds -> no unions
```

No union ever bridges the middle row: the down offsets from row 0 all land in water, which is the geometric fact that the two land pairs are separate islands. Surviving components are `{0, 1}`, `{7, 8}`, and five water singletons, `7` in all; `uf.components - water_cells = 7 - 5 = 2` matches the expected Output. Note index `1`'s scan needs no union with index `7` or `8`: under eight-direction adjacency `(0, 1)` and `(2, 1)` are two rows apart and genuinely not adjacent, so the water row decides the count, not the direction rule.

#### Solution

The code is the single scan from the walkthrough, with the `UnionFind` helper carrying the component count:

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x, root_y = self.find(x), self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            self.components -= 1


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        """Return the number of islands under eight-direction adjacency.

        Time:  O(rows × cols × α(rows × cols)) with α the inverse Ackermann
            function, practically constant per union/find.
        Space: O(rows × cols) for the parent and rank arrays.
        """
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        water_cells = 0
        uf = UnionFind(rows * cols)

        def get_index(row: int, col: int) -> int:
            return row * cols + col

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    water_cells += 1
                    continue

                current_idx = get_index(row, col)
                for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < rows and
                        0 <= new_col < cols and
                            grid[new_row][new_col] == 1):
                        uf.union(current_idx, get_index(new_row, new_col))

        return uf.components - water_cells
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols × α(rows × cols))`

Each cell is processed once and each of its four forward unions costs nearly constant amortized time with path compression and union by rank, where `α` is the inverse Ackermann function.

##### Space Complexity: `O(rows × cols)`

The parent and rank arrays hold one entry per cell; the recursion depth of `find` is collapsed by path compression.

#### Key Insights

- Four forward offsets per cell (right, down, down-right, down-left) cover all eight-direction adjacencies exactly once; listing eight would union every pair twice.
- Subtracting the water-cell count from the component count yields the island number without sinking anything, so the input grid is preserved.
- The component count, not the direction count, is what the answer reads from: water singletons inflate `components`, and `water_cells` removes them in one subtraction.

## Comparison of Solutions

### Time Complexity

- **DFS with Grid Modification**: `O(rows × cols)` - every cell is visited at most once across the scan and the fill.
- **BFS with Grid Modification**: `O(rows × cols)` - every cell is enqueued at most once with a constant eight-neighbor inspection.
- **Iterative DFS with Stack**: `O(rows × cols)` - each cell is sunk once and stacked at most once per sunk neighbor.
- **Union-Find**: `O(rows × cols × α(rows × cols))` - one scan with nearly constant inverse-Ackermann union/find operations.

### Space Complexity

- **DFS with Grid Modification**: `O(rows × cols)` - the recursion stack can hold a snake-shaped island threading the grid.
- **BFS with Grid Modification**: `O(rows × cols)` - the queue's worst-case wavefront on an eight-connected grid; typically `O(min(rows, cols))`.
- **Iterative DFS with Stack**: `O(rows × cols)` - the explicit stack may hold all cells, plus guard-rejected duplicates.
- **Union-Find**: `O(rows × cols)` - parent and rank arrays for every cell, with no input mutation.

### Trade-offs

- **DFS with Grid Modification**: the shortest expression of the idea and a one-line change from the four-direction classic, but it mutates the input and risks the interpreter's recursion limit at `100000` cells.
- **BFS with Grid Modification**: removes the recursion-depth hazard and bounds fill memory to the wavefront, at the cost of queue bookkeeping.
- **Iterative DFS with Stack**: keeps DFS's order without recursion, paying duplicate stack entries that the pop-time guard rejects.
- **Union-Find**: no traversal and no input mutation, and it extends naturally to dynamic grids, but it carries the most code and an algebraic twist (subtracting water cells).

### When to Use Each

- **DFS with Grid Modification (Recommended)**: the interview default: minimal code, optimal time, and the direction rule change is visible as exactly one line of data.
- **BFS with Grid Modification**: when recursion depth is a concern on large grids or level-order exploration is asked as a follow-up.
- **Iterative DFS with Stack**: when the recursion limit is the stated worry but the interviewer wants depth-first order preserved.
- **Union-Find**: when the grid arrives dynamically or connectivity queries must survive after the count.

### Optimization Notes

- The direction rule is data, not control flow: swapping the four-direction classic for this problem changes the offsets list and nothing else, which is the point to make in an interview.
- A common pitfall is iterating all eight offsets in the Union-Find scan; unioning each pair twice is harmless for correctness but doubles the union calls, and the four forward offsets cover every adjacency once.
- Another pitfall is reusing four-direction intuition when predicting which grids merge: Example 1's X-shape is three islands under four directions and one under eight, so test grids should always be checked against the stated adjacency rule.
- At the `500 × 500` size bound, all three traversal approaches pass comfortably; the recursion-based DFS is the only one where the cell count itself is the risk factor.
