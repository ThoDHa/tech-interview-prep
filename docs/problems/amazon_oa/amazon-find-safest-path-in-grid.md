# [Find the Safest Path in a Grid](https://www.fastprep.io/problems/amazon-find-safest-path-in-grid)

**Hard** | **NN minutes** | **Array, Matrix, Breadth First Search, Binary Search, Heap, Shortest Path**

You are given an n x n binary matrix grid. A cell containing 1 contains a thief, and a cell containing 0 is empty.

Start at (0, 0) and move to (n - 1, n - 1). Each move goes one cell up, down, left, or right, and a path may pass through a thief cell.

The safeness factor of a path is the minimum Manhattan distance from any cell on that path to any thief in the grid. Return the maximum safeness factor among all paths from the start to the destination.

The Manhattan distance between (r, c) and (x, y) is |r - x| + |c - y|.

## Examples

### Example 1

**Input:** `grid = [[1,0,0],[0,0,0],[0,0,1]]`

**Output:** `0`

**Explanation:** The start and destination both contain thieves, so every path has safeness factor 0.

### Example 2

**Input:** `grid = [[0,0,1],[0,0,0],[0,0,0]]`

**Output:** `2`

**Explanation:** A path through the left and bottom area stays at least Manhattan distance 2 from the thief at (0, 2), and no path can do better.

### Example 3

**Input:** `grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]`

**Output:** `2`

**Explanation:** A route through the central corridor remains at least distance 2 from both corner thieves.

## Constraints

- `1 <= grid.length == n <= 400`
- `grid[i].length == n`
- `grid[i][j] is 0 or 1.`
- `The grid contains at least one thief.`

## Solutions

### Brute Force Path Enumeration

#### Derivation

The most literal reading of the objective: a path's safeness factor is the smallest nearest-thief distance along it, and we want the best path. So enumerate paths from the start to the destination, score each one, and keep the maximum. Revisiting a cell can never raise a path's score (cutting the loop out leaves a simple path whose minimum is at least as high), so the enumeration only needs simple paths, each cell visited once, which a recursive walk with a `visited` marker produces naturally:

1. Collect `thieves`, the list of thief coordinates, so any cell's nearest-thief distance is one scan over that list.
2. Walk paths with `explore(row, col, safeness_so_far)`, where `safeness_so_far` is the smallest nearest-thief distance seen so far, including the current cell.
3. From each cell, recurse into the four neighbors that are in bounds and unvisited, passing `min(safeness_so_far, distance_to_nearest_thief(next_row, next_col))`.
4. On reaching `(size - 1, size - 1)`, fold the path's score into `best_safeness`.
5. Un-mark the cell when the recursion backtracks, so other paths may reuse it; return `best_safeness` after the initial call completes.

#### Walkthrough

Example 2: `grid = [[0,0,1],[0,0,0],[0,0,0]]`. The thief sits at `(0, 2)`, and the nearest-thief distance of every cell is fixed by the Manhattan metric:

```text
distance to nearest thief
2 1 0
3 2 1
4 3 2
```

`explore(0, 0, 2)` expands neighbors in the order right, down, left, up. Two branches decide the outcome:

```text
explore(0,0, safeness=2)
  explore(0,1, min(2,1)=1)          first branch heads east
    explore(0,2, min(1,0)=0)        steps onto the thief cell
      ... every completion keeps the minimum at 0
      reaches (2,2) with 0 -> best_safeness = 0
  explore(1,0, min(2,3)=2)          second branch heads south
    explore(2,0, min(2,4)=2)
      explore(2,1, min(2,3)=2)
        explore(2,2, min(2,2)=2)   destination along the bottom row
        best_safeness = max(0, 2) = 2
```

No path can beat 2, because every path includes the start cell whose distance is 2, and the south branch achieves exactly 2. Every remaining path threads through one of these two frontiers and scores no higher, so the search ends with `best_safeness = 2`, the expected Output for Example 2.

#### Solution

The code is the walkthrough's walk: score the start, recurse with the folded minimum, and close each path at the destination.

```python
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        size = len(grid)
        thieves = [(row, col)
                   for row in range(size)
                   for col in range(size)
                   if grid[row][col] == 1]

        def distance_to_nearest_thief(row: int, col: int) -> int:
            return min(abs(row - thief_row) + abs(col - thief_col)
                       for thief_row, thief_col in thieves)

        visited = [[False] * size for _ in range(size)]
        best_safeness = 0

        def explore(row: int, col: int, safeness_so_far: int) -> None:
            nonlocal best_safeness
            if row == size - 1 and col == size - 1:
                best_safeness = max(best_safeness, safeness_so_far)
                return

            visited[row][col] = True
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_row, next_col = row + dr, col + dc
                if (0 <= next_row < size and 0 <= next_col < size
                        and not visited[next_row][next_col]):
                    explore(next_row, next_col,
                            min(safeness_so_far,
                                distance_to_nearest_thief(next_row, next_col)))
            visited[row][col] = False

        explore(0, 0, distance_to_nearest_thief(0, 0))
        return best_safeness
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^(n^2) × t)`

The recursion walks every simple path, and each step branches to at most three unvisited neighbors, so the path count grows exponentially in the `n^2` cells; `t` is the thief count, paid per step to rescore the nearest-thief distance.

##### Space Complexity: `O(n^2)`

The visited matrix plus the recursion stack, which grows with the longest simple path.

#### Key Insights

- Cutting a loop out of a path removes cells from the minimum, so the best simple path is at least as good as any walk; enumerating simple paths loses no answers.
- The path score is computed incrementally: `min(safeness_so_far, ...)` folds in each new cell, so reaching the destination is all that closes a path.
- Un-marking on backtrack (`visited[row][col] = False`) is what lets paths share prefixes without confusing distinct walks.
- The exponential path count confines this approach to tiny grids; the two solutions below reframe the search.

### Binary Search on the Safeness Factor

#### Derivation

The brute force searches over paths. Flip the question: fix a candidate value `target_safeness` and ask whether any path survives it. A path with safeness factor at least `target_safeness` may only step on cells whose own nearest-thief distance is at least `target_safeness`, so the check becomes ordinary reachability: start from `(0, 0)` and BFS across cells with distance at least the target. Feasibility is monotone, since a path that survives a stricter target survives any looser one, and monotone feasibility is exactly the structure [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) needs:

1. Precompute `distance[row][col]`, the Manhattan distance from every cell to its nearest thief, with a multi-source BFS seeded from all thieves at layer 0; on an unobstructed grid the BFS layer of a cell equals its Manhattan distance to the nearest seed.
2. Binary search `target_safeness` in `[0, distance[0][0]]`: no path can beat the start cell's own distance, because the start sits on every path.
3. `reachable(target_safeness)` runs a BFS from the start over in-bounds, unvisited cells with `distance >= target_safeness` and reports whether the destination was reached.
4. Keep the largest feasible target and return it.

#### Walkthrough

Example 3: `grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]`, thieves at `(0, 3)` and `(3, 0)`. The multi-source BFS assigns:

```text
distance
3 2 1 0
2 3 2 1
1 2 3 2
0 1 2 3
```

`distance[0][0] = 3` bounds the search interval at `[0, 3]`:

```text
mid = (0 + 3 + 1) // 2 = 2
  reachable(2)   queue = [(0,0)]
  pop (0,0) d3   right (0,1) d2 in, down (1,0) d2 in
  pop (0,1) d2   right (0,2) d1 rejected, down (1,1) d3 in
  pop (1,0) d2   right (1,1) already queued, down (2,0) d1 rejected
  pop (1,1) d3   right (1,2) d2 in, down (2,1) d2 in
  pop (1,2) d2   right (1,3) d1 rejected, down (2,2) d3 in
  pop (2,1) d2   down (3,1) d1 rejected, left (2,0) d1 rejected
  pop (2,2) d3   right (2,3) d2 in, down (3,2) d2 in
  pop (2,3) d2   down (3,3) d3 in
  pop (3,2) d2   neighbors rejected or already queued
  pop (3,3) d3   destination -> feasible
  low = 2
mid = (2 + 3 + 1) // 2 = 3
  reachable(3): (0,0) d3 stands, but (1,0) d2 and (0,1) d2 are
  rejected, so the frontier dies before leaving the corner
  infeasible -> high = 2
low == high == 2 -> return 2
```

The corridor of distance-2-or-more cells carries the path to `(3, 3)`, and target 3 strands the start immediately, so the answer is 2, the expected Output for Example 3.

#### Solution

The code is the distance map, the monotone reachability check, and the binary search that brackets the largest feasible target.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        size = len(grid)
        distance = [[-1] * size for _ in range(size)]
        queue = deque()
        for row in range(size):
            for col in range(size):
                if grid[row][col] == 1:
                    distance[row][col] = 0
                    queue.append((row, col))
        while queue:
            row, col = queue.popleft()
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_row, next_col = row + dr, col + dc
                if (0 <= next_row < size and 0 <= next_col < size
                        and distance[next_row][next_col] == -1):
                    distance[next_row][next_col] = distance[row][col] + 1
                    queue.append((next_row, next_col))

        def reachable(target_safeness: int) -> bool:
            visited = [[False] * size for _ in range(size)]
            visited[0][0] = True
            queue = deque([(0, 0)])
            while queue:
                row, col = queue.popleft()
                if row == size - 1 and col == size - 1:
                    return True
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    next_row, next_col = row + dr, col + dc
                    if (0 <= next_row < size and 0 <= next_col < size
                            and not visited[next_row][next_col]
                            and distance[next_row][next_col] >= target_safeness):
                        visited[next_row][next_col] = True
                        queue.append((next_row, next_col))
            return False

        low, high = 0, distance[0][0]
        while low < high:
            mid = (low + high + 1) // 2
            if reachable(mid):
                low = mid
            else:
                high = mid - 1
        return low
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2 log n)`

The multi-source BFS fills the distance map in one pass over the `n^2` cells, and each of the `O(log n)` binary search rounds runs one `O(n^2)` reachability BFS.

##### Space Complexity: `O(n^2)`

The distance map plus the visited matrix and queue of one reachability check.

#### Key Insights

- Multi-source BFS from every thief at once computes each cell's nearest-thief distance in a single pass; on an open grid the BFS layer equals the Manhattan distance, so no per-cell scan is needed.
- Asking "does a path with safeness factor at least `target_safeness` exist" converts a max-min optimization into a reachability question, and monotone feasibility invites binary search.
- `distance[0][0]` is a tight upper bound: the start cell lies on every path, so no path can score above it.
- Biasing `mid` upward with `(low + high + 1) // 2` keeps the `low = mid` branch making progress when the interval shrinks to two values.

### Bottleneck Dijkstra

#### Derivation

The binary search answers a family of yes/no questions to converge on the answer. [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) answers the question directly in one sweep. The classic version minimizes a path sum; the bottleneck variant maximizes a path minimum, and the same greedy argument carries over: when the cell with the best-yet bottleneck leaves the priority queue, no later route can improve it, so its value is final. Relaxation swaps the sum for a minimum: the best bottleneck of a path ending at a neighbor is `min(safeness, distance[next_row][next_col])`, because the path minimum cannot exceed any cell it visits:

1. Compute the same `distance` map with the multi-source BFS from the previous section.
2. Track `best_safeness[row][col]`, the largest bottleneck found so far to reach that cell; initialize the start with `distance[0][0]` and everyone else below zero (`-1`, since safeness factors are non-negative).
3. Seed a max-heap with the start. Python's `heapq` is a min-heap, so bottlenecks travel negated and are restored on pop.
4. Pop the cell with the greatest bottleneck and skip stale entries, whose bottleneck trails the recorded `best_safeness`. Relax each neighbor with `next_safeness = min(safeness, distance[next_row][next_col])`; when it beats the neighbor's recorded best, update and push.
5. When the heap empties, `best_safeness[size - 1][size - 1]` holds the answer.

#### Walkthrough

Example 2 again, whose distance map appeared in the first walkthrough:

```text
distance
2 1 0
3 2 1
4 3 2
```

The start's bottleneck is `distance[0][0] = 2`. Heap entries are written `(safeness, cell)` here; in the code the safeness travels negated:

```text
pop (2, (0,0))   relax (0,1) min(2,1)=1, (1,0) min(2,3)=2
                 push (1,(0,1)), (2,(1,0))
pop (2, (1,0))   relax (1,1) min(2,2)=2, (2,0) min(2,4)=2
                 push (2,(1,1)), (2,(2,0))
pop (2, (1,1))   relax (1,2) min(2,1)=1, (2,1) min(2,3)=2
                 push (1,(1,2)), (2,(2,1))
pop (2, (2,0))   relax (2,1): min(2,3)=2 does not beat best 2 -> no push
pop (2, (2,1))   relax (2,2) min(2,2)=2 -> push (2,(2,2))
pop (2, (2,2))   relaxations find nothing better
...
return best_safeness[2][2] = 2
```

The corridor cells `(1,0)`, `(2,0)`, and `(2,1)` all finalize at bottleneck 2, so the destination `(2,2)` settles at 2, the expected Output for Example 2. Any entry popped later whose safeness trails its cell's recorded best was pushed before a better route appeared and is discarded by the `safeness < best_safeness` guard.

#### Solution

The code is the greedy sweep from the walkthrough: pop the best bottleneck, relax with `min`, and read the answer off the destination's recorded best.

```python
from collections import deque
from heapq import heappop, heappush
from typing import List


class Solution:
    def solve(self, grid: List[List[int]]) -> int:
        size = len(grid)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        distance = [[-1] * size for _ in range(size)]
        queue = deque()
        for row in range(size):
            for col in range(size):
                if grid[row][col] == 1:
                    distance[row][col] = 0
                    queue.append((row, col))
        while queue:
            row, col = queue.popleft()
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if (0 <= next_row < size and 0 <= next_col < size
                        and distance[next_row][next_col] == -1):
                    distance[next_row][next_col] = distance[row][col] + 1
                    queue.append((next_row, next_col))

        best_safeness = [[-1] * size for _ in range(size)]
        best_safeness[0][0] = distance[0][0]
        heap = [(-best_safeness[0][0], 0, 0)]
        while heap:
            negated_safeness, row, col = heappop(heap)
            safeness = -negated_safeness
            if safeness < best_safeness[row][col]:
                continue
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if 0 <= next_row < size and 0 <= next_col < size:
                    next_safeness = min(safeness, distance[next_row][next_col])
                    if next_safeness > best_safeness[next_row][next_col]:
                        best_safeness[next_row][next_col] = next_safeness
                        heappush(heap, (-next_safeness, next_row, next_col))

        return best_safeness[size - 1][size - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2 log n)`

The distance map costs one `O(n^2)` BFS; `best_safeness` only improves, and each improvement pushes once, so the heap handles `O(n^2)` entries at `O(log n)` each.

##### Space Complexity: `O(n^2)`

The distance map, the best-safeness matrix, and the heap.

#### Key Insights

- The problem is a maximum-bottleneck path: maximize the minimum cell weight along the route, which Dijkstra settles in one greedy sweep instead of one reachability check per candidate.
- Negating the bottleneck turns Python's min-heap into the max-heap the greedy needs.
- The only change from classic Dijkstra is the relaxation rule: `min(safeness, distance[next_row][next_col])` in place of `safeness + edge_weight`.
- Updating `best_safeness` at push time caps the heap at one entry per improvement, and the pop-time guard discards the entries a later improvement stranded.

## Comparison of Solutions

### Time Complexity

- **Brute Force Path Enumeration**: `O(3^(n^2) × t)` - every simple path is walked, with a thief rescore at each step.
- **Binary Search on the Safeness Factor**: `O(n^2 log n)` - one distance BFS plus `O(log n)` linear reachability sweeps.
- **Bottleneck Dijkstra**: `O(n^2 log n)` - one distance BFS plus a priority-queue sweep with logarithmic pops.

### Space Complexity

- **Brute Force Path Enumeration**: `O(n^2)` - the visited matrix and the recursion stack.
- **Binary Search on the Safeness Factor**: `O(n^2)` - the distance map, plus one visited matrix and queue at a time.
- **Bottleneck Dijkstra**: `O(n^2)` - two matrices and the heap.

### Trade-offs

- The brute force needs no preprocessing and no insight beyond "walk the paths", but it is unusable beyond trivial grids.
- The binary search turns the optimization into yes/no reachability with two standard tools, but it pays `O(log n)` full-grid sweeps where one sweep could finish the job.
- Dijkstra finalizes the answer in a single sweep and generalizes to any per-cell weights, but its greedy finalization argument is the hardest of the three to state.

### When to Use Each

- **Brute Force Path Enumeration**: tiny grids, or as the reference implementation that cross-checks the faster approaches.
- **Binary Search on the Safeness Factor (Recommended)**: the interview sweet spot: multi-source BFS and binary search compose into the optimal complexity without a new algorithm.
- **Bottleneck Dijkstra**: when the maximum-minimum pattern is already familiar, or when the weights vary in a way a flat threshold cannot express.

### Optimization Notes

- The distance map earns its cost in both fast approaches: one global BFS replaces an `O(t)` thief scan at every cell.
- The reachability check allocates a fresh `visited` matrix per round; for large grids, a generation counter (one integer per cell, compared against the current round number) avoids the reallocation.
- In Dijkstra, recording `best_safeness` the moment a better bottleneck is pushed keeps the heap to one entry per improvement; updating only at pop would admit duplicate entries that the guard then discards.
