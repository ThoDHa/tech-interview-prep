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

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
