# [Count Islands from Streaming Rows](https://www.fastprep.io/problems/amazon-streaming-island-count)

**Hard** | **NN minutes** | **Matrix, Graph, Union Find, Simulation**

A binary matrix arrives one row at a time from top to bottom. Given those rows as the finite ordered batch rows, return an array where result i is the number of islands present after rows 0 through i have arrived.

## Examples

### Example 1

**Input:** `rows = ["110","010","011"]`

**Output:** `[1,1,1]`

**Explanation:** Each new land cell joins the component that began in the first row.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-streaming-island-count; fill them in. -->

## Solutions

### Re-run Flood Fill per Prefix

#### Derivation

The most literal reading treats each moment of the stream as its own question. When row `prefix_end` has just arrived, the matrix held in memory is `rows[:prefix_end + 1]`, and `island_counts[prefix_end]` is simply the number of connected components of `'1'` in that prefix. The Number of Islands problem is therefore solved once per prefix, and the separate-visited flood fill from that page slots in unchanged as the counting helper:

1. For each `prefix_end` from `0` to `len(rows) - 1`, take the first
   `prefix_end + 1` rows as `prefix`.
2. Count the components of `'1'` in `prefix` with a `seen` matrix and recursive
   `dfs`, exactly the scan-and-fill from [Number of Islands](amazon-number-of-islands.md#dfs-with-separate-visited-array).
3. Append each count to `island_counts`.
4. Return `island_counts` after the last row lands.

#### Walkthrough

Let us run the three prefixes of Example 1, `rows = ["110","010","011"]`, by hand. Each line is one complete re-scan of the prefix built so far:

```text
prefix_end = 0   prefix = ["110"]              one "11" component            -> 1
prefix_end = 1   prefix = ["110","010"]        the component grew to (1,1)   -> 1
prefix_end = 2   prefix = ["110","010","011"]  the component grew to row 2   -> 1
```

No prefix ever contains a second component: every new land cell arrives attached to the component born at `(0, 0)`. The helper appends `1` three times and the function returns `[1, 1, 1]`, matching the expected Output for Example 1.

#### Solution

The code is the per-prefix loop with the flood-fill count as its helper.

```python
from typing import List


class Solution:
    def solve(self, rows: List[str]) -> List[int]:
        def count_islands(prefix: List[str]) -> int:
            prefix_rows, prefix_cols = len(prefix), len(prefix[0])
            seen = [[False] * prefix_cols for _ in range(prefix_rows)]
            islands = 0

            def dfs(row: int, col: int) -> None:
                if (row < 0 or row >= prefix_rows or
                    col < 0 or col >= prefix_cols or
                    seen[row][col] or
                        prefix[row][col] == '0'):
                    return
                seen[row][col] = True
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    dfs(row + dr, col + dc)

            for row in range(prefix_rows):
                for col in range(prefix_cols):
                    if prefix[row][col] == '1' and not seen[row][col]:
                        islands += 1
                        dfs(row, col)
            return islands

        return [count_islands(rows[:prefix_end + 1])
                for prefix_end in range(len(rows))]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R² × C)`

Let `R` be the row count and `C` the row length: the prefix that ends at row k already holds `(k + 1) × C` cells, and each is re-scanned from scratch, so the work sums over all prefixes to `C × (1 + 2 + ... + R)`.

##### Space Complexity: `O(R × C)`

The largest prefix's `seen` matrix plus the recursion stack, which can hold all of its cells.

#### Key Insights

- Correctness is inherited for free: the helper is the proven Number of Islands fill, applied once per arrival.
- Each re-scan throws away everything the previous scan learned, which is the entire cost: the same cells are flood-filled over and over.
- The helper reads the immutable string rows directly, so no grid copy is needed; only the `seen` matrix is allocated per prefix.

### Incremental Union-Find over Rows

#### Derivation

The re-scan pays because it recomputes a count that arrival cannot invalidate. Land only ever appears in a stream; no cell is ever removed, so an island can grow, or two islands can merge when a new cell bridges them, but an existing island can never split or vanish. The count therefore evolves by a local rule: each new land cell either starts its own island (count +1), joins exactly the islands under its already-arrived neighbors (count unchanged), or bridges two of them (count -1 per merge). Because rows arrive top to bottom, those neighbors are only the left and up cells, so at most two unions per new cell decide everything, which is exactly what [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) answers in near-constant time. The structure is the one from the Number of Islands page with one change: `union` returns whether a merge happened, and that boolean drives the running count:

1. Build `uf` over `R × C` cells flattened by
   `cell_id = row_number * cols + col`; start `islands` at `0` and keep
   `island_counts`, one entry per arrival.
2. For each arriving `row_number`, scan its columns and skip `'0'`.
3. For a land cell, increment `islands`; then, when the left neighbor exists
   and is `'1'`, call `uf.union(cell_id, cell_id - 1)` and decrement `islands`
   only on a `True` merge; do the same against `cell_id - cols` when the up
   neighbor exists and is `'1'`.
4. Append `islands` to `island_counts` once the row is finished.
5. Return `island_counts`.

#### Walkthrough

Let us stream Example 1, `rows = ["110","010","011"]`, cell by cell. Each line is one land cell landing; `u(4, 1)` abbreviates the call `uf.union(4, 1)` over the flattened ids, where `cell_id = row_number * 3 + col`:

```text
row 0 "110"
  (0,0) id 0   islands 1   no left, no up
  (0,1) id 1   islands 2   left land: u(1, 0) merges    -> islands 1
               count after row 0: 1
row 1 "010"
  (1,1) id 4   islands 2   left water; up land: u(4, 1) merges -> islands 1
               count after row 1: 1
row 2 "011"
  (2,1) id 7   islands 2   left water; up land: u(7, 4) merges -> islands 1
  (2,2) id 8   islands 2   left land: u(8, 7) merges -> islands 1; up water
               count after row 2: 1
```

Every cell joined the component born at id `0`, so `islands` returned to `1` after each merge and `island_counts` collected `[1, 1, 1]`, matching the expected Output for Example 1. Two behaviors the example does not show are the reason the boolean return matters: when a row bridges two islands (say a row of `"111"` landing under `"1.1"`) the count drops by one, and when the left and up neighbors already sit in the same island (a cell completing a ring) the first union merges while the second finds equal roots, returns `False`, and leaves the count alone, so the decrement happens exactly once.

#### Solution

The code is the streaming loop from the walkthrough, with the `UnionFind` helper whose `union` reports whether two islands became one.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        return True


class Solution:
    def solve(self, rows: List[str]) -> List[int]:
        total_rows, cols = len(rows), len(rows[0])
        uf = UnionFind(total_rows * cols)
        islands = 0
        island_counts = []

        for row_number, row in enumerate(rows):
            for col in range(cols):
                if row[col] == '0':
                    continue

                cell_id = row_number * cols + col
                islands += 1

                if col > 0 and row[col - 1] == '1' and uf.union(cell_id, cell_id - 1):
                    islands -= 1
                if (row_number > 0 and rows[row_number - 1][col] == '1'
                        and uf.union(cell_id, cell_id - cols)):
                    islands -= 1

            island_counts.append(islands)

        return island_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R × C × α(R × C))`

Let `R` be the row count and `C` the row length: every cell is scanned once and unions at most twice, and each union/find costs nearly constant inverse-Ackermann time `a` under path halving and union by rank.

##### Space Complexity: `O(R × C)`

The parent and rank arrays over all cells; the output itself adds `O(R)`.

#### Key Insights

- Arrival can only add land, so the island count moves by +1, 0, or -1 per new cell; maintaining it incrementally replaces every full re-scan.
- Unioning only the left and up neighbors is both a correctness and an efficiency property: they are the only cells that have already arrived, and right/down adjacencies get covered when those cells land in turn.
- `union` returning a boolean is the one API change over the batch version, and it is what lets the caller know a merge (not a fresh cell in an existing island) just happened.
- The double decrement hazard is real: when a new cell's left and up neighbors share an island, the second union must not decrement again; equal roots returning `False` is what protects the count.

## Comparison of Solutions

### Time Complexity

- **Re-run Flood Fill per Prefix**: `O(R² × C)` - each of the `R` prefixes is scanned in full, and prefix lengths grow linearly.
- **Incremental Union-Find over Rows**: `O(R × C × α(R × C))` - every cell is processed once with at most two near-constant union operations.

### Space Complexity

- **Re-run Flood Fill per Prefix**: `O(R × C)` - the largest prefix's `seen` matrix plus the recursion stack.
- **Incremental Union-Find over Rows**: `O(R × C)` - parent and rank arrays covering every cell.

### Trade-offs

- **Re-run Flood Fill per Prefix**: trivially correct because it reuses a proven fill unchanged, but the quadratic re-scanning repeats identical work `R` times.
- **Incremental Union-Find over Rows**: linear up to the inverse Ackermann factor and natural for a genuine stream, at the cost of union-find bookkeeping and the merge-counting edge cases.

### When to Use Each

- **Re-run Flood Fill per Prefix**: small inputs, or as the reference oracle when testing the incremental version.
- **Incremental Union-Find over Rows (Recommended)**: the interview answer: one pass, per-row counts as they arrive, and the natural form when rows truly stream in one at a time.

### Optimization Notes

- The incremental version is the batch Union-Find from Number of Islands with two streaming changes: cells arrive one at a time instead of all at once, and a boolean-returning `union` maintains the running count.
- Only the left and up neighbors are examined because rows arrive top to bottom; scanning right and down would find no land and waste half the checks.
- The iterative `find` with path halving (`parent[x] = parent[parent[x]]`) keeps the loop recursion-free, matching the no-recursion discipline of a streaming caller.
- A subtle pitfall is the completed ring: both neighbors land in one island, the first union merges, and the second must observe equal roots and skip the decrement; the boolean return encodes exactly this.
