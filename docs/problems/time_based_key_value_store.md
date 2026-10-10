# [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/)

**Medium** | **35 minutes** | **Hash Table, String, Binary Search, Design**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/time_based_key_value_store/solution.py`](../../practice/time_based_key_value_store/solution.py)

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the `TimeMap` class:

- `TimeMap()` Initializes the object of the data structure.
- `void set(String key, String value, int timestamp)` Stores the key `key` with the value `value` at the given time `timestamp`.
- `String get(String key, int timestamp)` Returns a value such that `set` was called previously, with `timestamp_prev <= timestamp`. If there are multiple such values, it returns the value associated with the largest `timestamp_prev`. If there are no values, it returns `""`.

## Examples

### Example 1

**Input:**

```text
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
```

**Output:**

```text
[null, null, "bar", "bar", null, "bar2", "bar2"]
```

**Explanation:**

```text
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);         // return "bar"
timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);         // return "bar2"
timeMap.get("foo", 5);         // return "bar2"
```

## Constraints

- `1 <= key.length, value.length <= 100`
- `key` and `value` consist of lowercase English letters and digits.
- `1 <= timestamp <= 10^7`
- All the timestamps `timestamp` of `set` are strictly increasing.
- At most `2 * 10^5` calls will be made to `set` and `get`.

## Deriving the Solution

All three designs share one storage decision: per key, keep the history of `(timestamp, value)` pairs in a list. Because the problem guarantees that `set` arrives with strictly increasing timestamps, a plain append keeps each history sorted by time for free. `get` then becomes a single classic question on a sorted list: find the rightmost entry whose timestamp does not exceed the query. The solutions differ only in how they answer it.

1. **Start literal.** Append on `set`; on `get`, walk the history backward and
   return the first entry old enough. Correct and dependency-free, but a lookup may inspect every stored version, `O(n)` per `get`: see [Linear Scan](#linear-scan).
2. **Spot the waste.** The backward walk never uses the fact that the list is
   sorted. Sortedness means one probe in the middle tells which half holds the answer, so half the candidates can be discarded at once instead of one at a time.
3. **Halve it by hand.** A hand-written binary search finds the first index
   whose timestamp is strictly greater than the query; the entry just before it is the answer. `O(log n)` per `get`: see [Manual Binary Search](#manual-binary-search).
4. **Delegate the search.** The pattern "rightmost entry `<=` query" is exactly
   what the standard library's `bisect_right` computes on a sorted list of timestamps: see [Binary Search with bisect](#binary-search-with-bisect).

## Solutions

### Linear Scan

#### Derivation

The class must support two calls: record a value under a key at a timestamp, and fetch the newest value at or before a queried timestamp. The design question is what storage shape makes both cheap. Each key accumulates a history of `(timestamp, value)` entries, and because the problem guarantees that `set` is called with strictly increasing timestamps, the history for any key is already sorted by time. The most recent valid value is therefore the last entry whose timestamp does not exceed the query, which the most literal `get` finds by walking the history backward:

1. Store, per key, a list of `(timestamp, value)` pairs in insertion order.
2. On `set`, append the pair; the increasing-timestamp guarantee keeps the list
   sorted without extra work.
3. On `get`, return `""` immediately if the key was never written.
4. Otherwise scan the history from newest to oldest and return the first value whose
   timestamp is `<=` the query. If no entry qualifies, return `""`.

This brute-force scan uses no library helpers: just a backward walk over the list.

#### Walkthrough

Trace the Linear Scan through Example 1, replaying each call in order. The only state is `self.store`, the dict mapping each key to its history of `(timestamp, value)` pairs. After each call below, the right column shows what `self.store` holds and what the call returns.

| Call | What happens | `self.store` after | Returns |
| --- | --- | --- | --- |
| `set("foo", "bar", 1)` | `setdefault` creates an empty list for `"foo"`, then appends `(1, "bar")`. | `{"foo": [(1, "bar")]}` | `null` |
| `get("foo", 1)` | Scan `[(1, "bar")]` backward: `1 <= 1`, so return its value. | unchanged | `"bar"` |
| `get("foo", 3)` | Scan backward: `1 <= 3`, so the first entry already qualifies. | unchanged | `"bar"` |
| `set("foo", "bar2", 4)` | `"foo"` already exists, so append `(4, "bar2")` to its list. | `{"foo": [(1, "bar"), (4, "bar2")]}` | `null` |
| `get("foo", 4)` | Scan backward, newest first: `4 <= 4`, so return `(4, "bar2")`'s value. | unchanged | `"bar2"` |
| `get("foo", 5)` | Scan backward: `4 <= 5`, so the newest entry qualifies immediately. | unchanged | `"bar2"` |

The `get("foo", 3)` step shows why the backward walk works: timestamp `3` was never written, so the scan skips past nothing newer and lands on `(1, "bar")`, the largest stored timestamp not exceeding `3`. The collected returns are `[null, null, "bar", "bar", null, "bar2", "bar2"]`, matching the expected Output.

#### Solution

The code is the append and the backward walk from the walkthrough.

```python
class TimeMap:

    def __init__(self):
        # key -> list of (timestamp, value), appended in ascending time order.
        self.store: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Timestamps for set are strictly increasing, so append keeps order.
        # setdefault initializes an empty history the first time a key is seen.
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        history = self.store[key]
        # Walk backward and return the first entry not exceeding the query.
        for ts, value in reversed(history):
            if ts <= timestamp:
                return value
        return ""


# Your TimeMap object will be instantiated and used as follows:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_2 = obj.get(key, timestamp)
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **set**: `O(1)` amortized, a constant-time append.
- **get**: `O(n)` where `n` is the number of values stored for that key, since the
  backward scan may inspect every entry before finding (or failing to find) a match.

##### Space Complexity: `O(n)`

Across all keys, every `set` stores one `(timestamp, value)` pair, so total storage is linear in the number of `set` calls.

#### Key Insights

- The strictly increasing timestamp guarantee means the history is sorted on
  insertion, so `set` stays `O(1)` and no re-sorting is ever required.
- Scanning backward returns the largest qualifying timestamp first, so the very
  first match is the answer.
- `setdefault(key, [])` initializes a key's history on first `set` without any
  imports, keeping this solution dependency-free.

### Manual Binary Search

#### Derivation

The Linear Scan's `get` may touch every stored version of a key, yet it walks a list it knows to be sorted. Sorted order is precisely what [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) exploits: one probe in the middle reveals which half holds the answer, so each step discards half the candidates. The storage and `set` logic stay identical to the Linear Scan; only `get` changes. The search is aimed at the first index whose timestamp is strictly greater than the query: that index equals the number of entries with timestamp `<=` the query, so the entry just before it holds the largest qualifying timestamp:

1. Keep the Linear Scan's storage: on `set`, append `(timestamp, value)` to the
   key's `history`.
2. On `get`, search with `lo, hi = 0, len(history)`, probing
   `mid = lo + (hi - lo) // 2` while `lo < hi`.
3. If `history[mid][0] <= timestamp`, the first strictly-greater entry lies
   further right, so set `lo = mid + 1`; otherwise it is at `mid` or earlier, so set `hi = mid`.
4. At loop exit, `lo` is the count of entries with timestamp `<=` the query.
   Return `""` when `lo == 0` (nothing is old enough), else `history[lo - 1][1]`.

#### Walkthrough

Trace the class through Example 1, replaying each call and, for every `get`, each probe of the search. `set` appends exactly as in the Linear Scan; the searches below show `lo`, `hi`, and `mid` narrowing until `lo == hi`:

```text
set("foo", "bar", 1)    store = {"foo": [(1, "bar")]}
get("foo", 1)           lo=0 hi=1  mid=0: history[0]=(1,"bar"), 1 <= 1 -> lo=1
                        lo == hi == 1, stop; lo != 0 -> history[0][1] = "bar"
get("foo", 3)           lo=0 hi=1  mid=0: 1 <= 3 -> lo=1
                        stop; history[0][1] = "bar"
set("foo", "bar2", 4)   store = {"foo": [(1, "bar"), (4, "bar2")]}
get("foo", 4)           lo=0 hi=2  mid=1: history[1]=(4,"bar2"), 4 <= 4 -> lo=2
                        lo == hi == 2, stop; history[1][1] = "bar2"
get("foo", 5)           lo=0 hi=2  mid=1: 4 <= 5 -> lo=2
                        stop; history[1][1] = "bar2"
```

In every search, `lo` finishes as the count of entries with timestamp `<=` the query, so `history[lo - 1]` is the newest qualifying entry; a query older than the whole history would leave `lo == 0` and return `""`. On these short histories each search settles in a single probe (the `hi = mid` branch fires when the probed timestamp exceeds the query), but the count of probes grows only logarithmically as a key's history lengthens. The collected returns are `[null, null, "bar", "bar", null, "bar2", "bar2"]`, matching the expected Output.

#### Solution

The code is the `lo`/`hi` search from the walkthrough, wrapped in the Linear Scan's storage.

```python
from collections import defaultdict


class TimeMap:

    def __init__(self):
        # key -> list of (timestamp, value), appended in ascending time order.
        self.store: dict[str, list[tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Timestamps for set are strictly increasing, so append keeps order.
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        history = self.store[key]

        # Hand-written binary search for the rightmost timestamp <= query.
        # `lo` ends as the count of entries with timestamp <= query.
        lo, hi = 0, len(history)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if history[mid][0] <= timestamp:
                lo = mid + 1
            else:
                hi = mid

        if lo == 0:
            return ""
        return history[lo - 1][1]


# Your TimeMap object will be instantiated and used as follows:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_2 = obj.get(key, timestamp)
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **set**: `O(1)` amortized, a constant-time append.
- **get**: `O(log n)` where `n` is the number of values stored for that key,
  dominated by the binary search.

##### Space Complexity: `O(n)`

Across all keys, every `set` stores one `(timestamp, value)` pair, so total storage is linear in the number of `set` calls.

#### Key Insights

- Searching for the first timestamp strictly greater than the query lands on the
  count of qualifying entries, so `lo - 1` is the rightmost valid index.
- Handling `lo == 0` covers the "query precedes every stored timestamp" case
  cleanly.
- Using `lo + (hi - lo) // 2` for the midpoint avoids integer overflow and keeps the
  bound-tracking search correct as the window narrows.

### Binary Search with bisect

#### Derivation

The hand-written search implements a textbook pattern, and Python ships that exact pattern as [`bisect`](https://docs.python.org/3/library/bisect.html): `bisect_right` returns the insertion point just past every element `<=` the probe, which is the same count the manual search computes as `lo`. The only adjustment is to storage: `bisect` searches a plain sorted list, so the timestamps move into their own list, with the values kept in a parallel list at matching indices:

1. Per key, keep two parallel lists: `self.times[key]` for timestamps and
   `self.values[key]` for values, appended together on `set`. The increasing-timestamp guarantee keeps `times` sorted.
2. On `get`, compute `insertion_point = bisect.bisect_right(self.times[key], timestamp)`,
   the count of timestamps `<=` the query.
3. Return `""` when `insertion_point == 0`, else `self.values[key][insertion_point - 1]`, the value
   stored with the largest qualifying timestamp.

#### Walkthrough

Trace the class through Example 1. Here `bisect_right` is itself the technique being delegated to: each `get` line shows the sorted timestamp list it probes and the insertion point it returns:

```text
set("foo", "bar", 1)    times["foo"] = [1]     values["foo"] = ["bar"]
get("foo", 1)           bisect_right([1], 1) = 1     insertion_point=1 -> values["foo"][0] = "bar"
get("foo", 3)           bisect_right([1], 3) = 1     insertion_point=1 -> values["foo"][0] = "bar"
set("foo", "bar2", 4)   times["foo"] = [1, 4]  values["foo"] = ["bar", "bar2"]
get("foo", 4)           bisect_right([1, 4], 4) = 2  insertion_point=2 -> values["foo"][1] = "bar2"
get("foo", 5)           bisect_right([1, 4], 5) = 2  insertion_point=2 -> values["foo"][1] = "bar2"
```

Each `insertion_point` equals the count of stored timestamps not exceeding the query, so `values["foo"][insertion_point - 1]` is the newest qualifying value; a query before the first timestamp would yield `insertion_point == 0` and return `""`. The collected returns are `[null, null, "bar", "bar", null, "bar2", "bar2"]`, matching the expected Output.

#### Solution

The code is the walkthrough's parallel-list bookkeeping with one `bisect_right` call per lookup.

```python
import bisect
from collections import defaultdict


class TimeMap:

    def __init__(self):
        # Per key, keep timestamps and values in two parallel lists. Both stay
        # sorted by time because set is called with strictly increasing stamps.
        self.times: dict[str, list[int]] = defaultdict(list)
        self.values: dict[str, list[str]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Strictly increasing timestamps mean a plain append keeps times sorted.
        self.times[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.times:
            return ""

        # bisect_right returns the count of timestamps <= query, so the entry
        # just before it (insertion_point - 1) holds the largest qualifying
        # timestamp.
        insertion_point = bisect.bisect_right(self.times[key], timestamp)
        if insertion_point == 0:
            return ""
        return self.values[key][insertion_point - 1]


# Your TimeMap object will be instantiated and used as follows:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_2 = obj.get(key, timestamp)
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **set**: `O(1)` amortized, two constant-time appends.
- **get**: `O(log n)` where `n` is the number of values stored for that key,
  dominated by the `bisect_right` call.

##### Space Complexity: `O(n)`

Across all keys, every `set` stores one timestamp and one value, so total storage is linear in the number of `set` calls.

#### Key Insights

- `bisect_right` returns exactly the count of qualifying timestamps, so `insertion_point - 1` is the
  rightmost valid index with no manual bound tracking.
- Splitting timestamps and values into parallel lists lets `bisect` operate on a plain
  list of integers without a key function or extra unpacking.
- This is the idiomatic Python form: the standard library performs the search that the
  Manual Binary Search approach spells out by hand.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `set` is `O(1)`; `get` is `O(n)` per key, since it may inspect
  every stored version.
- **Manual Binary Search**: `set` is `O(1)`; `get` is `O(log n)` per key, since each
  step halves the candidate range.
- **Binary Search with bisect**: `set` is `O(1)`; `get` is `O(log n)` per key, with the
  halving handled by `bisect_right`.

### Space Complexity

- **Linear Scan**: `O(n)` total across all keys.
- **Manual Binary Search**: `O(n)` total across all keys, identical storage.
- **Binary Search with bisect**: `O(n)` total across all keys, split into parallel
  timestamp and value lists.

### Trade-offs

- The linear scan is trivial to write and verify: append on `set`, walk backward on
  `get`, with no index arithmetic.
- The manual binary search is slightly more involved but keeps `get` fast even when a
  single key accumulates a long version history.
- The bisect version is the same speed as the manual search while removing the loop and
  off-by-one bookkeeping entirely.

### When to Use Each

- **Linear Scan**: Fine when keys hold only a few versions or when `get` is called
  rarely relative to `set`.
- **Manual Binary Search**: Useful when the search must be understood or ported to a
  language without a standard binary-search helper.
- **Binary Search with bisect**: Preferred in Python for the full constraint range (up
  to `2 * 10^5` calls), since it is the shortest correct form and the standard choice.

### Optimization Notes

- All three solutions rely on the strictly increasing timestamp guarantee to keep the
  per-key history sorted on insertion, which is what makes `set` constant time.
- The only algorithmic difference is the `get` lookup; the storage shape is otherwise a
  free choice.
- A single list of `(timestamp, value)` tuples (used by the first two approaches) and
  parallel timestamp/value lists (used by the bisect approach) are equivalent in cost; the parallel layout exists only so `bisect` can search the timestamps directly.
