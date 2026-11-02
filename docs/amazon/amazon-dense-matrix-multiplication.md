# [Dense Matrix Multiplication](https://www.fastprep.io/problems/amazon-dense-matrix-multiplication)

**Medium** | **NN minutes** | **Matrix, Simulation**

You are given two rectangular integer matrices: left has m rows and k columns, and right has k rows and n columns. Return their matrix product, which has m rows and n columns.

Each output entry is the dot product of one left row and one right column: result[i][j] = sum(left[i][t] * right[t][j]) for 0 <= t < k.

Optimization follow-up

After a correct simple implementation, explain how tiling reuses a small block of data and how contiguous memory access affects throughput. The interview report also asks about data coalescing. Discuss how adjacent GPU threads would access adjacent elements; no GPU API, kernel launch, timing target, or hardware-specific code is required by this portable exercise.

## Examples

### Example 1

**Input:** `left = [[1,2],[3,4]]`, `right = [[5,6],[7,8]]`

**Output:** `[[19,22],[43,50]]`

**Explanation:** Two-by-two dot products.

### Example 2

**Input:** `left = [[2],[3]]`, `right = [[4,5,6]]`

**Output:** `[[8,10,12],[12,15,18]]`

**Explanation:** Rectangular outer product.

### Example 3

**Input:** `left = [[1,0,-2]]`, `right = [[3],[4],[5]]`

**Output:** `[[-7]]`

**Explanation:** Signed row-column dot product.

## Constraints

- `1 <= m, k, n <= 64.`
- `Both matrices are rectangular and the inner dimensions agree.`
- `All elements are integers between -100 and 100.`
- `Every partial sum and result fits a signed 32-bit integer.`

## Deriving the Solution

The statement hands over the product's definition as a formula: entry `(i, j)` is the dot product of `left`'s row `i` with `right`'s column `t`-slice. That definition is already an algorithm; the ladder does not search for one, it reorganizes the same three loops so the memory access pattern improves while the arithmetic stays identical. The follow-up then asks how tiling and contiguous access scale the idea, so the last rung blocks the loops and the notes discuss coalescing:

1. **Start literal.** Three nested loops in definition order `(i, j, t)`, each output cell accumulated independently: see [Triple Loop in Definition Order](#triple-loop-in-definition-order).
2. **Reorder the loops row-wise.** The same three loops as `(i, t, j)` turn `right`'s access into a contiguous row walk per step and hoist the repeated `left[i][t]` load out of the innermost loop: see [Row-Wise Loop Reorder](#row-wise-loop-reorder).
3. **Tile the loops.** Blocking all three axes by a tile size keeps a small block of `left` and `right` in cache while a whole tile of the product is produced: see [Tiled Multiplication](#tiled-multiplication).

## Solutions

### Triple Loop in Definition Order

#### Derivation

The definition reads directly as three loops. Output cell `(i, j)` needs the sum of `left[i][t] * right[t][j]` over `t`, so loop over the `m` rows, the `n` columns, and the shared `k` inner dimension, accumulating into a fresh cell:

1. Allocate the `m` by `n` result filled with zeros.
2. For each `i`, for each `j`: walk `t` from `0` to `k - 1`, adding `left[i][t] * right[t][j]` into `result[i][j]`.
3. Return the result.

#### Walkthrough

Example 1 (`left = [[1,2],[3,4]]`, `right = [[5,6],[7,8]]`), cell by cell:

```text
(0, 0): 1*5 + 2*7 = 5 + 14  = 19
(0, 1): 1*6 + 2*8 = 6 + 16  = 22
(1, 0): 3*5 + 4*7 = 15 + 28 = 43
(1, 1): 3*6 + 4*8 = 18 + 32 = 50
```

The four dot products reproduce the expected Output exactly.

#### Solution

```python
from typing import List


class Solution:
    def multiplyMatrices(self, left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
        rows, inner, columns = len(left), len(right), len(right[0])
        result = [[0] * columns for _ in range(rows)]
        for i in range(rows):
            for j in range(columns):
                total = 0
                for t in range(inner):
                    total += left[i][t] * right[t][j]
                result[i][j] = total
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n * k)`

Every one of the `m * n` cells sums `k` products.

##### Space Complexity: `O(1)`

Beyond the returned `m` by `n` matrix, one accumulator.

#### Key Insights

- Nothing is optimized: the code is the formula, which is exactly what makes it the oracle every reordering is checked against.
- The inner loop reads `right[t][j]` with `t` increasing, so consecutive reads sit one row apart in memory: the walk jumps `n` elements each step.
- `left[i][t]` changes once per `t`, but sits three loops deep, so it is re-loaded `n` times per element.

### Row-Wise Loop Reorder

#### Derivation

Summation is commutative, so the order the `t`-products are added into `result[i][j]` does not matter, and the loop order may be permuted freely. The order `(i, t, j)` pays twice: for fixed `i` and `t`, the scalar `left[i][t]` is loaded once and reused across the whole row, and `right[t][j]` walks `j` contiguously, one memory word at a time, the layout rows are stored in:

1. Allocate the `m` by `n` result filled with zeros.
2. For each `i`, for each `t`: read `left_value = left[i][t]` once, then for each `j` add `left_value * right[t][j]` into `result[i][j]`.
3. Return the result.

#### Walkthrough

Example 1 again, in `(i, t, j)` order with running accumulators:

```text
i = 0, t = 0: left_value = 1;  row += 1*[5, 6]  -> [5, 6]
i = 0, t = 1: left_value = 2;  row += 2*[7, 8]  -> [5, 6] + [14, 16] = [19, 22]
i = 1, t = 0: left_value = 3;  row += 3*[5, 6]  -> [15, 18]
i = 1, t = 1: left_value = 4;  row += 4*[7, 8]  -> [15, 18] + [28, 32] = [43, 50]
```

The same four dot products, each assembled one row-update at a time, land on the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def multiplyMatrices(self, left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
        rows, inner, columns = len(left), len(right), len(right[0])
        result = [[0] * columns for _ in range(rows)]
        for i in range(rows):
            for t in range(inner):
                left_value = left[i][t]
                right_row = right[t]
                result_row = result[i]
                for j in range(columns):
                    result_row[j] += left_value * right_row[j]
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n * k)`

The same `m * n * k` multiply-adds as the definition order; only their order moved.

##### Space Complexity: `O(1)`

Beyond the returned matrix, two local references and two scalars.

#### Key Insights

- Correctness is untouched by the reorder: floating point would care about rounding order, integers do not care at all.
- The innermost loop now streams: `right[t]` and `result[i]` are walked left to right, which is the order both rows occupy in memory.
- This is the shape real matrix kernels start from; tiling in the next rung only changes which slice of the matrices is being streamed.

### Tiled Multiplication

#### Derivation

At the statement's bounds (64 by 64) the matrices fit in cache and the reorder is all the locality the product needs. The follow-up asks how the idea scales when they do not: block all three loops by a tile size `B`, so the product is computed tile by tile. While producing one `B` by `B` tile of the result, the algorithm touches only `B` rows of `left` and `B` rows of `right` per step, `B * B` elements each, and reuses them for `B` columns of output before moving on:

1. Allocate the `m` by `n` result.
2. For each tile row `ii`, tile column `jj`, tile inner `tt` (all stepping by `B`):
3. Run the reordered triple loop of the previous rung over the cells `i` in the `ii`-tile, `t` in the `tt`-tile, `j` in the `jj`-tile, accumulating in place.
4. Every `(i, j)` cell receives exactly its `k` products, one `t`-tile at a time; return the result.

#### Walkthrough

Example 1 with tile size `B = 1`: each tile holds one cell, so the walk degenerates to the definition-order rung, cell by cell:

```text
tile (0, 0): first inner tile adds 1*5, second adds 2*7 -> 5 + 14  = 19
tile (0, 1): first inner tile adds 1*6, second adds 2*8 -> 6 + 16  = 22
tile (1, 0): first inner tile adds 3*5, second adds 4*7 -> 15 + 28 = 43
tile (1, 1): first inner tile adds 3*6, second adds 4*8 -> 18 + 32 = 50
```

The tile decomposition visits the same four products and lands on the expected Output. A concrete `B` larger than 1 behaves identically, just with more cells resident per pass; the constructed scale corner in the gauntlet checks a 64 by 64 product against the oracle.

#### Solution

```python
from typing import List


class Solution:
    def multiplyMatrices(self, left: List[List[int]], right: List[List[int]], tile: int = 8) -> List[List[int]]:
        rows, inner, columns = len(left), len(right), len(right[0])
        result = [[0] * columns for _ in range(rows)]
        for tile_row in range(0, rows, tile):
            for tile_inner in range(0, inner, tile):
                for tile_column in range(0, columns, tile):
                    for i in range(tile_row, min(tile_row + tile, rows)):
                        result_row = result[i]
                        for t in range(tile_inner, min(tile_inner + tile, inner)):
                            left_value = left[i][t]
                            right_row = right[t]
                            for j in range(tile_column, min(tile_column + tile, columns)):
                                result_row[j] += left_value * right_row[j]
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n * k)`

Tiling changes where each multiply-add happens, never how many: the tile bounds partition the same three index ranges.

##### Space Complexity: `O(1)`

Beyond the returned matrix, loop indices and two scalars; no tile-sized copies are made.

#### Key Insights

- Tiling is a cache argument, not an algorithmic one: the operation count is invariant, the reuse per cache line loaded is what improves.
- A `B` by `B` result tile costs `B` row loads each from `left` and `right` per `t`, so `2 * B` rows serve `B * B` accumulations per step instead of `B * B` separate row pairs.
- The `min` bounds keep the code correct when a dimension is not a multiple of the tile; on this statement's 64 bounds and `B = 8` the edges never trigger, but the code does not rely on that.

## Comparison of Solutions

### Time Complexity

- **Triple Loop in Definition Order**: `O(m * n * k)` - the definition's three sums.
- **Row-Wise Loop Reorder**: `O(m * n * k)` - the same multiplies, reordered.
- **Tiled Multiplication**: `O(m * n * k)` - the same multiplies, blocked.

### Space Complexity

- **Triple Loop in Definition Order**: `O(1)` - one accumulator.
- **Row-Wise Loop Reorder**: `O(1)` - two locals.
- **Tiled Multiplication**: `O(1)` - loop indices only.

### Trade-offs

- **Triple Loop in Definition Order**: the formula verbatim, the natural oracle; its inner loop strides across `right`'s rows, wasting each cache line fetched.
- **Row-Wise Loop Reorder (Recommended)**: identical arithmetic with contiguous innermost reads and one load of each `left` element per row pass; the interview's correct simple implementation.
- **Tiled Multiplication**: the reorder plus cache blocking; indistinguishable at `64^3` work but the shape that carries to matrices that do not fit in cache.

### When to Use Each

- **Triple Loop in Definition Order**: first on the whiteboard, and always as the independent checker for the other two.
- **Row-Wise Loop Reorder (Recommended)**: the answer to "implement dense matrix multiplication": minimal code, definition-order flexibility exploited, memory walked in layout order.
- **Tiled Multiplication**: when the interviewer pushes on cache behavior or the matrices outgrow cache; also the bridge into GPU discussion.

### Optimization Notes

- Tiling reuses a small block of data by keeping a `B` by `B` neighborhood of both inputs resident while a whole result tile is produced; `B` is chosen so `2 * B` rows plus one result tile fit the cache hierarchy level being targeted.
- Contiguous access affects throughput because each cache line holds several consecutive elements: a row-wise inner loop spends every line it fetches, while a column-strided loop wastes all but one element per line.
- Data coalescing is the same argument on a GPU: threads in a warp execute the same instruction in lockstep, and the memory system services their addresses best when the addresses are adjacent. Assigning adjacent threads to adjacent `j` columns makes warp `w` read `right[t][j]` for consecutive `j` and write `result[i][j]` for consecutive `j`, both contiguous in row-major layout, so each warp's accesses coalesce into few transactions; a thread-per-row mapping would stride and defeat coalescing.
- The statement guarantees every partial sum fits a signed 32-bit integer: the worst magnitude here is `100 * 100 * 64 = 640000`, far inside the bound, and Python's integers make the point moot for the reference implementations.
