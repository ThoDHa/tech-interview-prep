# [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

**Medium** | **25 minutes** | **Linked List, Two Pointers**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Linked list](https://en.wikipedia.org/wiki/Linked_list) · [Two-pointer technique](https://usaco.guide/silver/two-pointers)

**Practice:** [`practice/remove_nth_node_from_end_of_list/solution.py`](../../practice/remove_nth_node_from_end_of_list/solution.py)

Given the `head` of a linked list and an integer `n`, remove the `nth` node from the end of the list and return its head.

## Examples

### Example 1

**Input:** `head = [1,2,3,4], n = 2`

**Output:** `[1,2,4]`

### Example 2

**Input:** `head = [5], n = 1`

**Output:** `[]`

### Example 3

**Input:** `head = [1,2], n = 2`

**Output:** `[2]`

## Constraints

- The number of nodes in the list is `sz`.
- `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

## Deriving the Solution

Deleting the `n`th node from the end of a singly linked list has one mechanical obstacle: after following `next` links there is no way back, and deletion needs the node *before* the victim. Every solution therefore locates that predecessor (or the victim first and backs up by other means) and rewires one `next` pointer; they differ in how the position-from-the-end is found.

1. **Start literal.** Walk the list to count its length `sz`, delete by
   front-position arithmetic (`sz - n`), and walk again to reach the
   predecessor. Two passes, simple and `O(1)` space: see
   [Two Passes](#two-passes).
2. **Delete nothing, rebuild everything.** Copy every node after the victim
   one position forward: shifting values over the victim deletes its payload
   without any relinking. One pass, but the boundary positions need guards
   and the trick buys nothing here: see [Value Shift](#value-shift).
3. **Both pointers in one pass.** Park a `fast` pointer `n` nodes ahead of
   `slow`, then advance both together; when `fast` runs off the end, `slow`
   sits on the predecessor. One pass with a constant two pointers: see
   [Two Pointers](#two-pointers).

## Solutions

### Two Passes

#### Derivation

The most direct reading turns "nth from the end" into "nth from the front" by counting. A list of length `sz` has its `n`th node from the end at front position `sz - n` (zero-based), so the deletion target's predecessor sits at front position `sz - n - 1`. The head itself may be the victim (when `n == sz`), which a dummy node in front of the head absorbs:

1. Walk once to count `sz`.
2. Anchor a `dummy` node in front of `head` and walk `sz - n` steps from
   `dummy`; the stopping node is the victim's predecessor.
3. Rewire `predecessor.next = predecessor.next.next`, skipping the victim.
4. Return `dummy.next`.

#### Walkthrough

Trace both passes on Example 1: `head = [1,2,3,4]`, `n = 2`:

```text
pass 1:   count sz = 4
steps:    walk sz - n = 2 steps from dummy:
          step 1 -> node 1   step 2 -> node 2
          predecessor = node 2, victim = node 3
pass 2:   node 2.next = node 4      (2 -> 4, node 3 skipped)
```

With `sz - n = 2`, the predecessor walk stops on the node holding `2`, exactly one before the node holding `3`. Relinking gives `1 -> 2 -> 4`, matching the expected Output for Example 1. The head-victim case is Example 3 (`[1,2]`, `n = 2`): `sz - n = 0` steps leaves the walk on `dummy`, and `dummy.next = head.next` deletes the first node, yielding `[2]`, matching the expected Output for Example 3.

#### Solution

The code is the count, the predecessor walk, and the rewire.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        size = 0
        node = head
        while node is not None:
            size += 1
            node = node.next

        dummy = ListNode(next=head)
        predecessor = dummy
        for _ in range(size - n):
            predecessor = predecessor.next

        predecessor.next = predecessor.next.next
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(sz)`

One pass to count and one pass to the predecessor position: at most two traversals of the list.

##### Space Complexity: `O(1)`

The dummy node and two walking references, whatever the list's length.

#### Key Insights

- Translating back-index to front-index (`sz - n`) is the whole idea; the
  second walk is ordinary front-position deletion.
- The dummy node is what makes `n == sz` (delete the head) the same code as
  every other deletion: the predecessor walk simply stops on `dummy`.
- Two passes is within every interview bound unless "one pass" is demanded
  explicitly; that demand is what motivates the Two Pointers version.

### Value Shift

#### Derivation

Deleting a node needs its predecessor only because `next` links are one-directional. A known trick for the variant where only the victim itself is given (LeetCode's "Delete Node in a Linked List") deletes without any predecessor: copy the successor's value into the victim, then unlink the duplicated tail. Applied here, the victim is first located with an offset walk, and the shift does the deletion:

1. Advance a `fast` pointer `n` steps from `head`, with `slow` left behind on
   `head`. If `fast` runs off the end, the victim is the head itself; a
   one-node list is deleted outright by returning `None`.
2. Otherwise advance both in lockstep until `fast` is the last node; the
   victim is `slow.next` (the `n`th node from the end).
3. Shift values forward: while the victim is at least two nodes from the end,
   copy the successor's value in and advance. Copy the last node's value in
   and terminate the list (`victim.next = None`).
4. When the victim has no successor (it is the last node), the shift has
   nothing to copy; the lockstep left `slow` on its predecessor, so rewire
   `slow.next = None` instead.

#### Walkthrough

Trace the shift on Example 1: `head = [1,2,3,4]`, `n = 2`. Nodes are named by value:

```text
offset:   fast = 1 -> 2 -> 3              slow stays at 1
lockstep: fast = 4, slow = 2              (fast.next is None -> stop)
victim:   slow.next = node 3
shift:    node3.next.next is None -> loop skipped
          node3.val = 4                   (list reads 1, 2, 4, 4)
          node3.next = None               (list reads 1 -> 2 -> 4)
```

The last node's value lands in the victim and the duplicated tail node is unlinked in the same step, leaving `1 -> 2 -> 4`, matching the expected Output for Example 1. A longer tail exercises the loop: on `[1,2,3,4,5]` with `n = 2` the victim is node `4`, which copies `5` forward and terminates, leaving `1 -> 2 -> 3 -> 5`. Example 2 (`[5]`, `n = 1`) never reaches the shift: the offset runs `fast` off the end, the step-1 guard sees the head has no successor, and the one-node list is deleted by returning `None`.

#### Solution

The code is the offset walk, the shift loop, and the two guards the shift cannot absorb.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        slow = fast = head
        for _ in range(n):
            fast = fast.next

        if fast is None:
            # n == sz: the victim is the head itself
            if head.next is None:
                return None
            victim = head
        else:
            while fast.next is not None:
                fast = fast.next
                slow = slow.next
            victim = slow.next

        if victim.next is None:
            # n == 1: the victim is the last node with no successor to
            # shift from; the lockstep left `slow` on its predecessor.
            slow.next = None
            return head

        while victim.next.next is not None:
            victim.val = victim.next.val
            victim = victim.next
        victim.val = victim.next.val
        victim.next = None
        return head
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(sz)`

The offset walk and lockstep traverse the list once, and the shift continues that traversal to the end.

##### Space Complexity: `O(1)`

Three walking references; no dummy head.

#### Key Insights

- The value shift is the LeetCode 237 trick, and its fit here is poor: the
  boundary positions (`n == 1`, `n == sz`) each need their own guard, since
  a victim with no successor cannot be deleted by copying.
- The offset walk that locates the victim also locates its predecessor in
  `slow`, which is exactly what the fallback and the Two Pointers approach
  use; the shift buys nothing in this problem.
- Copying the last node's value and terminating the list is one motion; a
  separate trim walk is unnecessary.

### Two Pointers

#### Derivation

The two-pass version walks twice because the first walk is spent learning the length. Two pointers moving together encode the same information without counting: advance `fast` exactly `n` steps ahead of `slow`, then move both in lockstep. The gap between them stays `n`, so when `fast` runs off the end, `slow` is the `n`th node from the end... one step before the victim, which is the predecessor. The dummy head absorbs the delete-the-head case as before:

1. Anchor `dummy` in front of `head`; set `fast` and `slow` both to `dummy`.
2. Advance `fast` exactly `n` steps.
3. While `fast.next` exists, advance both `fast` and `slow` one step.
4. Rewire `slow.next = slow.next.next` and return `dummy.next`.

#### Invariant

After the initial `n`-step offset and before every lockstep advance, `fast` is exactly `n` nodes ahead of `slow`, so `slow` always sits `n` nodes from the list's end:

```text
after offset:   slow at dummy, fast at node n-1 (0-based from head)
                gap = n nodes
each advance:   slow -> slow.next, fast -> fast.next   (gap stays n)
loop exit:      fast on last node (fast.next is None)
                -> slow is the (n+1)th node from the end
                -> the nth node from the end (the victim) is slow.next
```

Reading the exit condition from the invariant: the loop stops with `fast` on the last node, where `slow` is exactly the predecessor of the `n`th node from the end. Every advance preserves the gap, so the exit state follows from the offset state.

#### Walkthrough

Trace the lockstep on Example 1: `head = [1,2,3,4]`, `n = 2`. Positions name nodes by value, with `slow` and `fast` shown after each move:

```text
offset:   fast: dummy -> 1 -> 2            slow stays at dummy
lockstep: fast=2 slow=dummy -> fast=3 slow=1
          fast=3 slow=1     -> fast=4 slow=2   (fast.next is None -> stop)
rewire:   slow = node 2, slow.next.next = node 4 -> 2 -> 4
```

The offset of `n = 2` puts `fast` on node `2`, and the lockstep stops with `fast` on node `4` (the last node) and `slow` on node `2`: exactly the predecessor of node `3`, the second node from the end. The rewire sets `2.next = 4`, giving `1 -> 2 -> 4`, matching the expected Output for Example 1. Example 3 (`[1,2]`, `n = 2`) spends the whole offset putting `fast` on node `2`, which is the last node, so the lockstep never runs and `slow` is still on `dummy`; the rewire deletes the head through `dummy.next = dummy.next.next`, yielding `[2]`, matching the expected Output for Example 3.

#### Solution

The code is the offset, the lockstep, and the rewire.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(next=head)
        fast = dummy
        slow = dummy
        for _ in range(n):
            fast = fast.next

        while fast.next is not None:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(sz)`

`fast` traverses the whole list exactly once; `slow` walks a shorter prefix behind it. One pass, in the sense no node is visited twice by `fast`.

##### Space Complexity: `O(1)`

The dummy node and the two pointers.

#### Key Insights

- The fixed gap is the counting done in advance: offsetting `n` steps first
  replaces the length pass entirely.
- Stopping the lockstep on `fast.next` (not `fast`) is what parks `slow` on
  the *predecessor*, the node deletion needs; stopping on `fast` would land
  `slow` on the victim itself.
- The dummy head handles `n == sz`: the loop body never runs and `slow`
  deletes the head through `dummy`.

## Comparison of Solutions

### Time Complexity

- **Two Passes**: `O(sz)` - one counting pass plus one predecessor pass.
- **Value Shift**: `O(sz)` - one pass to the victim plus the shift and trim.
- **Two Pointers**: `O(sz)` - a single `fast` traversal with `slow` behind.

### Space Complexity

- **Two Passes**: `O(1)` - dummy node and walking references.
- **Value Shift**: `O(1)` - walking references, no dummy in the shift path.
- **Two Pointers**: `O(1)` - dummy node and two gap-locked references.

### Trade-offs

- All three are linear time and constant space; they differ in traversal
  count and in how much of the list they mutate.
- The two-pass version touches each node at most twice and is the easiest to
  argue correct.
- The value shift avoids relinking in the common case but rewrites node
  values and needs a guard per boundary position; it is the tool for the
  victim-only variant, not for this problem.
- The two-pointer version visits each node once, at the cost of the gap
  invariant being one abstraction harder to see.

### When to Use Each

- **Two Passes**: The default when one-pass is not demanded; the clearest
  translation of the problem into code.
- **Value Shift**: When nodes must not be relinked but values may be
  rewritten, or as the bridge to the victim-only deletion variant.
- **Two Pointers**: When the interviewer asks for one pass, which is this
  problem's canonical follow-up (recommended here).

### Optimization Notes

- In the two-pointer version the offset loop advances `fast` exactly `n`
  times with no bound check; the constraint `1 <= n <= sz` is what makes
  that safe.
- The dummy node earns its keep in both pointer versions: with `slow`
  starting at `dummy`, deleting the head is `dummy.next = dummy.next.next`,
  no branch needed.
- Both pointer versions leave the victim node's own `next` pointer dangling
  toward the list; languages with manual memory management would null it
  before freeing.
