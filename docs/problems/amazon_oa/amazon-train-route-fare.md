# [Fare Between Stops on a Train Route](https://www.fastprep.io/problems/amazon-train-route-fare)

**Easy** | **NN minutes** | **Array, Hash Table, Simulation**

A train route is given as an ordered array of unique stop names. Traveling across one adjacent segment costs one fare unit in either direction.

Implement calculateFare to return the fare between start and stop. Return -1 if either requested stop is absent.

## Examples

### Example 1

**Input:** `route = ["G","U","H","K","I"]`, `start = "G"`, `stop = "I"`

**Output:** `4`

**Explanation:** The endpoints are four adjacent segments apart.

### Example 2

**Input:** `route = ["A","B","C"]`, `start = "C"`, `stop = "A"`

**Output:** `2`

**Explanation:** Travel in the reverse direction costs the same two units.

### Example 3

**Input:** `route = ["A","B"]`, `start = "A"`, `stop = "Z"`

**Output:** `-1`

**Explanation:** Z is not a stop on the route.

## Constraints

- `1 ≤ route.length ≤ 100000.`
- `Every route entry is a non-empty unique printable ASCII string.`
- `start and stop are non-empty printable ASCII strings.`

## Solutions

### Single-Pass Linear Scan

#### Derivation

The route is a line: the stops sit in array order, each adjacent pair is one segment, and a segment costs one fare unit in either direction. So the fare between `start` and `stop` is exactly the number of segments separating them, which is the distance between their array positions: `abs(start_position - stop_position)`. The only work is finding the two positions, and one walk over `route` finds both at once, recording each position when its name matches:

1. Initialize `start_position` and `stop_position` to `-1`, a sentinel no real
   index can hold.
2. Walk `route` with `enumerate`. When the entry equals `start`, record its
   position in `start_position`; when it equals `stop`, record it in
   `stop_position`. Both records can fire on the same entry when the request is
   a same-stop query, which then fares `0`.
3. After the walk, either sentinel still `-1` means that stop is absent: return
   `-1`.
4. Otherwise return `abs(start_position - stop_position)`, the segment count in
   either direction.

No auxiliary structure is needed because the query is answered in the same pass that reads the route.

#### Walkthrough

Let us watch the scan on Example 1: `route = ["G","U","H","K","I"]`, `start = "G"`, `stop = "I"`. Each line is one comparison event:

```text
position 0   "G" == start -> start_position = 0      start_position = 0,  stop_position = -1
position 1   "U" matches nothing                     start_position = 0,  stop_position = -1
position 2   "H" matches nothing                     start_position = 0,  stop_position = -1
position 3   "K" matches nothing                     start_position = 0,  stop_position = -1
position 4   "I" == stop  -> stop_position = 4       start_position = 0,  stop_position = 4
```

Both sentinels were replaced, so the fare is `abs(0 - 4) = 4`, matching the expected Output. Direction never enters the computation: Example 2 asks for `C` to `A` on `["A","B","C"]` and the same subtraction gives `abs(2 - 0) = 2`. Example 3 walks `["A","B"]` looking for `"Z"`, finishes with `stop_position = -1`, and returns `-1`.

#### Solution

The code is the walk from the walkthrough: record both positions in one pass, then subtract.

```python
from typing import List


class Solution:
    def solve(self, route: List[str], start: str, stop: str) -> int:
        start_position = -1
        stop_position = -1
        for position, stop_name in enumerate(route):
            if stop_name == start:
                start_position = position
            if stop_name == stop:
                stop_position = position

        if start_position == -1 or stop_position == -1:
            return -1
        return abs(start_position - stop_position)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass compares every stop name at most twice, once against `start` and once against `stop`.

##### Space Complexity: `O(1)`

Two position variables regardless of the route length.

#### Key Insights

- On a line with symmetric segment costs, direction is irrelevant and the fare collapses to an index distance, so no path walk is ever needed.
- One pass suffices for both lookups; the sentinel `-1` doubles as the absence flag, avoiding a second existence check.
- This is optimal for a single query; making it faster per query requires paying to index the route first, which the next approach does.

### Position Hash Map

#### Derivation

The linear scan is optimal for one query but pays `O(n)` every time `calculateFare` runs. When the same route serves many fare queries, the positions should be built once into a [hash map](https://en.wikipedia.org/wiki/Hash_table) from stop name to index: building costs one pass, and each query afterwards becomes two constant-time lookups and a subtraction:

1. Build `position_of` with one comprehension: `position_of[stop_name] = position`
   for each entry of `route`.
2. Look up `start` and `stop`. A missing key means that stop is absent from the
   route: return `-1`.
3. Return `abs(position_of[start] - position_of[stop])`.

For a single call this is the linear scan plus an `O(n)` dictionary, which is why the scan ranks first; the map wins the moment the route is reused.

#### Walkthrough

Let us build `position_of` for Example 1: `route = ["G","U","H","K","I"]`:

```text
insert "G" -> 0    position_of = {"G": 0}
insert "U" -> 1    position_of = {"G": 0, "U": 1}
insert "H" -> 2    position_of = {"G": 0, "U": 1, "H": 2}
insert "K" -> 3    position_of = {"G": 0, "U": 1, "H": 2, "K": 3}
insert "I" -> 4    position_of = {"G": 0, "U": 1, "H": 2, "K": 3, "I": 4}
```

The query `"G"` to `"I"` then reads two entries and subtracts:

```text
position_of["G"] = 0
position_of["I"] = 4
fare = abs(0 - 4) = 4
```

Matching the expected Output. Example 2 reads `position_of["C"] = 2` and `position_of["A"] = 0` for `abs(2 - 0) = 2`, and Example 3 misses the key `"Z"`, so the membership test returns `-1` before any subtraction.

#### Solution

The code is the build-once map from the walkthrough, with the membership guard ahead of the lookups.

```python
from typing import List


class Solution:
    def solve(self, route: List[str], start: str, stop: str) -> int:
        position_of = {stop_name: position for position, stop_name in enumerate(route)}
        if start not in position_of or stop not in position_of:
            return -1
        return abs(position_of[start] - position_of[stop])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass builds the map; the two lookups are constant time on average.

##### Space Complexity: `O(n)`

The map holds one entry per stop.

#### Key Insights

- The stop names are unique, so the name-to-position map is lossless and a single entry per stop suffices.
- The build cost is amortized across queries: one build followed by `q` queries costs `O(n + q)` against the scan's `O(q × n)`.
- Per single call, this is never better than the linear scan; its value is entirely in reuse.

### Built-in Index Lookup

#### Derivation

The linear scan's two position searches are exactly what `list.index` does, so the whole procedure can be handed to the standard library: index both stops, subtract, and translate the missing-stop case into the `ValueError` that `.index` raises. The algorithm is unchanged from the [Single-Pass Linear Scan](#single-pass-linear-scan); only the bookkeeping moves into the built-in, and `try`/`except` replaces the sentinel check:

1. Evaluate `route.index(start)` and `route.index(stop)`.
2. Either call raising `ValueError` means that stop is absent: return `-1`.
3. Return the absolute difference of the two indices.

One behavioral nuance: `.index` scans the whole list for the leftmost occurrence, but the constraint that route entries are unique makes the leftmost occurrence the only one, so the result matches the single-pass scan exactly.

#### Walkthrough

Example 1: `route = ["G","U","H","K","I"]`, `start = "G"`, `stop = "I"`:

```text
route.index("G")   scans positions 0..0   returns 0
route.index("I")   scans positions 0..4   returns 4
fare = abs(0 - 4) = 4
```

Example 2 evaluates `route.index("C") = 2` and `route.index("A") = 0` for `2`. Example 3 raises the exception path: `route.index("Z")` scans `["A","B"]` without a match, `ValueError` fires, and the handler returns `-1`. All three match the expected Outputs.

#### Solution

The code is the two lookups and the guarded subtraction.

```python
from typing import List


class Solution:
    def solve(self, route: List[str], start: str, stop: str) -> int:
        try:
            return abs(route.index(start) - route.index(stop))
        except ValueError:
            return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each `.index` call is a linear scan; with both stops present the pair of scans covers the route at most twice.

##### Space Complexity: `O(1)`

No auxiliary structure beyond the returned integer.

#### Key Insights

- `list.index` is the library form of the hand-written scan; the sentinel logic becomes an exception handler, and the body shrinks to one expression.
- EAFP style fits Python: testing membership first would add two extra scans that the exception path makes unnecessary.
- Readability is the whole argument here; asymptotically it ties the hand-written scan, and the hash map remains the answer for repeated queries.

## Comparison of Solutions

### Time Complexity

- **Single-Pass Linear Scan**: `O(n)` - one walk compares every stop against both targets.
- **Position Hash Map**: `O(n)` - one pass to build, then constant-time lookups per query.
- **Built-in Index Lookup**: `O(n)` - two library scans, one per stop.

### Space Complexity

- **Single-Pass Linear Scan**: `O(1)` - two position variables.
- **Position Hash Map**: `O(n)` - one map entry per stop.
- **Built-in Index Lookup**: `O(1)` - no auxiliary structure.

### Trade-offs

- **Single-Pass Linear Scan**: constant extra space and a single pass, but every repeated query rescans the route.
- **Position Hash Map**: pays `O(n)` memory to make every later query constant time; for a one-off call it is strictly dominated by the scan.
- **Built-in Index Lookup**: the shortest code with identical asymptotics to the scan, delegating the loop and the error case to the runtime.

### When to Use Each

- **Single-Pass Linear Scan (Recommended)**: the interview default for a one-shot query: linear time, constant space, nothing to explain.
- **Position Hash Map**: when `calculateFare` is called repeatedly on the same route, or the follow-up asks for many queries.
- **Built-in Index Lookup**: in production Python where the team trusts stdlib behavior and values the one-line body.

### Optimization Notes

- The core reduction is that a fare on a line is an index distance; every approach is a different way to obtain two positions.
- The uniqueness constraint is load-bearing for the hash map: duplicate stop names would make `position_of` silently keep only the last occurrence.
- For genuinely huge route arrays with many queries, the map can be built once at load time and shared across calls, turning each call into the two-lookup tail of this approach.
