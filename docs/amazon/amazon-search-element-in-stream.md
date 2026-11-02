# [Search for an Element in a Stream](https://www.fastprep.io/problems/amazon-search-element-in-stream)

**Medium** | **NN minutes** | **Hash Table, Tree, Design**

Values arrive one at a time in a stream. At any moment, you may be asked whether a given value has already arrived.

You are given two arrays of the same length, operations and values. Process them from left to right. At index i:

If operations[i] is "add", the value values[i] arrives in the stream.
If operations[i] is "search", check whether values[i] arrived at an earlier index.

Return a boolean array with one entry for each "search", in the order the searches appear. An entry is true if that value arrived before the search, and false otherwise. A value may arrive more than once; a repeat arrival changes nothing. If there are no searches, return an empty array.

## Examples

### Example 1

**Input:** `operations = ["add","add","search","search","add","search"]`, `values = [5,3,3,7,7,7]`

**Output:** `[true,false,true]`

**Explanation:** The values 5 and 3 arrive first, so the search for 3 returns true. The value 7 has not arrived yet, so the next search returns false. After 7 arrives, searching for it again returns true.

## Constraints

- `For this exercise, assume 1 <= operations.length <= 100000 and values.length == operations.length.`
- `Every entry of operations is exactly "add" or "search", and every value is an integer.`
- `When the stream holds no searches, the result is an empty array.`

## Deriving the Solution

Every operation is a question about one growing collection: the set of values that have arrived so far. An `add` grows it, and a `search` asks whether a value joined it at some strictly earlier index. The repeated arrival rule ("a repeat arrival changes nothing") already reads like set insertion, and the approaches below are container choices for that one collection:

1. **Start literal.** Keep every arrival in a log and scan the log for each search. It is the definition, with each search reading the whole history: see [Arrival Log Scan](#arrival-log-scan).
2. **Hash the arrivals.** A set turns both operations into constant-time average work and absorbs the repeat-arrival rule for free: see [Value Set](#value-set).
3. **Order the arrivals instead.** When hashing is unavailable or adversarial, keeping the arrivals sorted lets a binary search answer membership in logarithmic comparisons: see [Sorted Arrival List with Binary Search](#sorted-arrival-list-with-binary-search).
4. **Hand the search to the standard library.** The hand-rolled binary search's loop is bookkeeping around `bisect`: see [Sorted Arrival List with bisect](#sorted-arrival-list-with-bisect).

## Solutions

### Arrival Log Scan

#### Derivation

The statement's most literal reading: a search returns true exactly when some earlier `add` carried the same value. Record every arrival in a list `arrived_log`, duplicates included, and answer each search by scanning the log:

1. Keep `arrived_log`, and collect `results`.
2. On `add`: append the value to `arrived_log`.
3. On `search`: append `value in arrived_log` to `results`.
4. Return `results`, one boolean per search in order.

Because operations are processed left to right, the log at a search contains exactly the arrivals at earlier indices, which is the statement's timing rule with no extra bookkeeping.

#### Walkthrough

Example 1, `operations = ["add","add","search","search","add","search"]`, `values = [5,3,3,7,7,7]`:

```text
add 5        arrived_log = [5]
add 3        arrived_log = [5, 3]
search 3     scan hits 3          -> true
search 7     scan misses          -> false
add 7        arrived_log = [5, 3, 7]
search 7     scan hits 7          -> true
```

The searches collect into `[true, false, true]`, matching the expected Output. The third arrival is a repeat of 7's search value but the first `add 7`; the duplicate-arrival rule has nothing to undo here because the log simply grows.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, operations: List[str], values: List[int]) -> List[bool]:
        arrived_log: List[int] = []
        results: List[bool] = []
        for operation, value in zip(operations, values):
            if operation == "add":
                arrived_log.append(value)
            else:
                results.append(value in arrived_log)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * u)`

Each of the `m` operations scans the log of `u` arrivals on the search path, so a search-heavy stream reads its whole history repeatedly.

##### Space Complexity: `O(u)`

The log holds every arrival, duplicates included.

#### Key Insights

- Sequential processing makes the timing rule automatic: no timestamps, no bookkeeping, the log *is* "earlier".
- Keeping duplicates in the log costs scan length but buys nothing, since one hit answers the search; the next approach drops them.
- The two operation shapes differ only in their append, which marks this as a container-selection problem.

### Value Set

#### Derivation

The log scan re-reads arrivals it has already seen, but the question "has this value arrived?" is membership, and a [hash set](https://en.wikipedia.org/wiki/Hash_table) answers it by direct bucket computation. The set's insert-idiempotence also implements the statement's repeat rule natively: adding a value that is already present changes nothing. Both operations become constant time on average:

1. Keep the set `arrived`.
2. On `add`: add the value; a repeat add is a no-op.
3. On `search`: append `value in arrived`.
4. Return `results`.

#### Walkthrough

Example 1, with `arrived` shown after each operation:

```text
add 5        arrived = {5}
add 3        arrived = {5, 3}
search 3     3 in arrived    -> true
search 7     7 not arrived   -> false
add 7        arrived = {5, 3, 7}
search 7     7 in arrived    -> true
```

The searches collect into `[true, false, true]`, matching the expected Output.

#### Solution

```python
from typing import List, Set


class Solution:
    def solve(self, operations: List[str], values: List[int]) -> List[bool]:
        arrived: Set[int] = set()
        results: List[bool] = []
        for operation, value in zip(operations, values):
            if operation == "add":
                arrived.add(value)
            else:
                results.append(value in arrived)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m)`

Each of the `m` operations performs one average-constant-time set operation.

##### Space Complexity: `O(d)`

The set holds one entry per distinct arrived value, `d <= u`; duplicates collapse.

#### Key Insights

- The statement's "a repeat arrival changes nothing" is literally set-insertion semantics; the rule costs no code at all.
- Set membership does not care when a value arrived, only whether it did, which is all this problem's searches ask.
- Hashing is the one assumption: adversarial or unhashable inputs would push toward the ordered alternative below.

### Sorted Arrival List with Binary Search

#### Derivation

The Value Set leans on hashing; when the container must stay comparison-based (the "Tree" in this problem's category list is exactly this structure in tree form), keeping the arrivals in a sorted list preserves logarithmic searches. A search binary-searches for the value; an insert finds the same position with the search it just ran and splices the value in, keeping the list sorted for the next query. Duplicate arrivals are dropped by construction: if the search finds the value already present, the add is a no-op, which is the repeat-arrival rule again:

1. Keep the sorted list `arrived_sorted`.
2. On `add`: binary-search for the value's insertion position; when the
   position does not already hold the value, insert it there.
3. On `search`: binary-search and report whether the probe lands on the
   value.
4. Return `results`.

#### Walkthrough

Example 1, with `arrived_sorted` shown after each operation and the binary search's probe range marked:

```text
add 5        arrived_sorted = [5]
add 3        probe [0, 1) lands at 0      insert    [3, 5]
search 3     probe [0, 2) lands on 3      found     -> true
search 7     probe [0, 2) lands past 5    missing   -> false
add 7        probe lands at index 2       insert    [3, 5, 7]
search 7     probe [0, 3) lands on 7      found     -> true
```

The searches collect into `[true, false, true]`, matching the expected Output. The list stays sorted through every splice, so each search halves its range instead of scanning.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, operations: List[str], values: List[int]) -> List[bool]:
        arrived_sorted: List[int] = []
        results: List[bool] = []

        def find_position(value: int) -> int:
            low = 0
            high = len(arrived_sorted)
            while low < high:
                middle = (low + high) // 2
                if arrived_sorted[middle] < value:
                    low = middle + 1
                else:
                    high = middle
            return low

        for operation, value in zip(operations, values):
            position = find_position(value)
            if operation == "add":
                if position == len(arrived_sorted) or arrived_sorted[position] != value:
                    arrived_sorted.insert(position, value)
            else:
                results.append(
                    position < len(arrived_sorted)
                    and arrived_sorted[position] == value
                )
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * u)`

Each search is `O(log u)` comparisons, but the splice that keeps the list sorted shifts up to `u` entries on every arrival, which dominates in the worst case.

##### Space Complexity: `O(d)`

The list holds one slot per distinct arrived value.

#### Key Insights

- The binary search's insertion position serves both operations: membership probe for `search`, splice point for `add`.
- This is the hash-free counterpart of the Value Set: same membership semantics, ordered instead of hashed, and the same duplicate-dropping behavior falls out of the probe.
- The sorted order is preserved by inserting *at the probe position*; inserting anywhere else silently breaks every later search.

### Sorted Arrival List with bisect

#### Derivation

The hand-rolled `find_position` is the binary-search algorithm with its loop written out, and the loop is bookkeeping: [`bisect.bisect_left`](https://docs.python.org/3/library/bisect.html) computes the same insertion position in one call, in C. The surrounding logic (probe, compare, splice) is unchanged, so the tidy-up replaces one helper with one import:

1. Keep the sorted list `arrived_sorted`.
2. On `add`: when `bisect_left`'s position does not already hold the value,
   insert the value there.
3. On `search`: append whether the position is inside the list and holds the
   value.
4. Return `results`.

#### Walkthrough

Example 1, with `bisect_left`'s returned position noted per operation:

```text
add 5        bisect_left -> 0    insert    [5]
add 3        bisect_left -> 0    insert    [3, 5]
search 3     bisect_left -> 0    arrived_sorted[0] == 3    -> true
search 7     bisect_left -> 2    past the end              -> false
add 7        bisect_left -> 2    insert                    [3, 5, 7]
search 7     bisect_left -> 2    arrived_sorted[2] == 7    -> true
```

The searches collect into `[true, false, true]`, matching the expected Output, with the positions agreeing with the hand-rolled probes one for one.

#### Solution

```python
from bisect import bisect_left
from typing import List


class Solution:
    def solve(self, operations: List[str], values: List[int]) -> List[bool]:
        arrived_sorted: List[int] = []
        results: List[bool] = []
        for operation, value in zip(operations, values):
            position = bisect_left(arrived_sorted, value)
            if operation == "add":
                if position == len(arrived_sorted) or arrived_sorted[position] != value:
                    arrived_sorted.insert(position, value)
            else:
                results.append(
                    position < len(arrived_sorted)
                    and arrived_sorted[position] == value
                )
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * u)`

`bisect_left` is `O(log u)` per call, and the splice still shifts up to `u` entries per arrival, as in the hand-rolled version.

##### Space Complexity: `O(d)`

The list holds one slot per distinct arrived value.

#### Key Insights

- The algorithm is untouched: `bisect_left` returns the same position the loop computed, which makes the tidy-up safe to apply mechanically.
- The ordered structure remains the linear-splice bottleneck; when that matters, the real upgrade is a tree or skip list, not a better slice.
- `bisect_left` (not `bisect_right`) is what makes the duplicate check one comparison: an existing value probes onto itself.

## Comparison of Solutions

### Time Complexity

- **Arrival Log Scan**: `O(m * u)` - each search reads the whole arrival log.
- **Value Set**: `O(m)` - constant-time average insert and probe.
- **Sorted Arrival List with Binary Search**: `O(m * u)` - logarithmic probes, linear splices.
- **Sorted Arrival List with bisect**: `O(m * u)` - the same bounds with the probe in C.

### Space Complexity

- **Arrival Log Scan**: `O(u)` - every arrival, duplicates included.
- **Value Set**: `O(d)` - one entry per distinct value.
- **Sorted Arrival List with Binary Search**: `O(d)` - one slot per distinct value.
- **Sorted Arrival List with bisect**: `O(d)` - one slot per distinct value.

### Trade-offs

- **Arrival Log Scan**: the definition transcribed, no containers beyond a list; the scan is re-read on every search.
- **Value Set**: linear overall and the least code, resting on hashing, which unhashable or adversarial inputs would undermine.
- **Sorted Arrival List with Binary Search**: comparison-based and ordered, at the price of the splice and the loop's correctness burden.
- **Sorted Arrival List with bisect**: the same structure with the loop delegated; still splices linearly.

### When to Use Each

- **Arrival Log Scan**: as the baseline to state first and to test the others against on small streams.
- **Value Set (Recommended)**: the answer to give in an interview: linear overall, duplicate rule free, nothing to maintain.
- **Sorted Arrival List with Binary Search**: when the interviewer rules out hashing and asks how membership survives anyway.
- **Sorted Arrival List with bisect**: in Python, the idiomatic form of the ordered alternative once the loop has been written once.

### Optimization Notes

- **Value Set** is the recommended choice: it is linear, its duplicate handling is the container's own semantics, and it needs no invariants to hold.
- The sorted list's splice is the real bottleneck, not the probe; a balanced tree (or a skip list) would move both operations to `O(log u)` while keeping the order, which is the structure this problem's "Tree" category gestures at.
- The no-searches stream returns an empty `results` in every approach because `results` only grows on the search branch; the statement's empty-array rule needs no code.
