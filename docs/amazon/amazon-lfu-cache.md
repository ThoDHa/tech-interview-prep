# [LFU Cache](https://www.fastprep.io/problems/amazon-lfu-cache)

**Hard** | **NN minutes** | **Design, Hash Table, Linked List, Simulation**

Process commands on an initially empty least-frequently-used cache with positive integer capacity.

put key value inserts a new key or updates an existing key.get key returns the stored value, or -1 when the key is absent.For this exercise, assume a successful get and a put that updates an existing key each increase that key's frequency by one and make it most recently used within its new frequency. A new key starts with frequency one.

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

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
