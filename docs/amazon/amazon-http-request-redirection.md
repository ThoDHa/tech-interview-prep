# [HTTP Request Redirection](https://www.fastprep.io/problems/amazon-http-request-redirection)

**Medium** | **NN minutes** | **Array, Hash Table, Sorting, Simulation, Geometry**

Amazon engineers are investigating an HTTP request that is redirected among servers.

There are n servers on an infinite two-dimensional plane. The coordinates of server i are given by locations[i] = [x, y]. The request starts at locations[0], and that server is marked as visited.

Each value in redirectRecords specifies one redirect direction from the current server (a, b). In every formula below, Z is an arbitrary positive integer:

Direction 1: (a, b) -> (a + Z, b + Z).Direction 2: (a, b) -> (a + Z, b - Z).Direction 3: (a, b) -> (a - Z, b + Z).Direction 4: (a, b) -> (a - Z, b - Z).Process the redirect records in order. For each record, redirect the request to the nearest server in the specified direction that has not previously been visited. If no eligible server exists in that direction, skip that redirect. Whenever the request reaches a server, mark it as visited.

Return the coordinates [x, y] of the server holding the request after all redirect records have been processed.

## Examples

### Example 1

**Input:** `locations = [[3,4],[1,2],[7,8],[5,6]]`, `redirectRecords = [1,4]`

**Output:** `[1,2]`

**Explanation:** The request starts at [3, 4]. Direction 1 points toward both [5, 6] and [7, 8], so the nearest unvisited server is [5, 6].

Direction 4 points back toward [3, 4] and then [1, 2]. Because [3, 4] has already been visited, the request moves to [1, 2].

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-http-request-redirection; fill them in. -->

## Solutions

### Simulation with Linear Scan

#### Derivation

The literal reading asks one question per record: which unvisited servers sit exactly on a diagonal ray from the current server, and which of them is closest? A server is eligible when its offset from the current position points along the record's direction and the two offset components have equal magnitude, which is the diagonal condition. That magnitude is then the travel distance, so "nearest" is simply the smallest offset, and `Z` never needs to be known in advance: whatever `Z` was, the landed server's offset is it:

1. Track `visited`, a boolean list with the start server 0 already marked, and
   `holder`, the index of the server currently holding the request.
2. For each record, read its step from `DIRECTION_STEPS` (`1` maps to
   `(1, 1)`, `2` to `(1, -1)`, `3` to `(-1, 1)`, `4` to `(-1, -1)`).
3. Scan every server: skip visited ones, skip any whose `offset_x * step_x` or
   `offset_y * step_y` is not strictly positive (wrong way, or zero offset),
   and skip any where `abs(offset_x) != abs(offset_y)` (not on the diagonal
   ray).
4. Keep the eligible server with the smallest `offset_x`. When one exists, mark
   it visited and move `holder` to it; when none exists, the record is skipped
   and `holder` stays put.
5. Return `locations[holder]` after all records.

#### Walkthrough

Example 1, `locations = [[3,4],[1,2],[7,8],[5,6]]`, `redirectRecords = [1,4]`. The request starts at `[3, 4]` with server 0 already visited:

```text
record 1  step (+1, +1), holder at [3, 4]
  server 1 at [1, 2]   offset (-2, -2)   offset_x * 1 <= 0           -> skip
  server 2 at [7, 8]   offset (4, 4)     diagonal, offset 4          -> candidate
  server 3 at [5, 6]   offset (2, 2)     diagonal, offset 2 < 4      -> nearest
  holder moves to server 3 at [5, 6]
record 4  step (-1, -1), holder at [5, 6]
  server 1 at [1, 2]   offset (-4, -4)   both signs match, diagonal  -> candidate, offset 4
  server 2 at [7, 8]   offset (2, 2)     offset_x * -1 = -2 <= 0     -> skip
  holder moves to server 1 at [1, 2]
```

The final holder is server 1, so the function returns `[1, 2]`, matching the expected Output. Record 4 stepping over `[3, 4]` is the visited rule at work: the start server was marked before the first record.

#### Solution

```python
from typing import Dict, List, Tuple


DIRECTION_STEPS: Dict[int, Tuple[int, int]] = {
    1: (1, 1), 2: (1, -1), 3: (-1, 1), 4: (-1, -1),
}


class Solution:
    def solve(self, locations: List[List[int]], redirectRecords: List[int]) -> List[int]:
        visited = [False] * len(locations)
        visited[0] = True
        holder = 0

        for record in redirectRecords:
            step_x, step_y = DIRECTION_STEPS[record]
            x, y = locations[holder]
            nearest_server = -1
            nearest_offset = 0
            for server, (server_x, server_y) in enumerate(locations):
                if visited[server]:
                    continue
                offset_x, offset_y = server_x - x, server_y - y
                if (offset_x * step_x <= 0 or offset_y * step_y <= 0
                        or abs(offset_x) != abs(offset_y)):
                    continue
                offset = abs(offset_x)
                if nearest_server == -1 or offset < nearest_offset:
                    nearest_server = server
                    nearest_offset = offset
            if nearest_server != -1:
                visited[nearest_server] = True
                holder = nearest_server

        return list(locations[holder])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R × n)`

Each of the `R` records scans all `n` servers with constant work per server.

##### Space Complexity: `O(n)`

The visited list is the only extra structure.

#### Key Insights

- Eligibility is two checks: the offset must point along the record's step, and the two offset magnitudes must agree, which is the diagonal condition `offset_x == abs(offset_y)`.
- `Z` is never needed as a number: the eligible server's offset magnitude is the travel distance, so "nearest" reduces to the smallest `offset_x`.
- A record with no eligible server leaves `holder` untouched; skipping is a no-op, not an error.
- The start server must be marked visited before the first record, or a redirect could send the request back where it started.

### Diagonal Bucketing with Binary Search

#### Derivation

The linear scan re-derives the geometry from scratch at every record, but the geometry never changes: a direction 1 or 4 move adds or subtracts the same `Z` from both coordinates, so it preserves `x - y`, and a direction 2 or 3 move preserves `x + y`. Every server eligible for a record therefore lives in one fixed bucket, keyed by `x - y` for records 1 and 4 and by `x + y` for records 2 and 3, and inside a bucket "nearest" is decided by x alone: records 1 and 2 want the smallest entry x above the current server's x, records 3 and 4 the largest entry x below. Sorting each bucket by x turns every record into a binary search plus one removal:

1. Bucket every server into `diagonal_rows` (key `x - y`) and `antidiagonal_rows`
   (key `x + y`) as `(x, server)` entries, and sort every bucket by x.
2. Retire the start server: remove its entry from both of its buckets, because
   visited servers must never be landed on again.
3. For each record, pick the table the record preserves (`diagonal_rows` for
   records 1 and 4, `antidiagonal_rows` for records 2 and 3) and the bucket of
   the current server's position.
4. Records 1 and 2: `position = bisect_left(rows, (x + 1,))` is the first entry
   with entry x greater than the current x, and the bucket is exhausted when
   `position == len(rows)`. Records 3 and 4: `position = bisect_left(rows, (x,)) - 1`
   is the last entry with entry x below, exhausted when `position < 0`. The
   one-tuple boundaries work because `(x,)` sorts before every `(x, server)`
   pair: a tuple that prefixes a longer one compares smaller.
5. Land on the entry's server, retire it from both buckets, and continue.
6. Return `locations[holder]`.

#### Walkthrough

Example 1 again. All four servers share `x - y = -1`, so one diagonal bucket holds everything and the antidiagonal buckets stay singletons:

```text
diagonal_rows[-1] sorted by x:  [(1, 1), (3, 0), (5, 3), (7, 2)]
start      retire server 0  ->  [(1, 1), (5, 3), (7, 2)]
record 1   bisect_left(rows, (4,)) -> 1, entry (5, server 3): land at [5, 6]
           retire server 3  ->  [(1, 1), (7, 2)]
record 4   bisect_left(rows, (5,)) -> 1, step back -> 0, entry (1, server 1): land at [1, 2]
return     locations[1] = [1, 2]
```

Record 1 needed the successor of x = 3 and found `(5, server 3)` at index 1; record 4 needed the predecessor of x = 5 and found `(1, server 1)` by stepping back from index 1. Retired entries never appear in a search, so no eligibility checks remain on the query path.

#### Solution

```python
from bisect import bisect_left
from typing import Dict, List, Tuple


MAIN_DIAGONAL_DIRECTIONS = (1, 4)
LARGER_X_DIRECTIONS = (1, 2)


class Solution:
    def solve(self, locations: List[List[int]], redirectRecords: List[int]) -> List[int]:
        diagonal_rows: Dict[int, List[Tuple[int, int]]] = {}
        antidiagonal_rows: Dict[int, List[Tuple[int, int]]] = {}
        for server, (x, y) in enumerate(locations):
            diagonal_rows.setdefault(x - y, []).append((x, server))
            antidiagonal_rows.setdefault(x + y, []).append((x, server))
        for rows in list(diagonal_rows.values()) + list(antidiagonal_rows.values()):
            rows.sort()

        def retire(server: int) -> None:
            x, y = locations[server]
            for rows in (diagonal_rows[x - y], antidiagonal_rows[x + y]):
                rows.pop(bisect_left(rows, (x, server)))

        holder = 0
        retire(holder)

        for record in redirectRecords:
            x, y = locations[holder]
            rows = (diagonal_rows[x - y] if record in MAIN_DIAGONAL_DIRECTIONS
                    else antidiagonal_rows[x + y])
            if record in LARGER_X_DIRECTIONS:
                position = bisect_left(rows, (x + 1,))
                if position == len(rows):
                    continue
            else:
                position = bisect_left(rows, (x,)) - 1
                if position < 0:
                    continue
            holder = rows[position][1]
            retire(holder)

        return list(locations[holder])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n + R log n + n × b)`

Sorting the buckets costs `O(n log n)`; each of the `R` records binary-searches one bucket in `O(log n)`; each of the at most `n` landings retires a server from two buckets, and a Python list removal shifts the tail, `O(b)` per removal where `b` is the largest bucket length.

##### Space Complexity: `O(n)`

Every server is stored once per table, two entries in all.

#### Key Insights

- The four direction formulas collapse into two invariants: directions 1 and 4 preserve `x - y`, directions 2 and 3 preserve `x + y`, so two bucket tables serve all four queries.
- Within a sorted diagonal bucket, "nearest in direction" is a successor or predecessor query on x, which one binary search answers.
- Retiring a server the moment it is visited keeps every bucket holding exactly the unvisited servers, so eligibility disappears from the query path entirely.
- Each server can be landed on at most once, so the number of retirements is bounded by `n` even when `R` is large.

## Comparison of Solutions

### Time Complexity

- **Simulation with Linear Scan**: `O(R × n)` - every record inspects every server.
- **Diagonal Bucketing with Binary Search**: `O(n log n + R log n + n × b)` - sorted buckets answer each record by binary search, and landings pay list-removal shifts bounded by the largest bucket length `b`.

### Space Complexity

- **Simulation with Linear Scan**: `O(n)` - one boolean visited list.
- **Diagonal Bucketing with Binary Search**: `O(n)` - two bucket entries per server.

### Trade-offs

- **Simulation with Linear Scan**: no preprocessing and almost no state, but the cost grows linearly with the product of records and servers.
- **Diagonal Bucketing with Binary Search**: pays one sorting pass and retirement bookkeeping up front, then drops each record to a logarithmic lookup; the removal step adds bucket-sized shifts that only matter when servers crowd onto few diagonals.

### When to Use Each

- **Simulation with Linear Scan (Recommended)**: the right call at typical OA sizes, where `n` and the record count are both small and the constant-free clarity wins.
- **Diagonal Bucketing with Binary Search**: when `n` and the record count both grow into the tens of thousands and the quadratic product would time out.

### Optimization Notes

- The `O(n × b)` removal term is the only superlogarithmic piece left: a `SortedList` (third-party `sortedcontainers`) or a Fenwick tree over compressed x per bucket drops it to `O(log n)` per landing, for a total `O((n + R) log n)`.
- The one-tuple boundary `(x + 1,)` avoids a sentinel infinity: `(x,)` sorts before every `(x, server)` pair, so `bisect_left(rows, (x,)) - 1` reads "last strictly smaller" directly.
- Bucketing assumes nothing about the order of `locations`; no sorting of the input list itself is needed, only the per-bucket sorts.
