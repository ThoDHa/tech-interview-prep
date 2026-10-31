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

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
