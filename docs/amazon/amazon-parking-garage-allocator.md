# [Parking Garage Allocator](https://www.fastprep.io/problems/amazon-parking-garage-allocator)

**Medium** | **NN minutes** | **Array, Simulation, String**

Manage spaceCount parking spaces. Each operation is "PARK size" or "LEAVE start size". A park request occupies the leftmost available run of the requested size and contributes its starting index, or -1 when no run fits. A leave operation frees the stated valid occupied range and contributes no output.

Sizes are 1, 2, or 3.

## Examples

### Example 1

**Input:** `spaceCount = 6`, `operations = ["PARK 2","PARK 3","LEAVE 0 2","PARK 1"]`

**Output:** `[0,2,0]`

**Explanation:** The final request reuses the leftmost freed space.

### Example 2

**Input:** `spaceCount = 2`, `operations = ["PARK 3","PARK 2"]`

**Output:** `[-1,0]`

**Explanation:** The oversized request fails without changing state.

## Constraints

- `1 <= spaceCount, operations.length <= 100000.`
- `Every leave operation refers to a currently occupied range.`

## Deriving the Solution

Two operations, and every park asks one question: where does the leftmost run of `size` consecutive free spaces begin? The approaches below differ only in how the garage remembers its free space, and the ladder re-represents that state three times, each step buying a cheaper answer for the next park.

1. **Start literal.** Keep one boolean per space and scan candidate starts left to right for the first all-free window: see [Occupancy-Array Scan](#occupancy-array-scan).
2. **Spot the waste.** The array stores every space, but only the gaps between occupied islands matter: a garage with one occupied corner still walks up to a hundred thousand cells on every park.
3. **Fix it.** Keep only the free runs, sorted by start; the first run long enough is the leftmost fit, and a leave re-inserts its range while absorbing the free runs that touch it: see [Free-Interval First Fit](#free-interval-first-fit).
4. **Hand the bookkeeping to the library.** The one search the design still writes by hand, a leave's insertion point, is a `bisect` call away: see [Free-Interval First Fit with Bisect](#free-interval-first-fit-with-bisect).

## Solutions

### Occupancy-Array Scan

#### Derivation

The statement's most literal reading: the garage is a row of spaces, each either occupied or free, and a park is a search for the first window that fits:

1. Keep `occupied`, one boolean per space, all false for the empty garage.
2. On `PARK size`: try every `start` from `0` through `spaceCount - size`; the first window with no occupied cell wins, occupy its cells, and contribute `start`. Contribute `-1` when no window fits.
3. On `LEAVE start size`: clear the cells `start` through `start + size - 1` and contribute nothing. The parameter is named `size` and the statement fixes "Sizes are 1, 2, or 3", naming a length rather than a position, so the second argument counts the freed cells; the occupied-range guarantee then makes `start` through `start + size - 1` exactly the run a car holds.
4. Collect the contributions of the park operations in order.

This is the statement's definition transcribed directly, which makes it the oracle the faster versions are checked against.

#### Walkthrough

Example 1, the occupancy array after each operation (`#` occupied, `.` free):

```text
operation    occupied 0..5            result
PARK 2       [# # . . . .]            0
PARK 3       [# # # # # .]            2
LEAVE 0 2    [. . # # # .]
PARK 1       [# . # # # .]            0
```

The parks collect into `[0,2,0]`, matching the expected Output. The final park reuses cell 0, freed by the preceding leave, because the scan meets it first.

#### Solution

```python
from typing import List


class Solution:
    def processParking(self, spaceCount: int, operations: List[str]) -> List[int]:
        occupied = [False] * spaceCount
        results: List[int] = []
        for operation in operations:
            parts = operation.split()
            if parts[0] == "PARK":
                size = int(parts[1])
                placed = -1
                for start in range(spaceCount - size + 1):
                    if not any(occupied[start:start + size]):
                        placed = start
                        break
                if placed >= 0:
                    for cell in range(placed, placed + size):
                        occupied[cell] = True
                results.append(placed)
            else:
                start, size = int(parts[1]), int(parts[2])
                for cell in range(start, start + size):
                    occupied[cell] = False
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

`m` operations; a park scans up to `spaceCount - size + 1` candidate starts and each window check costs at most `size <= 3` reads, so O(n) per park in the worst case, whatever the occupancy. A leave is O(1).

##### Space Complexity: `O(n)`

One boolean per space, plus one output per park.

#### Key Insights

- The cost tracks the garage's size, not its free space: an almost-empty garage pays the same scan as a full one.
- The leave branch is the cheapest code and the most dangerous to get wrong: clearing one cell too many corrupts every later park that lands there.
- As the definition written down, this version is the independent oracle for the gauntlet: it shares no mechanism with the interval versions below.

### Free-Interval First Fit

#### Derivation

The scan re-reads occupied cells it could have skipped, because the array forgets which stretches are entirely free. The repair is to remember exactly that: the garage's free space is always a set of maximal runs, and a fresh garage is a single run spanning the whole row. Keep those runs sorted by start; then the leftmost run of at least `size` spaces is simply the first run in list order that is long enough, and a leave only has to put its range back, absorbing the free runs that touch it:

1. Keep `free_runs`, a list of `(run_start, run_end)` pairs sorted by `run_start`, pairwise disjoint, and never adjacent.
2. On `PARK size`: walk `free_runs` left to right; the first run with `run_end - run_start >= size` is the fit. Shrink it from its start, delete it on an exact fit, and return its `run_start`. Return `-1` after the walk fails.
3. On `LEAVE start size`: binary-search the first run starting at or after `start`; absorb a left neighbor ending exactly at `start`, absorb a right neighbor starting exactly at `start + size`, and insert one merged run at the surviving index.
4. Collect the park results in order; leaves contribute nothing.

#### Invariant

`free_runs` is sorted by start, its runs are pairwise disjoint, and no two runs touch:

```text
fresh garage:  free_runs = [(0, spaceCount)]
park:          the chosen run shrinks from its start or vanishes;
               a vanished run leaves occupied cells on both sides,
               so its neighbors still do not touch
leave:         the statement guarantees the freed range is occupied,
               so the runs that touch it are exactly the left neighbor
               ending at freed_start and the right neighbor starting at
               freed_end; absorbing them and inserting one merged run
               restores the no-touch property
```

The payoff is that step 2 needs no separate leftmost logic: with the runs sorted and separated, first fit in list order is the statement's leftmost available run. The same invariant caps a leave's work: exactly two equality checks decide the merge, and the run count rises by at most one per leave.

#### Walkthrough

Example 1 never merges (its freed range touches no free run), so this trace uses a longer tailored sequence, `spaceCount = 7` with `operations = ["PARK 3","PARK 2","PARK 2","LEAVE 0 3","LEAVE 5 2","LEAVE 3 2","PARK 3"]`, chosen to force both one-sided merges and the two-sided one:

```text
operation    free_runs                          result
PARK 3       [(3, 7)]                           0
PARK 2       [(5, 7)]                           3
PARK 2       []                                 5
LEAVE 0 3    [(0, 3)]                           no free neighbor touches it
LEAVE 5 2    [(0, 3), (5, 7)]                   no free neighbor touches it
LEAVE 3 2    left neighbor (0, 3) ends at 3 and
             right neighbor (5, 7) starts at 5:
             both absorbed -> [(0, 7)]
PARK 3       [(3, 7)]                           0
```

The parks collect into `[0,3,5,0]`. The final park is the merge paying off: only the coalesced run `(0, 7)` can hold three consecutive spaces, and it holds them at index 0.

#### Solution

The code is the invariant written down: the park walk shrinks or deletes, and the leave absorbs neighbors around the insertion point.

```python
from typing import List, Tuple


class Solution:
    def processParking(self, spaceCount: int, operations: List[str]) -> List[int]:
        free_runs: List[Tuple[int, int]] = [(0, spaceCount)]
        results: List[int] = []
        for operation in operations:
            parts = operation.split()
            if parts[0] == "PARK":
                size = int(parts[1])
                placed = -1
                for run_index, (run_start, run_end) in enumerate(free_runs):
                    if run_end - run_start >= size:
                        placed = run_start
                        if run_end - run_start == size:
                            del free_runs[run_index]
                        else:
                            free_runs[run_index] = (run_start + size, run_end)
                        break
                results.append(placed)
            else:
                freed_start, freed_size = int(parts[1]), int(parts[2])
                freed_end = freed_start + freed_size
                low, high = 0, len(free_runs)
                while low < high:
                    middle = (low + high) // 2
                    if free_runs[middle][0] < freed_start:
                        low = middle + 1
                    else:
                        high = middle
                insertion = low
                if insertion > 0 and free_runs[insertion - 1][1] == freed_start:
                    freed_start = free_runs[insertion - 1][0]
                    del free_runs[insertion - 1]
                    insertion -= 1
                if insertion < len(free_runs) and free_runs[insertion][0] == freed_end:
                    freed_end = free_runs[insertion][1]
                    del free_runs[insertion]
                free_runs.insert(insertion, (freed_start, freed_end))
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * g)`

`m` operations and `g` the live free-run count: a park scans at most `g` runs and a leave binary-searches in O(log g) before list deletions and an insertion that move O(g) entries in the worst case. Fragmentation bounds `g` by the number of occupied islands, so the bound is O(n) per operation at worst and typically far below it: a fresh garage is one run whatever its capacity.

##### Space Complexity: `O(g)`

One run per occupied island, O(n) worst case, plus one output per park.

#### Key Insights

- The state tracks fragmentation, not capacity: the empty 100000-space garage and the empty one-space garage are the same single run.
- Runs that never touch reduce a leave to two equality checks; both merges firing at once still end in one insert.
- The statement's guarantee that every leave names a currently occupied range is load-bearing: the design never re-validates it, and the merge tests may look only one run to each side.

### Free-Interval First Fit with Bisect

#### Derivation

The interval design writes exactly one search by hand: the leave's binary hunt for the first run starting at or after `freed_start`. That is a plain leftmost insertion point over run starts, which is [`bisect.bisect_left`](https://docs.python.org/3/library/bisect.html) with a `key`. The park keeps its left-to-right walk, because "first run long enough" has no binary-search form over a list sorted by start rather than length, and the merges stay as they were. The algorithm is unchanged; only the hand-written loop disappears:

1. Keep `free_runs` exactly as before.
2. On `PARK size`: the same first-fit walk.
3. On `LEAVE start size`: `insertion = bisect.bisect_left(free_runs, freed_start, key=lambda run: run[0])`, then the same two merge checks and one insert.
4. Collect the park results in order.

#### Walkthrough

Example 1 again, now showing the `bisect` decision inside the leave:

```text
operation    free_runs                          result
PARK 2       [(2, 6)]                           0
PARK 3       [(5, 6)]                           2
LEAVE 0 2    bisect_left for start 0 -> insertion 0:
             no left neighbor, and the right neighbor
             (5, 6) starts at 5, not 2: plain insert
             [(0, 2), (5, 6)]
PARK 1       walk finds (0, 2) first -> [(1, 2), (5, 6)]     0
```

The parks collect into `[0,2,0]`, matching the expected Output, with the freed range landing at index 0 exactly where the hand-written loop would have put it.

#### Solution

```python
import bisect
from typing import List, Tuple


class Solution:
    def processParking(self, spaceCount: int, operations: List[str]) -> List[int]:
        free_runs: List[Tuple[int, int]] = [(0, spaceCount)]
        results: List[int] = []
        for operation in operations:
            parts = operation.split()
            if parts[0] == "PARK":
                size = int(parts[1])
                placed = -1
                for run_index, (run_start, run_end) in enumerate(free_runs):
                    if run_end - run_start >= size:
                        placed = run_start
                        if run_end - run_start == size:
                            del free_runs[run_index]
                        else:
                            free_runs[run_index] = (run_start + size, run_end)
                        break
                results.append(placed)
            else:
                freed_start, freed_size = int(parts[1]), int(parts[2])
                freed_end = freed_start + freed_size
                insertion = bisect.bisect_left(
                    free_runs, freed_start, key=lambda run: run[0]
                )
                if insertion > 0 and free_runs[insertion - 1][1] == freed_start:
                    freed_start = free_runs[insertion - 1][0]
                    del free_runs[insertion - 1]
                    insertion -= 1
                if insertion < len(free_runs) and free_runs[insertion][0] == freed_end:
                    freed_end = free_runs[insertion][1]
                    del free_runs[insertion]
                free_runs.insert(insertion, (freed_start, freed_end))
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * g)`

Same algorithm, same bounds: `bisect` speeds the search to O(log g), but the surrounding list deletions and insertion keep every operation at O(g) worst case over the `g` live free runs.

##### Space Complexity: `O(g)`

Identical state: one run per occupied island, plus one output per park.

#### Key Insights

- The `key` parameter is what makes the flat list searchable by `run_start` alone; no parallel index of starts is needed.
- The library replaces the search only: the merge discipline and the no-touch invariant remain hand-written, and remain the correctness risk.
- Knowing what not to convert is part of the tidy-up: the park scan cannot become a `bisect` without an index keyed by length, which is a different data structure.

## Comparison of Solutions

### Time Complexity

- **Occupancy-Array Scan**: `O(m * n)` - every park sweeps candidate starts across the whole garage.
- **Free-Interval First Fit**: `O(m * g)` - every operation touches the `g` live free runs, `g` bounded by the occupied-island count.
- **Free-Interval First Fit with Bisect**: `O(m * g)` - same algorithm with a faster search and the same list surgery.

### Space Complexity

- **Occupancy-Array Scan**: `O(n)` - one flag per space.
- **Free-Interval First Fit**: `O(g)` - one run per occupied island.
- **Free-Interval First Fit with Bisect**: `O(g)` - identical state, one `bisect` call shorter.

### Trade-offs

- **Occupancy-Array Scan**: the definition written down and the easiest to trust; the per-park sweep over all `n` spaces is brutal at the statement's 100000 bounds.
- **Free-Interval First Fit**: time and state scale with fragmentation rather than capacity; the worst case is still linear once fragmentation peaks.
- **Free-Interval First Fit with Bisect**: fewer moving parts to mistranscribe at the leave; the same asymptotics, since the insert still shifts entries.

### When to Use Each

- **Occupancy-Array Scan**: as the baseline stated first and the oracle the interval versions are checked against; also fine when the garage is known to stay small.
- **Free-Interval First Fit (Recommended)**: the interview answer: the design whose cost follows the gaps, with the merge invariant stated and defended.
- **Free-Interval First Fit with Bisect**: the Python default once the design is settled: hand the search to `bisect` and keep the invariant comments.

### Optimization Notes

- The linear worst case is genuine: adversarial fragmentation grows `g` to the occupied-island bound, and every interval version pays it. The known fix is a segment tree over the spaces storing the longest free run per segment with lazy range assignment, which answers "leftmost position where `size` spaces fit", a park's occupy, and a leave's free in `O(log n)` each. That construction trades the interval design's clarity for a worst-case guarantee worth naming in an interview; under these bounds the interval list is the practical answer.
- The leave branch leans entirely on the statement's guarantee that the freed range is currently occupied; a defensive validity check would need an occupancy probe the interval design deliberately does not keep.
- Exact-fit parks delete the chosen run, so `free_runs` never accumulates empty husks; forgetting that delete is the natural bug and the gauntlet catches it.
