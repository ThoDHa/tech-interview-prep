# [Merge k Sorted Lists](https://www.fastprep.io/problems/amazon-merge-k-sorted-lists)

**Hard** | **NN minutes** | **Linked List, Heap**

You are given an array lists containing k linked-list heads. Every linked list is sorted in ascending order.

Merge all of the linked lists into one ascending linked list and return its head.

## Examples

### Example 1

**Input:** `lists = [[1,4,5],[1,3,4],[2,6]]`

**Output:** `[1,1,2,3,4,4,5,6]`

**Explanation:** The linked lists are:

1 -> 4 -> 5
1 -> 3 -> 4
2 -> 6Merging them produces the sorted linked list 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6.

### Example 2

**Input:** `lists = []`

**Output:** `[]`

### Example 3

**Input:** `lists = [[]]`

**Output:** `[]`

## Constraints

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `Each lists[i] is sorted in ascending order.`
- `The sum of all lists[i].length values does not exceed 10^4.`

## Solutions

### Repeated Minimum Scan

#### Derivation

All `k` inputs are already sorted, so the greedy reading of the problem is immediate: the next node of the merged list must be the smallest of the `k` current heads. Hold one live cursor per list, find that smallest head by scanning all of them, splice it onto the growing tail, and advance only the cursor it came from. No heap and no merge helper: just the scan, repeated until every cursor has run off the end of its list:

1. Copy the heads into `heads`, one live cursor per input list, with `None` marking an exhausted list.
2. Seed a `dummy` node and a `tail` pointer that builds the merged list.
3. Each round, scan `heads` for `min_idx`, the index of the smallest non-`None` head. The strict `<` comparison keeps the lowest index when values tie.
4. If `min_idx` stays `-1`, every list is exhausted: stop the loop.
5. Otherwise splice `heads[min_idx]` onto `tail`, advance `heads[min_idx]` to its successor, and go to step 3.
6. Pin `tail.next = None` as the list terminator and return `dummy.next`.

#### Walkthrough

Run the scan on Example 1: `lists = [[1,4,5],[1,3,4],[2,6]]`. The `heads` row of the table shows the cursor values at the start of each step; the scan picks the smallest, emits it behind `tail`, and advances only that cursor. When two cursors hold the same value, the strict `<` test keeps the first one found:

| Step | `heads` (cursor values) | `min_idx` | Emitted | Merged so far |
|------|-------------------------|-----------|---------|---------------|
| 1 | `[1, 1, 2]` | 0 | `1` | `1` |
| 2 | `[4, 1, 2]` | 1 | `1` | `1 -> 1` |
| 3 | `[4, 3, 2]` | 2 | `2` | `1 -> 1 -> 2` |
| 4 | `[4, 3, 6]` | 1 | `3` | `1 -> 1 -> 2 -> 3` |
| 5 | `[4, 4, 6]` | 0 | `4` | `1 -> 1 -> 2 -> 3 -> 4` |
| 6 | `[5, 4, 6]` | 1 | `4` | `1 -> 1 -> 2 -> 3 -> 4 -> 4` |
| 7 | `[5, None, 6]` | 0 | `5` | `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5` |
| 8 | `[None, None, 6]` | 2 | `6` | `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6` |

Step 8 exhausts the last cursor, so the next scan leaves `min_idx == -1`, the loop breaks, and `dummy.next` is `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6`, matching the expected Output `[1,1,2,3,4,4,5,6]`. (The empty inputs of Examples 2 and 3 never enter the loop at all: every cursor starts as `None` or the cursor array itself is empty.)

#### Solution

The code is the walkthrough's loop: scan `heads` for `min_idx`, splice that node onto `tail`, advance one cursor.

```python
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next_node


class Solution:
    def solve(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heads = list(lists)

        dummy = ListNode(0)
        tail = dummy

        while True:
            min_idx = -1
            for list_idx, node in enumerate(heads):
                if node and (min_idx == -1 or node.val < heads[min_idx].val):
                    min_idx = list_idx

            if min_idx == -1:
                break

            tail.next = heads[min_idx]
            tail = tail.next
            heads[min_idx] = heads[min_idx].next

        tail.next = None
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × k)`

Where `N` is the total number of nodes across all lists: each of the `N` nodes is emitted once, and emitting it costs an `O(k)` scan over the cursors to find the current minimum.

##### Space Complexity: `O(k)`

The `heads` array holds one cursor per list, and the merged list is built by relinking the input nodes rather than copying them.

#### Key Insights

- The greedy core of the problem needs no clever structure: the smallest current head always belongs next in the merged list.
- Splicing the input nodes instead of allocating new ones keeps the extra space to the `k`-entry cursor array.
- The strict `<` comparison gives a deterministic tie-break (lowest list index wins), which is what makes the trace reproducible.
- The `O(k)` work spent per node to locate the minimum is exactly the cost the two approaches below cut down to `O(log k)`.

### Divide and Conquer

#### Derivation

Merging two sorted lists is a solved problem with a linear splice loop, so the real question is how to schedule `k` two-way merges. Folding the lists into one accumulator left to right is wasteful: the accumulator keeps growing, so its early nodes are re-walked by every later merge. The repair is to keep every merge between lists of similar length. [Divide and conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) pairing does that: merge the lists two at a time, halving the count each round, until a single list remains. Each node then takes part in one merge per round, and there are only `log k` rounds:

1. Return `None` immediately when `lists` is empty.
2. Write `merge_two_lists(first, second)`: a `dummy` node and a `tail` pointer; while both lists are live, splice the smaller head and advance that list; when one empties, attach the survivor with `tail.next = first or second`.
3. While more than one list remains, walk `pending` two at a time with `pair_start`, merging `pending[pair_start]` with `pending[pair_start + 1]`, guarding the odd tail with `None`.
4. Replace `pending` with the round's outputs; when one list remains, return it.

#### Walkthrough

Run the rounds on Example 1: `lists = [[1,4,5],[1,3,4],[2,6]]`, so `k = 3`. Round 1 pairs list 0 with list 1, and the odd list out merges against `None`, which returns it unchanged. The splice loop inside the first pair, with the heads shown before each comparison:

```text
round 1   merge_two_lists(1->4->5, 1->3->4):
            1 <= 1   splice first's 1    first = 4->5
            4 >  1   splice second's 1   second = 3->4
            4 >  3   splice second's 3   second = 4
            4 <= 4   splice first's 4    first = 5
            5 >  4   splice second's 4   second = None
            second empty: tail.next = first  ->  1->1->3->4->4->5
          merge_two_lists(2->6, None): odd tail, unchanged  ->  2->6
          pending = [1->1->3->4->4->5, 2->6]
round 2   merge_two_lists(1->1->3->4->4->5, 2->6)  ->  1->1->2->3->4->4->5->6
          pending = [1->1->2->3->4->4->5->6]
```

The tie at `4 <= 4` keeps the node from `first`, the accumulated pair, so equal values stay in their input order. After round 2 a single list remains and is returned: `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6`, matching the expected Output `[1,1,2,3,4,4,5,6]`.

#### Solution

The code is the walkthrough's schedule: an outer loop that pairs off `pending`, with `merge_two_lists` doing each splice.

```python
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next_node


class Solution:
    def solve(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None

        def merge_two_lists(
            first: Optional[ListNode], second: Optional[ListNode]
        ) -> Optional[ListNode]:
            dummy = ListNode(0)
            tail = dummy

            while first and second:
                if first.val <= second.val:
                    tail.next = first
                    first = first.next
                else:
                    tail.next = second
                    second = second.next
                tail = tail.next

            tail.next = first or second
            return dummy.next

        pending = list(lists)
        while len(pending) > 1:
            merged_pairs: List[Optional[ListNode]] = []
            for pair_start in range(0, len(pending), 2):
                first = pending[pair_start]
                second = (
                    pending[pair_start + 1]
                    if pair_start + 1 < len(pending)
                    else None
                )
                merged_pairs.append(merge_two_lists(first, second))
            pending = merged_pairs

        return pending[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Each round merges every node exactly once, costing `O(N)` total, and pairing halves the list count, so there are `log k` rounds.

##### Space Complexity: `O(k)`

Each round allocates `merged_pairs` holding up to `⌈k/2⌉` heads, and both the outer loop and the splice helper are iterative, so no recursion stack grows.

#### Key Insights

- Pairing similar-length lists is what separates this from the quadratic left-to-right fold: a whole round costs `O(N)`, and `log k` rounds give `O(N log k)`.
- Guarding the odd tail with `None` is the entire odd-count story: the unpaired list merges against `None` and passes through unchanged.
- The approach reaches the optimal bound entirely from scratch; the only helper it needs is the classic two-list splice.
- Relinking input nodes means the merged list shares storage with the input, which is fine for a functional merge but worth stating out loud in an interview.

### Min-Heap

#### Derivation

The Repeated Minimum Scan already emits nodes in the right order; its only flaw is paying `O(k)` per node to find the smallest head. A [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) is the structure built for exactly that job: it returns the minimum of its entries in `O(log k)` and accepts a replacement in `O(log k)`. Keep one candidate per list in the heap, and the scan's search becomes a pop:

1. Push `(head.val, list_idx, head)` for each non-empty list. The `list_idx` between the value and the node breaks ties between equal values, so the heap never compares `ListNode` objects, which have no ordering.
2. Pop the smallest triple and splice its node onto `tail`.
3. If the popped node has a successor, push `(node.next.val, list_idx, node.next)`, which keeps exactly one candidate per live list in the heap.
4. When the heap empties, every node has been spliced; return `dummy.next`.

#### Walkthrough

The heap is the technique here, so the trace follows its contents on Example 1: `lists = [[1,4,5],[1,3,4],[2,6]]`. Entries are shown as `(val, list_idx)` in priority order; each step pops the minimum, splices its node, and pushes the successor when one exists:

```text
init: push (1,0), (1,1), (2,2)     heap = [(1,0), (1,1), (2,2)]
pop (1,0)   splice 1   push (4,0)  heap = [(1,1), (2,2), (4,0)]
pop (1,1)   splice 1   push (3,1)  heap = [(2,2), (3,1), (4,0)]
pop (2,2)   splice 2   push (6,2)  heap = [(3,1), (4,0), (6,2)]
pop (3,1)   splice 3   push (4,1)  heap = [(4,0), (4,1), (6,2)]
pop (4,0)   splice 4   push (5,0)  heap = [(4,1), (5,0), (6,2)]
pop (4,1)   splice 4   list 1 exhausted        heap = [(5,0), (6,2)]
pop (5,0)   splice 5   list 0 exhausted        heap = [(6,2)]
pop (6,2)   splice 6   list 2 exhausted        heap = []
```

The tie-break shows twice: `(1,0)` pops before `(1,1)` and `(4,0)` before `(4,1)`, because tuple comparison falls through to `list_idx` when the values are equal. The heap never holds more than `k = 3` entries while all eight nodes flow through it, and `dummy.next` ends up as `1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6`, matching the expected Output `[1,1,2,3,4,4,5,6]`.

#### Solution

The code is the walkthrough's pop-splice-push cycle, with `heapq` maintaining the priority order shown on the right of the trace.

```python
import heapq
from typing import List, Optional, Tuple


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next_node


class Solution:
    def solve(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap: List[Tuple[int, int, ListNode]] = []
        for list_idx, head in enumerate(lists):
            if head:
                heapq.heappush(heap, (head.val, list_idx, head))

        dummy = ListNode(0)
        tail = dummy

        while heap:
            _, list_idx, node = heapq.heappop(heap)
            tail.next = node
            tail = tail.next
            if node.next:
                heapq.heappush(heap, (node.next.val, list_idx, node.next))

        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Each of the `N` nodes is pushed and popped once, and every heap operation costs `O(log k)` on a heap bounded by `k` entries.

##### Space Complexity: `O(k)`

The heap holds one candidate per live list, so it never grows beyond `k` triples.

#### Key Insights

- The heap entry `(value, list_idx, node)` places `list_idx` between the value and the node, so ties break on list index and `ListNode` objects are never compared.
- Holding one candidate per list bounds the heap by `k` regardless of `N`, which is what keeps the space linear in the number of lists rather than the number of nodes.
- This approach is the Repeated Minimum Scan with the linear minimum search handed to `heapq`; the divide and conquer version reaches the same bound from scratch.

## Comparison of Solutions

### Time Complexity

- **Repeated Minimum Scan**: `O(N × k)` - an `O(k)` scan per emitted node to find the smallest current head.
- **Divide and Conquer**: `O(N log k)` - `log k` rounds of pairwise merges, each round touching every node once.
- **Min-Heap**: `O(N log k)` - one `O(log k)` pop and push per node on a heap bounded by `k`.

### Space Complexity

- **Repeated Minimum Scan**: `O(k)` - the per-list cursor array, with input nodes relinked.
- **Divide and Conquer**: `O(k)` - the per-round `merged_pairs` array of up to `⌈k/2⌉` heads.
- **Min-Heap**: `O(k)` - one `(val, list_idx, node)` triple per live list.

### Trade-offs

- **Repeated Minimum Scan**: the most self-derivable expression of the greedy idea, but its per-node `O(k)` scan makes it impractical when both `k` and `N` grow.
- **Divide and Conquer**: optimal time from scratch with no library reliance, at the cost of writing and testing the two-list splice helper and the pairing loop.
- **Min-Heap**: optimal time with the shortest optimal code, but it leans on `heapq` to do the core minimum-finding work.

### When to Use Each

- **Repeated Minimum Scan**: as a first explanation of why the merged order is well-defined, or when `k` is small enough that the quadratic cost is harmless.
- **Divide and Conquer (Recommended)**: the strongest interview answer: optimal time, `O(k)` extra space, and no library dependence.
- **Min-Heap**: when `k` is very large or the interviewer expects the standard heap-based k-way merge, and a library is welcome.

### Optimization Notes

- Both optimal approaches attack the same bottleneck, the scan's `O(k)` minimum search: the heap lowers it to an `O(log k)` pop, divide and conquer removes it by giving each node only `log k` pairwise merges.
- The tie-break conventions matter for stability: the scan's strict `<` and the heap's `list_idx` field both preserve the input order of equal values.
- The divide and conquer pairing loop must guard its odd tail (`pending[pair_start + 1] if pair_start + 1 < len(pending) else None`); merging the leftover list against `None` is what keeps an odd `k` correct.
- Each approach terminates the merged list differently: the divide and conquer helper pins it explicitly with `tail.next = first or second`, while the scan and the heap rely on the emission order leaving the final node's successor `None`; the scan's post-loop `tail.next = None` pins that terminus anyway, cheap insurance against a future edit that reorders the emissions.
