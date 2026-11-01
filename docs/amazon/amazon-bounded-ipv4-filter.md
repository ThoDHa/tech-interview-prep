# [Bounded IPv4 Filter](https://www.fastprep.io/problems/amazon-bounded-ipv4-filter)

**Easy** | **NN minutes** | **Array, Hash Table, Simulation**

Source note: The report specifies three IPv4 pool operations, a 128-entry limit, and a small Linux environment. Initial state, full-pool behavior, and input conventions are specified for practice. The judged core task matches the source at about 90%.

Implement an IPv4 address pool that can store at most 128 distinct addresses. The pool supports adding an address, removing an address, and checking whether an address is currently present.

You are given two arrays, operations and addresses, of equal length. Start with an empty pool and process their entries in order. Entry i applies operations[i] to addresses[i].

add_ip: if the address is already present, leave the pool unchanged. Otherwise, add it only if the pool has fewer than 128 distinct addresses. If the pool is full, ignore the addition without removing any stored address.
remove_ip: remove the address if present. Removing an absent address leaves the pool unchanged.
check_ip: report true if the exact address is currently present and false otherwise.

Return the results of only the check_ip operations, in their original order. Adding and removing addresses produce no output. If there are no checks, return an empty boolean array.

All addresses are valid IPv4 addresses in canonical dotted-decimal notation: four decimal octets from 0 through 255, with no leading zeros except the single digit 0. Every address from 0.0.0.0 through 255.255.255.255 is a valid pool key. Match complete addresses; there are no subnets, prefixes, or wildcard rules.

Memory and implementation trade-offs

The interview setting is a small Linux system with at most 128 stored records. Consider how to keep the pool representation small and explain the time and memory costs of your chosen data structure. This exercise does not impose a language-specific memory limit or require one particular representation.

## Examples

### Example 1

**Input:** `operations = ["check_ip","add_ip","check_ip","add_ip","remove_ip","check_ip"]`, `addresses = ["10.0.0.1","10.0.0.1","10.0.0.1","10.0.0.1","10.0.0.1","10.0.0.1"]`

**Output:** `[false,true,false]`

**Explanation:** The first check finds an empty pool. After adding 10.0.0.1, the next check returns true. Adding the same address again does not create another copy, so one removal makes the final check return false.

### Example 2

**Input:** `operations = ["add_ip","add_ip","remove_ip","check_ip","check_ip","check_ip"]`, `addresses = ["0.0.0.0","255.255.255.255","128.0.0.0","255.255.255.255","128.0.0.0","0.0.0.0"]`

**Output:** `[true,false,true]`

**Explanation:** Both endpoint addresses remain present. Removing the absent address 128.0.0.0 changes nothing, and its check returns false.

### Example 3

**Input:** `operations = ["add_ip","remove_ip"]`, `addresses = ["192.168.1.1","192.168.1.1"]`

**Output:** `[]`

**Explanation:** There are no check_ip operations, so the output is empty.

## Constraints

- `0 <= operations.length = addresses.length <= 10^4.`
- `Every operation is add_ip, remove_ip, or check_ip.`
- `Every address uses the canonical IPv4 format described above.`
- `The pool contains at most 128 distinct addresses after every operation.`
- `Operations are processed sequentially, with a new empty pool for each call.`

## Deriving the Solution

The whole problem is one question asked three ways about a small bounded set: is this address in the pool, and can it join, and how does it leave. With at most 128 stored addresses every operation is cheap by definition, so the real decisions are the membership container and the per-record representation. The ladder walks both:

1. **Start literal.** Keep the stored addresses in a list and scan it for every membership question. It is the definition, at a per-operation cost that grows with the pool: see [Address List with Linear Scan](#address-list-with-linear-scan).
2. **Hash the addresses.** A set answers membership, insertion, and removal without scanning; the records are the canonical strings: see [Address Set](#address-set).
3. **Shrink the record.** A canonical dotted quad carries at most 15 characters but only 32 bits of information, so each address packs into one integer and the set stores one machine word per record, the memory trade the statement's closing note asks about: see [Packed Octet Integer Set](#packed-octet-integer-set).

## Solutions

### Address List with Linear Scan

#### Derivation

The statement's most literal reading: the pool is the collection of addresses currently stored. A list holds them in arrival order, and each operation scans: `add_ip` adds only when a scan misses and the pool is below 128, `remove_ip` deletes the scan's hit, and `check_ip` reports whether the scan hit:

1. Keep the pool in a list `stored`, and collect `results`.
2. On `add_ip`: when `address not in stored` and `len(stored) < 128`,
   append it; otherwise leave the pool unchanged.
3. On `remove_ip`: when `address in stored`, remove it.
4. On `check_ip`: append `address in stored` to `results`.
5. Return `results`, one boolean per check.

#### Walkthrough

Example 1, all six operations touch `10.0.0.1`. `stored` is the list, the boolean the check appends:

```text
check_ip    stored = []                     scan misses   -> false
add_ip      scan misses, 0 < 128            stored = [10.0.0.1]
check_ip    scan hits                       -> true
add_ip      scan hits (duplicate)           stored unchanged
remove_ip   scan hits                       stored = []
check_ip    stored = []                     scan misses   -> false
```

The checks collect into `[false, true, false]`, matching the expected Output. The duplicate add is visible in the trace: the scan hit leaves the pool unchanged, so one removal empties it.

#### Solution

```python
from typing import List


class Solution:
    def processIpOperations(
        self, operations: List[str], addresses: List[str]
    ) -> List[bool]:
        stored: List[str] = []
        results: List[bool] = []
        for operation, address in zip(operations, addresses):
            if operation == "add_ip":
                if address not in stored and len(stored) < 128:
                    stored.append(address)
            elif operation == "remove_ip":
                if address in stored:
                    stored.remove(address)
            else:
                results.append(address in stored)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * u)`

Each of the `m` operations scans the pool of `u <= 128` stored addresses. The bound is a genuine constant here, but a scan-heavy workload pays it on every operation.

##### Space Complexity: `O(u)`

The list holds at most 128 address strings, plus the results.

#### Key Insights

- The three operations share one primitive, the membership scan; getting its two guards (absence for add, presence for remove) right is the entire correctness burden.
- The capacity rule needs the size check only on the add path: removals and checks never grow the pool.
- Arrival-order storage preserves nothing the problem asks about, which is the clue that a membership-first container fits better.

### Address Set

#### Derivation

The linear scan answers "is this address stored?" by reading every record, but the question is exactly set membership, and a [hash set](https://en.wikipedia.org/wiki/Hash_table) answers it by computing the record's bucket directly. Insertion and removal collapse to `add` and `discard`, both constant time on average, and the capacity guard still reads the set's size:

1. Keep the pool in the set `stored`.
2. On `add_ip`: when `len(stored) < 128`, add the address. Adding a present
   address is a no-op, so the duplicate rule needs no separate probe.
3. On `remove_ip`: discard the address; discarding an absent address is a
   no-op.
4. On `check_ip`: append `address in stored`.

#### Walkthrough

Example 2, the boundary addresses. `stored` shown after each operation:

```text
add_ip 0.0.0.0             stored = {0.0.0.0}
add_ip 255.255.255.255     stored = {0.0.0.0, 255.255.255.255}
remove_ip 128.0.0.0        absent, discard is a no-op
check_ip 255.255.255.255   in stored  -> true
check_ip 128.0.0.0         not stored -> false
check_ip 0.0.0.0           in stored  -> true
```

The checks collect into `[true, false, true]`, matching the expected Output. The absent removal changed nothing, which the third check confirms.

#### Solution

```python
from typing import List, Set


class Solution:
    def processIpOperations(
        self, operations: List[str], addresses: List[str]
    ) -> List[bool]:
        stored: Set[str] = set()
        results: List[bool] = []
        for operation, address in zip(operations, addresses):
            if operation == "add_ip":
                if len(stored) < 128:
                    stored.add(address)
            elif operation == "remove_ip":
                stored.discard(address)
            else:
                results.append(address in stored)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m)`

Each of the `m` operations does one average-constant-time set operation plus its string hashing.

##### Space Complexity: `O(u)`

The set holds at most 128 address strings, plus the results.

#### Key Insights

- The set's no-op-on-duplicate semantics for `add` and `discard` absorb two of the statement's special cases wholesale; no explicit presence probes are needed.
- The capacity guard `len(stored) < 128` is correct on its own: a full pool ignores every add, and an add of an already-present address changes nothing whether or not the pool is full.
- What remains is the record's footprint: each entry is the full string, whose characters carry the same 32 bits the address was born with.

### Packed Octet Integer Set

#### Derivation

The Address Set is already linear overall, so the honest question left is the one the statement's closing note asks: how small can each stored record be? A canonical dotted quad has four octets, each 0 through 255, which is exactly 32 bits of information. Packing the octets into one integer, `(o1 << 24) | (o2 << 16) | (o3 << 8) | o4`, turns every record into a single machine word: the set's hashing shrinks to small-integer hashing, and canonical form (no leading zeros) makes the packing injective, so distinct addresses cannot collide:

1. Keep `pool_to_int(address)` returning the packed 32-bit integer.
2. Keep the pool in the set `stored` of packed integers.
3. On `add_ip`: when `len(stored) < 128`, add the packing of the address.
4. On `remove_ip`: discard the packing.
5. On `check_ip`: append whether the packing is in `stored`.

#### Walkthrough

Example 1, showing the packing of every address (they are all `10.0.0.1`), with `stored` the set of packed words:

```text
pack 10.0.0.1   (10 << 24) | (0 << 16) | (0 << 8) | 1 = 167772161

check_ip    stored = {}                    miss           -> false
add_ip      insert 167772161               stored = {167772161}
check_ip    167772161 in stored            -> true
add_ip      duplicate insert, no change
remove_ip   discard 167772161              stored = {}
check_ip    stored = {}                    miss           -> false
```

The checks collect into `[false, true, false]`, matching the expected Output. Every membership decision ran on the integer `167772161`; the string form never entered the pool.

#### Solution

The code is the Address Set's dispatch loop with the packing in front of every set operation.

```python
from typing import List, Set


class Solution:
    def processIpOperations(
        self, operations: List[str], addresses: List[str]
    ) -> List[bool]:
        def pool_to_int(address: str) -> int:
            first_octet, second_octet, third_octet, fourth_octet = (
                int(part) for part in address.split(".")
            )
            return (
                (first_octet << 24)
                | (second_octet << 16)
                | (third_octet << 8)
                | fourth_octet
            )

        stored: Set[int] = set()
        results: List[bool] = []
        for operation, address in zip(operations, addresses):
            packed = pool_to_int(address)
            if operation == "add_ip":
                if len(stored) < 128:
                    stored.add(packed)
            elif operation == "remove_ip":
                stored.discard(packed)
            else:
                results.append(packed in stored)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m)`

Each operation pays one four-octet parse plus one average-constant set operation; the parse replaces the string hash with cheaper integer hashing.

##### Space Complexity: `O(u)`

The set holds at most 128 machine words, plus the results. In a fixed-width language this is four bytes per record versus up to 15 for the string form (16 on the hashing cell plus allocator overhead), the reduction the statement's trade-off note invites.

#### Key Insights

- Canonical form is what makes packing safe: no leading zeros means exactly one integer per address, so membership on packed words is membership on addresses.
- One branch tip per octet means the four shifts and ors rebuild the whole address; nothing else about the string matters to the pool.
- The pool's operation count never leaves `O(m)`: every representation choice on this page changes the constant, not the complexity class. The 128-entry bound and the linear operation count are where the statement's "small Linux environment" lives.

## Comparison of Solutions

### Time Complexity

- **Address List with Linear Scan**: `O(m * u)` - every operation scans up to 128 records.
- **Address Set**: `O(m)` - constant-time set operations with string hashing.
- **Packed Octet Integer Set**: `O(m)` - constant-time set operations with one four-octet parse per operation.

### Space Complexity

- **Address List with Linear Scan**: `O(u)` - up to 128 full address strings.
- **Address Set**: `O(u)` - up to 128 full address strings in hash cells.
- **Packed Octet Integer Set**: `O(u)` - up to 128 machine words.

### Trade-offs

- **Address List with Linear Scan**: the definition written down and the easiest to verify by eye, with the scan paid on every operation.
- **Address Set**: the idiomatic membership container; strings are hashed as-is and the code carries no encoding logic.
- **Packed Octet Integer Set**: the smallest record and the cheapest hash, at the price of a packing step whose correctness leans on the canonical-format guarantee.

### When to Use Each

- **Address List with Linear Scan**: as the baseline to state first, or in a language where a set is not at hand and the operation count is small.
- **Address Set**: the default answer: linear overall, trivially correct, no encoding assumptions.
- **Packed Octet Integer Set (Recommended)**: when the follow-up lands on memory or cache behavior: one word per record, and the natural bridge to bitmask and integer-key designs.

### Optimization Notes

- **Packed Octet Integer Set** is the recommended choice: same linear time as the Address Set with a smaller per-record footprint and cheaper hashing, which is exactly the trade the statement's closing note asks candidates to discuss.
- The capacity guard can move into the packing: a 128-entry pool is small enough that the set never needs resizing past its initial buckets, so rehashing never fires on this problem's inputs.
- If the judged form ever asked for the pool's contents, the packing would need its inverse (`((word >> 24) & 255)` per octet); the check/add/remove surface used here never unpacks.
- The statement guarantees canonical input; a real pool facing non-canonical strings would normalize once at the boundary and keep everything downstream keyed on packed words.
