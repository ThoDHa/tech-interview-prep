# [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

**Easy** | **15 minutes** | **Linked List, Recursion**

**Pattern:** [Linked List Reversal](../patterns/linked_list_in_place_reversal/intuition.md)

**Algorithm:** [Linked list](https://en.wikipedia.org/wiki/Linked_list) · [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/reverse_linked_list/solution.py`](../../practice/reverse_linked_list/solution.py)

Given the `head` of a singly linked list, reverse the list, and return the reversed list.

## Examples

### Example 1

![Reverse Linked List Example 1](assets/reverse_linked_list_example1.jpg)

**Input:** `head = [1,2,3,4,5]`

**Output:** `[5,4,3,2,1]`

### Example 2

![Reverse Linked List Example 2](assets/reverse_linked_list_example2.jpg)

**Input:** `head = [1,2]`

**Output:** `[2,1]`

### Example 3

**Input:** `head = []`

**Output:** `[]`

## Constraints

- The number of nodes in the list is the range `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

## Follow-up

A linked list can be reversed either iteratively or recursively. Could you implement both?

## Deriving the Solution

A reversed list is one in which every node's `next` points to its old predecessor instead of its old successor. The solutions below differ in whether they achieve that by moving the data or by rewiring the links, and, for the rewiring, whether a loop or the call stack keeps track of the predecessor.

1. **Start literal.** Leave the structure alone and move the payload: copy every
   value into an array, then walk the nodes again writing the values back in reverse order. Correct in `O(n)` time, but it buffers the whole list in `O(n)` extra space: see [Brute Force](#brute-force).
2. **Spot the waste.** The values never needed to move; only the links point the
   wrong way. Reversal really asks for each node's `next` to be flipped toward its predecessor, and flipping a pointer needs no buffer at all.
3. **Flip the links in place.** Walk the list once with a `prev` and a `curr`
   pointer, flipping one edge per step. The only subtlety is saving `curr.next` before overwriting it, or the rest of the list is lost. One pass, `O(1)` extra space: see [Iterative](#iterative).
4. **Let recursion track the predecessor.** The same rewiring can be phrased
   top-down: reverse the tail by a recursive call, then hook the current node in behind its old successor. Elegant, and it answers the Follow-up, but the call stack costs `O(n)` space: see [Recursive](#recursive).

## Solutions

### Brute Force

#### Derivation

The most direct idea ignores pointer rewiring entirely and asks a simpler question: does the list even have to change shape, or is it enough for the same nodes to hold the values in the opposite order? Read all the node values into an array, then walk the same nodes a second time, writing the values back in reverse order. The list structure never changes; only the payload in each node is swapped end for end.

1. Traverse the list once, appending every node's `val` to a `values` array in
   forward order.
2. Traverse the list a second time from `head`, writing `values[i]` into the
   current node while `i` counts down from the last index.
3. Return the original `head`, whose nodes now hold the values in reversed order.

#### Walkthrough

Trace the brute force solution on Example 1: `head = [1,2,3,4,5]`.

**Pass 1: collect values.** Walk from `head`, appending each `val`. After the loop, `values = [1, 2, 3, 4, 5]` and `i` starts at `len(values) - 1 = 4`.

**Pass 2: overwrite each node.** Walk the same nodes again from `head`. Each step writes `values[i]` into the current node, then decrements `i`. The node positions never move; only the value stored at each position changes.

| Step | `i` | Value written (`values[i]`) | List after this step |
|------|-----|-----------------------------|----------------------|
| 1 | 4 | `5` | `[5, 2, 3, 4, 5]` |
| 2 | 3 | `4` | `[5, 4, 3, 4, 5]` |
| 3 | 2 | `3` | `[5, 4, 3, 4, 5]` |
| 4 | 1 | `2` | `[5, 4, 3, 2, 5]` |
| 5 | 0 | `1` | `[5, 4, 3, 2, 1]` |

Notice step 3 leaves the list unchanged: the middle node already held `3`, so writing `3` back is a no-op. After the loop `curr` is `None`, and the method returns the original `head`, whose nodes now read `[5, 4, 3, 2, 1]`. This matches the expected Output `[5,4,3,2,1]`.

#### Solution

The code is the two passes from the walkthrough: collect `values`, then write them back while `i` counts down.

```python
from typing import Optional


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Collect every value in forward order
        values = []
        curr = head
        while curr:
            values.append(curr.val)
            curr = curr.next
        # Walk the nodes again, overwriting each with the value from the back
        curr = head
        i = len(values) - 1
        while curr:
            curr.val = values[i]
            i -= 1
            curr = curr.next
        return head
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. Two separate passes each touch every node once, which is still linear.

##### Space Complexity: `O(n)`

The `values` array holds a copy of every node's value, so the auxiliary storage grows linearly with the list length.

#### Key Insights

- Reverses by relocating values rather than flipping links, which is the easiest correct idea to reach without knowing the pointer trick.
- Requires `O(n)` extra space for the value buffer, the cost of not touching the structure.
- Mutating values in place works for a singly linked list, but it would not generalize to cases where node identity or attached payloads must move with the data.

### Iterative

#### Derivation

The Brute Force spends `O(n)` extra space buffering values that never needed to move: the nodes are all still there, and only their links point the wrong way. So ask instead: can each node's `next` be flipped to point at its predecessor during a single walk of the [linked list](https://en.wikipedia.org/wiki/Linked_list)?

Flipping needs to know the predecessor, so we carry it along: a `prev` pointer that starts at `None` (the new tail, since the old head ends up last), and a `curr` pointer at the node being processed. The one catch is that overwriting `curr.next` severs the only route to the rest of the list, so the forward link must be saved into `next_node` before the flip. For each node in the original list, we:

1. Save the current node's `next` into `next_node` before the link is overwritten.
2. Point the current node's `next` back to `prev`, reversing that edge.
3. Advance `prev` to the current node, growing the reversed portion.
4. Advance `curr` to the saved `next_node`, moving on to the next node.

When `curr` becomes `None`, every edge has been flipped and `prev` points to the original tail, which is the new head of the reversed list.

#### Walkthrough

Let us run the loop by hand on Example 1: `head = [1,2,3,4,5]`. Each line below is one full iteration (save `next_node`, flip `curr.next` to `prev`, advance both pointers). The chain growing from `prev` is the reversed part; the chain from `curr` is what is still to process:

```text
start    prev = None                     curr = 1 -> 2 -> 3 -> 4 -> 5
step 1   prev = 1                        curr = 2 -> 3 -> 4 -> 5     next_node was 2
step 2   prev = 2 -> 1                   curr = 3 -> 4 -> 5          next_node was 3
step 3   prev = 3 -> 2 -> 1              curr = 4 -> 5               next_node was 4
step 4   prev = 4 -> 3 -> 2 -> 1         curr = 5                    next_node was 5
step 5   prev = 5 -> 4 -> 3 -> 2 -> 1    curr = None                 next_node was None
```

Step 1 shows why `next_node` is saved first: the flip `curr.next = prev` points node `1` at `None`, and without the saved reference to node `2` the rest of the list would be unreachable. After step 5, `curr` is `None`, the loop exits, and `prev` points at node `5`, the head of the chain `5 -> 4 -> 3 -> 2 -> 1`. Returning `prev` yields `[5,4,3,2,1]`, the expected Output.

#### Solution

The code is the four-step loop from the walkthrough, one edge flip per iteration.

```python
from typing import Optional


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. We visit each node exactly once.

##### Space Complexity: `O(1)`

We use a constant amount of extra space regardless of input size. Only three pointer variables are needed.

#### Key Insights

- An in-place algorithm that flips one edge per iteration without any auxiliary data structure.
- Saving `curr.next` before rewiring is essential: once `curr.next` is reassigned to `prev`, the forward link is gone, so the traversal must capture it first.
- A single pass with constant space makes it the most efficient choice for long lists.

### Recursive

#### Derivation

The Iterative solution tracks the predecessor by hand in `prev`. The Follow-up asks for a [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) version as well, and recursion can let the call stack do that bookkeeping instead. Ask: if the rest of the list (everything after `head`) were already reversed, what would be left to do? Only two pointer writes: the old successor `head.next` is now the tail of the reversed sublist, so point it back at `head`, and then clear `head.next` so `head` becomes the new tail. That reduces the problem to reversing a list one node shorter, which is exactly a recursion:

1. The base case returns `head` directly for an empty list or a single node,
   since either is already reversed.
2. Recurse on `head.next` to reverse the rest of the list; `new_head` is the
   original tail, which becomes the head of the reversed list and is passed back unchanged through every frame.
3. After the recursion returns, `head.next` is the tail of the already-reversed
   sublist, so set `head.next.next = head` to make it point back to `head`.
4. Set `head.next = None` so `head` becomes the new tail and the old forward
   link is broken.

#### Walkthrough

Let us run the recursion by hand on Example 1: `head = [1,2,3,4,5]`. The trace indents one level per recursive call: the descent reaches the old tail `5` (the base case), and each unwinding frame performs the two pointer writes, passing `new_head = 5` back unchanged:

```text
reverseList(1)                     recurse on 2
  reverseList(2)                   recurse on 3
    reverseList(3)                 recurse on 4
      reverseList(4)               recurse on 5
        reverseList(5)             base case: 5.next is None, return 5
      4: 5.next = 4; 4.next = None    reversed so far: 5 -> 4         return new_head = 5
    3: 4.next = 3; 3.next = None      reversed so far: 5 -> 4 -> 3    return new_head = 5
  2: 3.next = 2; 2.next = None        reversed so far: 5 -> 4 -> 3 -> 2
1: 2.next = 1; 1.next = None          reversed so far: 5 -> 4 -> 3 -> 2 -> 1
```

In the frame for node `4`, `head.next` is node `5`, so `head.next.next = head` writes `5.next = 4`, and `head.next = None` detaches the old forward edge. Every frame repeats the same two writes one node closer to the front. The outermost call returns `new_head`, node `5`, heading the chain `5 -> 4 -> 3 -> 2 -> 1`: the expected Output `[5,4,3,2,1]`.

#### Solution

The code is the descent and unwind from the walkthrough: the base case, the recursive call, and the two pointer writes.

```python
from typing import Optional


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. Each node is visited once during the descent and fixed once during the return.

##### Space Complexity: `O(n)`

The recursion creates a stack of function calls proportional to the list length. In the worst case, the recursion depth equals the number of nodes.

#### Key Insights

- Elegant recursive formulation that naturally expresses reversing the tail before the head.
- The `head.next = None` line is mandatory: skipping it leaves the old forward link intact and creates a cycle between the last two nodes of the reversed list.
- More concise to read but carries call-stack overhead, which matters for long lists.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - Two passes, but still linear overall
- **Iterative**: `O(n)` - Single pass through the list
- **Recursive**: `O(n)` - Also processes each node once

### Space Complexity

- **Brute Force**: `O(n)` - Buffers every node's value in an array
- **Iterative**: `O(1)` - Uses fixed amount of extra space
- **Recursive**: `O(n)` - Uses call stack space proportional to list length

### Trade-offs

- The brute force solution is the easiest to derive but spends `O(n)` extra space to copy values rather than rewire links
- The iterative solution is more space-efficient but requires tracking multiple pointers
- The recursive solution is more elegant but uses more memory due to the call stack

### When to Use Each

- **Brute Force**: As a first correct attempt or when reversing values is acceptable and structure must stay fixed
- **Iterative**: When memory efficiency is important or the list might be very long
- **Recursive**: When code readability is valued over memory efficiency and the list is reasonably sized

### Optimization Notes

- **The iterative approach is the recommended solution**: it reverses the list in a single pass using `O(1)` space and avoids the call-stack overhead of recursion, which matters given the constraint of up to 5000 nodes
- A key implementation detail is saving `curr.next` into a `next_node` variable before rewiring the pointer: once `curr.next` is reassigned to `prev`, the original forward link is lost, so the traversal must capture it first
- Avoid the recursive approach for long lists: its `O(n)` stack depth can trigger a stack overflow (Python's default recursion limit is around 1000), and the same per-node pointer rewiring is achievable iteratively without that risk
- In the recursive solution, do not forget the `head.next = None` line: skipping it leaves the old forward link intact and creates a cycle between the last two nodes of the reversed list
