# [LRU Cache for Query Results](https://www.fastprep.io/problems/amazon-lru-query-result-cache)

**Medium** | **NN minutes** | **Design, Hash Table, Linked List, Simulation**

Maintain a cache with positive integer capacity. Process each operation atomically in the supplied completed serialization order:

[1, key] performs get(key). Return the stored value, or -1 when the key is absent. A successful get makes the key most recently used.[2, key, value] performs put(key, value). Insert or update the key and make it most recently used. Updating an existing key does not change the cache size. If an insertion exceeds capacity, evict exactly the least recently used key.Return one string per operation: the decimal result of each get and the literal string "null" for each put. Implement both operations in O(1) expected time.

The supplied order is a deterministic linearization of completed concurrent operations; an implementation exposed to threads would guard each public operation as one atomic critical section.

## Examples

### Example 1

**Input:** `capacity = 2`, `operations = [[2,1,10],[2,2,20],[1,1],[2,3,30],[1,2],[1,3]]`

**Output:** `["null","null","10","null","-1","30"]`

**Explanation:** Reading key 1 makes it recent, so inserting key 3 evicts key 2.

### Example 2

**Input:** `capacity = 2`, `operations = [[2,1,5],[2,2,6],[2,1,7],[2,3,8],[1,1],[1,2],[1,3]]`

**Output:** `["null","null","null","null","7","-1","8"]`

**Explanation:** Updating key 1 changes its value and recency without growing the cache, so key 2 is evicted next.

## Constraints

- `1 <= capacity <= 100000.`
- `1 <= operations.length <= 100000.`
- `Every operation has one of the two documented forms.`
- `Keys and values are signed 32-bit integers. The value -1 may be stored and remains distinguishable only by whether the key is present.`

## Solutions

### Brute Force

#### Derivation

The most direct design keeps the two things an LRU cache needs side by side: a [hash table](https://en.wikipedia.org/wiki/Hash_table) `values` for key lookup, and a plain list `order` of keys arranged by recency, front = least recently used, back = most recently used. Every access renews its key's place in `order` by hand. This works, but each renewal pays a linear cost, which is exactly what the problem's `O(1)` requirement forbids:

1. Keep `values` (key to value) and `order` (keys by recency).
2. `touch(key)` removes `key` from wherever it sits in `order` and appends it to
   the back, marking it most recently used.
3. On `get`, append `"-1"` to `results` when the key is absent; otherwise touch
   the key and append `str(values[key])`.
4. On `put`, update and touch an existing key (no size change). For a new key,
   first evict `order.pop(0)` and its `values` entry when the cache is at
   capacity, then store and append.
5. Append `"null"` for every `put`, and return `results`.

`order.remove` scans the list and `order.pop(0)` shifts every remaining key, so each operation is linear in the cache size.

#### Walkthrough

Example 1, `capacity = 2`, shown as the state after each operation finishes:

| Operation | What happens | `values` after | `order` after | Returns |
|------|--------------|---------------|---------------|---------|
| `put(1, 10)` | new key, not full: store and append | `{1: 10}` | `[1]` | `"null"` |
| `put(2, 20)` | new key, not full: store and append | `{1: 10, 2: 20}` | `[1, 2]` | `"null"` |
| `get(1)` | present: touch `1`, return value | `{1: 10, 2: 20}` | `[2, 1]` | `"10"` |
| `put(3, 30)` | new key, full: evict front `2` | `{1: 10, 3: 30}` | `[1, 3]` | `"null"` |
| `get(2)` | absent | `{1: 10, 3: 30}` | `[1, 3]` | `"-1"` |
| `get(3)` | present: touch `3`, return value | `{1: 10, 3: 30}` | `[1, 3]` | `"30"` |

The decisive row is `put(3, 30)`: the earlier `get(1)` moved `1` behind `2` in `order`, leaving `2` at the front as the least recently used, so `order.pop(0)` evicts `2`. Collecting the returns gives `["null","null","10","null","-1","30"]`, matching the expected Output.

#### Solution

The code is the walkthrough's bookkeeping in method form: `touch` is the remove-and-append move every access performs.

```python
from typing import Dict, List


class Solution:
    def solve(self, capacity: int, operations: List[List[int]]) -> List[str]:
        values: Dict[int, int] = {}
        order: List[int] = []
        results: List[str] = []

        def touch(key: int) -> None:
            order.remove(key)
            order.append(key)

        for operation in operations:
            if operation[0] == 1:
                key = operation[1]
                if key not in values:
                    results.append("-1")
                    continue
                touch(key)
                results.append(str(values[key]))
            else:
                key, value = operation[1], operation[2]
                if key in values:
                    values[key] = value
                    touch(key)
                else:
                    if len(values) >= capacity:
                        del values[order.pop(0)]
                    values[key] = value
                    order.append(key)
                results.append("null")

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **get**: `O(k)` - the dict read is constant, but `order.remove(key)` scans up to
  the whole list and `pop` shifts everything after the removal point, with `k` the
  current cache size.
- **put**: `O(k)` - touching or evicting walks and shifts `order`;
  `order.pop(0)` alone shifts every remaining key.

With `m` operations this is `O(m × capacity)` overall, against the required `O(1)` per operation.

##### Space Complexity: `O(capacity)`

The dict and the order list each hold at most `capacity` entries.

#### Key Insights

- A dict plus a hand-tracked recency list captures the full semantics with no specialized structure, which makes it a useful baseline for checking the faster versions against.
- A `put` on an existing key still counts as a recent access and must touch the key; skipping that would evict the wrong entry later.
- A miss must not change recency: only a successful `get` promotes the key.
- The linear `remove` and `pop(0)` costs are the whole gap between this and the required bound, which points directly at a linked structure.

### Hash Map + Doubly Linked List

#### Derivation

The brute force fails only on the list. `order.remove(key)` scans to find the key, and `order.pop(0)` shifts everything behind it. A [doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list) removes both costs: unlinking a node rewires two pointers regardless of position, and storing each key's node in the hash map means no scan is ever needed to find it. Sentinels `head` and `tail` bracket the list so the endpoints need no special cases: the least recently used node sits just after `head`, the most recently used just before `tail`:

1. Keep `nodes`, mapping key to a `Node` carrying `key`, `value`, and the two
   neighbor pointers.
2. `unlink(node)` splices a node out; `append_to_back(node)` splices it in just
   before `tail`. Every access performs exactly this pair.
3. On `get`, append `"-1"` when the key is absent; otherwise unlink and re-append
   its node, and append `str(node.value)`.
4. On `put`, update and re-append an existing node. For a new key, append a fresh
   node; when `nodes` then exceeds `capacity`, unlink `head.next` (the least
   recently used) and delete its `nodes` entry, which works only because the
   node itself carries its key.
5. Append `"null"` for every `put`, and return `results`.

#### Walkthrough

Example 2, `capacity = 2`, with the list read from `head` (least recently used end) to `tail` (most recently used end):

```text
put(1, 5)      append node 1              head <-> 1 <-> tail          nodes {1}
put(2, 6)      append node 2              head <-> 1 <-> 2 <-> tail    nodes {1, 2}
put(1, 7)      update: unlink 1, re-append (size unchanged)
                                          head <-> 2 <-> 1 <-> tail    nodes {1, 2}
put(3, 8)      append node 3, size 3 > 2:
               unlink head.next = 2, del nodes[2]
                                          head <-> 1 <-> 3 <-> tail    nodes {1, 3}
get(1) -> 7    unlink 1, re-append        head <-> 3 <-> 1 <-> tail    nodes {1, 3}
get(2) -> -1   absent                     head <-> 3 <-> 1 <-> tail    nodes {1, 3}
get(3) -> 8    unlink 3, re-append        head <-> 1 <-> 3 <-> tail    nodes {1, 3}
```

The decisive call is `put(1, 7)`: updating an existing key rewires recency without growing the cache, so the next eviction targets `2`, not `1`. Collecting the returns gives `["null","null","null","null","7","-1","8"]`, matching the expected Output.

#### Solution

The code is the walkthrough's pointer surgery: `unlink` and `append_to_back` are the two splices every access performs.

```python
from typing import Dict, List


class Node:

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.previous_node: "Node | None" = None
        self.next: "Node | None" = None


class Solution:
    def solve(self, capacity: int, operations: List[List[int]]) -> List[str]:
        nodes: Dict[int, Node] = {}
        head = Node()
        tail = Node()
        head.next = tail
        tail.previous_node = head
        results: List[str] = []

        def unlink(node: Node) -> None:
            previous_node, next_node = node.previous_node, node.next
            previous_node.next = next_node
            next_node.previous_node = previous_node

        def append_to_back(node: Node) -> None:
            last_node = tail.previous_node
            last_node.next = node
            node.previous_node = last_node
            node.next = tail
            tail.previous_node = node

        def get(key: int) -> str:
            if key not in nodes:
                return "-1"
            node = nodes[key]
            unlink(node)
            append_to_back(node)
            return str(node.value)

        def put(key: int, value: int) -> None:
            if key in nodes:
                node = nodes[key]
                node.value = value
                unlink(node)
                append_to_back(node)
                return
            node = Node(key, value)
            nodes[key] = node
            append_to_back(node)
            if len(nodes) > capacity:
                least_recent = head.next
                unlink(least_recent)
                del nodes[least_recent.key]

        for operation in operations:
            if operation[0] == 1:
                results.append(get(operation[1]))
            else:
                put(operation[1], operation[2])
                results.append("null")

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **get**: `O(1)` expected - one dict lookup plus a constant number of pointer
  reassignments.
- **put**: `O(1)` expected - a dict membership test, node creation or update,
  and at most one eviction, all constant work.

With `m` operations this is `O(m)` overall, meeting the required per-operation bound.

##### Space Complexity: `O(capacity)`

The dict and the linked nodes, plus two sentinels, scale linearly with capacity.

#### Key Insights

- Storing the key inside each node is what makes eviction constant time: unlinking `head.next` yields the dict entry to delete without a search.
- Sentinels remove every endpoint special case, the classic source of bugs in hand-built lists.
- Eviction happens only on insertion of a new key and only when the size exceeds capacity; updates never evict.
- The supplied order is a completed serialization: each `get`/`put` above runs as one atomic critical section, and a threaded implementation would guard each public operation the same way.

### OrderedDict

#### Derivation

The previous solution hand-builds a hash map fused with a doubly linked list, and that fusion already ships in the standard library: Python's [`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict) is exactly that structure, with `move_to_end` and `popitem(last=False)` covering the two splices. Only the operation mapping remains:

1. Keep `cache`, an `OrderedDict` whose front holds the least recently used key
   and whose back holds the most recently used.
2. On `get`, append `"-1"` when the key is absent; otherwise `move_to_end(key)`
   and append `str(cache[key])`.
3. On `put`, `move_to_end(key)` first when the key exists (updates count as
   recent use), then assign `cache[key] = value`.
4. After an insertion that grows the dict past `capacity`, evict with
   `popitem(last=False)`, which pops the front, the least recently used entry.
5. Append `"null"` for every `put`, and return `results`.

#### Walkthrough

Example 1, `capacity = 2`, with `cache` shown front to back, so the leftmost pair is the least recently used:

```text
put(1, 10)     new key                    cache = {1: 10}
put(2, 20)     new key                    cache = {1: 10, 2: 20}
get(1) -> 10   move_to_end(1)             cache = {2: 20, 1: 10}
put(3, 30)     insert 3, len 3 > 2:
               popitem(last=False) evicts (2, 20)
                                          cache = {1: 10, 3: 30}
get(2) -> -1   absent                     cache = {1: 10, 3: 30}
get(3) -> 30   move_to_end(3)             cache = {1: 10, 3: 30}
```

The eviction inside `put(3, 30)` removes `2` rather than `1` because the earlier `get(1)` had already moved `1` to the back. Collecting the returns gives `["null","null","10","null","-1","30"]`, matching the expected Output.

#### Solution

The code is the walkthrough's trace with `OrderedDict` supplying the order maintenance.

```python
from collections import OrderedDict
from typing import List


class Solution:
    def solve(self, capacity: int, operations: List[List[int]]) -> List[str]:
        cache: OrderedDict[int, int] = OrderedDict()
        results: List[str] = []

        for operation in operations:
            if operation[0] == 1:
                key = operation[1]
                if key not in cache:
                    results.append("-1")
                    continue
                cache.move_to_end(key)
                results.append(str(cache[key]))
            else:
                key, value = operation[1], operation[2]
                if key in cache:
                    cache.move_to_end(key)
                cache[key] = value
                if len(cache) > capacity:
                    cache.popitem(last=False)
                results.append("null")

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **get**: `O(1)` expected - a membership test, a `move_to_end`, and an indexing
  read, each constant expected on `OrderedDict`.
- **put**: `O(1)` expected - an optional `move_to_end`, an assignment, and at
  most one `popitem(last=False)`.

With `m` operations this is `O(m)` overall.

##### Space Complexity: `O(capacity)`

The dict never holds more than `capacity` key-value pairs; the hash table and linked nodes inside it scale with that bound.

#### Key Insights

- `OrderedDict` pairs hash access with a recency-ordered linked list, so `move_to_end` and `popitem(last=False)` are exactly `unlink` plus `append_to_back` and the head eviction, delegated to well-tested C code.
- The presence check, not a `-1` sentinel comparison, decides hits and misses: the constraint allows storing `-1` as a value, which stays distinguishable only by membership.
- Insert, check size, evict is the safe sequence; evicting before insert would drop a key when capacity is not yet reached on an update path.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(k)` per operation - `order.remove` scans and `order.pop(0)` shifts the recency list, with `k` the current cache size.
- **Hash Map + Doubly Linked List**: `O(1)` expected per operation - constant pointer splices replace all list maintenance.
- **OrderedDict**: `O(1)` expected per operation - the same pointer work, delegated to `move_to_end` and `popitem(last=False)`.

### Space Complexity

- **Brute Force**: `O(capacity)` - the value dict plus a separate key-order list.
- **Hash Map + Doubly Linked List**: `O(capacity)` - the node dict plus the explicit nodes and two sentinels.
- **OrderedDict**: `O(capacity)` - the equivalent hash map and linked list inside one container.

### Trade-offs

- **Brute Force**: the simplest mental model and a correct oracle for testing, but it violates the problem's `O(1)` requirement.
- **Hash Map + Doubly Linked List**: meets the bound while depending on nothing beyond the language, at the cost of the most code and the most places to slip a pointer.
- **OrderedDict**: the same design in a few lines, battle-tested, giving up visibility into the pointer mechanics.

### When to Use Each

- **Brute Force**: as a teaching baseline and a reference oracle when testing the faster versions.
- **Hash Map + Doubly Linked List (Recommended for interviews)**: when the interviewer forbids library shortcuts or asks how `OrderedDict` works underneath.
- **OrderedDict**: the default production and OA answer where the standard library is allowed.

### Optimization Notes

- All three designs share one core idea: a hash map for lookup plus a recency ordering for eviction; they differ only in what maintains the ordering.
- Touching on update is the subtlest requirement: both Example 1's eviction of `2` after a read of `1` and Example 2's eviction of `2` after an update of `1` hinge on it.
- Batch processing changes nothing per operation: the `results` list is just each operation's return collected in the supplied serialization order.
- Under real concurrency each public operation must run as one atomic critical section, since interleaving a `get` between an insert and its eviction would expose a transient over-capacity state.
