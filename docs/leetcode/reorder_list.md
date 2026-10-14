# [Reorder List](https://leetcode.com/problems/reorder-list/)

**Medium** | **25 minutes** | **Linked List, Two Pointers, Stack, Recursion**

**Pattern:** [Linked List Reversal](../patterns/linked_list_in_place_reversal/intuition.md), [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Linked list](https://en.wikipedia.org/wiki/Linked_list) · [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

**Practice:** [`practice/reorder_list/solution.py`](../../practice/reorder_list/solution.py)

You are given the head of a singly linked-list.

The positions of a linked list of `length = 7` for example, can intially be represented as:

`[0, 1, 2, 3, 4, 5, 6]`

Reorder the nodes of the linked list to be in the following order:

`[0, 6, 1, 5, 2, 4, 3]`

In the general case, label the nodes by their original zero-based positions from `0` to `n - 1`. After reordering, those original positions appear in this order:

`[0, n-1, 1, n-2, 2, n-3, ...]`

These numbers represent node positions, not the values stored in the nodes.

You may not modify the values in the list's nodes, but instead you must reorder the nodes themselves.

## Examples

### Example 1

**Input:** `head = [2,4,6,8]`

**Output:** `[2,8,4,6]`

### Example 2

**Input:** `head = [2,4,6,8,10]`

**Output:** `[2,10,4,8,6]`

## Constraints

- `1 <= Length of the list <= 1000`.
- `1 <= Node.val <= 1000`

## Deriving the Solution

The target order, `0, n-1, 1, n-2, ...`, interleaves the first half of the list with the reversed second half. Every solution therefore performs the same three conceptual steps: split the list into halves, reverse one of them, and interleave. Since values may not be touched, all of it is pointer surgery; the solutions differ in where the second half's order comes from.

1. **Start literal.** Copy the list into an array, then relink nodes by walking
   the array from both ends. Linear time and trivial to write, but `O(n)`
   extra space and, strictly speaking, a relink driven by an array rather than
   by the list itself: see [Array Copy](#array-copy).
2. **Store the nodes on a stack.** Push every node while scanning, then pop
   against a walk from the head: each pop yields the next node from the end,
   which is exactly the node the current front node must point to. Same `O(n)`
   space as the array, no random access: see [Stack Pairing](#stack-pairing).
3. **Cut, flip, and stitch in place.** A slow/fast pointer split finds the
   middle in one pass; in-place reversal rewires the second half; a two-pointer
   merge stitches the halves alternately. Three linear passes, `O(1)` space:
   see [Reverse-and-Merge](#reverse-and-merge).

## Solutions

### Array Copy

#### Derivation

The most direct reading writes the node order down, then acts on it. Nodes keep their identity; only the `next` pointers change:

1. Walk the list, collecting every node into a `nodes` array.
2. Use two indices, `i = 0` and `j = len(nodes) - 1`, alternating: link
   `nodes[i] -> nodes[j]`, then `nodes[j] -> nodes[i + 1]`.
3. Advance the pair inward after each round and NUL-terminate the last node.

#### Walkthrough

Trace the pairing on Example 1: `head = [2,4,6,8]`, so `nodes = [n0, n1, n2, n3]` holding values `2, 4, 6, 8`:

```text
i=0 j=3   n0 -> n3   (2 -> 8)   then n3 -> n1   (8 -> 4)
i=1 j=2   n1 -> n2   (4 -> 6)   then n2 -> None
i=2 j=1   i >= j, stop; n2.next is already None
```

Following the relinked pointers from `n0` visits values `2, 8, 4, 6`, matching the expected Output for Example 1.

#### Solution

The code is the two-index relink from the walkthrough.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def solve(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return head
        nodes = []
        current = head
        while current is not None:
            nodes.append(current)
            current = current.next
        i, j = 0, len(nodes) - 1
        while i < j:
            nodes[i].next = nodes[j]
            nodes[j].next = nodes[i + 1]
            i += 1
            j -= 1
        nodes[i].next = None
        return head
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear passes: one to collect the nodes, one to relink them.

##### Space Complexity: `O(n)`

The `nodes` array holds a reference to every node.

#### Key Insights

- Copying references (not values) respects the "modify the nodes themselves"
  rule: values never change.
- The odd-length case needs no branch: when `i == j` the middle node is left
  pointing at `None` by the final assignment.
- The array is the give-away: interviewers ask this question to see the `O(1)`
  version.

### Stack Pairing

#### Derivation

The array exists to pair node `i` with node `n - 1 - i`. A stack provides the same pairing through pops instead of indices: collect every node in one pass, then pop. The pops come out back-to-front (`n-1`, `n-2`, ...), which is exactly the order the interleaved output demands, and the front walk supplies the other partner one step at a time. The only subtlety is stopping: the two cursors meet at the middle, and the meeting looks different for odd and even lengths, which identity checks handle without a parity branch:

1. Collect every node into `stack` (bottom-to-top order, `head` at the bottom).
2. Walk `current` from `head`; each round pops `back` off the stack.
3. If `back is current`, the walk reached the middle of an odd-length list:
   terminate the list there.
4. If `back is following` (the node after `current`), the last pair sits
   adjacent: terminate after `back`.
5. Otherwise splice: `current -> back -> following`, advance `current` to
   `following`, and continue.

#### Walkthrough

Trace the pop-and-splice on Example 1: `head = [2,4,6,8]`, nodes `n0..n3`. The collection pass fills `stack = [n0, n1, n2, n3]` (top `n3`) and the walk starts at `current = n0`:

```text
round 1:  pop n3 (8)   following = n1   n0 -> n3 -> n1   current = n1
round 2:  pop n2 (6)   following = n2, which is back -> adjacent pair:
          n1 -> n2, n2.next = None, stop
```

Round 2 stops without splicing because the popped node `n2` is exactly `current`'s successor: the cursors have met inside one link, so the list is complete. Reading the relinked chain from `n0` gives `2, 8, 4, 6`, matching the expected Output for Example 1.

Run the odd case, Example 2: `head = [2,4,6,8,10]`, `stack = [n0..n4]`:

```text
round 1:  pop n4 (10)   n0 -> n4 -> n1   current = n1
round 2:  pop n3 (8)    n1 -> n3 -> n2   current = n2
round 3:  pop n2 (6)    back is current -> n2.next = None, stop
```

The middle node closes the list in the odd case, where the popped node coincides with the walk cursor itself. The chain reads `2, 10, 4, 8, 6`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's collect pass and pop-and-splice loop with the two identity stops.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def solve(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        stack = []
        node = head
        while node is not None:
            stack.append(node)
            node = node.next

        current = head
        while True:
            back = stack.pop()
            following = current.next
            if back is current:
                # Odd length: the middle node closes the list
                current.next = None
                break
            if back is following:
                # Even length: the last pair sits adjacent
                current.next = back
                back.next = None
                break
            current.next = back
            back.next = following
            current = following
        return head
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The collection pass visits every node once; the interleave performs `n // 2` splice rounds plus the final stop.

##### Space Complexity: `O(n)`

The stack holds a reference to every node.

#### Key Insights

- Pops replay the list backwards for free: no index arithmetic, no second
  pass to reach the end.
- Identity comparisons (`back is current`, `back is following`) terminate the
  loop correctly for both parities with no length arithmetic.
- The stack still costs linear memory; the reverse-and-merge version below is
  what removes it.

### Reverse-and-Merge

#### Derivation

Both slower versions store pointers to recreate the second half backwards. But a linked list can be turned backwards in place: cutting the list at the middle, reversing the second half, and merging the two halves alternately produces the interleave with no auxiliary storage. Each of the three passes is linear, and every step is plain pointer rewiring:

1. **Split.** Advance `slow` one node and `fast` two per step; when `fast`
   reaches the end, `slow` sits on the middle node (the last node of the first
   half for odd lengths). Cut with `second_half = slow.next; slow.next = None`.
2. **Reverse.** Walk the second half flipping each `next` pointer backwards
   (`previous <- current`), returning the new head.
3. **Merge.** Alternately splice one node of the reversed second half after one
   node of the first half; the first half is never shorter, so the loop runs
   until the second half is consumed.
The invariant that makes step 3 safe: after the split, `first` and `second` each hold intact chains, and splicing preserves both remainders.

#### Walkthrough

Trace all three passes on Example 1: `head = [2,4,6,8]`, with nodes `n0..n3` for values `2, 4, 6, 8`:

```text
split:    slow=n1, fast reaches end; second_half = n2; n1.next = None
          first  = n0 -> n1            (2 -> 4)
          second = n2 -> n3            (6 -> 8)
reverse:  previous=None; flip n2, flip n3
          second = n3 -> n2            (8 -> 6)
merge:    round 1: n0 -> n3 -> n1      (2 -> 8 -> 4)
          round 2: n1 -> n2, second consumed; n2.next = None
```

After the merge the chain from `n0` reads `2, 8, 4, 6`, matching the expected Output for Example 1. On odd lengths (Example 2, `[2,4,6,8,10]`) the split leaves the middle node `n2` closing the first half (`2, 4, 6`), the reverse flips `10, 8`, and the merge produces `2, 10, 4, 8, 6`, with the middle node's trailing position falling out of the stitch.

#### Solution

The code is the three passes from the walkthrough, each extracted into a named helper so the top-level read matches the plan: split, reverse, merge.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def solve(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        second_half = split_second_half(head)
        second_half = reverse_list(second_half)
        merge_alternating(head, second_half)
        return head


def split_second_half(head: ListNode) -> Optional[ListNode]:
    """Cut after the midpoint; return the second half's head."""
    slow, fast = head, head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    second_half = slow.next
    slow.next = None
    return second_half


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a chain in place; return its new head."""
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous


def merge_alternating(first: ListNode, second: Optional[ListNode]) -> None:
    """Splice `second` into `first` one node at a time, consuming both."""
    while second is not None:
        first_next = first.next
        second_next = second.next
        first.next = second
        second.next = first_next
        first = first_next
        second = second_next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes (slow/fast split, reversal, merge), each touching every node at most once.

##### Space Complexity: `O(1)`

Only pointer variables: no node is allocated and no array or stack is built.

#### Key Insights

- The slow/fast split is the standard "find the middle" idiom; its odd-length
  behavior (slow ends on the middle node, not after it) is what makes the merge
  asymmetry safe.
- In-place reversal is the workhorse that turns "pair from both ends" into
  "walk two forward chains".
- The merge leans on `first` never being shorter than `second`: for even `n`
  the halves are equal, for odd `n` the first half keeps the middle node.
- This is the version interviewers are listening for when they say "O(1)
  extra space".

## Comparison of Solutions

### Time Complexity

- **Array Copy**: `O(n)` - collect, then relink.
- **Stack Pairing**: `O(n)` - split, then interleave with pops.
- **Reverse-and-Merge**: `O(n)` - split, reverse, and merge in three passes.

### Space Complexity

- **Array Copy**: `O(n)` - one array of node references.
- **Stack Pairing**: `O(n)` - half the nodes on a stack.
- **Reverse-and-Merge**: `O(1)` - pointer variables only.

### Trade-offs

- All three are linear; only the space behavior separates them.
- The array version is the easiest to get right and the easiest to reason about
  when debugging.
- The stack version removes random access but keeps linear auxiliary memory and
  the fiddliest stitch of the three.
- The in-place version costs the most careful pointer reasoning and pays with
  constant space; it is also the least readable at a glance.

### When to Use Each

- **Array Copy**: Prototyping, tests, or whenever memory is not the interview's
  subject.
- **Stack Pairing**: As a stepping stone when the in-place stitch feels too
  slippery; it demonstrates the pairing idea without array indexing.
- **Reverse-and-Merge**: The canonical answer for the problem as asked,
  including its implicit demand of `O(1)` auxiliary space (recommended here).

### Optimization Notes

- The split's stop condition (`fast.next` then `fast.next.next`) is what puts
  `slow` on the last node of the first half; stopping one earlier or later
  breaks the merge's asymmetry assumption.
- The merge consumes `second` completely and never needs a post-loop fixup for
  the even case; the odd case's middle node was parked in the first half by the
  split.
- All three versions return `head` for convenience; the LeetCode signature
  returns nothing because the list is modified in place through the node
  references.
