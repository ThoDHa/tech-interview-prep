# [LFU Cache](https://www.fastprep.io/problems/amazon-lfu-cache)

**Hard** | **NN minutes** | **Design, Hash Table, Linked List, Simulation**

Process commands on an initially empty least-frequently-used cache with positive integer capacity.

put key value inserts a new key or updates an existing key.
get key returns the stored value, or -1 when the key is absent.

For this exercise, assume a successful get and a put that updates an existing key each increase that key's frequency by one and make it most recently used within its new frequency. A new key starts with frequency one.

When a new insertion would exceed capacity, evict the key with the smallest frequency. Break a frequency tie by evicting the least recently used key. Return the results of all get commands in order. Each operation should run in average O(1) time.

## Examples

### Example 1

**Input:** `capacity = 2`, `operations = ["put 1 1","put 2 2","get 1","put 3 3","get 2","get 3","put 4 4","get 1","get 3","get 4"]`

**Output:** `[1,-1,3,-1,3,4]`

**Explanation:** Reading key 1 raises its frequency, so key 2 is evicted first. Later keys 1 and 3 tie on frequency, and key 1 is least recent.

### Example 2

**Input:** `capacity = 1`, `operations = ["put 7 5","put 7 8","get 7","put 9 4","get 7","get 9"]`

**Output:** `[8,-1,4]`

**Explanation:** Updating key 7 changes its value and frequency. Inserting key 9 into a one-entry cache then evicts key 7.

## Constraints

- `1 <= capacity <= 3000.`
- `1 <= operations.length <= 2 * 10^4.`
- `Each command is exactly get key or put key value.`
- `Keys and values fit in signed 32-bit integers.`
- `At least one command is get.`

## Deriving the Solution

Every operation is a dict lookup plus one question: when a fresh insert lands on a full cache, which key leaves? The statement fixes the answer (smallest frequency, least recently used within the tie), so the approaches below differ only in how fast that question gets answered. The ladder climbs by making it cheaper:

1. **Start literal.** Keep one record per key (value, frequency, last-use stamp) and answer eviction by scanning every record for the smallest `(frequency, stamp)`: see [Linear-Scan Eviction](#linear-scan-eviction).
2. **Heapify the scan.** A min-heap ordered by `(frequency, stamp)` surfaces the victim without a scan; a key's ordering changes on every touch, so each touch pushes a fresh entry and stale entries are discarded when they surface: see [Lazy Binary Heap](#lazy-binary-heap).
3. **Exploit the +1 step.** A frequency only ever rises by exactly one, and recency only matters inside one frequency, so each frequency keeps its own recency list while a `min_frequency` pointer that only climbs by one names the eviction bucket; the lists are doubly linked so promotion and eviction are pointer splices: see [Frequency Buckets with Doubly Linked Lists](#frequency-buckets-with-doubly-linked-lists).
4. **Hand the bookkeeping to the library.** `OrderedDict` implements each bucket's recency list with constant-time append and pop-from-front, and the hand-written nodes disappear: see [Ordered Dictionary per Frequency](#ordered-dictionary-per-frequency).

## Solutions

### Linear-Scan Eviction

#### Derivation

The statement's most literal reading: the cache is the collection of records currently stored, and eviction is a search for the right one to drop. A dict maps each key to its record, a stamp counter marks recency, and the eviction scan reads them all:

1. Keep `records` mapping key to `(value, frequency, stamp)` and a `stamp` counter advanced on every successful touch.
2. On `get key`: a miss returns -1; a hit bumps the record's frequency, refreshes its stamp, and returns the value.
3. On `put key value` for a stored key: update the value, bump the frequency, refresh the stamp.
4. On a fresh insert with `len(records) == capacity`: scan for the key minimizing `(frequency, stamp)` and delete it.
5. Insert the new key with frequency 1 and the current stamp.

#### Walkthrough

Example 1, all ten commands. Each line shows the records touched or scanned, as `key: value, frequency, stamp`:

```text
put 1 1    records: 1: 1,1,1
put 2 2    records: 1: 1,1,1   2: 2,1,2
get 1      1 -> freq 2, stamp 3                    out 1
put 3 3    full: scan finds min (freq, stamp) = (1,2) on key 2, evict
           records: 1: 1,2,3   3: 3,1,4
get 2      miss                                    out -1
get 3      3 -> freq 2, stamp 5                    out 3
put 4 4    full: 1:(2,3) vs 3:(2,5): tie on freq 2, older stamp wins
           evict key 1; records: 3: 3,2,5   4: 4,1,6
get 1      miss                                    out -1
get 3      3 -> freq 3, stamp 8                    out 3
get 4      4 -> freq 2, stamp 9                    out 4
```

The gets collect into `[1,-1,3,-1,3,4]`, matching the expected Output. The second eviction is the tie in action: both candidates sit at frequency 2, so the older stamp (key 1) decides.

#### Solution

```python
from typing import Dict, List, Tuple


class Solution:
    def processLfuCache(self, capacity: int, operations: List[str]) -> List[int]:
        records: Dict[int, Tuple[int, int, int]] = {}
        stamp = 0
        results: List[int] = []
        for operation in operations:
            parts = operation.split()
            key = int(parts[1])
            if parts[0] == "get":
                if key in records:
                    value, frequency, _ = records[key]
                    stamp += 1
                    records[key] = (value, frequency + 1, stamp)
                    results.append(value)
                else:
                    results.append(-1)
            else:
                value = int(parts[2])
                if key in records:
                    _, frequency, _ = records[key]
                    stamp += 1
                    records[key] = (value, frequency + 1, stamp)
                else:
                    if len(records) == capacity:
                        victim_key = min(
                            records,
                            key=lambda candidate: (
                                records[candidate][1], records[candidate][2]
                            ),
                        )
                        del records[victim_key]
                    stamp += 1
                    records[key] = (value, 1, stamp)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * u)`

`m` operations, each a constant-time dict update except an eviction, which scans all `u <= capacity` stored records. A scan-heavy workload on a full cache pays the scan on every fresh insert.

##### Space Complexity: `O(u)`

One record per cached key, plus the results list.

#### Key Insights

- Eviction is the only cost: gets, updates, and inserts are O(1) dict work, so the whole problem reduces to "find the victim fast".
- The stamp turns both eviction rules into one tuple minimum: smallest frequency first, oldest touch breaking the tie.
- A miss touches nothing: no frequency moves and no stamp advances, so the next eviction would pick the same victim either way.

### Lazy Binary Heap

#### Derivation

The scan re-finds the same minimum from scratch on every eviction, but the candidates barely change between evictions, which is exactly what a [binary heap](https://en.wikipedia.org/wiki/Binary_heap) maintains: order the entries by `(frequency, stamp)` and the victim is always at the top. The obstacle is that a key's ordering changes on every touch, and a heap cannot update entries in place. The repair is laziness: push a fresh entry per touch, and treat any entry whose `(frequency, stamp)` no longer matches the key's live record as stale garbage to discard when it surfaces:

1. Keep `live` mapping key to `(value, frequency, stamp)` and a `heap` of `(frequency, stamp, key)` entries.
2. On every successful get or updating put: bump the record and push the new `(frequency, stamp, key)`.
3. On eviction with `len(live) == capacity`: pop while the top's `(frequency, stamp)` differs from the live record of its key; the first matching top is the true minimum, and its key is evicted.
4. On a fresh insert: push `(1, stamp, key)` and record frequency 1.

#### Walkthrough

Example 1, showing what each eviction finds at the heap top. The first eviction runs with a clean heap; the second must discard two stale entries first:

```text
put 1 1    push (1, 1, key 1)
put 2 2    push (1, 2, key 2)
get 1      push (2, 3, key 1)                              out 1
put 3 3    full: top (1, 2, key 2) matches live -> evict key 2
           push (1, 4, key 3)
get 2      miss, nothing pushed                            out -1
get 3      push (2, 5, key 3)                              out 3
put 4 4    full: top (1, 2, key 2): key 2 gone      -> stale, pop
           top (1, 4, key 3): live[3] sits at (2, 5) -> stale, pop
           top (2, 3, key 1): matches live          -> evict key 1
           push (1, 6, key 4)
get 1      miss, nothing pushed                            out -1
get 3      push (3, 8, key 3)                              out 3
get 4      push (2, 9, key 4)                              out 4
```

The victims are key 2 then key 1, and the gets collect into `[1,-1,3,-1,3,4]`, matching the expected Output. The stale-entry discipline is the whole mechanism: an entry is trustworthy exactly when it matches the key's live record, and every pop retires at most one stale entry forever.

#### Solution

The code is the touch-push discipline with the stale-skip loop in front of the eviction:

```python
import heapq
from typing import Dict, List, Tuple


class Solution:
    def processLfuCache(self, capacity: int, operations: List[str]) -> List[int]:
        live: Dict[int, Tuple[int, int, int]] = {}
        heap: List[Tuple[int, int, int]] = []
        stamp = 0
        results: List[int] = []

        def touch(key: int, value: int, frequency: int) -> None:
            nonlocal stamp
            stamp += 1
            live[key] = (value, frequency, stamp)
            heapq.heappush(heap, (frequency, stamp, key))

        for operation in operations:
            parts = operation.split()
            key = int(parts[1])
            if parts[0] == "get":
                if key in live:
                    value, frequency, _ = live[key]
                    touch(key, value, frequency + 1)
                    results.append(value)
                else:
                    results.append(-1)
            else:
                value = int(parts[2])
                if key in live:
                    _, frequency, _ = live[key]
                    touch(key, value, frequency + 1)
                else:
                    if len(live) == capacity:
                        while live[heap[0][2]][1:] != heap[0][:2]:
                            heapq.heappop(heap)
                        evicted = heapq.heappop(heap)
                        del live[evicted[2]]
                    touch(key, value, 1)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m log m)`

Each of the `m` operations pushes at most one entry into a heap that holds at most `m` entries, and every stale entry is popped at most once, so total pop work is bounded by total push work.

##### Space Complexity: `O(m)`

`O(u)` live records plus the heap, which retains one entry per touch until an eviction surfaces it.

#### Key Insights

- Laziness replaces decrease-key: a touch pushes a fresh entry and orphans the old one instead of repairing the heap.
- The stale test is exact: an entry is stale iff its `(frequency, stamp)` differs from the live record's `(frequency, stamp)`, so a stale entry can never win an eviction.
- Misses push nothing, which keeps the heap proportional to the number of successful touches, not to the operation count.

### Frequency Buckets with Doubly Linked Lists

#### Derivation

The heap pays a logarithmic factor for comparisons the data never needs. Two structural facts make the search unnecessary: a key's frequency only ever changes by exactly one, and recency only decides among keys of equal frequency. So keep one bucket per frequency, order each bucket's keys by recency in a doubly linked list, and let a `min_frequency` pointer name the eviction bucket. Promotion splices a node out of its bucket and appends it to the next bucket's most-recent end; eviction pops the least-recent end of `buckets[min_frequency]`; and `min_frequency` only ever climbs, by one, when the bucket it names empties:

1. Keep `key_node` mapping key to node, and `buckets` mapping frequency to a sentinel-bracketed doubly linked list (least recently used right after the head, most recently used right before the tail).
2. On `get key`: a miss returns -1; a hit promotes the node and returns its value.
3. On `put key value` for a stored key: update the value and promote.
4. Promotion: unlink the node; if its old bucket just emptied and held `min_frequency`, advance `min_frequency` by one; append the node to `buckets[frequency + 1]`.
5. On a fresh insert with `len(key_node) == capacity`: unlink the node right after `buckets[min_frequency]`'s head and delete its key.
6. Insert the new node at frequency 1 and set `min_frequency = 1`.

#### Invariant

`min_frequency` always names a non-empty bucket, and no key anywhere has a smaller frequency:

```text
buckets[min_frequency] is non-empty          while the cache holds any key
fresh insert:        min_frequency = 1       (the new key has frequency 1)
promotion:           if the old bucket was min_frequency and just emptied,
                       min_frequency += 1    (every key below has moved up or out)
eviction:            pops the head of buckets[min_frequency], which
                       stays valid because promotion only ever empties
                       the bucket the pointer names, never another one
```

The pointer can never skip past a non-empty bucket: promotion empties at most one bucket per operation, and if that bucket is `min_frequency`'s, all keys of frequency `min_frequency` are gone, so the minimum among the remaining keys is exactly one higher. Eviction therefore reads a bucket that exists and holds the least-frequent keys, with the list head breaking the recency tie.

#### Walkthrough

Example 1, each line showing the non-empty buckets after the operation, least recently used first:

```text
put 1 1    bucket 1: [1]                                min 1
put 2 2    bucket 1: [1, 2]                             min 1
get 1      bucket 1: [2]     bucket 2: [1]              min 1    out 1
put 3 3    evict head of bucket 1: key 2
           bucket 1: [3]     bucket 2: [1]              min 1
get 2      miss                                                  out -1
get 3      bucket 1 empties, min advances to 2
           bucket 2: [1, 3]                             min 2    out 3
put 4 4    evict head of bucket 2: key 1
           bucket 1: [4]     bucket 2: [3]              min 1
get 1      miss                                                  out -1
get 3      bucket 2 empties but min stays 1 (bucket 1 holds key 4)
           bucket 3: [3]                                min 1    out 3
get 4      bucket 1 empties, min advances to 2
           bucket 2: [4]     bucket 3: [3]              min 2    out 4
```

The gets collect into `[1,-1,3,-1,3,4]`, matching the expected Output. The trace shows both pointer behaviors: `min` advancing when the bucket it names empties (get 3, get 4), and staying put when a different bucket empties (get 3 after `put 4 4`).

#### Solution

The code is the invariant written down: `promote` splices and advances the pointer, eviction pops the pointer's bucket head.

```python
from typing import Dict, List, Optional, Tuple


class Node:
    def __init__(self, key: int, value: int, frequency: int) -> None:
        self.key = key
        self.value = value
        self.frequency = frequency
        self.prev_node: Optional["Node"] = None
        self.next_node: Optional["Node"] = None


class Solution:
    def processLfuCache(self, capacity: int, operations: List[str]) -> List[int]:
        key_node: Dict[int, Node] = {}
        buckets: Dict[int, Tuple[Node, Node]] = {}
        min_frequency = 0
        results: List[int] = []

        def bucket_of(frequency: int) -> Tuple[Node, Node]:
            if frequency not in buckets:
                head, tail = Node(0, 0, 0), Node(0, 0, 0)
                head.next_node = tail
                tail.prev_node = head
                buckets[frequency] = (head, tail)
            return buckets[frequency]

        def append(frequency: int, node: Node) -> None:
            tail = bucket_of(frequency)[1]
            last_node = tail.prev_node
            node.prev_node = last_node
            node.next_node = tail
            last_node.next_node = node
            tail.prev_node = node

        def unlink(node: Node) -> None:
            node.prev_node.next_node = node.next_node
            node.next_node.prev_node = node.prev_node

        def promote(node: Node) -> None:
            nonlocal min_frequency
            head, tail = bucket_of(node.frequency)
            unlink(node)
            emptied = head.next_node is tail
            if emptied:
                if node.frequency == min_frequency:
                    min_frequency += 1
                del buckets[node.frequency]
            node.frequency += 1
            append(node.frequency, node)

        for operation in operations:
            parts = operation.split()
            key = int(parts[1])
            if parts[0] == "get":
                node = key_node.get(key)
                if node is None:
                    results.append(-1)
                else:
                    promote(node)
                    results.append(node.value)
            else:
                value = int(parts[2])
                node = key_node.get(key)
                if node is not None:
                    node.value = value
                    promote(node)
                else:
                    if len(key_node) == capacity:
                        head = buckets[min_frequency][0]
                        lru_node = head.next_node
                        unlink(lru_node)
                        del key_node[lru_node.key]
                    node = Node(key, value, 1)
                    key_node[key] = node
                    append(1, node)
                    min_frequency = 1
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m)`

Every operation is a constant number of dict probes and pointer splices: O(1) average per operation across `m` operations.

##### Space Complexity: `O(u)`

One node per cached key and at most `u` non-empty buckets; emptied buckets are deleted, so nothing outlives the keys it describes.

#### Key Insights

- The +1 step is the whole design: because frequencies move by exactly one, buckets plus a climbing pointer answer "smallest frequency" without any search.
- Recency lives inside the bucket, not in a global order: the least recently used key of the minimum frequency is always the head of one specific list.
- A put that updates an existing key never evicts and never allocates; only a fresh insert into a full cache touches the eviction path.

### Ordered Dictionary per Frequency

#### Derivation

The doubly linked list exists to give each bucket two operations, append at the recent end and pop from the stale end, in constant time. [`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict) ships exactly those: a new key joins at the end, `move_to_end` repositions it, and `popitem(last=False)` removes the oldest. The buckets stay, the nodes and sentinels disappear, and the code reads as the bucket algorithm's bookkeeping handed to the library:

1. Keep `records` mapping key to `(value, frequency)` and `buckets` mapping frequency to an `OrderedDict` of keys, oldest first.
2. Promotion: delete the key from its bucket; if that bucket empties and held `min_frequency`, advance the pointer; re-insert the key at the front of `buckets[frequency + 1]` (a fresh entry joins at the most-recent end) and update its record.
3. Eviction: `popitem(last=False)` on `buckets[min_frequency]` returns the least recently used key of the minimum frequency.
4. Fresh insert: put the key at frequency 1 and set `min_frequency = 1`.

#### Walkthrough

Example 1 again, now with each bucket shown as the `OrderedDict`'s key order, oldest first:

```text
put 1 1    bucket 1: [1]                                min 1
put 2 2    bucket 1: [1, 2]                             min 1
get 1      delete 1 from bucket 1, re-insert at
           bucket 2's recent end: 1: [2]  2: [1]        min 1    out 1
put 3 3    popitem(last=False) on bucket 1 -> key 2
           1: [3]  2: [1]                               min 1
get 2      miss                                                  out -1
get 3      bucket 1 empties, min advances to 2
           2: [1, 3]                                    min 2    out 3
put 4 4    popitem(last=False) on bucket 2 -> key 1
           1: [4]  2: [3]                               min 1
get 1      miss                                                  out -1
get 3      bucket 2 empties but min stays 1
           3: [3]                                       min 1    out 3
get 4      bucket 1 empties, min advances to 2
           2: [4]  3: [3]                               min 2    out 4
```

The gets collect into `[1,-1,3,-1,3,4]`, matching the expected Output; the eviction victims (key 2, then key 1) are the same keys the linked-list version dropped.

#### Solution

```python
from collections import OrderedDict
from typing import Dict, List, Tuple


class Solution:
    def processLfuCache(self, capacity: int, operations: List[str]) -> List[int]:
        records: Dict[int, Tuple[int, int]] = {}
        buckets: Dict[int, OrderedDict] = {}
        min_frequency = 0
        results: List[int] = []

        def promote(key: int, value: int, frequency: int) -> None:
            nonlocal min_frequency
            del buckets[frequency][key]
            if not buckets[frequency]:
                if frequency == min_frequency:
                    min_frequency += 1
                del buckets[frequency]
            records[key] = (value, frequency + 1)
            buckets.setdefault(frequency + 1, OrderedDict())[key] = None

        for operation in operations:
            parts = operation.split()
            key = int(parts[1])
            if parts[0] == "get":
                if key in records:
                    value, frequency = records[key]
                    promote(key, value, frequency)
                    results.append(value)
                else:
                    results.append(-1)
            else:
                value = int(parts[2])
                if key in records:
                    _, frequency = records[key]
                    promote(key, value, frequency)
                else:
                    if len(records) == capacity:
                        lru_key, _ = buckets[min_frequency].popitem(last=False)
                        del records[lru_key]
                    records[key] = (value, 1)
                    buckets.setdefault(1, OrderedDict())[key] = None
                    min_frequency = 1
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m)`

`OrderedDict` deletes, inserts, and `popitem(last=False)` all run in O(1) average, so every operation stays constant across `m` operations.

##### Space Complexity: `O(u)`

One record per cached key and at most `u` non-empty bucket dictionaries.

#### Key Insights

- `OrderedDict` is the linked list: insertion order is the recency order, so the algorithm is unchanged and only the node plumbing vanishes.
- The min-frequency pointer survives verbatim; the library changes the container, not the invariant.
- Same complexity class as the hand-written version, with less code and the same O(u) footprint; the hand-written list is what earns the O(1) claims in languages without an ordered-dict type.

## Comparison of Solutions

### Time Complexity

- **Linear-Scan Eviction**: `O(m * u)` - every fresh insert into a full cache scans all stored records.
- **Lazy Binary Heap**: `O(m log m)` - one push per touch; stale pops are bounded by pushes.
- **Frequency Buckets with Doubly Linked Lists**: `O(m)` - O(1) average per operation.
- **Ordered Dictionary per Frequency**: `O(m)` - O(1) average per operation.

### Space Complexity

- **Linear-Scan Eviction**: `O(u)` - one record per cached key.
- **Lazy Binary Heap**: `O(m)` - stale entries linger until an eviction surfaces them.
- **Frequency Buckets with Doubly Linked Lists**: `O(u)` - nodes plus non-empty buckets only.
- **Ordered Dictionary per Frequency**: `O(u)` - records plus non-empty buckets only.

### Trade-offs

- **Linear-Scan Eviction**: the definition written down and the easiest to verify; the scan makes it unusable as the statement's O(1) answer.
- **Lazy Binary Heap**: meets the log factor halfway and survives arbitrary frequency jumps, but pays `O(log m)` and `O(m)` space for stale entries the bucket design never creates.
- **Frequency Buckets with Doubly Linked Lists**: the statement's average O(1) per operation, at the price of hand-maintained nodes and the min-frequency invariant.
- **Ordered Dictionary per Frequency**: the same O(1) average with library-maintained order; leans on `OrderedDict`, which not every language's standard library offers.

### When to Use Each

- **Linear-Scan Eviction**: as the baseline to state first, or when capacity is tiny and the operation count is small.
- **Lazy Binary Heap**: when frequencies can jump by more than one (a variant statement that adds frequency on every read of any key), where the +1 bucket structure does not apply.
- **Frequency Buckets with Doubly Linked Lists (Recommended)**: the interview answer: the classic O(1) LFU construction, and the one to reproduce on a whiteboard.
- **Ordered Dictionary per Frequency**: the Python default once the design is settled: fewer moving parts, identical guarantees.

### Optimization Notes

- **Frequency Buckets with Doubly Linked Lists** is the recommended choice: it is the only from-scratch construction that meets the statement's average O(1) requirement with O(u) space.
- Deleting emptied buckets keeps both indexes proportional to the cached keys; keeping them would leave sentinels parked at frequencies no key holds.
- The statement allows any 32-bit value, so a get returning -1 cannot by itself distinguish a miss from a stored -1; only the judged output collides, never the cache's internal state.
- The lazy heap's stale-entry trick generalizes to any "keyed priority that changes" problem; the bucket structure does not, so the two are complementary tools rather than competing ones.
