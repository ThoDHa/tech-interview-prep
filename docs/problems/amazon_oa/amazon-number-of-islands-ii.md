# [Number of Islands II](https://www.fastprep.io/problems/amazon-number-of-islands-ii)

**Hard** | **NN minutes** | **Array, Matrix, Graph, Union Find**

Start with an m by n grid containing only water. For each distinct position [row, col] in positions, turn that cell into land and append the current number of islands to the result.

An island is a maximal group of land cells connected vertically or horizontally. Diagonal cells are not connected.

Interview follow-upThe rest of the discussion covered the DSU approach, how union-find works, edge cases, and the time and space complexity.

## Examples

### Example 1

**Input:** `m = 3`, `n = 3`, `positions = [[0,0],[0,1],[1,2],[2,1]]`

**Output:** `[1,1,2,3]`

**Explanation:** The second cell joins the first island. The final two additions are not four-directionally adjacent to existing land.

### Example 2

**Input:** `m = 2`, `n = 2`, `positions = [[0,0],[1,1],[0,1]]`

**Output:** `[1,2,1]`

**Explanation:** The third addition connects the two existing islands into one.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-number-of-islands-ii; fill them in. -->

## Solutions

### Recount by Flood Fill

#### Derivation

The most literal reading of the statement: after each addition the grid changes by one cell, and the current island count is wanted. Recompute it from scratch every time: build the grid, turn the added positions into land one by one, and after each addition run the standard flood-fill count over the whole grid, the same traversal as [Number of Islands](../number_of_islands.md):

1. Allocate `land`, an `m × n` matrix of `False`.
2. For each `(row, col)` in `positions`: set `land[row][col] = True`, then count
   islands by scanning every cell and running `mark_component` from each
   unvisited land cell, marking its whole component visited.
3. Append the count to `island_counts`.

#### Walkthrough

Example 1, `m = 3`, `n = 3`, `positions = [[0,0],[0,1],[1,2],[2,1]]`. Each addition is followed by a full recount; `L` marks land, `.` water:

```text
add (0,0)   grid        count
            L..         1
            ...
            ...
add (0,1)   LL.         1
            ...
            ...
add (1,2)   LL.         2
            ..L
            ...
add (2,1)   LL.         3
            ..L
            .L.
```

The counts `[1, 1, 2, 3]` match the expected Output. The repeated work is visible in the last step: the recount walks all nine cells, re-deriving an answer that differs from the previous one by at most one.

#### Solution

```python
from typing import List


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        land = [[False] * n for _ in range(m)]
        island_counts = []

        def mark_component(row: int, col: int) -> None:
            if (row < 0 or row >= m or
                col < 0 or col >= n or
                    not land[row][col] or
                    visited[row][col]):
                return
            visited[row][col] = True
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                mark_component(row + dr, col + dc)

        for row, col in positions:
            land[row][col] = True
            visited = [[False] * n for _ in range(m)]
            islands = 0
            for start_row in range(m):
                for start_col in range(n):
                    if land[start_row][start_col] and not visited[start_row][start_col]:
                        islands += 1
                        mark_component(start_row, start_col)
            island_counts.append(islands)
        return island_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(p × m × n)`

Each of the `p` additions triggers a full-grid scan and flood fill over up to `m × n` cells.

##### Space Complexity: `O(m × n)`

The land matrix, plus a recursion stack that can hold every cell of one snake-shaped island.

#### Key Insights

- Correctness is effortless: the count is recomputed from the actual grid, so repeated positions and merges need no special handling.
- The waste is equally effortless: each addition changes one cell, yet the recount touches every cell, which the incremental approaches below stop paying for.
- The flood fill marks a fresh `visited` matrix instead of sinking land cells: clearing `land` would corrupt every later round, because land turned to water never comes back.

### Union-Find with Component Counter

#### Derivation

The recount re-derives global information after a local change. The incremental question: when one water cell becomes land, how can the island count change with only local work? The new cell either forms its own island (`count + 1`), or it merges with the neighboring islands, and each distinct neighboring island it touches collapses the count by one. Union-Find answers "which island is this cell in?" in nearly constant time, so the per-addition work reduces to inspecting the four neighbors and merging distinct components:

1. Map each added `(row, col)` to a flat id `row * n + col`; the map also
   makes a repeated position a one-lookup no-op.
2. Keep `parent` and `rank` maps plus a `component_count` inside the
   `UnionFind` helper.
3. For each position: skip and re-append the current count if the cell is
   already land; otherwise add the cell as a new component, then for each of
   the four in-bounds land neighbors call `union`; each union that merges two
   distinct roots decrements `component_count`.
4. Append `component_count` after every addition.

#### Walkthrough

Example 1, `m = 3`, `n = 3`, `positions = [[0,0],[0,1],[1,2],[2,1]]`, flat ids `row * 3 + col`:

```text
add (0,0) id 0   new component, count 0 -> 1; no land neighbors
add (0,1) id 1   new component, count 1 -> 2; left (0,0) land
                 union(1, 0): distinct roots -> count 2 -> 1
add (1,2) id 5   new component, count 1 -> 2; up (0,2) water,
                 left (1,1) water, down (2,2) water
add (2,1) id 7   new component, count 2 -> 3; up (1,1) water,
                 left (2,0) water, right (2,2) water
counts [1, 1, 2, 3]
```

Each addition after the first does at most one union here, and the count moves exactly as the expected Output describes: `1`, `1`, `2`, `3`.

The merge case is Example 2, `m = 2`, `n = 2`, `positions = [[0,0],[1,1],[0,1]]`:

```text
add (0,0) id 0   is_land[0] = True, count 0 -> 1; neighbors water
add (1,1) id 3   is_land[3] = True, count 1 -> 2; neighbors water
add (0,1) id 1   is_land[1] = True, count 2 -> 3
                 left id 0 land: find(1)=1, find(0)=0, ranks equal
                                 -> parent[0]=1, rank[1]=1, count 3 -> 2
                 down id 3 land: find(1)=1, find(3)=3
                                 -> parent[3]=1, count 2 -> 1
counts [1, 2, 1]
```

The third addition touches two distinct islands and two unions collapse both, matching the expected Output of `1`.

#### Solution

```python
from typing import List


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[int, int] = {}
        self.rank: dict[int, int] = {}
        self.component_count = 0

    def add(self, cell_id: int) -> None:
        self.parent[cell_id] = cell_id
        self.rank[cell_id] = 0
        self.component_count += 1

    def find(self, cell_id: int) -> int:
        root = cell_id
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[cell_id] != root:
            self.parent[cell_id], cell_id = root, self.parent[cell_id]
        return root

    def union(self, first_id: int, second_id: int) -> None:
        first_root, second_root = self.find(first_id), self.find(second_id)
        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1
        self.component_count -= 1


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        uf = UnionFind()
        cell_ids = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        island_counts = []
        for row, col in positions:
            cell_id = row * n + col
            if cell_id in cell_ids:
                island_counts.append(uf.component_count)
                continue
            cell_ids[cell_id] = True
            uf.add(cell_id)
            for dr, dc in directions:
                neighbor_row, neighbor_col = row + dr, col + dc
                neighbor_id = neighbor_row * n + neighbor_col
                if (0 <= neighbor_row < m and
                        0 <= neighbor_col < n and
                        neighbor_id in cell_ids):
                    uf.union(cell_id, neighbor_id)
            island_counts.append(uf.component_count)
        return island_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(p × α(p))`

Each addition inspects four neighbors and runs a constant number of union-find operations, each nearly constant with path compression and union by rank (`α` is the inverse Ackermann function, effectively constant).

##### Space Complexity: `O(min(p, m × n))`

The union-find dictionaries and the id map hold one entry per added cell.

#### Key Insights

- Only the four neighbors of the new cell can change connectivity, so island counting becomes incremental: start at one component and subtract one per successful merge.
- The `component_count` lives inside the union-find and moves with every union, so no separate bookkeeping pass is needed.
- Idempotent repeats are the standard edge case: the statement's "distinct positions" guard makes them impossible, but the `cell_id in cell_ids` check costs one lookup and makes the routine safe regardless.
- Allocating the structure lazily per added cell (rather than for the whole grid) keeps the space proportional to the number of land cells, which matters when the grid is huge and `positions` is short.

### Grid Array Union-Find

#### Derivation

The dictionary-based union-find pays hashing on every lookup and allocates per cell. When the grid is modest, a flat array indexed by `row * n + col` replaces every dictionary with a list access, and the union-find over all `m × n` cells starts with `parent[cell] = cell` for every cell. Land is tracked in a boolean array; a union attempt against a water cell is skipped by that check. The algorithm is otherwise the counter-driven incremental merge from [Union-Find with Component Counter](#union-find-with-component-counter):

1. Allocate `parent` over all `m × n` cells and `is_land`, all `False`.
2. For each position: if already land, append the current count and continue;
   otherwise set `is_land[cell] = True` and increment `component_count`.
3. Union with each in-bounds land neighbor; every merged union decrements
   `component_count`.
4. Append `component_count`.

#### Walkthrough

Example 2, `m = 2`, `n = 2`, `positions = [[0,0],[1,1],[0,1]]`, ids `row * 2 + col`, with `parent` shown only for touched cells:

```text
add (0,0) id 0   new component, count 0 -> 1; neighbors water
add (1,1) id 3   new component, count 1 -> 2; neighbors water
add (0,1) id 1   new component, count 2 -> 3
                 left (0,0) land: union(1, 0): roots 1, 0, equal ranks
                                  -> parent[0] = 1, rank[1] = 1, count 3 -> 2
                 down (1,1) land: union(1, 3): roots 1, 3
                                  -> parent[3] = 1, count 2 -> 1
counts [1, 2, 1]
```

The third addition merges two islands through two unions and the counter lands on `1`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        total_cells = m * n
        parent = list(range(total_cells))
        rank = [0] * total_cells
        is_land = [False] * total_cells
        component_count = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        island_counts = []

        def find(cell_id: int) -> int:
            root = cell_id
            while parent[root] != root:
                root = parent[root]
            while parent[cell_id] != root:
                parent[cell_id], cell_id = root, parent[cell_id]
            return root

        for row, col in positions:
            cell_id = row * n + col
            if is_land[cell_id]:
                island_counts.append(component_count)
                continue
            is_land[cell_id] = True
            component_count += 1
            for dr, dc in directions:
                neighbor_row, neighbor_col = row + dr, col + dc
                if 0 <= neighbor_row < m and 0 <= neighbor_col < n:
                    neighbor_id = neighbor_row * n + neighbor_col
                    if is_land[neighbor_id]:
                        cell_root, neighbor_root = find(cell_id), find(neighbor_id)
                        if cell_root != neighbor_root:
                            if rank[cell_root] < rank[neighbor_root]:
                                cell_root, neighbor_root = neighbor_root, cell_root
                            parent[neighbor_root] = cell_root
                            if rank[cell_root] == rank[neighbor_root]:
                                rank[cell_root] += 1
                            component_count -= 1
            island_counts.append(component_count)
        return island_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(p × α(m × n))`

Each addition runs a constant number of union-find operations over array-backed sets, nearly constant with path compression and union by rank.

##### Space Complexity: `O(m × n)`

The three flat arrays cover every cell of the grid whether it becomes land or not.

#### Key Insights

- The array version is the dictionary version with hashing removed: same algorithm, same counter logic, lower constant factors and no per-cell allocation.
- The trade is space: all `m × n` cells are provisioned up front, so this variant fits moderate grids, while the dictionary version fits huge grids with few additions.
- Initializing `parent` over the whole grid is safe even though water cells never union: their entries are simply never read once `is_land` gates every access.

## Comparison of Solutions

### Time Complexity

- **Recount by Flood Fill**: `O(p × m × n)` - a full-grid scan and fill after every addition.
- **Union-Find with Component Counter**: `O(p × α(p))` - four neighbor checks plus near-constant unions per addition.
- **Grid Array Union-Find**: `O(p × α(m × n))` - the same work with array indexing instead of hashing.

### Space Complexity

- **Recount by Flood Fill**: `O(m × n)` - the land matrix plus recursion stack.
- **Union-Find with Component Counter**: `O(min(p, m × n))` - union-find state only for added cells.
- **Grid Array Union-Find**: `O(m × n)` - three flat arrays over the whole grid.

### Trade-offs

- **Recount by Flood Fill**: the shortest path to a correct answer and a useful oracle, but it repeats the entire traversal `p` times and cannot survive tight limits.
- **Union-Find with Component Counter**: incremental, near-linear overall, and frugal with memory on huge grids, at the cost of dictionary hashing and a union-find implementation.
- **Grid Array Union-Find**: the fastest constants of the three, but it provisions the whole grid even when only a few cells ever become land.

### When to Use Each

- **Recount by Flood Fill**: as the correctness oracle when prototyping, or when both grid and addition count are tiny.
- **Union-Find with Component Counter (Recommended)**: the interview answer: incremental, asymptotically optimal, and it scales to grids far larger than memory would allow if the whole grid had to be materialized.
- **Grid Array Union-Find**: when the grid is modest and additions are many, where array indexing beats dictionary lookups.

### Optimization Notes

- The per-addition answer depends only on the four neighbors of the added cell; any solution that looks further afield per addition is doing avoidable work.
- Union by rank with path compression is what turns "merge two islands" into a nearly constant operation; either technique alone leaves a logarithmic factor in the worst case.
- Repeated positions must return the unchanged count rather than double-add; the statement promises distinct positions, and the one-lookup guard honors that promise cheaply.
