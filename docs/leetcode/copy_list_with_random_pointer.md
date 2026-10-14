# [Copy List With Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)

**Medium** | **25 minutes** | **Hash Table, Linked List**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Linked list](https://en.wikipedia.org/wiki/Linked_list)

**Practice:** [`practice/copy_list_with_random_pointer/solution.py`](../../practice/copy_list_with_random_pointer/solution.py)

You are given the head of a linked list of length `n`. Unlike a singly linked list, each node contains an additional pointer `random`, which may point to any node in the list, or `null`.

Create a **deep copy** of the list. 

The deep copy should consist of exactly `n` **new** nodes, each including:
* The original value `val` of the copied node
* A `next` pointer to the new node corresponding to the `next` pointer of the original node
* A `random` pointer to the new node corresponding to the `random` pointer of the original node

Note: None of the pointers in the new list should point to nodes in the original list.

*Return the head of the copied linked list.*

In the examples, the linked list is represented as a list of `n` nodes. Each node is represented as a pair of `[val, random_index]` where `random_index` is the index of the node (0-indexed) that the `random` pointer points to, or `null` if it does not point to any node.

## Examples

### Example 1

**Input:** `head = [[3,null],[7,3],[4,0],[5,1]]`

**Output:** `[[3,null],[7,3],[4,0],[5,1]]`

### Example 2

**Input:** `head = [[1,null],[2,2],[3,2]]`

**Output:** `[[1,null],[2,2],[3,2]]`

## Constraints

- `0 <= n <= 100`
- `-100 <= Node.val <= 100`
- Node values are not guaranteed to be unique.
- `random` is `null` or is pointing to some node in the linked list.

## Deriving the Solution

A deep copy of the `next` chain alone is the linked-list reversal warm-up: one pass allocating fresh nodes. The `random` pointer breaks that simplicity, because at the moment a copy is created the node it should point to may not exist yet. Every solution therefore defers some `random` assignments, and they differ in where the deferred information waits: in a scan, in a hash map, or folded into the list itself.

1. **Start literal.** Copy the `next` chain into an array of fresh nodes, then
   resolve each `random` by locating the original node's position with a scan
   and indexing the copy array. Two nested passes, `O(n^2)`: see
   [Array Indexing](#array-indexing).
2. **Spot the waste.** The scan exists only to answer "which copy corresponds
   to this original node?". A hash map from original to copy answers it in
   `O(1)` after one building pass, making the whole algorithm two linear
   passes at `O(n)` extra space: see [Hash Map](#hash-map).
3. **Store the pairing inside the list.** Splice every fresh node directly
   after its original (`orig -> copy -> orig.next`) and the pairing becomes
   the `next` pointer itself: `orig.next.random` is the copy of
   `orig.random`. Set the copies' `random` pointers in one pass, then unzip
   the two interleaved chains in a third: `O(1)` extra space, no map: see
   [Interleaving](#interleaving).

## Solutions

### Array Indexing

#### Derivation

The most direct reading copies the easy part first, then hunts for each `random` target's position:

1. Walk the original list, allocating one fresh node per original and linking
   them by `next`, while collecting the original nodes in an array `originals`
   and the fresh nodes in a parallel array `copies` (index `i` of `copies` is
   the copy of index `i` of `originals`).
2. For each original node, find where it sits in `originals` by scanning for
   identity; call that position `i`.
3. If the original's `random` is `None`, leave the copy's `random` `None`;
   otherwise set `copies[i].random = copies[j]`, where `j` is the position of
   the original's `random` target.
4. Return the head of `copies`.

#### Walkthrough

Trace the position hunts on Example 2: `head = [[1,null],[2,2],[3,2]]`. The building pass produces `originals = [n1, n2, n3]` and `copies = [c1, c2, c3]`:

```text
n1.random = None        -> c1.random = None
n2.random = n3          -> scan: n3 at index 2   -> c2.random = c3
n3.random = n3          -> scan: n3 at index 2   -> c3.random = c3
```

Each `random` target is found by walking `originals` until identity matches. The copy list reads `[[1,null],[2,2],[3,2]]` when serialized: `c2.random` is `c3` and `c3.random` is itself, exactly the original's structure, matching the expected Output for Example 2.

#### Solution

The code is the two arrays plus the identity scan per node.

```python
from typing import Optional


class Node:
    def __init__(self, val: int, next: "Optional[Node]" = None, random: "Optional[Node]" = None) -> None:
        self.val = val
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if head is None:
            return None

        originals = []
        copies = []
        current = head
        while current is not None:
            copies.append(Node(current.val))
            originals.append(current)
            current = current.next
        for i in range(len(copies) - 1):
            copies[i].next = copies[i + 1]

        for i, original in enumerate(originals):
            if original.random is None:
                continue
            # Find the random target's position by identity scan
            for j, candidate in enumerate(originals):
                if candidate is original.random:
                    copies[i].random = copies[j]
                    break
        return copies[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Building the chains is linear, but each of the `n` `random` resolutions scans up to `n` original nodes for identity.

##### Space Complexity: `O(n)`

The output itself is `n` fresh nodes (unavoidable for a deep copy) plus two arrays of `n` references.

#### Key Insights

- The arrays make "the copy of the node at position `i`" an index lookup;
  only the target's position is expensive to learn.
- Identity comparison (`is`, not `==`) is essential: values may repeat, and
  `Node` defines no equality anyway.
- The quadratic scan is pure bookkeeping, which is what the map and the
  interleaving remove.

### Hash Map

#### Derivation

The scan answers one question repeatedly: "which copy belongs to this original?". A [hash map](https://en.wikipedia.org/wiki/Hash_table) keyed by node identity answers it once per node: build every copy first, remembering the pairing, then read the map to wire both pointer kinds. Wiring `random` after all copies exist is what dissolves the "the target may not exist yet" problem:

1. First pass: for each original node, store `map[original] = Node(original.val)`
   with pointers unset.
2. Second pass: for each original node, set
   `map[original].next = map[original.next]` and
   `map[original].random = map[original.random]`, where the map answers `None`
   for a `None` key.
3. Return `map[head]`.

#### Walkthrough

Trace the two passes on Example 1: `head = [[3,null],[7,3],[4,0],[5,1]]` with originals `n0..n3`. The first pass fills `map = {n0: c0, n1: c1, n2: c2, n3: c3}`:

```text
pass 2, node n0 (3):  next is n1 -> c0.next = c1   random None -> c0.random = None
pass 2, node n1 (7):  next is n2 -> c1.next = c2   random n3   -> c1.random = c3
pass 2, node n2 (4):  next is n3 -> c2.next = c3   random n0   -> c2.random = c0
pass 2, node n3 (5):  next is None -> c3.next = None   random n1 -> c3.random = c1
```

Every lookup is a constant-time map hit because the first pass guaranteed every original has a copy. The serialized copy list is `[[3,null],[7,3],[4,0],[5,1]]`, matching the expected Output for Example 1.

#### Solution

The code is the two passes with the map answering every "which copy?" question. `map[None] = None` folds the null-pointer cases into the same lookup.

```python
from typing import Optional


class Node:
    def __init__(self, val: int, next: "Optional[Node]" = None, random: "Optional[Node]" = None) -> None:
        self.val = val
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if head is None:
            return None

        node_map = {None: None}
        current = head
        while current is not None:
            node_map[current] = Node(current.val)
            current = current.next

        current = head
        while current is not None:
            node_map[current].next = node_map[current.next]
            node_map[current].random = node_map[current.random]
            current = current.next
        return node_map[head]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two passes over the list with `O(1)` average map operations each.

##### Space Complexity: `O(n)`

The `n` copied nodes count toward any deep copy; the map adds another `n` references on top.

#### Key Insights

- Deferred wiring is the whole trick: allocate everything, then connect.
- Keying by node identity (default object hashing) sidesteps the repeated
  values constraint entirely.
- The map is pure overhead next to the interleaving below, which stores the
  same pairing without any auxiliary structure.

### Interleaving

#### Derivation

The hash map spends linear memory to keep every original next to its copy's identity. The list itself can hold that pairing: splice each fresh node immediately after its original, turning `n0 -> n1 -> n2` into `n0 -> c0 -> n1 -> c1 -> n2 -> c2`. In the interleaved list the copy of `node` is `node.next`, so a node's `random` target's copy is `node.random.next`, and the whole wiring pass needs no map at all. A final pass unzips the two chains by alternating:

1. First pass: for each original `current`, allocate `copy` and splice it in:
   `copy.next = current.next; current.next = copy; current = copy.next`.
2. Second pass: for each original `current`, set
   `current.next.random = current.random.next` when `current.random` exists
   (the `.next` reaches over the original to its copy), else `None`.
3. Third pass: unlink the copies into their own list, restoring the original
   list, and return the copy list's head.

#### Walkthrough

Trace all three passes on Example 2: `head = [[1,null],[2,2],[3,2]]`, originals `n1, n2, n3` with `n2.random = n3.random = n3`:

```text
pass 1 (splice):   n1 -> c1 -> n2 -> c2 -> n3 -> c3
pass 2 (randoms):  c1.random = None            (n1.random is None)
                   c2.random = n3.next = c3
                   c3.random = n3.next = c3
pass 3 (unzip):    originals: n1 -> n2 -> n3
                   copies:    c1 -> c2 -> c3
```

After the splice, reaching a copy never needs a search: it is one `next` from its original, so both `c2.random` and `c3.random` are single-hop lookups. The unzipped copy list serializes to `[[1,null],[2,2],[3,2]]`, matching the expected Output for Example 2, and the original list is left as it began.

#### Solution

The code is the three passes from the walkthrough.

```python
from typing import Optional


class Node:
    def __init__(self, val: int, next: "Optional[Node]" = None, random: "Optional[Node]" = None) -> None:
        self.val = val
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if head is None:
            return None

        current = head
        while current is not None:
            copy = Node(current.val, current.next)
            current.next = copy
            current = copy.next

        current = head
        while current is not None:
            if current.random is not None:
                current.next.random = current.random.next
            current = current.next.next

        copy_head = head.next
        original = head
        while original is not None:
            copy = original.next
            original.next = copy.next
            if copy.next is not None:
                copy.next = copy.next.next
            original = original.next
        return copy_head
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes: splice, wire, unzip. Each touches every node a constant number of times.

##### Space Complexity: `O(1)`

Beyond the `n` copied nodes every deep copy must produce, only pointer variables: no map, no arrays.

#### Key Insights

- The `next` pointer becomes the map: splicing copies into the original list
  encodes the pairing structurally instead of in a hash table.
- `current.random.next` is the idiom to internalize: from an original, one
  hop to its `random` target, one more to that target's copy.
- The unzip pass restores the input list while extracting the copy list,
  which the problem's "none of the pointers should point to nodes in the
  original list" requirement makes mandatory.

## Comparison of Solutions

The practice harness's `practice/copy_list_with_random_pointer/reference.py` implements the **Interleaving** solution.

### Time Complexity

- **Array Indexing**: `O(n^2)` - each `random` resolution scans the list.
- **Hash Map**: `O(n)` - two linear passes with constant-time lookups.
- **Interleaving**: `O(n)` - three linear passes, no lookups.

### Space Complexity

- **Array Indexing**: `O(n)` - the two parallel reference arrays.
- **Hash Map**: `O(n)` - the node map on top of the mandatory copies.
- **Interleaving**: `O(1)` - the pairing lives in the list's own pointers.

### Trade-offs

- All three produce correct deep copies; they differ in where the
  original-to-copy pairing waits while copies are being created.
- The array version is the easiest to see and the hardest to scale.
- The hash map is the standard interview answer: two clean passes, easy to
  reason about, linear extra memory.
- The interleaving reaches constant auxiliary space by temporarily mutating
  the input list, restored by the final pass; it is the answer when the
  follow-up demands `O(1)` space.

### When to Use Each

- **Array Indexing**: When clarity outranks cost, or as the correctness
  oracle for the faster versions.
- **Hash Map**: The default and the version to write first in an interview
  (recommended here).
- **Interleaving**: When the interviewer asks for the map's memory back, the
  canonical follow-up for this problem.

### Optimization Notes

- Every approach defers `random` wiring until all copies exist; wiring during
  the building pass is what forces the quadratic scan in the first place.
- The hash map's `map[None] = None` entry is the cheapest null handling:
  without it, both passes need explicit `is None` branches.
- The interleaving's unzip pass must restore `original.next` before reading
  `copy.next`; the copy's `next` still points into the interleaved order
  while the split is in progress.
