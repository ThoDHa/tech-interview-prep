# [Latest-Timestamp Key-Value Store](https://www.fastprep.io/problems/amazon-latest-timestamp-key-value-store)

**Medium** | **NN minutes** | **Hash Table, Design**

Source note: The source reports set(timestamp,key,value) and get(key) returning the greatest-timestamp value. This exercise uses a finite operation sequence with authored tie handling, missing-key output, bounds and examples. The LRU comparison in the report does not specify a capacity or eviction policy; this version has no eviction. Approximate source match: 96%.

Implement a key-value store that chooses values by their supplied timestamps, not by arrival order. The four aligned arrays describe a finite sequence of operations:

operations[i] = 0: perform set(timestamps[i], keys[i], values[i]).operations[i] = 1: perform get(keys[i]). Ignore timestamps[i] and values[i] for this operation.A get returns the value from a preceding set for that key whose timestamp is greatest. If several preceding sets have that greatest timestamp, use the one that occurs latest in the operation sequence. If the key has never been set, return the empty string.

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

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
