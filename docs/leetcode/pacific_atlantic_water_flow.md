# [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/)

**Medium** | **25 minutes** | **Array, Depth-First Search, Breadth-First Search, Matrix**

**Pattern:** [Multi-Source BFS](../patterns/grid_bfs_multi_source/intuition.md), [Graph Traversal](../patterns/graph/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Flood fill](https://en.wikipedia.org/wiki/Flood_fill)

**Practice:** [`practice/pacific_atlantic_water_flow/solution.py`](../../practice/pacific_atlantic_water_flow/solution.py)

You are given a rectangular island `heights` where `heights[r][c]` represents the **height above sea level** of the cell at coordinate `(r, c)`.

The islands borders the **Pacific Ocean** from the top and left sides, and borders the **Atlantic Ocean** from the bottom and right sides.

Water can flow in **four directions** (up, down, left, or right) from a cell to a neighboring cell with **height equal or lower**. Water can also flow into the ocean from cells adjacent to the ocean.

Find all cells where water can flow from that cell to **both** the Pacific and Atlantic oceans. Return it as a **2D list** where each element is a list `[r, c]` representing the row and column of the cell. You may return the answer in **any order**.

## Examples

### Example 1

**Input:**

```text
heights = [
  [4,2,7,3,4],
  [7,4,6,4,7],
  [6,3,5,3,6]
]
```

**Output:**

```text
[[0,2],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0]]
```

### Example 2

**Input:** `heights = [[1],[1]]`

**Output:** `[[0,0],[1,0]]`

## Constraints

- `1 <= heights.length, heights[r].length <= 100`
- `0 <= heights[r][c] <= 1000`

## Deriving the Solution

A cell qualifies when water can walk downhill (never up) from it to the Pacific border and, along some path, to the Atlantic border. Asking that question forward from every cell repeats the same walks on shared downhill paths; asking it backwards from the oceans shares them. The reversal is the key reformulation: a cell can flow to an ocean exactly when that ocean can be climbed to from the cell's coast-side entry, so flooding inland with a `>=` test marks every cell whose water reaches that ocean. Every solution below answers the two reachability questions; they differ in which direction the search runs and how per-cell results are kept.

1. **Start literal.** From every cell, run a downhill DFS/BFS and check
   whether the walk touches each ocean's border: see
   [Forward Search Per Cell](#forward-search-per-cell).
2. **Spot the waste.** Cells on a shared downhill path re-walk it once per
   query, and each walk re-derives answers its neighbors already have.
3. **Reverse the flow.** Flood inward from the Pacific border cells with a
   `>=` test to get one reachability set, flood inward from the Atlantic
   border for the other, and intersect: see
   [Reverse Two-Ocean DFS](#reverse-two-ocean-dfs).

## Solutions

### Forward Search Per Cell

#### Derivation

The most literal reading tests each cell independently: can water leaving this cell reach ocean X? A downhill walk answers it, the same BFS for every cell, succeeding the moment the walk stands on the ocean's border (row 0 or column 0 for the Pacific, last row or last column for the Atlantic):

1. For each cell, run `reaches(cell, ocean)` for both oceans.
2. The walk expands downhill only (`neighbor height <= current height`),
   remembering visited cells to terminate.
3. Success is border contact: the Pacific when any visited cell sits in row
   0 or column 0, the Atlantic for the last row or last column.
4. Collect the cells that succeed against both.

#### Walkthrough

Trace Example 1's cell `(1,2)` (height 6). Its downhill walks:

```text
Pacific walk from (1,2)=6
  down (2,2)=5 -> left (2,1)=3 -> left (2,0)=6 no (uphill); up (1,1)=4
  up (0,2)=7 no; left (1,1)=4 -> left (1,0)=7 no, up (0,1)=2 -> row 0: reached
Atlantic walk from (1,2)=6
  right (1,3)=4 -> down (2,3)=3 -> last row: reached; down (2,2)=5 -> last row: reached too
```

Both walks succeed, so `(1,2)` is in the answer, matching Example 1's output list. Contrast `(0,0)`: its water flows only downhill to the Pacific border it already touches and can never climb to the Atlantic side, and the walk confirms it, so `(0,0)` is absent from the output.

#### Solution

The code is the per-cell double walk with an explicit visited set per query.

```python
from collections import deque
from typing import List, Tuple


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, columns = len(heights), len(heights[0])

        def reaches(start: Tuple[int, int], ocean: str) -> bool:
            queue = deque([start])
            seen = {start}
            while queue:
                row, column = queue.popleft()
                if ocean == "pacific" and (row == 0 or column == 0):
                    return True
                if ocean == "atlantic" and (
                    row == rows - 1 or column == columns - 1
                ):
                    return True
                for next_row, next_column in (
                    (row + 1, column),
                    (row - 1, column),
                    (row, column + 1),
                    (row, column - 1),
                ):
                    if (
                        0 <= next_row < rows
                        and 0 <= next_column < columns
                        and (next_row, next_column) not in seen
                        and heights[next_row][next_column]
                        <= heights[row][column]
                    ):
                        seen.add((next_row, next_column))
                        queue.append((next_row, next_column))
            return False

        result = []
        for row in range(rows):
            for column in range(columns):
                if reaches((row, column), "pacific") and reaches(
                    (row, column), "atlantic"
                ):
                    result.append([row, column])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((rows * columns)²)`

Each of the cells launches up to two walks, each flooding up to the whole grid.

##### Space Complexity: `O(rows * columns)`

One `seen` set per walk (plus the queue and the output).

#### Key Insights

- The border test makes each walk's success condition trivial to state.
- Every cell's walk recomputes the flow structure its neighbors already
  explored; on large grids this squares work that is almost shared.

### Reverse Two-Ocean DFS

#### Derivation

The forward version re-walks shared paths once per cell. Run the question backwards instead: which cells can reach the Pacific is the same set as which cells are reachable by climbing inland from the Pacific's border cells, where "climbing" reverses the flow direction, so the walk moves to neighbors with height `>=` the current cell's. Two floods, one seeded from each ocean's border, produce two reachability sets, and their intersection is the answer. Each flood visits every cell at most once, and nothing is recomputed:

1. Seed the Pacific set with the left column and top row; seed the Atlantic
   set with the right column and bottom row.
2. Flood each set inland: from a cell, recurse on in-bounds neighbors with
   height `>=` the current cell's height.
3. Return the cells present in both sets, in any order.

The reverse test needs no special-casing at the border: coastal cells enter their sets as seeds, and a neighbor of equal height flows both ways.

#### Walkthrough

Trace both floods on Example 1: `heights` is 3 rows by 5 columns. The Pacific flood seeds the top row and left column; the Atlantic seeds the bottom row and right column, and each expands inland over `>=` steps:

```text
pacific seeds   (0,0) (0,1) (0,2) (0,3) (0,4) (1,0) (2,0)
atlantic seeds  (2,0) (2,1) (2,2) (2,3) (2,4) (1,4) (0,4)

pacific flood growth (post-seed):
  from (0,0)=4 -> down (1,0)=7 seed; from (0,3)=3 -> down (1,3)=4 -> (1,2)=6
      -> down (2,2)=5 no; from (1,3): left (1,2)=6 -> up (0,2) seed
  from (0,1)=2 -> down (1,1)=4 (the only way in: from (1,2)=6 the step up-left to 4 is blocked)
pacific set    {(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0)}

atlantic flood growth (post-seed):
  from (2,4)=6 -> up (1,4)=7 seed -> left (1,3)=4 -> left (1,2)=6 -> up (0,2)=7
  from (2,1)=3 -> up (1,1)=4 -> left (1,0)=7 -> up (0,0)=4 no, down (2,0)=6 seed
atlantic set   {(0,2),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)}
```

The intersection is `[(0,2), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (2,0)]`, exactly Example 1's output. Note `(2,0)` appears in both sets: it is on both borders, water trickles off it into either ocean.

#### Solution

The code is the two seeded floods plus the scan-order intersection.

```python
from typing import List, Set, Tuple


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights:
            return []
        rows, columns = len(heights), len(heights[0])

        pacific = set()
        atlantic = set()

        def flood(row: int, column: int, reachable: Set[Tuple[int, int]]) -> None:
            if (row, column) in reachable:
                return
            reachable.add((row, column))
            for next_row, next_column in (
                (row + 1, column),
                (row - 1, column),
                (row, column + 1),
                (row, column - 1),
            ):
                if (
                    0 <= next_row < rows
                    and 0 <= next_column < columns
                    and heights[next_row][next_column]
                    >= heights[row][column]
                ):
                    flood(next_row, next_column, reachable)

        for row in range(rows):
            flood(row, 0, pacific)
            flood(row, columns - 1, atlantic)
        for column in range(columns):
            flood(0, column, pacific)
            flood(rows - 1, column, atlantic)

        return [
            [row, column]
            for row in range(rows)
            for column in range(columns)
            if (row, column) in pacific and (row, column) in atlantic
        ]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * columns)`

Each flood visits every cell at most once (the set membership guard rejects re-entry), and the seeds and intersection are linear scans.

##### Space Complexity: `O(rows * columns)`

Two reachability sets and the DFS stack, which on a snake path of equal heights can hold a full traversal.

#### Key Insights

- Reversing the flow direction (moving inland over `>=` neighbors) turns
  "which cells drain here?" from many searches into one per ocean.
- The intersection replaces all per-cell bookkeeping: a cell qualifies by
  membership, not by a successful walk.
- The `>=` (not `>`) is what lets water sit still: equal-height neighbors
  pass flow, and border cells of both oceans qualify through their seeds.

## Comparison of Solutions

### Time Complexity

- **Forward Search Per Cell**: `O((rows * columns)²)` - a fresh walk per cell per ocean.
- **Reverse Two-Ocean DFS**: `O(rows * columns)` - two floods total.

### Space Complexity

- **Forward Search Per Cell**: `O(rows * columns)` - one `seen` set at a time.
- **Reverse Two-Ocean DFS**: `O(rows * columns)` - two sets plus the DFS stack.

### Trade-offs

- The forward version is the direct transcription of the problem statement
  and is easy to trust; its cost squares with the grid size.
- The reverse version needs the flow-reversal insight but does constant
  work per cell, and its two sets are reusable for follow-up queries.

### When to Use Each

- **Forward Search Per Cell**: tiny grids, or as a cross-check oracle for
  the reverse version.
- **Reverse Two-Ocean DFS**: the intended solution; the same
  flood-from-the-border pattern solves any "reachability to a boundary"
  question (recommended here).

### Optimization Notes

- A single visited grid of three states (unvisited, pacific-only, both)
  replaces the two sets if memory is tight; the code gets branchier.
- The recursive DFS can be swapped for a BFS queue with identical bounds;
  recursion depth is bounded by the longest strictly-nonincreasing inland
  path, which worst cases push toward `rows * columns`.
- Cells on both borders (corners of Example 2's `[[1],[1]]`) are seeds of
  both floods and always qualify, which the intersection handles without
  special cases.
