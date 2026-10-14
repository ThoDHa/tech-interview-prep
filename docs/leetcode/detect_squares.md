# [Detect Squares](https://leetcode.com/problems/detect-squares/)

**Medium** | **25 minutes** | **Array, Hash Table, Design, Counting**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md), [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Counting](https://en.wikipedia.org/wiki/Counting) · [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics)

**Practice:** [`practice/detect_squares/solution.py`](../../practice/detect_squares/solution.py)

You are given a stream of points consisting of x-y coordinates on a 2-D plane. Points can be added and queried as follows:

* **Add** - new points can be added to the stream into a data structure. Duplicate points are allowed and should be treated as separate points.
* **Query** - Given a single query point, **count** the number of ways to choose three additional points from the data structure such that the three points and the query point form a **square**. The square must have all sides parallel to the x-axis and y-axis, i.e. no diagonal squares are allowed. Recall that a **square** must have four equal sides.


Implement the `CountSquares` class:
* `CountSquares()` Initializes the object.
* `void add(int[] point)` Adds a new point `point = [x, y]`.
* `int count(int[] point)` Counts the number of ways to form valid **squares** with point `point = [x, y]` as described above.

## Examples

### Example 1

**Input:** `["CountSquares", "add", [[1, 1]], "add", [[2, 2]], "add", [[1, 2]], "count", [[2, 1]], "count", [[3, 3]], "add", [[2, 2]], "count", [[2, 1]]]`

**Output:** `[null, null, null, null, 1, 0, null, 2]`

**Explanation:** CountSquares countSquares = new CountSquares();
countSquares.add([1, 1]);
countSquares.add([2, 2]);
countSquares.add([1, 2]);

countSquares.count([2, 1]);   // return 1.
countSquares.count([3, 3]);   // return 0.
countSquares.add([2, 2]);     // Duplicate points are allowed.
countSquares.count([2, 1]);   // return 2.

## Constraints

- `point.length == 2`
- `0 <= x, y <= 1000`

## Deriving the Solution

A query point `q` participates in an axis-aligned square exactly through its diagonal partner `p`: given `p`, the side length is `|px - qx|`, and the square's other two corners are fully determined as `[px, qy]` and `[qx, py]`. So counting squares is counting stored points that can play the diagonal role, and the data structure only has to answer multiplicity questions about coordinates.

1. **Start literal.** Store every point in a list; on `count`, scan the list,
   test each stored point as a potential diagonal (equal `|dx| == |dy|`,
   both nonzero), and for each candidate check the two corner points by
   scanning again. Correct, but each query costs a scan inside a scan:
   see [Brute Force Pair Scan](#brute-force-pair-scan).
2. **Spot the repeated work.** The corner checks re-ask "how many points at
   `[x, y]`?" for every candidate, which is one dictionary lookup if the
   stream is a coordinate-count map: see
   [Count Map with Diagonal Scan](#count-map-with-diagonal-scan).
3. **Index by query column.** The candidate diagonal always shares the
   query's x or narrows by the side length; bucketing counts by x-coordinate
   lets the query iterate only the relevant columns: see
   [Column Buckets](#column-buckets).

## Solutions

### Brute Force Pair Scan

#### Derivation

The most literal reading of `count`: a square with `q = [qx, qy]` as a corner has another corner at `[qx + d, qy + d]` or `[qx - d, qy - d]` (diagonal), plus corners `[qx + d, qy]`/`[qx - d, qy]` and `[qx, qy + d]`/`[qx, qy - d]`, for some side `d > 0`. Try every stored point as the diagonal, and verify the two side corners by scanning the list again:

1. `add` appends the point to a `points` list; duplicates become duplicate
   entries, which is exactly the multiplicity the problem demands.
2. `count(q)` loops over `points`; for each candidate `p`, compute
   `dx = px - qx` and `dy = py - qy`, and skip unless `abs(dx) == abs(dy)`
   with `dx != 0`.
3. For a passing candidate, scan `points` twice more: once for `[px, qy]`,
   once for `[qx, py]`, counting occurrences of each.
4. Add `corner1_count * corner2_count` to the total: each copy of one corner
   pairs with each copy of the other.

#### Walkthrough

Run Example 1's stream against the scan. After three adds, `points = [[1,1], [2,2], [1,2]]`; query `q = [2, 1]`:

```text
p = [1,1]   dx = -1, dy = 0     abs mismatch -> skip
p = [2,2]   dx = 0, dy = 1     abs mismatch -> skip
p = [1,2]   dx = -1, dy = 1    diagonal! corners [1,1] and [2,2]
            count([1,1]) = 1, count([2,2]) = 1  -> 1 * 1 = 1
total = 1
```

Exactly one stored point is a valid diagonal partner, and both of its corners exist once each, so `count([2, 1])` returns `1`, matching the expected Output. The mid-stream query `[3, 3]` does find a diagonal-shaped candidate: `p = [1, 1]` gives `dx = dy = -2`, but its corners `[1, 3]` and `[3, 1]` are absent from the stream, both corner counts are `0`, and the contribution is `1 * 0 * 0 = 0`; every other candidate fails the diagonal test, so the query returns `0`, also matching the expected Output.

#### Solution

The code is the candidate loop with the two corner re-scans.

```python
from typing import List


class CountSquares:
    def __init__(self) -> None:
        self.points: List[List[int]] = []

    def add(self, point: List[int]) -> None:
        self.points.append(point)

    def count(self, point: List[int]) -> int:
        qx, qy = point
        total = 0
        for px, py in self.points:
            dx, dy = px - qx, py - qy
            if abs(dx) != abs(dy) or dx == 0:
                continue
            corner1 = corner2 = 0
            for cx, cy in self.points:
                if [cx, cy] == [px, qy]:
                    corner1 += 1
                if [cx, cy] == [qx, py]:
                    corner2 += 1
            total += corner1 * corner2
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `add` `O(1)`, `count` `O(P^2)`

For each of the `P` stored candidates, two full re-scans of the `P` points; at the stream scale the problem implies, this collapses under its own weight.

##### Space Complexity: `O(P)`

The list stores every added point, duplicates included.

#### Key Insights

- The diagonal test `abs(dx) == abs(dy) and dx != 0` is the complete geometry: side length, orientation (up-right or down-right diagonal), and the degenerate zero-side rejection in one line.
- Corner multiplicities multiply because the two corners are chosen independently from the stream's duplicates.
- The nested scan recomputes corner counts that never change between candidates, which is the redundancy the counting version removes.

### Count Map with Diagonal Scan

#### Derivation

The inner re-scans all answer one question, "how many stored copies of `[x, y]`?", for which a dictionary keyed by coordinate tuples answers in `O(1)`. Keep the candidate scan (it enumerates diagonals with their multiplicities for free) but replace the corner checks with lookups:

1. `add` bumps `counts[(x, y)] += 1`.
2. `count(q)` loops over the `counts` entries; each key `p` with multiplicity
   `c_p` is tested as a diagonal exactly as before.
3. A passing diagonal contributes `c_p * counts.get((px, qy), 0) *
   counts.get((qx, py), 0)`: the diagonal's copies times the corners' copies.

#### Walkthrough

Replay Example 1's stream against the map. After the three adds and the duplicate add (the stream's sixth operation), `counts = {(1,1): 1, (2,2): 2, (1,2): 1}`; query `q = [2, 1]` (the fourth operation, before the duplicate):

```text
counts = {(1,1): 1, (2,2): 1, (1,2): 1}    first count([2,1])
p = (1,1)  c=1  dx=-1, dy=0    skip (abs mismatch)
p = (2,2)  c=1  dx=0,  dy=1    skip (abs mismatch)
p = (1,2)  c=1  dx=-1, dy=1    diagonal
           corners (1,1): 1 copy, (2,2): 1 copy -> 1 * 1 * 1 = 1
returns 1
```

Then the stream adds `[2, 2]` again and repeats `count([2, 1])` with `counts = {(1,1): 1, (2,2): 2, (1,2): 1}`:

```text
p = (1,1), (2,2) skip as before
p = (1,2)  c=1  diagonal
           corners (1,1): 1 copy, (2,2): 2 copies -> 1 * 1 * 2 = 2
returns 2
```

The second query returns `2` because the diagonal's corner `(2, 2)` now exists in two copies, matching the expected Output's final `2`. The `count([3, 3])` mid-stream finds only `(1,1)` as a diagonal candidate (`dx = dy = -2`), but its corners `(1, 3)` and `(3, 1)` are missing from the map, contributing `0`, matching the expected Output.

#### Solution

The code is the map, the candidate loop over its entries, and the multiplied lookup.

```python
from typing import List


class CountSquares:
    def __init__(self) -> None:
        self.counts: dict = {}

    def add(self, point: List[int]) -> None:
        self.counts[(point[0], point[1])] = self.counts.get((point[0], point[1]), 0) + 1

    def count(self, point: List[int]) -> int:
        qx, qy = point
        total = 0
        for (px, py), copies in self.counts.items():
            dx, dy = px - qx, py - qy
            if abs(dx) != abs(dy) or dx == 0:
                continue
            total += (
                copies
                * self.counts.get((px, qy), 0)
                * self.counts.get((qx, py), 0)
            )
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `add` `O(1)` average, `count` `O(U)` average

`U` is the number of distinct stored points; each entry is tested once with `O(1)` dictionary lookups.

##### Space Complexity: `O(U)`

One map entry per distinct point, multiplicities folded into values.

#### Key Insights

- Folding duplicates into counts (rather than list entries) removes the re-scans without changing the arithmetic: multiplicity moves from list repetition to integer factors.
- The candidate that is the query point itself (`p == q`) is rejected by `dx == 0`, which cleanly excludes degenerate zero-side squares.
- Iterating `counts.items()` yields each distinct diagonal once, already carrying its multiplicity, so the product needs no further scanning.

### Column Buckets

#### Derivation

The map scan still walks every distinct point, including the vast majority that share nothing with the query. Every valid diagonal `p` of `q = [qx, qy]` satisfies `px = qx + d` or `px = qx - d` with the same `|d| = |py - qy|`; bucketing the counts by x-coordinate lets the query visit only columns that actually hold points, and each candidate's y-difference is checked the same way as before:

1. `add` bumps `points_by_x[x][y] += 1` using nested dictionaries.
2. `count(q)` iterates `points_by_x.items()`: for each column `px` and its
   `y`-counts, compute `d = px - qx`; skip the query's own column (`d == 0`,
   no positive side) and otherwise test each stored `py` for
   `abs(py - qy) == abs(d)`.
3. A candidate `(px, py)` contributes its copies times the corner lookups
   `points_by_x[px].get(qy, 0)` (same column as the diagonal) and
   `points_by_x[qx].get(py, 0)` (same column as the query).

#### Walkthrough

Bucket Example 1's final stream: adds of `[1,1]`, `[2,2]`, `[1,2]`, `[2,2]` give `points_by_x = {1: {1: 1, 2: 1}, 2: {2: 2}}`; the second query `q = [2, 1]`:

```text
column px = 1:  d = 1 - 2 = -1, abs(d) = 1
  py = 1: abs(1 - 1) = 0 != 1          -> skip
  py = 2: abs(2 - 1) = 1 == 1          diagonal (1, 2), copies 1
          corner (1, qy=1): col 1 has 1 copy -> 1
          corner (qx=2, py=2): col 2 has 2 copies -> 2
          contributes 1 * 1 * 2 = 2
column px = 2:  d = 0 -> skip (zero side)
total = 2
```

The only column visited besides the query's own contributes exactly the expected `2`, matching the final expected Output. The first query (before the duplicate add) walks the same column with `col 2 has 1 copy` and returns `1`; `count([3, 3])` finds two y-aligned diagonal candidates, `(1, 1)` with `abs(1 - 3) = 2 = abs(1 - 2)` and `(2, 2)` with `abs(2 - 3) = 1 = abs(2 - 3)`, but every corner involved (`(1, 3)`, `(3, 1)`, `(2, 3)`, `(3, 2)`) is absent, all corner lookups return `0`, and the query returns `0`.

#### Solution

The code is the nested-dictionary bucketing with the same multiplied corners.

```python
from collections import defaultdict
from typing import List


class CountSquares:
    def __init__(self) -> None:
        # Inner defaultdict(int); .get on the outer dict avoids materializing
        # the query's column mid-iteration when it holds no points
        self.points_by_x: dict = defaultdict(lambda: defaultdict(int))

    def add(self, point: List[int]) -> None:
        self.points_by_x[point[0]][point[1]] += 1

    def count(self, point: List[int]) -> int:
        qx, qy = point
        total = 0
        query_column = self.points_by_x.get(qx, {})
        for px, y_counts in self.points_by_x.items():
            d = px - qx
            if d == 0:
                continue
            for py, copies in y_counts.items():
                if abs(py - qy) != abs(d):
                    continue
                total += (
                    copies
                    * y_counts.get(qy, 0)
                    * query_column.get(py, 0)
                )
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `add` `O(1)` average, `count` `O(V)` average

`V` is the number of stored points lying in columns other than the query's; the query's own column is skipped entirely, and each visited point costs `O(1)` lookups.

##### Space Complexity: `O(U)`

The nested dictionaries hold one entry per distinct point, grouped by column.

#### Key Insights

- Column pruning turns the scan's `O(U)` into `O(V)` with `V <= U`, a data-dependent win that grows with real streams where queries cluster geographically.
- The corner `(px, qy)` lives in the diagonal's own column, so `y_counts.get(qy, 0)` reuses the loop's bucket without a second dictionary hop.
- `defaultdict` of `defaultdict` keeps `add` branch-free; a plain dict with `get` chains works identically at the cost of explicit presence checks.

## Comparison of Solutions

The practice harness's `practice/detect_squares/reference.py` implements the **Count Map with Diagonal Scan** solution.

### Time Complexity

- **Brute Force Pair Scan**: `count` `O(P^2)` - two full re-scans per stored candidate.
- **Count Map with Diagonal Scan**: `count` `O(U)` average - one `O(1)`-lookup test per distinct point.
- **Column Buckets**: `count` `O(V)` average - only points in foreign columns are visited.

### Space Complexity

- **Brute Force Pair Scan**: `O(P)` - the raw point list.
- **Count Map with Diagonal Scan**: `O(U)` - one map entry per distinct point.
- **Column Buckets**: `O(U)` - the same entries, grouped by x-coordinate.

### Trade-offs

- **Brute Force Pair Scan**: The direct transcription of the geometry with the least machinery, undone by quadratic query time on any realistic stream.
- **Count Map with Diagonal Scan**: The multiplicity-aware middle ground: every stored point examined once, corners resolved by lookup.
- **Column Buckets**: The same arithmetic with column-level pruning, at the price of nested-container bookkeeping.

### When to Use Each

- **Brute Force Pair Scan**: Never in production; useful as the correctness oracle while the counting versions are developed.
- **Count Map with Diagonal Scan** (recommended): The default; the simplest structure that makes `count` linear in distinct points and `add` constant.
- **Column Buckets**: When queries cluster on few columns or the stream concentrates points in known regions, making the pruning pay.

### Optimization Notes

- Coordinates are bounded by `0 <= x, y <= 1000`, so the universe of point keys is at most a million; a flat `1001 x 1001` count grid replaces the dictionaries with array indexing, trading memory for the fastest possible lookups when the stream is dense.
- The diagonal enumeration can be inverted: for each of the four side lengths implied by a stored point, look up `q`'s two corner columns directly, giving `O(1)` per candidate with a column index keyed by `(x, y - x)` pairs; this is the classic `O(1)`-query formulation.
- The product of corner counts is the only combinatorics in the problem: duplicates multiply choices, and forgetting `get(..., 0)` defaults is the common off-by-absence bug.

