# [Reverse Nodes In K Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)

**Hard** | **40 minutes** | **Linked List, Recursion**

**Pattern:** [Linked List Reversal](../patterns/linked_list_in_place_reversal/intuition.md)

**Algorithm:** [Linked list](https://en.wikipedia.org/wiki/Linked_list) · [Recursion (computer science)](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/reverse_nodes_in_k_group/solution.py`](../../practice/reverse_nodes_in_k_group/solution.py)

You are given the head of a singly linked list `head` and a positive integer `k`.

You must reverse the first `k` nodes in the linked list, and then reverse the next `k` nodes, and so on. If there are fewer than `k` nodes left, leave the nodes as they are.

Return the modified list after reversing the nodes in each group of `k`.

You are only allowed to modify the nodes' `next` pointers, not the values of the nodes.

## Examples

### Example 1

**Input:** `head = [1,2,3,4,5,6], k = 3`

**Output:** `[3,2,1,6,5,4]`

### Example 2

**Input:** `head = [1,2,3,4,5], k = 3`

**Output:** `[3,2,1,4,5]`

## Constraints

- The length of the linked list is `n`.
- `1 <= k <= n <= 5000`
- `0 <= Node.val <= 100`

## Deriving the Solution

Reversing one group of `k` consecutive nodes is plain in-place pointer flipping; the problem's difficulty lives entirely in the bookkeeping between groups: knowing where a group starts, confirming it has `k` nodes left, and reconnecting the reversed group to what came before and after. Every solution is "reverse each full group and stitch"; they differ in whether the stitching state is carried by iteration or by the call stack.

1. **Start literal.** Read the whole list into an array, reverse each
   aligned `k`-slice, and rebuild the list. Linear time, trivial to argue,
   `O(n)` extra space and no pointer surgery: see
   [Array Rebuild](#array-rebuild).
2. **Spot the waste.** Only the `next` pointers need to change; the values
   and the array are scaffolding. Reverse each group in place with the
   standard three-pointer flip, tracking each group's predecessor and the
   next group's head for the stitching: see
   [Iterative In-place Reversal](#iterative-in-place-reversal).
3. **Let recursion carry the state.** The list after one reversed group is
   the same problem on a shorter list: reverse the first group, recurse on
   the rest, and attach. The stack holds the "what comes after me"
   information the iterative version tracks by hand: see
   [Recursive Reversal](#recursive-reversal).

## Solutions

### Array Rebuild

#### Derivation

The most direct reading collects the nodes, rearranges them, and relinks:

1. Walk the list, collecting every node into an array `nodes`.
2. For each aligned block `nodes[start : start + k]` of exactly `k` nodes,
   reverse that block in the array. The trailing partial block stays put.
3. Relink: `nodes[i].next = nodes[i + 1]` for every `i`, terminate the last
   node, and return `nodes[0]`.

#### Walkthrough

Trace the slice reversal on Example 1: `head = [1,2,3,4,5,6]`, `k = 3`, collected as `nodes = [n1, n2, n3, n4, n5, n6]`:

```text
block 0..2:  [n1, n2, n3] -> [n3, n2, n1]
block 3..5:  [n4, n5, n6] -> [n6, n5, n4]
relink:      n3 -> n2 -> n1 -> n6 -> n5 -> n4 -> None
```

Both full blocks reverse and the relink reproduces the array order. Reading the values gives `3, 2, 1, 6, 5, 4`, matching the expected Output for Example 1. Example 2 (`[1,2,3,4,5]`, `k = 3`) has one full block and a partial remainder: only `[n1, n2, n3]` reverses, and the relink yields `3, 2, 1, 4, 5`, matching the expected Output for Example 2.

#### Solution

The code is the collect, the per-block reversal, and the relink.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        nodes = []
        current = head
        while current is not None:
            nodes.append(current)
            current = current.next

        for start in range(0, len(nodes) - k + 1, k):
            nodes[start : start + k] = reversed(nodes[start : start + k])

        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        nodes[-1].next = None
        return nodes[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One collection pass, one reversal pass (each node moves once), one relink pass.

##### Space Complexity: `O(n)`

The `nodes` array holds a reference to every node.

#### Key Insights

- The aligned-block slicing (`range(0, len - k + 1, k)`) encodes the "leave
  the remainder alone" rule without any special case.
- The array makes reversal and relinking index operations, which is exactly
  why it is not the interview answer: the problem is about pointers.
- Every later approach replaces the array with pointer surgery.

### Iterative In-place Reversal

#### Derivation

The array exists only to remember three positions per group: where the group starts, what precedes it, and what follows it. A group reversal in place needs the same three. The flip itself is the standard previous/current walk; the stitching rule falls out of what reversal does to the group's ends: the group's first node becomes its last, so it must be wired to the *next group's* head, and the group's last node becomes its first, so the predecessor must be wired to it. One lookahead check per group ("are there `k` nodes left?") keeps partial groups untouched:

1. Anchor `dummy` in front of `head`; let `group_head = dummy`, the node
   before the group about to be reversed.
2. From `group_head`, walk `k` nodes to the group's last node; falling off
   the end first means fewer than `k` nodes remain, the remainder stays, and
   the loop ends. The next group's head is that last node's `next`.
3. Reverse the `k` nodes after `group_head` with the three-pointer flip,
   returning the group's new first node (`new_first`... the old tail) and
   leaving the old first node (`new_last`) as the group's last.
4. Stitch: `group_head.next = new_first` and
   `new_last.next = next_group`.
5. Set `group_head = new_last` (the node before the next group) and repeat.

#### Walkthrough

Trace one full round plus the second on Example 1: `head = [1,2,3,4,5,6]`, `k = 3`, nodes named by value:

```text
round 1:
  check:   group_head=dummy, walk 3 nodes -> group_last = node 3
           next_group = node 3.next = node 4
  reverse: flip 1, flip 2, flip 3
           group reads 3 -> 2 -> 1, old head 1 becomes the group's tail
  stitch:  dummy.next = 3;  node 1.next = next_group = 4
  list:    dummy -> 3 -> 2 -> 1 -> 4 -> 5 -> 6
  advance: group_head = node 1
round 2:
  check:   from node 1, walk 3 nodes (4, 5, 6) -> group_last = node 6
           next_group = node 6.next = None
  reverse: flips produce 6 -> 5 -> 4; node 4.next = None
  stitch:  node 1.next = 6;  node 4.next = next_group = None
  list:    dummy -> 3 -> 2 -> 1 -> 6 -> 5 -> 4
  advance: group_head = node 4
round 3:
  check:   fewer than k nodes after node 4 -> stop
```

Each round reverses exactly one aligned group and the stitch lands the group between its predecessor and the next group's head. After round 2 the chain reads `3, 2, 1, 6, 5, 4`, matching the expected Output for Example 1. On Example 2 (`[1,2,3,4,5]`, `k = 3`) round 2's check finds only nodes `4, 5` left, so the loop ends with `3, 2, 1, 4, 5`, matching the expected Output for Example 2.

#### Solution

The code is the per-group check, flip, and stitch, repeated until the check fails. The flip helper reverses exactly `k` nodes and reports both new ends.

```python
from typing import Optional, Tuple


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        def reverse_k(node: ListNode) -> Tuple[ListNode, ListNode]:
            """Reverse k nodes starting at `node`; return (new first, new last)."""
            previous = node
            current = node.next
            for _ in range(k - 1):
                following = current.next
                current.next = previous
                previous = current
                current = following
            return previous, node

        dummy = ListNode(next=head)
        group_head = dummy
        while True:
            group_last = group_head
            for _ in range(k):
                group_last = group_last.next
                if group_last is None:
                    return dummy.next
            next_group = group_last.next
            new_first, new_last = reverse_k(group_head.next)
            group_head.next = new_first
            new_last.next = next_group
            group_head = new_last
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The lookahead walk and the flip together advance over each node a constant number of times per group; every node belongs to exactly one group.

##### Space Complexity: `O(1)`

The dummy node and a constant number of pointers, whatever `n` and `k`.

#### Key Insights

- The lookahead (walking `k` nodes from `group_head` to the group's last
  node) is the "fewer than `k` nodes are left" rule; performing it before
  any flip is what keeps partial groups pristine, and reading `next_group`
  off `group_last.next` after the walk (not during it) is what keeps the
  stitch from landing inside the group about to be reversed.
- After the flip, the old group head is the new tail, so
  `new_last.next = next_group` is what reconnects the rest of the list.
- Advancing `group_head` to `new_last` (the reversed group's tail) is the
  subtle step: the next group's predecessor is the node just placed at the
  group boundary, not the old `group_head`.

### Recursive Reversal

#### Derivation

The iterative loop carries `group_head` forward by hand, but the structure is self-similar: the answer is (reversed first group) followed by (the same answer on the rest of the list). Recursion expresses that directly. The base case is the partial remainder, and the recursive call returns the already-processed suffix, which the reversed first group's tail must adopt:

1. From `head`, count `k` nodes ahead to `next_group`; fewer than `k` nodes
   remain means return `head` untouched.
2. Reverse exactly the first `k` nodes with the three-pointer flip, keeping
   the old `head` (now the group's tail) in `new_last`.
3. Set `new_last.next = reverseKGroup(next_group, k)`, delegating the rest of
   the list to the recursive call.
4. Return the reversed group's new first node.

#### Walkthrough

Trace the call tree on Example 2: `head = [1,2,3,4,5]`, `k = 3`:

```text
call A (head=1):  lookahead 3 nodes: 1, 2, 3 -> next_group = 4
                  flip 1..3 -> group 3 -> 2 -> 1, head (node 1) is the tail
                  node 1.next = call B(head=4)
  call B (head=4): lookahead: node 4, node 5, then None -> partial remainder
                   return 4 untouched
result: 3 -> 2 -> 1 -> 4 -> 5
```

Call B is the base case firing on the partial remainder: its lookahead walks nodes `4` and `5` and then hits `None`, so it returns its `head` unchanged. Call A wires its group's tail (`node 1`) to that returned node. The result reads `3, 2, 1, 4, 5`, matching the expected Output for Example 2. On Example 1 (`[1,2,3,4,5,6]`, `k = 3`) the recursion nests one level deeper: call A's lookahead lands on `next_group = 4`, and call B's lookahead walks `4, 5, 6` and lands on `None` with all `k` nodes present, so call B reverses `4..6` into `6 -> 5 -> 4` and recurses on `next_group = None`. That deepest call's lookahead fails immediately and returns `None`, which call B attaches as `node 4.next`; call A then attaches `node 1.next = 6`. The chain reads `3, 2, 1, 6, 5, 4`, matching the expected Output for Example 1.

#### Solution

The code is the check, the flip, and the recursive attachment.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        next_group = head
        for _ in range(k):
            if next_group is None:
                return head
            next_group = next_group.next

        previous = head
        current = head.next
        for _ in range(k - 1):
            following = current.next
            current.next = previous
            previous = current
            current = following

        head.next = self.reverseKGroup(next_group, k)
        return previous
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each call reverses one group of `k` nodes (or returns immediately at the base case), and each node belongs to exactly one group.

##### Space Complexity: `O(n / k)`

One stack frame per reversed group; the pointer work inside each frame is constant. (The iterative version makes this `O(1)`.)

#### Key Insights

- The recursion is the loop turned inside out: `group_head`'s advance
  becomes the call stack's unwind.
- The base case does double duty: it handles both the empty list and the
  partial remainder, because both fail the `k`-node lookahead.
- Depth `n / k` is the practical constraint to mention in an interview; the
  constraint's `n <= 5000` keeps it safe in Python, but the iterative form
  is the one that scales without limit.

## Comparison of Solutions

### Time Complexity

- **Array Rebuild**: `O(n)` - collect, reverse slices, relink.
- **Iterative In-place Reversal**: `O(n)` - per-group lookahead plus flip.
- **Recursive Reversal**: `O(n)` - one group reversed per call.

### Space Complexity

- **Array Rebuild**: `O(n)` - the node array.
- **Iterative In-place Reversal**: `O(1)` - constant pointers, no stack.
- **Recursive Reversal**: `O(n / k)` - one frame per group.

### Trade-offs

- All three leave the values untouched and produce the same relinking; they
  differ in auxiliary memory and in how much pointer reasoning they demand.
- The array version is the easiest to verify and the furthest from what the
  problem is testing.
- The iterative version is the canonical answer: constant space, no stack
  limit, at the price of the fiddliest stitching.
- The recursive version is the shortest pointer-only form and the easiest to
  argue correct, paying one frame per group.

### When to Use Each

- **Array Rebuild**: Prototyping, tests, or as the oracle the pointer
  versions are checked against.
- **Iterative In-place Reversal**: The interview answer, especially when the
  follow-up demands `O(1)` space (recommended here).
- **Recursive Reversal**: When the interviewer asks for the recursive
  formulation or stack depth is known to be safe.

### Optimization Notes

- Both pointer versions run their lookahead *before* any flip; flipping
  first and discovering a partial group afterwards would leave the list
  scrambled and unrecoverable in place.
- The flip loop runs `k - 1` times, not `k`: the group's first node needs no
  flip, only its `k - 1` links reversed around it.
- The recursive version tails into `head.next = self.reverseKGroup(...)`:
  computing the attachment before returning is what keeps the group's tail
  correct without a separate stitch pass.
