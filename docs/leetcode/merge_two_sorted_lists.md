# [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

**Easy** | **20 minutes** | **Linked List**

**Pattern:** [K-Way Merge](../patterns/k_way_merge/intuition.md)

**Algorithm:** [Merge algorithm](https://en.wikipedia.org/wiki/Merge_algorithm) · [Linked list](https://en.wikipedia.org/wiki/Linked_list)

**Practice:** [`practice/merge_two_sorted_lists/solution.py`](../../practice/merge_two_sorted_lists/solution.py)

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

## Examples

### Example 1

![merged](assets/merge_two_sorted_list_ex1.jpg)

**Input:** `list1 = [1,2,4]`, `list2 = [1,3,4]`

**Output:** `[1,1,2,3,4,4]`

### Example 2

**Input:** `list1 = []`, `list2 = []`

**Output:** `[]`

### Example 3

**Input:** `list1 = []`, `list2 = [0]`

**Output:** `[0]`

## Constraints

- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

## Deriving the Solution

Both inputs arrive already sorted, and the observation every fast solution shares is that the head of the merged list must be the smaller of the two input heads. The rest is deciding how to repeat that one choice.

1. **Start literal.** Ignore the sortedness: dump every value into an array and
   repeatedly extract the minimum by hand, selection-sort style. Correct but `O((n + m)^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** The scan for the minimum is pointless. Each list is
   sorted, so the smallest remaining value overall is always one of the two current heads: a single comparison replaces the whole scan.
3. **Splice instead of copy.** Walk both lists with a tail pointer, linking the
   smaller head into the result and advancing its list; a dummy head removes the first-node special case, and the leftover list attaches in one step. `O(n + m)` time and `O(1)` space: see [Iterative](#iterative).
4. **Say it as a recurrence.** The same choice reads naturally as recursion:
   the merged list is the smaller head followed by the merge of what remains. Elegant, at the cost of `O(n + m)` call stack: see [Recursive](#recursive).

## Solutions

### Brute Force

#### Derivation

The most direct idea ignores the gift that both inputs are sorted and treats the problem as "produce a sorted list from a bag of numbers." Collect every value into an array, then build the answer one node at a time by scanning for the minimum remaining value and removing it, [selection-sort style](https://en.wikipedia.org/wiki/Sorting_algorithm). This never exploits the sorted order, which is exactly why it is the brute force.

1. Walk both lists and append every node's value to an array.
2. Repeatedly scan the array for the smallest remaining value, remove it, and
   append a new node holding that value to the result.
3. Continue until the array is empty, then return the built list.

#### Walkthrough

Let us watch the Brute Force run on Example 1: `list1 = [1,2,4]` and `list2 = [1,3,4]`.

First the code walks both lists and dumps every value into `values`, in order: first `list1` then `list2`, giving `values = [1, 2, 4, 1, 3, 4]`.

Now the main loop repeatedly scans for the smallest remaining value, pops it, and appends a fresh node to the result. The `smallest` index starts at `0` each round and only moves when a strictly smaller value is found, so on ties the leftmost minimum wins. Each row below shows one pop:

| Step | `smallest` index | value popped | `result` so far | `values` remaining |
|------|------------------|--------------|-----------------|--------------------|
| 1    | `0`              | `1`          | `[1]`           | `[2, 4, 1, 3, 4]`  |
| 2    | `2`              | `1`          | `[1, 1]`        | `[2, 4, 3, 4]`     |
| 3    | `0`              | `2`          | `[1, 1, 2]`     | `[4, 3, 4]`        |
| 4    | `1`              | `3`          | `[1, 1, 2, 3]`  | `[4, 4]`           |
| 5    | `0`              | `4`          | `[1, 1, 2, 3, 4]` | `[4]`            |
| 6    | `0`              | `4`          | `[1, 1, 2, 3, 4, 4]` | `[]`          |

In step 1 both `1`s are tied, so the scan keeps index `0` (the first one) and pops it. In step 2 the remaining `1` now sits at index `2`, so `smallest` walks there. Once `values` is empty the loop stops, and the code returns `dummy.next`: the merged list `[1, 1, 2, 3, 4, 4]`, which matches the expected Output.

#### Solution

The code is the walkthrough's two phases: the dump into `values`, then the scan-pop-append loop.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode],
                      list2: Optional[ListNode]) -> Optional[ListNode]:
        # Dump every value from both lists into a plain array
        values = []
        for head in (list1, list2):
            node = head
            while node:
                values.append(node.val)
                node = node.next

        # Build the result by repeatedly pulling out the smallest value by hand,
        # ignoring the fact that the inputs were already sorted
        dummy = ListNode(-1)
        current = dummy
        while values:
            smallest = 0
            for i in range(1, len(values)):
                if values[i] < values[smallest]:
                    smallest = i
            current.next = ListNode(values.pop(smallest))
            current = current.next

        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n + m)^2)`

Let `k = n + m` be the total number of values. Each of the `k` output nodes requires a linear scan to find the smallest remaining value, giving quadratic work overall.

##### Space Complexity: `O(n + m)`

The `values` array holds all `k` numbers, and the result list allocates `k` brand-new nodes rather than reusing the input nodes.

#### Key Insights

- Reframes the task as a plain sort, which is the most obvious starting point
  before noticing that the inputs are already sorted.
- Selecting the minimum by hand each step avoids any library sort, but pays for
  it with quadratic time.
- Allocates fresh nodes instead of splicing the originals, using extra memory
  the smarter approaches avoid.

### Iterative

#### Derivation

The brute force pays quadratic time for ignoring a gift: each input is already sorted, so the smallest remaining value is always the smaller of the two current heads. One comparison replaces the entire minimum scan, and it also removes the need for fresh nodes, since the winning node can be [spliced](https://en.wikipedia.org/wiki/Merge_algorithm) directly into the result. A `current` pointer builds the merged list while both inputs are traversed simultaneously:

1. Create `dummy` and point `current` at it; the dummy absorbs the special case
   of inserting the very first node.
2. While both `list1` and `list2` are non-empty, compare their head values:
   link the smaller node with `current.next`, advance that list's pointer, then advance `current`.
3. When one list empties, attach the other in a single step
   (`current.next = list1 if list1 else list2`); it is already sorted.
4. Return `dummy.next`, the real head sitting behind the dummy.

#### Walkthrough

Let us splice the lists of Example 1 by hand: `list1 = [1,2,4]` and `list2 = [1,3,4]`. `current` starts at `dummy`; each line compares the two current heads, links the smaller node, and advances two pointers:

```text
list1=1  list2=1    1 <= 1   splice list1's 1   merged: 1               list1 = 2->4
list1=2  list2=1    2 >  1   splice list2's 1   merged: 1->1            list2 = 3->4
list1=2  list2=3    2 <= 3   splice list1's 2   merged: 1->1->2         list1 = 4
list1=4  list2=3    4 >  3   splice list2's 3   merged: 1->1->2->3      list2 = 4
list1=4  list2=4    4 <= 4   splice list1's 4   merged: 1->1->2->3->4   list1 = None
list1 empty: current.next = list2   merged: 1->1->2->3->4->4
```

Both ties (`1 <= 1` and `4 <= 4`) splice the node from `list1`, keeping the merge stable. When `list1` runs out, the loop exits and the remainder of `list2` (its final `4`) attaches in one step. The method returns `dummy.next`, the list `[1, 1, 2, 3, 4, 4]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's comparison loop plus the one-step attach.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode],
                      list2: Optional[ListNode]) -> Optional[ListNode]:
        # Create a dummy node to serve as the head of our result list
        dummy = ListNode(-1)
        current = dummy

        # Iterate while both lists have nodes
        while list1 and list2:
            # Compare values and link the smaller node to our result
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            # Move the current pointer forward
            current = current.next

        # Attach remaining nodes (if any)
        current.next = list1 if list1 else list2

        # Return the merged list (skip the dummy node)
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Where `n` and `m` are the lengths of `list1` and `list2` respectively. We traverse each node in both lists exactly once.

##### Space Complexity: `O(1)`

We only use a constant amount of extra space for pointers. The solution reuses the existing nodes without allocating additional memory for the merged list structure.

#### Key Insights

- Using a dummy head node simplifies handling corner cases and avoids special treatment for the first node insertion
- The solution leverages the fact that both input lists are already sorted
- Attaching remaining nodes at once is more efficient than continuing comparisons after one list is exhausted
- In-place merging saves memory by reusing existing nodes instead of creating new ones

### Recursive

#### Derivation

The iterative loop makes the same decision at every step, which suggests expressing the merge as a [recurrence](https://en.wikipedia.org/wiki/Recursion_(computer_science)): the smaller of the two heads is the head of the merged list, and its `next` is the merge of the remainder of that list with the entire other list. The recursion bottoms out when either list becomes empty, at which point the other list is already sorted and can be returned as-is.

1. If `list1` is empty, the merge is simply `list2`, and vice versa
2. Otherwise compare the heads, splice the smaller node onto the front of the
   recursively merged tail (`list1.next = self.mergeTwoLists(list1.next, list2)`), and return that node as the new head

#### Walkthrough

Let us unwind the recursion on Example 1: `list1 = [1,2,4]` and `list2 = [1,3,4]`. Indentation follows the call depth; each call keeps its smaller head and recurses on what remains:

```text
mergeTwoLists(1->2->4, 1->3->4)    1 <= 1: keep list1's 1
  mergeTwoLists(2->4, 1->3->4)     2 >  1: keep list2's 1
    mergeTwoLists(2->4, 3->4)      2 <= 3: keep list1's 2
      mergeTwoLists(4, 3->4)       4 >  3: keep list2's 3
        mergeTwoLists(4, 4)        4 <= 4: keep list1's 4
          mergeTwoLists(None, 4)   base case: list1 empty -> return list2 (4)
        returns 4->4
      returns 3->4->4
    returns 2->3->4->4
  returns 1->2->3->4->4
returns 1->1->2->3->4->4
```

Descending, each call chooses a head; the base case hands back the leftover `4` from `list2` untouched. Ascending, every frame sets its kept node's `next` to the list returned from below and passes the result upward, so the answer assembles back to front. The outermost call returns the list `[1, 1, 2, 3, 4, 4]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's call tree: two base cases, then the splice of the smaller head onto the merged remainder.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode],
                      list2: Optional[ListNode]) -> Optional[ListNode]:
        # Base cases: if one list is empty, the merged result is the other list
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        # Pick the smaller head, then merge the rest behind it
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Each recursive call consumes exactly one node from one of the lists, so the total number of calls equals the combined length of both lists.

##### Space Complexity: `O(n + m)`

The recursion stack grows one frame per node consumed, reaching depth `n + m` in the worst case before any frame returns. Unlike the iterative version, this does not achieve constant space.

#### Key Insights

- The recursive formulation reads almost like the problem statement: the merged
  list is the smaller head followed by the merge of what remains
- No dummy node is needed because each call returns the correct head directly
- The tradeoff for this clarity is `O(n + m)` stack space, which can overflow
  for very long lists in languages without tail-call optimization

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O((n + m)^2)` - Each output node costs a linear scan for the minimum remaining value
- **Iterative**: `O(n + m)` - Each node from both lists is visited exactly once
- **Recursive**: `O(n + m)` - One recursive call consumes one node, totaling `n + m` calls

### Space Complexity

- **Brute Force**: `O(n + m)` - Buffers every value and allocates fresh nodes for the result
- **Iterative**: `O(1)` - Only a handful of pointers regardless of list length
- **Recursive**: `O(n + m)` - Recursion stack reaches depth equal to the combined length

### Trade-offs

- **Brute Force** is the most intuitive starting point and needs no insight about the inputs, but it discards the sorted-order gift and pays with quadratic time and extra allocations
- **Iterative** uses constant space and avoids any risk of stack overflow, at the cost of slightly more bookkeeping with the dummy node and current pointer
- **Recursive** is more concise and maps directly onto the recurrence, but its stack usage scales linearly and can overflow on very long lists

### When to Use Each

- **Brute Force**: As a teaching baseline or first instinct before noticing the inputs are already sorted
- **Iterative**: The default choice for interviews and production, especially when lists may be long or constant space is required
- **Recursive**: When clarity matters most and inputs are known to be small, or to demonstrate the recursive structure of the problem

### Optimization Notes

- The iterative solution is recommended for its `O(1)` space and freedom from recursion-depth limits; both linear approaches share the same `O(n + m)` time
- Exploiting the already-sorted inputs is the key leap from the brute force: a single comparison of the two heads replaces the repeated minimum scan, collapsing `O((n + m)^2)` to `O(n + m)`
- The iterative and recursive solutions splice existing nodes rather than allocating new ones, so no extra heap memory is used for the merged structure itself
- The `<=` comparison (rather than `<`) preserves the relative order of equal-valued nodes, keeping the merge stable
