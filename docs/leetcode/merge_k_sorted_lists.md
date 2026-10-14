# [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

**Hard** | **45 minutes** | **Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md), [K-Way Merge](../patterns/k_way_merge/intuition.md)

**Algorithm:** [K-way merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm) · [Divide and conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))

**Practice:** [`practice/merge_k_sorted_lists/solution.py`](../../practice/merge_k_sorted_lists/solution.py)

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

## Examples

### Example 1

**Input:** `lists = [[1,4,5],[1,3,4],[2,6]]`

**Output:** `[1,1,2,3,4,4,5,6]`

**Explanation:** The linked-lists are:

```text
[
  1->4->5,
  1->3->4,
  2->6
]
```

merging them into one sorted list: `1->1->2->3->4->4->5->6`

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
- `lists[i]` is sorted in **ascending** order.
- The sum of `lists[i].length` will not exceed `10^4`.

## Deriving the Solution

All k inputs are already sorted, so the next node of the merged list is always the smallest of the k current heads. Every solution below either speeds up finding that minimum or reorganizes the k-way merge into balanced two-way merges.

1. **Start literal.** Keep one cursor per list and scan all k of them for the
   minimum before emitting each node: `O(N × k)`: see [Repeated Minimum Scan](#repeated-minimum-scan).
2. **Reuse a known tool.** Merging two sorted lists is a solved problem, so fold
   the lists into an accumulated result one at a time. Simpler code, but the accumulator is re-walked on every merge, so the cost stays `O(N × k)`: see [Sequential Merge](#sequential-merge).
3. **Balance the merging.** The waste is the ever-longer accumulator. Merging
   the lists in pairs halves their count each round, so every node takes part in only `log k` merges: `O(N log k)`, entirely from scratch: see [Divide and Conquer](#divide-and-conquer).
4. **Or fix the scan directly.** Replace the linear minimum search of step 1
   with a min-heap of the k current heads: each pop and push costs `O(log k)`, reaching the same `O(N log k)` via the library: see [Min-Heap](#min-heap).

## Solutions

### Repeated Minimum Scan

#### Derivation

The most direct idea is the [greedy](https://en.wikipedia.org/wiki/Greedy_algorithm) one: at every step, the next node of the merged list must be the smallest of the k current heads. Hold one cursor per list and find that minimum by scanning all cursors by hand, no sort and no heap. Append it, advance only the list it came from, and repeat until every cursor is `None`.

1. Copy the list heads into a `heads` array of live cursors, one per input list.
2. Scan all cursors and record the index of the smallest non-`None` head.
3. If no live cursor remains, stop; otherwise append that node and advance its cursor.
4. Terminate the merged list with `tail.next = None` so no stale link survives from a reused node.

#### Walkthrough

Let us watch the Repeated Minimum Scan run on Example 1: `lists = [[1,4,5],[1,3,4],[2,6]]`, expected output `[1,1,2,3,4,4,5,6]`.

The `heads` array holds one live cursor per list, starting at each list's first node: `[1, 1, 2]`. Each step scans those cursors for the smallest value, appends that node to the merged tail, and advances only the cursor it came from. When two cursors tie (like the two leading `1`s), the scan keeps the first one it found because the test is a strict `node.val < heads[min_idx].val`, so the lower index wins.

Each row below shows the cursor values at the start of the step (`None` marks an exhausted list), which index the scan picks, and the value emitted:

| Step | `heads` (cursor values) | `min_idx` | Emitted | Merged so far |
|------|-------------------------|-----------|---------|---------------|
| 1 | `[1, 1, 2]` | 0 | `1` | `1` |
| 2 | `[4, 1, 2]` | 1 | `1` | `1,1` |
| 3 | `[4, 3, 2]` | 2 | `2` | `1,1,2` |
| 4 | `[4, 3, 6]` | 1 | `3` | `1,1,2,3` |
| 5 | `[4, 4, 6]` | 0 | `4` | `1,1,2,3,4` |
| 6 | `[5, 4, 6]` | 1 | `4` | `1,1,2,3,4,4` |
| 7 | `[5, None, 6]` | 0 | `5` | `1,1,2,3,4,4,5` |
| 8 | `[None, None, 6]` | 2 | `6` | `1,1,2,3,4,4,5,6` |

After step 8 every cursor is `None`, so the next scan returns `min_idx == -1` and the loop breaks. The function sets `tail.next = None` and returns `dummy.next`, the head of `1->1->2->3->4->4->5->6`, which matches the expected Output `[1,1,2,3,4,4,5,6]`.

#### Solution

The code is the walkthrough's loop: scan `heads` for `min_idx`, splice that node onto `tail`, and advance one cursor.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Keep a live cursor into each list; None marks an exhausted list
        heads = list(lists)

        dummy = ListNode(0)
        tail = dummy

        while True:
            # Scan every cursor by hand to find the smallest current head
            min_idx = -1
            for i, node in enumerate(heads):
                if node and (min_idx == -1 or node.val < heads[min_idx].val):
                    min_idx = i

            # No live cursor left: every list is exhausted
            if min_idx == -1:
                break

            # Append the smallest node and advance only that list's cursor
            tail.next = heads[min_idx]
            tail = tail.next
            heads[min_idx] = heads[min_idx].next

        tail.next = None
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × k)`

Each of the `N` nodes is emitted once, and emitting it costs an `O(k)` scan over the k cursors to find the current minimum, giving `N × k` total work.

##### Space Complexity: `O(k)`

The `heads` cursor array holds k entries. Result nodes are spliced from the input rather than copied, so no per-node storage grows with `N`.

#### Key Insights

- Implements the core lesson, repeatedly choosing the smallest available head, with a hand-written linear minimum search instead of a library `sort` or `heapq`.
- Reuses the existing input nodes by relinking them, so the only extra space is the k-entry cursor array.
- The `O(k)` scan per emitted node is exactly the work the heap and divide-and-conquer approaches later replace with `O(log k)` per node.

### Sequential Merge

#### Derivation

The minimum scan builds its machinery from nothing, yet merging two sorted lists is already a solved problem: the classic two-pointer [merge](https://en.wikipedia.org/wiki/Merge_algorithm) splices the smaller head onto a growing tail until one list empties. So ask: can that known tool be reused as-is? It can, by folding the k lists into an accumulated result one at a time:

1. Return `None` immediately when `lists` is empty.
2. Write `merge_two_lists(l1, l2)`: a `dummy` head and a `current` tail pointer;
   while both lists are non-empty, splice the smaller of `l1` and `l2` onto `current` and advance that list; when one empties, attach the survivor with `current.next = l1 or l2`.
3. Seed `result = lists[0]` and merge each remaining list into it:
   `result = merge_two_lists(result, lists[i])` for `i` from `1` to `k - 1`.

The simplicity has a cost: `result` grows toward length `N`, and every one of its nodes is re-walked during each later merge. Early nodes are compared over and over, which is the flaw the pairing scheme in the next approach removes.

#### Walkthrough

Let us fold the lists of Example 1 one at a time: `lists = [[1,4,5],[1,3,4],[2,6]]`. The first merge combines `result = 1->4->5` with `1->3->4`. Each line shows the two current heads, the comparison, and the merged prefix behind `current`:

```text
merge_two_lists(1->4->5, 1->3->4):
  l1=1  l2=1    1 <= 1   splice l1's 1    merged: 1                l1 = 4->5
  l1=4  l2=1    4 >  1   splice l2's 1    merged: 1->1             l2 = 3->4
  l1=4  l2=3    4 >  3   splice l2's 3    merged: 1->1->3          l2 = 4
  l1=4  l2=4    4 <= 4   splice l1's 4    merged: 1->1->3->4       l1 = 5
  l1=5  l2=4    5 >  4   splice l2's 4    merged: 1->1->3->4->4    l2 = None
  l2 empty: current.next = l1   ->   result = 1->1->3->4->4->5
```

The tie at `4 <= 4` keeps the node from `l1`, the accumulated result, preserving stability. The second merge folds in the last list, `2->6`, re-walking the six-node accumulator that the first merge produced:

```text
merge_two_lists(1->1->3->4->4->5, 2->6):
  1 <= 2  splice 1     1 <= 2  splice 1     3 > 2  splice 2
  3 <= 6  splice 3     4 <= 6  splice 4     4 <= 6  splice 4
  5 <= 6  splice 5     l1 empty: attach 6
  result = 1->1->2->3->4->4->5->6
```

That re-walk is the approach's weakness in miniature: nodes `1, 1, 3` were already compared in the first merge and are compared again here. The final `result` is `1->1->2->3->4->4->5->6`, matching the expected Output `[1,1,2,3,4,4,5,6]`.

#### Solution

The code is the walkthrough generalized: `merge_two_lists` does each splice, and the loop folds every list into `result`.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Sequential merge: merge lists one by one
        """
        if not lists:
            return None

        def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
            """Merge two sorted linked lists"""
            dummy = ListNode(0)
            current = dummy

            while l1 and l2:
                if l1.val <= l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next

            current.next = l1 or l2
            return dummy.next

        # Sequentially merge all lists
        result = lists[0]
        for i in range(1, len(lists)):
            result = merge_two_lists(result, lists[i])

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × k)`

The first merge processes the first list, the second merge processes the first two lists, etc. This leads to quadratic behavior in the number of lists.

##### Space Complexity: `O(1)`

Uses constant extra space, only manipulating pointers.

#### Key Insights

- Reusing the standard two-list merge keeps the implementation small, but folding the lists in a left-to-right line means early nodes are revisited on every subsequent merge.
- The accumulating result grows toward length `N`, so the i-th merge costs proportional to the running total, producing the `O(N × k)` behavior.
- Pairing the lists instead of accumulating them linearly is what turns this into the optimal divide and conquer approach below.

### Divide and Conquer

#### Derivation

Sequential Merge is slow because its merges are lopsided: the accumulator keeps growing while each incoming list stays short, so early nodes are re-walked on every later merge. The repair is to keep every merge between lists of similar length. Merge the lists in pairs, [divide and conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) style: one round turns k lists into `⌈k/2⌉` longer ones, the next round halves that again, and after `log k` rounds a single list remains. Each node is touched once per round, never once per list:

1. Return `None` immediately when `lists` is empty.
2. While more than one list remains, walk `lists` two at a time: merge
   `lists[i]` with `lists[i + 1]` using the same two-pointer `merge_two_lists` helper as the Sequential Merge, guarding the odd tail with `lists[i + 1] if i + 1 < len(lists) else None`.
3. Collect the round's outputs in `merged_lists` and replace `lists` with it.
4. When one list remains, return it.

#### Cost Recurrence

Merging two sorted lists is linear in their combined length. Pairing the `k` lists halves their count each round, and the two halves split the nodes between them, so both parameters shrink together. Writing \(k\) for the lists still to merge and \(N\) for the total nodes across them:

$$ T(k, N) = 2\,T\!\left(\frac{k}{2}, \frac{N}{2}\right) + O(N), \qquad T(1, n) = O(1) $$

```text
T(k, N) = 2 * T(k / 2, N / 2) + O(N)
T(1, n) = O(1)
          (k = lists still to merge, N = total nodes across them)
```

Both parameters have to appear. Holding the node count fixed at every level would give \(T(k) = 2\,T(k/2) + O(N)\), which solves to \(\Theta(Nk)\), the sequential cost rather than this one. What makes the divide-and-conquer version cheaper is that a whole round of merges costs \(O(N)\) in total, not \(O(N)\) per subproblem.

Every round touches all \(N\) nodes exactly once, and there are \(\log_2 k\) rounds, so the total is:

$$ T(k) = \sum_{r=1}^{\lceil \log_2 k \rceil} O(N) = O(N \log k) $$

```text
T(k) = sum over r = 1 to ceil(log2 k) of O(N) = O(N log k)
```

The contrast with Sequential Merge is worth reading off the sum. Folding one list in at a time re-walks the accumulated result on every step, so its cost is

$$ \sum_{i=1}^{k} O\!\left(\frac{iN}{k}\right) = O(Nk) $$

```text
sum over i = 1 to k of O(i * N / k) = O(N * k)
```

The growing prefix is what makes it quadratic in `k`. Pairwise merging keeps each node in exactly \(\log k\) merges instead of up to \(k\).

#### Walkthrough

Let us run the rounds on Example 1: `lists = [[1,4,5],[1,3,4],[2,6]]`, so `k = 3`. Each round pairs the lists off and calls `merge_two_lists` on each pair; the odd list out merges against `None`, which returns it unchanged:

```text
round 1   pair (1->4->5, 1->3->4)  ->  1->1->3->4->4->5
          pair (2->6, None)        ->  2->6              odd list, merged with None
          lists = [1->1->3->4->4->5, 2->6]
round 2   pair (1->1->3->4->4->5, 2->6)  ->  1->1->2->3->4->4->5->6
          lists = [1->1->2->3->4->4->5->6]
```

Each pairwise merge is the splice loop traced step by step in the Sequential Merge walkthrough; only the pairing schedule differs. After round 2 a single list remains, so the `while` loop exits and `lists[0]` is returned: `1->1->2->3->4->4->5->6`, matching the expected Output `[1,1,2,3,4,4,5,6]`.

#### Solution

The code is the walkthrough's rounds: an outer `while` that pairs off `lists`, with `merge_two_lists` doing each splice.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Divide and conquer approach: merge pairs recursively
        """
        if not lists:
            return None

        def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
            """Merge two sorted linked lists"""
            dummy = ListNode(0)
            current = dummy

            while l1 and l2:
                if l1.val <= l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next

            # Attach remaining nodes
            current.next = l1 or l2
            return dummy.next

        # Divide and conquer
        while len(lists) > 1:
            merged_lists = []

            # Merge pairs of lists
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged_lists.append(merge_two_lists(l1, l2))

            lists = merged_lists

        return lists[0] if lists else None
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Where N is the total number of nodes and k is the number of lists. Each node is processed log(k) times through the merging levels.

##### Space Complexity: `O(k)`

Each merging round allocates a `merged_lists` array holding up to `⌈k/2⌉` list heads, so the auxiliary space is linear in the number of lists. Both the outer loop and the `merge_two_lists` helper are iterative, so there is no recursion stack.

#### Key Insights

- Merging in pairs halves the number of lists each round, so after `log k` rounds a single list remains, and every node participates in exactly `log k` merges.
- Guarding the second list with `lists[i + 1] if i + 1 < len(lists) else None` cleanly handles an odd count by merging the leftover list against `None`.
- This matches the heap approach at `O(N log k)` time with the same `O(k)` extra space (the per-round array of merged heads), while staying entirely library-free, making it the strongest all-around choice.

### Min-Heap

#### Derivation

The Repeated Minimum Scan already emits nodes in the right order; its only cost is the `O(k)` scan per node to find the smallest current head. A [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) (priority queue) is the data structure built for exactly that job: it hands back the minimum of k candidates in `O(log k)` and accepts a replacement in `O(log k)`. Keep one candidate per list in the heap and the merge falls out:

1. Push `(head.val, i, head)` for each non-empty list. The list index `i` in
   the middle breaks ties between equal values, so the heap never has to compare `ListNode` objects, which are not orderable.
2. Pop the smallest tuple `(val, list_idx, node)` and splice `node` onto
   `current`.
3. When the popped node has a successor, push
   `(node.next.val, list_idx, node.next)` so its list stays represented by exactly one candidate.
4. When the heap empties, every node has been spliced; return `dummy.next`.

#### Walkthrough

Here the heap itself is the technique, so the trace follows its contents on Example 1: `lists = [[1,4,5],[1,3,4],[2,6]]`. Entries are shown as `(val, list_idx)`, listed in priority order; each step pops the minimum, splices its node, and pushes the popped node's successor when one exists:

```text
init: push (1,0), (1,1), (2,2)           heap = [(1,0), (1,1), (2,2)]
pop (1,0)  splice 1   push (4,0)         heap = [(1,1), (2,2), (4,0)]
pop (1,1)  splice 1   push (3,1)         heap = [(2,2), (3,1), (4,0)]
pop (2,2)  splice 2   push (6,2)         heap = [(3,1), (4,0), (6,2)]
pop (3,1)  splice 3   push (4,1)         heap = [(4,0), (4,1), (6,2)]
pop (4,0)  splice 4   push (5,0)         heap = [(4,1), (5,0), (6,2)]
pop (4,1)  splice 4   list 1 exhausted   heap = [(5,0), (6,2)]
pop (5,0)  splice 5   list 0 exhausted   heap = [(6,2)]
pop (6,2)  splice 6   list 2 exhausted   heap = []
```

The tie-break shows up twice: `(1,0)` pops before `(1,1)`, and `(4,0)` before `(4,1)`, because tuple comparison falls through to the list index when values are equal. The heap never holds more than `k = 3` entries even as all eight nodes flow through it. With the heap empty, the loop ends and `dummy.next` is `1->1->2->3->4->4->5->6`, matching the expected Output `[1,1,2,3,4,4,5,6]`.

#### Solution

The code is the walkthrough's pop-splice-push cycle, with `heapq` maintaining the priority order shown on the right.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
import heapq
from typing import List, Optional


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Min-heap approach to always select the smallest available node
        """
        if not lists:
            return None

        # Initialize heap with the first node from each non-empty list
        heap = []
        for i, head in enumerate(lists):
            if head:
                heapq.heappush(heap, (head.val, i, head))

        dummy = ListNode(0)
        current = dummy

        while heap:
            # Get the node with minimum value
            val, list_idx, node = heapq.heappop(heap)

            # Add to result
            current.next = node
            current = current.next

            # Add the next node from the same list to heap
            if node.next:
                heapq.heappush(heap, (node.next.val, list_idx, node.next))

        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Each of the N nodes is pushed and popped from the heap once, and heap operations take O(log k) time.

##### Space Complexity: `O(k)`

The heap contains at most k nodes (one from each list) at any time.

#### Key Insights

- The heap entry stores `(value, list_index, node)` so that the list index breaks ties and the heap never has to compare `ListNode` objects, which are not orderable.
- Only one candidate per list lives in the heap at a time, so the heap size stays bounded by `k` even as `N` nodes flow through it.
- This generalizes the brute force's "scan all heads" idea by replacing the linear minimum search with an `O(log k)` heap pop, which is the key to handling very large `k`. It leans on the `heapq` library; the divide and conquer approach above reaches the same `O(N log k)` bound entirely from scratch.

## Comparison of Solutions

### Time Complexity

- **Repeated Minimum Scan**: `O(N × k)` - an `O(k)` minimum scan per emitted node
- **Sequential Merge**: `O(N × k)` - quadratic in the number of lists
- **Divide and Conquer**: `O(N log k)` - optimal, from scratch
- **Min-Heap**: `O(N log k)` - optimal, via the `heapq` library

### Space Complexity

- **Repeated Minimum Scan**: `O(k)` - the per-list cursor array
- **Sequential Merge**: `O(1)` - constant space, only pointer manipulation
- **Divide and Conquer**: `O(k)` - each round allocates an array of up to `⌈k/2⌉` merged heads
- **Min-Heap**: `O(k)` - the heap stores one node per list

### Trade-offs

- **Repeated Minimum Scan**: Poor time efficiency, but the most self-derivable approach. Implements the greedy "smallest current head" lesson by hand with no `sort` or `heapq`, splicing input nodes so extra space is just the k cursors. The natural first idea and the from-scratch baseline.
- **Sequential Merge**: Poor time efficiency but excellent space efficiency. Implementation is simple and it does leverage the sorted property by reusing the standard two-list merge. Acceptable as an interview answer.
- **Divide and Conquer**: Optimal time efficiency with good space efficiency (`O(k)` for the per-round head arrays). Implementation complexity is medium and it leverages the sorted property entirely from scratch. This is the most preferred solution in interviews.
- **Min-Heap**: Optimal time efficiency with good space efficiency. Implementation complexity is medium and it leverages the sorted property, but leans on the `heapq` library to find the minimum. Well-regarded in interviews.

### When to Use Each

- **Repeated Minimum Scan**: As a teaching baseline, or when k is small enough that the `O(N × k)` scan is acceptable.
- **Sequential Merge**: When simplicity is paramount and k is small.
- **Divide and Conquer**: Best overall solution for interviews and production: optimal time, `O(k)` space, library-free.
- **Min-Heap**: When you want to demonstrate knowledge of heap data structures or when k is very large and a library is welcome.

### Optimization Notes

- The **Divide and Conquer** solution is the recommended approach: it achieves optimal `O(N log k)` time with `O(k)` auxiliary space by reducing k lists to `log(k)` levels of pairwise merges, all from scratch. The **Min-Heap** approach matches the same time complexity and is preferred when k is very large, at the cost of leaning on the `heapq` library.
- Both `O(N log k)` approaches replace the brute force's `O(k)` minimum scan: the heap with an `O(log k)` pop, divide and conquer by giving each node `log k` pairwise merges instead.
- The key implementation detail of the merge approaches is the two-list merge helper, which uses a dummy head node to simplify pointer manipulation and attaches the remaining list with `current.next = l1 or l2` once one list is exhausted.
- A common pitfall in the divide and conquer approach is mishandling the odd list out when pairing: guard the second list with `lists[i + 1] if i + 1 < len(lists) else None` so the final unpaired list merges against `None` cleanly.
- The difference between `O(N log k)` and `O(N × k)` becomes significant as k grows, so leveraging the already-sorted property of each input list is crucial for an optimal solution.
