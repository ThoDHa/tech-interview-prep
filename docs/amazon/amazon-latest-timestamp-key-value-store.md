# [Latest-Timestamp Key-Value Store](https://www.fastprep.io/problems/amazon-latest-timestamp-key-value-store)

**Medium** | **NN minutes** | **Hash Table, Design**

Source note: The source reports set(timestamp,key,value) and get(key) returning the greatest-timestamp value. This exercise uses a finite operation sequence with authored tie handling, missing-key output, bounds and examples. The LRU comparison in the report does not specify a capacity or eviction policy; this version has no eviction. Approximate source match: 96%.

Implement a key-value store that chooses values by their supplied timestamps, not by arrival order. The four aligned arrays describe a finite sequence of operations:

operations[i] = 0: perform set(timestamps[i], keys[i], values[i]).
operations[i] = 1: perform get(keys[i]). Ignore timestamps[i] and values[i] for this operation.

A get returns the value from a preceding set for that key whose timestamp is greatest. If several preceding sets have that greatest timestamp, use the one that occurs latest in the operation sequence. If the key has never been set, return the empty string.

Return only the get results, in encounter order. Sets do not produce output. Each call starts with an empty store, and there is no eviction, expiration, capacity limit, or historical timestamp query.

Timestamps may arrive out of order. A later set with a smaller timestamp must not replace the current greatest-timestamp value. Every get sees only the sets before it in the supplied sequence.

## Examples

### Example 1

**Input:** `operations = [0,0,1,0,1,0,1]`, `keys = ["a","a","a","a","a","a","a"]`, `values = ["newer","older","","tie","","newest",""]`, `timestamps = [10,3,0,10,99,12,1]`

**Output:** `["newer","tie","newest"]`

**Explanation:** The write at timestamp 3 does not replace timestamp 10. The later timestamp-10 write wins the tie. Timestamp 12 then becomes the greatest. Get timestamps are ignored.

### Example 2

**Input:** `operations = [1,0,0,1,1]`, `keys = ["x","x","y","x","y"]`, `values = ["ignored","red","blue","",""]`, `timestamps = [8,0,5,999,0]`

**Output:** `["","red","blue"]`

**Explanation:** The first get has no preceding write. Keys x and y maintain independent values, including a valid write at timestamp zero.

## Constraints

- `All four arrays have the same length q, where 0 <= q <= 200.`
- `Each operation code is 0 or 1.`
- `Keys contain 1 through 20 lowercase English letters.`
- `Values contain 0 through 20 lowercase English letters.`
- `0 <= timestamps[i] <= 1000000000, including ignored get fields.`

## Deriving the Solution

The store answers one question per key: which set is that key's current winner? The statement fixes the ranking (greatest timestamp, the later set winning a tie) and then hands over the decisive sentence: there is no historical timestamp query. Nothing ever asks about a past winner, so the store never needs the losers:

1. **Start literal.** Keep every set in a history list and answer each get by scanning the whole history for the key's greatest timestamp, preferring the later entry on ties: see [Scan All Prior Sets](#scan-all-prior-sets).
2. **Keep only the winner.** A get re-derives a ranking the sets already decided, and since no query ever looks backwards, one winner entry per key, replaced whenever a candidate's timestamp is greater or equal, is the entire state: see [Latest-Write Winner Map](#latest-write-winner-map).

## Solutions

### Scan All Prior Sets

#### Derivation

The statement's most literal reading: the store remembers every set, and a get ranks the history for its key on the spot. Iterating the history in order with a `>=` comparison discharges both rules at once: a strictly greater timestamp replaces the best-so-far, and an equal timestamp replaces it too, which is exactly the later set winning the tie:

1. Keep `history`, the list of `(timestamp, key, value)` set entries in arrival order, and `results`.
2. On a set: append `(timestamp, key, value)`.
3. On a get of `key`: walk the history tracking `best_timestamp` and `best_value`, replacing whenever an entry for `key` has `timestamp >= best_timestamp`.
4. Append `best_value`, which stays the empty string when no entry matched.

#### Walkthrough

Example 1, all on key `a`. The scan column shows the candidates the walk compares:

```text
set 10 a newer    history: (10, a, newer)
set 3  a older    history: (10, a, newer)  (3, a, older)
get a             (10, a, newer): best    (3, a, older): 3 < 10, keep
                                                        out "newer"
set 10 a tie      history: ..., (10, a, newer)  (10, a, tie)
get a             (10, a, newer): best    (10, a, tie): 10 >= 10, take
                                                        out "tie"
set 12 a newest   history: ..., (10, a, tie)  (12, a, newest)
get a             (12, a, newest): greatest timestamp        out "newest"
```

The gets collect into `["newer", "tie", "newest"]`, matching the expected Output. The middle get is the tie rule in action: both candidates sit at timestamp 10, and the `>=` comparison keeps the later one.

#### Solution

```python
from typing import List, Tuple


class Solution:
    def latestTimestampValues(
        self,
        operations: List[int],
        keys: List[str],
        values: List[str],
        timestamps: List[int],
    ) -> List[str]:
        history: List[Tuple[int, str, str]] = []
        results: List[str] = []
        for operation, key, value, timestamp in zip(operations, keys, values, timestamps):
            if operation == 0:
                history.append((timestamp, key, value))
            else:
                best_timestamp = -1
                best_value = ""
                for entry_timestamp, entry_key, entry_value in history:
                    if entry_key == key and entry_timestamp >= best_timestamp:
                        best_timestamp = entry_timestamp
                        best_value = entry_value
                results.append(best_value)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(q^2)`

`q` operations; each of the `g` gets scans all sets before it, which is `O(q)` per get and `O(q^2)` when every operation is a get over a full history.

##### Space Complexity: `O(q)`

The history holds every set, plus the results.

#### Key Insights

- The `>=` comparison is the whole tie rule: walking the history in order and replacing on equal keeps the latest set, with no extra bookkeeping.
- A set with a smaller timestamp still lands in the history but can never win a later scan; the scan's `>=` filter drops it.
- The empty string falls out of the initialization: an unmatched get returns the untouched `best_value`.

### Latest-Write Winner Map

#### Derivation

The scan re-ranks a history whose winner never changes after the fact: a set only dethrones the current winner when its timestamp is greater, or equal (the tie favors the later set), and a get reads the winner without changing it. That is a single map update: keep one `(timestamp, value)` winner per key, and let every set challenge it with `timestamp >= stored`. The statement's sentence that there is no historical timestamp query is the license: no operation ever needs a dethroned value, so discarding losers loses nothing:

1. Keep `winners` mapping key to `(timestamp, value)`.
2. On a set: when the key is new, or `timestamp >= winners[key]`'s timestamp, overwrite the winner.
3. On a get: return the winner's value, or the empty string when the key is absent.

#### Walkthrough

Example 1 again, now as winner challenges. Each line shows `winners` after the operation:

```text
set 10 a newer    a: (10, newer)
set 3  a older    3 >= 10 is false, no replace;  a: (10, newer)
get a                                                     out "newer"
set 10 a tie      10 >= 10, replace;  a: (10, tie)
get a                                                     out "tie"
set 12 a newest   12 >= 10, replace;  a: (12, newest)
get a                                                     out "newest"
```

The gets collect into `["newer", "tie", "newest"]`, matching the expected Output, and the store's whole state after seven operations is the single winner entry `a: (12, newest)`.

#### Solution

```python
from typing import Dict, List, Tuple


class Solution:
    def latestTimestampValues(
        self,
        operations: List[int],
        keys: List[str],
        values: List[str],
        timestamps: List[int],
    ) -> List[str]:
        winners: Dict[str, Tuple[int, str]] = {}
        results: List[str] = []
        for operation, key, value, timestamp in zip(operations, keys, values, timestamps):
            if operation == 0:
                if key not in winners or timestamp >= winners[key][0]:
                    winners[key] = (timestamp, value)
            else:
                results.append(winners[key][1] if key in winners else "")
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(q)`

Each of the `q` operations is a constant number of average O(1) dict probes.

##### Space Complexity: `O(k)`

One winner entry per distinct key, `k <= q`, plus the results.

#### Key Insights

- "No historical timestamp query" is the design constraint doing real work: it collapses the entire history into one winner per key.
- `>=` is the tie rule compressed: sets arrive in sequence order, so an equal-timestamp challenge is automatically the later set.
- The judged array form ignores a get row's timestamp and value fields by construction: the wrapper never passes them to the store, whose get takes only the key.

## Comparison of Solutions

### Time Complexity

- **Scan All Prior Sets**: `O(q^2)` - every get ranks the history for its key.
- **Latest-Write Winner Map**: `O(q)` - constant-time map updates per operation.

### Space Complexity

- **Scan All Prior Sets**: `O(q)` - the history holds every set.
- **Latest-Write Winner Map**: `O(k)` - one winner per distinct key.

### Trade-offs

- **Scan All Prior Sets**: the definition written down, with the tie rule visible in one comparison; the per-get scan repeats work the sets already settled.
- **Latest-Write Winner Map**: linear time and minimal state, at the price of trusting the no-historical-query guarantee; a single added query type ("value at time t") would force the history back.

### When to Use Each

- **Scan All Prior Sets**: as the baseline to state first, or when the sequence is short enough that the quadratic term is irrelevant.
- **Latest-Write Winner Map (Recommended)**: the interview answer under this statement: linear time, constant work per operation, and the smallest possible state.

### Optimization Notes

- **Latest-Write Winner Map** is the recommended choice: it meets the statement's contract exactly and keeps only what a future get can still read.
- The winner challenge uses `>=`, not `>`: with `>`, an equal-timestamp set would lose to the stored winner, contradicting the latest-set-wins tie rule. Timestamp 0 makes the difference observable, since a stored 0 must be replaceable by another 0.
- If the statement ever added a historical query, the winner map would generalize to a per-key list of `(timestamp, value)` pairs searched by bisect; the tie rule would need the search to land on the last equal timestamp, which is what `bisect_right` returns.
- That generalized store is the contract of [Time Based Key-Value Store](../leetcode/time_based_key_value_store.md): its `get` names a past timestamp, so it must keep the full per-key `(timestamp, value)` history that this statement lets the store reduce to one current winner per key.
