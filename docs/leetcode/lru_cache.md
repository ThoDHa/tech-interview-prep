# [LRU Cache](https://leetcode.com/problems/lru-cache/)

**Medium** | **30 minutes** | **Hash Table, Linked List, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Linked list](https://en.wikipedia.org/wiki/Linked_list)

**Practice:** [`practice/lru_cache/solution.py`](../../practice/lru_cache/solution.py)

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the `LRUCache` class:

- `LRUCache(int capacity)` Initialize the LRU cache with positive size capacity.
- `int get(int key)` Return the value of the key if the key exists, otherwise return `-1`.
- `void put(int key, int value)` Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions `get` and `put` must each run in `O(1)` average time complexity.

## Examples

### Example 1

**Input:**

```text
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
```

**Output:**

```text
[null, null, null, 1, null, -1, null, -1, 3, 4]
```

**Explanation:**

```text
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4
```

## Constraints

- `1 <= capacity <= 3000`
- `0 <= key <= 10^4`
- `0 <= value <= 10^5`
- At most `2 * 10^5` calls will be made to `get` and `put`.

## Deriving the Solution

An LRU cache must do two things on every operation: look a key up, and know at all times which key was used least recently. A hash map makes the lookup `O(1)`; the entire difficulty is maintaining the recency ordering just as cheaply.

1. **Start literal.** Keep the ordering by hand: a dict for values plus a list
   of keys in access order, front = least recently used. Correct, but every touch calls `order.remove(key)` and every eviction `order.pop(0)`, both of which scan or shift the list, so each operation costs `O(n)`: see [Brute Force](#brute-force).
2. **Make the reorder a splice.** The list is slow for two reasons: finding a
   key means scanning, and moving a key means shifting everything after it. A doubly linked list removes a node by rewiring two pointers, and storing each key's node in the hash map removes the scan, so every touch and eviction becomes `O(1)` pointer surgery: see [Hash Map + Doubly Linked List](#hash-map-doubly-linked-list).
3. **Recognize the library structure.** A hash map fused with a doubly linked
   list kept in insertion order is exactly what Python's `OrderedDict` is; with `move_to_end` and `popitem(last=False)` the same design collapses to a few lines: see [OrderedDict](#ordereddict).

## Solutions

### Brute Force

#### Derivation

The most direct idea is to store values in a [dict](https://en.wikipedia.org/wiki/Hash_table) and track recency by hand in a separate list of keys, kept in access order. This mirrors what an LRU cache must do without reaching for any specialized structure: it just pays a linear cost to maintain the ordering.

1. Keep a dict mapping key to value, plus a list `order` whose front is the least
   recently used key and whose back is the most recently used.
2. To mark a key as recently used, remove it from wherever it sits in `order` and
   append it to the back: the `_touch` helper.
3. On `get`, return `-1` if the key is absent; otherwise touch the key and return
   its value.
4. On `put`, update and touch an existing key. For a new key, first evict the
   front of `order` (and its dict entry) if the cache is full, then store the value and append the key to the back.

The design is correct but the `order.remove` and `order.pop(0)` calls scan and shift the list, so each operation is `O(n)` rather than the required `O(1)`.

#### Walkthrough

Let us watch the Brute Force run on Example 1, with `capacity = 2`. The two pieces of state are `cache` (the key-to-value dict) and `order` (the recency list, where the front is least recently used and the back is most recently used). Each row shows both pieces of state and what the call returns after it finishes:

| Call | What happens | `cache` after | `order` after | Returns |
|------|--------------|---------------|---------------|---------|
| `LRUCache(2)` | start empty | `{}` | `[]` | `null` |
| `put(1, 1)` | new key, cache not full: store and append | `{1: 1}` | `[1]` | `null` |
| `put(2, 2)` | new key, cache not full: store and append | `{1: 1, 2: 2}` | `[1, 2]` | `null` |
| `get(1)` | key present: touch `1` (remove, append), return value | `{1: 1, 2: 2}` | `[2, 1]` | `1` |
| `put(3, 3)` | new key, cache full: evict front `2`, store `3` | `{1: 1, 3: 3}` | `[1, 3]` | `null` |
| `get(2)` | key absent | `{1: 1, 3: 3}` | `[1, 3]` | `-1` |
| `put(4, 4)` | new key, cache full: evict front `1`, store `4` | `{3: 3, 4: 4}` | `[3, 4]` | `null` |
| `get(1)` | key absent | `{3: 3, 4: 4}` | `[3, 4]` | `-1` |
| `get(3)` | key present: touch `3` (remove, append), return value | `{3: 3, 4: 4}` | `[4, 3]` | `3` |
| `get(4)` | key present: touch `4` (remove, append), return value | `{3: 3, 4: 4}` | `[3, 4]` | `4` |

The key moment is `put(3, 3)`: the cache holds `1` and `2`, but the earlier `get(1)` moved `1` to the back of `order`, leaving `2` at the front as the least recently used. So `order.pop(0)` evicts `2`, exactly as the problem requires. Later, `put(4, 4)` finds `1` at the front (untouched since its store) and evicts it.

Collecting the `Returns` column gives `[null, null, null, 1, null, -1, null, -1, 3, 4]`, which matches the expected Output.

#### Solution

The code is the walkthrough's bookkeeping in method form: `_touch` is the remove-and-append move every access performs.

```python
from typing import Dict, List


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        # Plain dict for key -> value lookup.
        self.cache: Dict[int, int] = {}
        # Separate list tracks recency by hand: front = least recently used.
        self.order: List[int] = []

    def _touch(self, key: int) -> None:
        # Move a key to the back, marking it most recently used.
        self.order.remove(key)
        self.order.append(key)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._touch(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self._touch(key)
            return
        if len(self.cache) >= self.capacity:
            # Evict the least recently used key, at the front of the order list.
            lru = self.order.pop(0)
            del self.cache[lru]
        self.cache[key] = value
        self.order.append(key)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **get**: `O(n)` - the dict read is `O(1)`, but `order.remove(key)` scans the
  list to find the key and then shifts the elements after it.
- **put**: `O(n)` - touching or evicting walks or shifts the `order` list;
  `order.pop(0)` in particular shifts every remaining key forward.

##### Space Complexity: `O(capacity)`

The dict and the `order` list each hold at most `capacity` entries, so storage scales linearly with the configured capacity.

#### Key Insights

- An LRU cache only needs two things: value lookup and a recency ordering. A dict
  plus an explicitly maintained list captures both with no special data structure.
- The cost is in list maintenance: `remove` and `pop(0)` are linear, which is why
  this fails the problem's `O(1)` requirement despite being correct.
- A `put` on an existing key still counts as a recent access, so it must touch the
  key; forgetting this would evict the wrong entry later.
- This is the natural first attempt, and seeing its linear bottleneck motivates
  the doubly linked list, where every reorder and eviction becomes `O(1)`.

### Hash Map + Doubly Linked List

#### Derivation

The Brute Force is correct; its only failure is the list. `order.remove(key)` must scan to find the key, and `order.pop(0)` must shift every remaining element. What removes both costs? A [doubly linked list](https://en.wikipedia.org/wiki/Linked_list): unlinking a node rewires two pointers regardless of position, and the hash map can store each key's *node* rather than its value, so no scan is ever needed to find it. This is the from-scratch implementation using no imports, pairing a hash map for `O(1)` lookup with a linked list that tracks recency order.

1. Each entry is a `Node` holding its key, value, and `prev`/`next` pointers. A
   dict maps key to node for constant-time access.
2. Two sentinel nodes, `head` and `tail`, bracket the list. The least recently
   used node sits just after `head`; the most recently used sits just before `tail`. Sentinels remove all special-casing for the list endpoints.
3. Two helpers do the pointer surgery: `_remove` unlinks a node, and
   `_add_to_back` splices a node in just before `tail`.
4. On `get`, return `-1` if the key is absent; otherwise move the touched node to
   the back (most recently used) and return its value.
5. On `put`, update and promote an existing key, or create a new node and add it
   to the back. When the size exceeds `capacity`, evict the node right after `head` (the least recently used) and drop it from the dict.

Storing the key inside each node is what lets eviction delete the correct dict entry in `O(1)`.

#### Walkthrough

Let us run Example 1 through the linked-list design, with `capacity = 2`. The recency order is read off the list from `head` (least recently used end) to `tail` (most recently used end); `cache` maps each key to its node. Each line shows one call, the pointer surgery it performs, and the state afterward:

```text
LRUCache(2)   link sentinels                 head <-> tail                keys {}
put(1, 1)     _add_to_back(node 1)           head <-> 1 <-> tail          keys {1}
put(2, 2)     _add_to_back(node 2)           head <-> 1 <-> 2 <-> tail    keys {1, 2}
get(1) -> 1   _remove(1), _add_to_back(1)    head <-> 2 <-> 1 <-> tail    keys {1, 2}
put(3, 3)     _add_to_back(node 3), size 3 > 2:
              _remove(head.next = 2), del cache[2]
                                             head <-> 1 <-> 3 <-> tail    keys {1, 3}
get(2) -> -1  key absent, no surgery         head <-> 1 <-> 3 <-> tail    keys {1, 3}
put(4, 4)     _add_to_back(node 4), size 3 > 2:
              _remove(head.next = 1), del cache[1]
                                             head <-> 3 <-> 4 <-> tail    keys {3, 4}
get(1) -> -1  key absent, no surgery         head <-> 3 <-> 4 <-> tail    keys {3, 4}
get(3) -> 3   _remove(3), _add_to_back(3)    head <-> 4 <-> 3 <-> tail    keys {3, 4}
get(4) -> 4   _remove(4), _add_to_back(4)    head <-> 3 <-> 4 <-> tail    keys {3, 4}
```

The decisive call is again `put(3, 3)`: the earlier `get(1)` spliced node `1` to the back, so `head.next` is node `2`, and the eviction unlinks it and deletes `cache[2]` using the key stored on the node itself. Every line's surgery is a constant number of pointer reassignments: no scan, no shift. Collecting the returns, with `null` for the constructor and each `put`, gives `[null, null, null, 1, null, -1, null, -1, 3, 4]`, matching the expected Output.

#### Solution

The code is the walkthrough's pointer surgery: `_remove` and `_add_to_back` are the two splices every access performs.

```python
from typing import Dict


class Node:

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        # Map key -> node for O(1) lookup.
        self.cache: Dict[int, Node] = {}
        # Sentinel head and tail bracket the list so no corner cases on ends.
        # head <-> ... <-> tail; most recently used sits just before tail.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        # Unlink a node from its current position.
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_back(self, node: Node) -> None:
        # Insert just before the tail sentinel (most recently used end).
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # Touching a node makes it most recently used: move it to the back.
        self._remove(node)
        self._add_to_back(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing node and mark it most recently used.
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_back(node)
            return

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_back(node)

        if len(self.cache) > self.capacity:
            # Evict the least recently used node, just after the head sentinel.
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **get**: `O(1)` - a dict lookup plus a constant number of pointer
  reassignments to move the node to the back.
- **put**: `O(1)` - a dict membership test, node creation or update, and a
  constant number of pointer splices, including at most one eviction.

##### Space Complexity: `O(capacity)`

The dict and the linked list together hold at most `capacity` nodes, so storage scales linearly with the configured capacity.

#### Key Insights

- Pairing a hash map (fast lookup) with a doubly linked list (fast reordering and
  eviction) is the canonical way to get `O(1)` for every LRU operation.
- Sentinel `head` and `tail` nodes eliminate null checks when inserting or
  removing at the ends of the list.
- Storing the key on the node is essential: when evicting from the list you need
  the key to remove the matching dict entry.
- Treating a `put` on an existing key as a recent access (move it to the back)
  prevents the wrong key from being evicted later.

### OrderedDict

#### Derivation

The previous solution hand-builds a hash map fused with a doubly linked list, and that exact fusion already ships in the standard library. An LRU cache needs `O(1)` lookup by key plus `O(1)` identification and removal of the least recently used entry, and Python's [`OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict) provides exactly this: hash-table access combined with a doubly linked list that preserves insertion and re-insertion order. All that remains is mapping the cache operations onto its methods.

1. Maintain an `OrderedDict` whose front holds the least recently used key and
   whose back holds the most recently used key.
2. On `get`, return `-1` if the key is absent; otherwise call `move_to_end` to
   mark it most recently used and return its value.
3. On `put`, if the key already exists move it to the end before overwriting so
   updates also count as recent use.
4. After inserting, if the size exceeds `capacity`, call `popitem(last=False)`
   to evict the front entry, the least recently used key.

`move_to_end`, `popitem`, and dictionary indexing are all `O(1)` on `OrderedDict`, satisfying the required average time bound.

#### Walkthrough

Let us run Example 1 on the `OrderedDict`, with `capacity = 2`. The dict is shown front to back, so the leftmost pair is the least recently used and the rightmost the most recently used:

```text
LRUCache(2)   start empty                          cache = {}
put(1, 1)     new key: cache[1] = 1                cache = {1: 1}
put(2, 2)     new key: cache[2] = 2                cache = {1: 1, 2: 2}
get(1) -> 1   move_to_end(1)                       cache = {2: 2, 1: 1}
put(3, 3)     cache[3] = 3, len 3 > 2:
              popitem(last=False) evicts (2, 2)    cache = {1: 1, 3: 3}
get(2) -> -1  key absent                           cache = {1: 1, 3: 3}
put(4, 4)     cache[4] = 4, len 3 > 2:
              popitem(last=False) evicts (1, 1)    cache = {3: 3, 4: 4}
get(1) -> -1  key absent                           cache = {3: 3, 4: 4}
get(3) -> 3   move_to_end(3)                       cache = {4: 4, 3: 3}
get(4) -> 4   move_to_end(4)                       cache = {3: 3, 4: 4}
```

The eviction inside `put(3, 3)` removes key `2` rather than key `1` because the earlier `get(1)` had already moved `1` to the back: `popitem(last=False)` always pops the front, the least recently used entry. Collecting the returns, with `null` for the constructor and each `put`, gives `[null, null, null, 1, null, -1, null, -1, 3, 4]`, matching the expected Output.

#### Solution

The code is the walkthrough's trace with `OrderedDict` supplying the order maintenance.

```python
from collections import OrderedDict


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        # OrderedDict keeps keys in access order: front = least recently used.
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Touching a key makes it the most recently used.
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Evict the least recently used entry (front of the ordering).
            self.cache.popitem(last=False)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **get**: `O(1)` average - a membership test, a `move_to_end`, and an indexing
  read, each `O(1)` average on `OrderedDict`.
- **put**: `O(1)` average - an optional `move_to_end`, an assignment, and an
  optional `popitem(last=False)`, every one `O(1)` average.

##### Space Complexity: `O(capacity)`

The cache never holds more than `capacity` key-value pairs; the underlying hash table and linked-list nodes scale linearly with that bound.

#### Key Insights

- `OrderedDict` already pairs a hash map with a doubly linked list, so it gives
  both `O(1)` lookup and `O(1)` recency reordering for free.
- Treating an update (`put` on an existing key) as a recent access is essential;
  forgetting `move_to_end` there would evict the wrong entry.
- `popitem(last=False)` pops from the front, which is precisely the least
  recently used end of the ordering.
- This is the concise expected answer when standard-library shortcuts are
  allowed; the manual node-and-dict version yields identical complexity when they are not.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` per operation - dict access is `O(1)`, but maintaining
  the recency list with `remove` and `pop(0)` scans and shifts the list.
- **Hash Map + Doubly Linked List**: `O(1)` per operation - constant pointer
  splices replace the linear list maintenance.
- **OrderedDict**: `O(1)` average per operation - `move_to_end`, indexing, and
  `popitem(last=False)` are each `O(1)` average, delegated to the standard library.

### Space Complexity

- **Brute Force**: `O(capacity)` - a dict plus a separate key-order list, each
  holding at most `capacity` entries.
- **Hash Map + Doubly Linked List**: `O(capacity)` - the dict and the explicit
  nodes plus sentinels scale linearly with capacity.
- **OrderedDict**: `O(capacity)` - the equivalent hash map and linked list, hidden
  inside the C implementation.

### Trade-offs

- Brute Force gains the simplest mental model (a dict plus a hand-tracked order
  list) but gives up the required `O(1)` bound: `remove` and `pop(0)` are linear.
- Hash Map + Doubly Linked List gains `O(1)` per operation by spelling out every
  pointer move, at the cost of more code and more room for off-by-one mistakes, while depending on nothing beyond the language.
- OrderedDict gains brevity and reliability by leaning on a well-tested
  standard-library structure that already fuses a hash map with a recency-ordered linked list, giving up some conceptual transparency.

### When to Use Each

- **Brute Force**: As a teaching baseline that shows what an LRU cache must
  track, before the linear list cost motivates a better structure.
- **Hash Map + Doubly Linked List**: The expected interview answer when library
  shortcuts are disallowed, or when you need full control over the node structure (for example to attach extra metadata per entry).
- **OrderedDict**: Preferred for production and concise solutions where the
  standard library is available, since it is shorter, clearer, and battle-tested.

### Optimization Notes

- All three designs hinge on the same core idea: a hash map for `O(1)` key lookup
  combined with a recency ordering for eviction. They differ only in how cheaply that ordering is maintained.
- The brute force's bottleneck is list maintenance; replacing the order list with
  a doubly linked list turns every reorder and eviction from `O(n)` into `O(1)`.
- Sentinel head and tail nodes in the from-scratch linked-list version remove
  endpoint corner cases, the most common source of bugs in a manual implementation.
- `OrderedDict` is essentially the hash-map-plus-doubly-linked-list structure
  implemented in C, so choosing it trades a small amount of conceptual transparency for brevity and reliability without changing the complexity.
