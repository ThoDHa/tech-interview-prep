# [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)

**Medium** | **30 minutes** | **Array, BFS, Matrix**

**Pattern:** [Multi-Source BFS](../patterns/grid_bfs_multi_source/intuition.md)

**Algorithm:** [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/rotting_oranges/solution.py`](../../practice/rotting_oranges/solution.py)

You are given an `m x n` grid where each cell can have one of three values:

- `0` representing an empty cell,
- `1` representing a fresh orange, or
- `2` representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return `-1`.

## Examples

### Example 1

![Rotting Oranges Example 1](assets/rotting_oranges_example1.png)

**Input:** `grid = [[2,1,1],[1,1,0],[0,1,1]]`

**Output:** `4`

### Example 2

**Input:** `grid = [[2,1,1],[0,1,1],[1,0,1]]`

**Output:** `-1`

**Explanation:** The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

### Example 3

**Input:** `grid = [[0,2]]`

**Output:** `0`

**Explanation:** Since there are already no fresh oranges at minute 0, the answer is just 0.

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10`
- `grid[i][j]` is `0`, `1`, or `2`.

## Deriving the Solution

The rot spreads from every rotten orange at once, one ring of 4-directional neighbors per minute, and the answer is how many rings pass before no fresh orange remains. Both solutions advance the spread minute by minute; they differ in how much of the grid they look at to find each ring.

1. **Start literal.** Simulate the statement directly: each minute, scan the
   whole grid for fresh oranges touching a rotten one, and rot them all in one batch. Up to `O(m × n)` minutes of full rescans costs `O((m × n)²)`: see [Simulation](#simulation).
2. **Spot the waste.** Only the oranges that rotted last minute can rot anyone
   this minute, yet the simulation rescans every cell every minute, almost all of which cannot change.
3. **Track just the frontier.** Keep the most recently rotted oranges in a
   queue: seed it with every orange that starts rotten, then expand one level of neighbors per minute. That is multi-source breadth-first search, where each BFS level is one elapsed minute and every cell is touched a constant number of times, for `O(m × n)` total: see [Multi-Source BFS](#multi-source-bfs).

## Solutions

### Simulation

#### Derivation

The problem is a literal simulation: each minute, every fresh orange adjacent to a rotten one becomes rotten, and we count how many minutes pass before the grid stops changing. The most direct way to model this is to do exactly that, scanning the whole grid once per minute.

1. Count the fresh oranges. If there are none, return `0` immediately because no
   time has to elapse.
2. Each minute, scan every cell. For each fresh orange, check its four neighbors;
   if any neighbor is rotten, mark this orange for rotting. Collect these into a `to_rot` list rather than rotting in place.
3. Deferring the rot is essential. If a fresh orange were marked rotten the
   instant it is found, a later cell in the same scan could see it and rot in the same minute, collapsing two minutes of spread into one. Batching the changes keeps each minute's spread to a single ring.
4. If a full scan finds no orange to rot, the process has stalled. Stop and
   return `minutes` if no fresh oranges remain, otherwise `-1` for the unreachable survivors.

#### Walkthrough

Let us run the Simulation on Example 1: `grid = [[2,1,1],[1,1,0],[0,1,1]]`. Read the grid as 3 rows by 3 cols, where `2` is rotten, `1` is fresh, and `0` is empty. Up front we count `fresh = 6`, which is not zero, so we start the minute loop with `minutes = 0`.

Each minute, we scan the whole grid for fresh oranges that touch a rotten one, collect them in `to_rot`, then rot them all at once. The grid after each minute:

Starting grid:

```text
2 1 1
1 1 0
0 1 1
```

| Minute | `to_rot` (fresh cells next to rot) | Grid after rotting | `fresh` |
|--------|-------------------------------------|--------------------|---------|
| 1 | `(0,1)`, `(1,0)` | `2 2 1` / `2 1 0` / `0 1 1` | 4 |
| 2 | `(0,2)`, `(1,1)` | `2 2 2` / `2 2 0` / `0 1 1` | 2 |
| 3 | `(2,1)` | `2 2 2` / `2 2 0` / `0 2 1` | 1 |
| 4 | `(2,2)` | `2 2 2` / `2 2 0` / `0 2 2` | 0 |

Walking minute 1 in detail: cells `(0,1)` and `(0,2)` are both fresh, but only `(0,1)` has a rotten neighbor (the `2` at `(0,0)`), so `(0,2)` is left alone this minute. Cell `(1,0)` is fresh and sits below the rotten `(0,0)`, so it joins `to_rot`. We rot both together, which is why `(0,2)` does not also fall this minute: batching keeps one minute's spread to a single ring.

After minute 4, `fresh` reaches `0`. On the next scan `to_rot` is empty, so the loop breaks. Since `fresh == 0`, we return `minutes`, which is `4`. This matches the expected Output of `4`.

#### Solution

The code is the scan-batch-rot cycle from the walkthrough, repeated until a scan finds nothing to rot.

```python
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        fresh = sum(
            1 for r in range(rows) for c in range(cols) if grid[r][c] == 1
        )

        # No fresh oranges to begin with means zero minutes elapse.
        if fresh == 0:
            return 0

        minutes = 0
        while True:
            # Find every fresh orange that touches a rotten one this minute.
            to_rot = []
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == 1:
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 2:
                                to_rot.append((r, c))
                                break

            # No orange rots this minute means we have stalled.
            if not to_rot:
                break

            # Rot them all at once so this minute's spread does not cascade.
            for r, c in to_rot:
                grid[r][c] = 2
                fresh -= 1
            minutes += 1

        # Any fresh orange left unreachable means it can never rot.
        return minutes if fresh == 0 else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m × n)²)`

In the worst case the rot advances one ring per minute, which can take up to `O(m × n)` minutes, and each minute rescans all `m × n` cells. The product gives a quadratic bound in the number of cells.

##### Space Complexity: `O(m × n)`

The `to_rot` list can hold up to `O(m × n)` positions in a single minute. The grid is mutated in place, so no separate visited structure is needed.

#### Key Insights

- Direct simulation mirrors the problem statement, which makes it the easiest
  approach to derive and to convince yourself is correct.
- Batching the rotting into `to_rot` and applying it after the scan is the one
  subtlety: rotting in place would let one minute's spread leak into the next.
- The repeated full-grid rescans are wasted work, since most cells do not change
  between minutes. That inefficiency is exactly what the BFS approach removes.

### Multi-Source BFS

#### Derivation

The Simulation rescans all `m × n` cells every minute, yet the only oranges that can rot a neighbor this minute are the ones that rotted last minute. The fix is to remember that frontier instead of rediscovering it. The rot spreads outward from every rotten orange simultaneously, one ring of neighbors per minute, and that "all sources advance together, one step at a time" behavior is exactly multi-source [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search): seed the BFS frontier with *all* rotten oranges at once, then expand level by level, where each level corresponds to one elapsed minute.

1. Scan the grid once. Push every rotten orange (`2`) onto the queue and count
   the fresh oranges (`1`).
2. If there are no fresh oranges, the answer is `0` immediately (nothing has to
   rot, even if the grid is empty of oranges entirely).
3. Run BFS in level order. Before processing each level, increment `minutes`,
   then drain exactly the oranges that were rotten at the start of that minute.
4. For each rotten orange, rot any fresh 4-directional neighbor, decrement the
   fresh count, and enqueue it. Marking it rotten on enqueue prevents the same orange from being processed twice.
5. When the queue empties, return `minutes` if no fresh oranges remain,
   otherwise return `-1` because the survivors are unreachable.

Processing a full level per minute is what makes the minute count correct: every orange enqueued during minute `k` rots its neighbors at minute `k + 1`. The Invariant below states that formally, along with why the `fresh > 0` half of the loop guard is needed to stop the final level from adding a phantom minute.

#### Invariant

At the top of every pass of the `while` loop, the queue holds exactly the oranges that became rotten at minute `minutes`:

$$ \textit{queue} = \{\,\text{cells that rotted at minute } \textit{minutes}\,\} $$

```text
at the top of every while pass:
    queue = { cells that rotted at minute minutes }
    (initially minutes = 0 and queue holds the cells already rotten in the input)
```

It starts true: `minutes` is `0` and the queue holds the oranges already rotten in the input, which is the level-`0` frontier. Each pass preserves it. The `for _ in range(len(queue))` snapshot fixes the level size before any append, so the pass drains precisely that level and everything appended during it belongs to the next one. Incrementing `minutes` *before* the drain is what labels that next level correctly: the oranges enqueued during the pass are the ones that rot at the new `minutes`, so the loop re-enters one level deeper with the property restored.

The `fresh > 0` guard is what keeps the final level from being counted. After the pass that rots the last fresh orange, `minutes` already holds the answer, yet the queue is not empty: it still carries that final level, whose oranges have no fresh neighbors left to rot. Under `while queue` alone the loop would run once more, increment `minutes` one past the answer, drain the level, rot nothing, and return an off-by-one count. Testing `fresh > 0` stops the moment there is nothing left to rot, so the last harmless level never adds a phantom minute.

The other exit, an empty queue with `fresh > 0`, means the survivors are unreachable. `minutes` is over-counted by one there as well, and it does not matter: that branch returns `-1`.

#### Walkthrough

Let us run the BFS by hand on Example 1: `grid = [[2,1,1],[1,1,0],[0,1,1]]`. The seeding scan pushes the one rotten orange onto the queue and counts the fresh ones: `queue = [(0,0)]`, `fresh = 6`. Since `fresh` is not zero, the level loop starts with `minutes = 0`. Each pass below increments `minutes`, drains exactly the snapshot `len(queue)` oranges, and rots their fresh neighbors, enqueueing each as it rots:

```text
seed        queue = [(0,0)]              fresh = 6    minutes = 0
minute 1    drain (0,0)      rot (0,1), (1,0)      queue = [(0,1), (1,0)]    fresh = 4
minute 2    drain (0,1)      rot (0,2), (1,1)      queue = [(0,2), (1,1)]    fresh = 2
            drain (1,0)      no fresh neighbors
minute 3    drain (0,2)      no fresh neighbors    queue = [(2,1)]           fresh = 1
            drain (1,1)      rot (2,1)
minute 4    drain (2,1)      rot (2,2)             queue = [(2,2)]           fresh = 0
```

The grid after each minute, with the level just rotted spreading one ring further from the corner source:

```text
start       2 1 1 / 1 1 0 / 0 1 1
minute 1    2 2 1 / 2 1 0 / 0 1 1
minute 2    2 2 2 / 2 2 0 / 0 1 1
minute 3    2 2 2 / 2 2 0 / 0 2 1
minute 4    2 2 2 / 2 2 0 / 0 2 2
```

Minute 2 shows the frontier in action: `(0,1)` rots `(0,2)` and `(1,1)`, while `(1,0)` finds all its neighbors already rotten or empty, so it contributes nothing. The `for _ in range(len(queue))` snapshot keeps the freshly enqueued `(0,2)` and `(1,1)` out of this pass; they wait for minute 3.

After minute 4, `fresh` is `0`, so the `fresh > 0` half of the guard stops the loop even though the queue still holds `(2,2)`: draining that last level would rot nothing and would only push `minutes` past the answer. The function returns `minutes = 4`, matching the expected Output of `4`.

#### Solution

The code is the level loop from the walkthrough: seed all sources, then one snapshot-sized drain per minute.

```python
from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        # Seed the queue with every rotten orange and count fresh ones.
        queue = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        # No fresh oranges to begin with means zero minutes elapse.
        if fresh == 0:
            return 0

        minutes = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Process the grid one minute (one BFS level) at a time.
        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2  # rot it now so it isn't queued twice
                        fresh -= 1
                        queue.append((nr, nc))

        # Any fresh orange left unreachable means it can never rot.
        return minutes if fresh == 0 else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The initial scan touches every cell once. During BFS each cell is enqueued at most once and dequeued at most once, and each dequeue inspects four neighbors. Total work is linear in the number of cells.

##### Space Complexity: `O(m × n)`

In the worst case (the whole grid starts rotten) the queue holds every cell at once. No separate visited structure is needed because the grid itself records state by flipping `1` to `2`.

#### Key Insights

- Multi-source BFS handles simultaneous spread cleanly: seed every source first,
  then a single level of expansion equals a single minute.
- Counting fresh oranges up front gives an O(1) termination check and lets us
  distinguish "all rotted" from "some unreachable" without re-scanning.
- Rotting a neighbor at enqueue time (not dequeue time) is the standard guard
  that keeps each cell out of the queue more than once.
- The `if fresh == 0: return 0` guard covers the subtle corner case where the grid
  has no fresh oranges, so zero minutes elapse even if rotten oranges exist.
- Looping `for _ in range(len(queue))` snapshots the current frontier size,
  which is the trick that separates one minute's oranges from the next.

## Comparison of Solutions

### Time Complexity

- **Simulation**: `O((m × n)²)` - up to `O(m × n)` minutes, each rescanning all
  `m × n` cells.
- **Multi-Source BFS**: `O(m × n)` - every cell is enqueued and dequeued at most
  once.

### Space Complexity

- **Simulation**: `O(m × n)` - the `to_rot` batch can hold every cell in one
  minute.
- **Multi-Source BFS**: `O(m × n)` - the queue can hold every cell when the whole
  grid starts rotten.

### Trade-offs

- Simulation reads exactly like the problem statement, so it is the quickest to
  write and verify, but it pays for that clarity with repeated full-grid scans.
- Multi-Source BFS touches each cell a constant number of times by tracking the
  active frontier, at the cost of recognizing the spread as a level-order graph traversal.

### When to Use Each

- **Simulation**: Reach for it when the grid is small (here `m, n <= 10`) and
  readability matters more than asymptotic speed, or as a correctness reference.
- **Multi-Source BFS** (recommended): The right call for larger grids or when
  optimal linear time is required.

### Optimization Notes

- Both approaches mutate the grid in place to record rotten cells, avoiding a
  separate visited matrix.
- Counting fresh oranges up front gives both an O(1) termination test and a clean
  way to distinguish "all rotted" from "some unreachable."
- The BFS guard of rotting a neighbor at enqueue time (rather than dequeue time)
  is what keeps each cell out of the queue more than once; the simulation's equivalent guard is batching changes into `to_rot` before applying them.
