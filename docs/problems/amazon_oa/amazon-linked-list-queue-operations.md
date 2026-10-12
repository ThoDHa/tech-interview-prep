# [Linked-List Queue with Delete and Deduplication](https://www.fastprep.io/problems/amazon-linked-list-queue-operations)

**Medium** | **NN minutes** | **Linked List, Design, Simulation**

Source note: The source omits whether deletion removes one or all matches, which duplicate occurrence survives, and the callable batch format. The judged core task matches the visible report at about 90%.

Implement a queue whose state is stored in a hand-built singly linked list. The queue starts empty. Process operations from left to right, using the integer at the same index in values when an operation needs an argument.

The supported operations are:

enqueue: append a new node containing values[i] at the tail in O(1) time.dequeue: remove the head in O(1) time and append its value to the result.delete: remove the first node, from the head, whose value equals values[i]. If no node matches, leave the queue unchanged.removeAllDuplicates: retain the first occurrence of every value and remove all later occurrences, preserving the relative order of the retained nodes.Return the values produced by dequeue operations in encounter order. The value paired with dequeue or removeAllDuplicates is ignored.

Use explicit node, head, and tail references for the queue state. Do not use a library queue, deque, or linked-list container to represent it. An auxiliary membership set may be used only while processing removeAllDuplicates.

## Examples

### Example 1

**Input:** `operations = ["enqueue","enqueue","enqueue","enqueue","enqueue","removeAllDuplicates","dequeue","delete","dequeue"]`, `values = [3,1,3,2,1,0,0,1,0]`

**Output:** `[3,2]`

**Explanation:** Deduplication changes [3,1,3,2,1] to [3,1,2]. The first dequeue returns 3, deletion removes the first 1, and the final dequeue returns 2.

### Example 2

**Input:** `operations = ["enqueue","enqueue","enqueue","delete","enqueue","dequeue","dequeue","dequeue"]`, `values = [4,5,6,6,7,0,0,0]`

**Output:** `[4,5,7]`

**Explanation:** Deleting the tail value 6 must repair the tail pointer, so the later enqueue appends 7 after 5.

### Example 3

**Input:** `operations = ["enqueue","enqueue","enqueue","delete","dequeue","dequeue"]`, `values = [8,9,8,8,0,0]`

**Output:** `[9,8]`

**Explanation:** delete 8 removes only the first matching node. The later 8 remains behind 9.

## Constraints

- `1 <= operations.length <= 2000`
- `values.length == operations.length`
- `Every operation is enqueue, dequeue, delete, or removeAllDuplicates.`
- `-10^9 <= values[i] <= 10^9`
- `Every dequeue occurs when the queue is nonempty.`
- `The queue state must use hand-built singly linked nodes with explicit head and tail references.`

## Solutions

### Simulate with Node References

#### Derivation

The problem asks for a queue whose state is a hand-built singly linked list, so the most direct reading is also the required one: define a `QueueNode` carrying `value` and `next`, keep `head` and `tail` references, and translate each operation into pointer surgery. The statement pins the costs that shape the design. `enqueue` must append at the tail in `O(1)`, which is exactly why a bare `head`-only list will not do: without a `tail` reference, every append would walk the list. `dequeue` removes the head in `O(1)`, and `delete` removes the first node whose value matches, which needs the node *before* the match so its `next` can be redirected; a sentinel-free `delete` of the head is the classic special case. The statement also fixes the semantics: `delete` stops at the first match (Example 3), and `removeAllDuplicates` keeps the first occurrence of every value, which is one ordered scan with a membership set. The steps:

1. Represent state as `head` and `tail` references (both `None` when empty).
2. `enqueue(value)`: wrap `value` in a `QueueNode`, append via `tail`, creating
   the head when the queue was empty.
3. `dequeue()`: read `head.value`, advance `head` (clearing `tail` when the
   last node leaves), and return the value.
4. `delete(value)`: track `previous_node` while scanning from `head`; on the
   first match, redirect the predecessor's `next` (or advance `head` when the
   match is the head), repair `tail` when the match is the last node, and stop.
5. `remove_all_duplicates()`: one scan keeping nodes whose value is new to the
   `seen` set, rewiring `next` past repeats and repairing `tail` at the end.
6. Collect the values returned by `dequeue` operations.

#### Walkthrough

Example 1: five enqueues, then `removeAllDuplicates`, `dequeue`, `delete(1)`, `dequeue`. Each line shows the queue from head to tail:

```text
enqueue 3        [3]
enqueue 1        [3, 1]
enqueue 3        [3, 1, 3]
enqueue 2        [3, 1, 3, 2]
enqueue 1        [3, 1, 3, 2, 1]
removeAllDups    [3, 1, 2]        keep first 3, first 1, first 2
dequeue          -> 3, queue [1, 2]
delete 1         [2]              first match from the head is the 1
dequeue          -> 2, queue []
```

The deduplication keeps one node per distinct value in first-seen order, and the `delete` removes only the first matching `1`. The dequeues return `3` and `2`, matching the expected Output.

Example 2 is the pointer-repair case: `[4, 5, 6]` then `delete 6`. The match is the tail, so `tail` must move back to node `5`; skipping that repair leaves `tail` pointing at the detached node, and the following `enqueue 7` would append to a phantom list. With the repair, the queue reads `[4, 5]`, `enqueue 7` gives `[4, 5, 7]`, and the three dequeues return `4, 5, 7`, matching the expected Output. Example 3 shows `delete` stopping at the first match: `delete 8` on `[8, 9, 8]` removes only the head, leaving `[9, 8]`, so the dequeues return `9, 8`, matching its expected Output.

#### Solution

The code is the walkthrough's pointer rules written down, one method per operation.

```python
from typing import List, Optional


class QueueNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Optional["QueueNode"] = None


class LinkedQueue:
    def __init__(self) -> None:
        self.head: Optional[QueueNode] = None
        self.tail: Optional[QueueNode] = None

    def enqueue(self, value: int) -> None:
        node = QueueNode(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def dequeue(self) -> int:
        if self.head is None:
            raise ValueError("dequeue called on an empty queue")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        return node.value

    def delete(self, value: int) -> None:
        previous_node: Optional[QueueNode] = None
        node = self.head
        while node is not None:
            if node.value == value:
                if previous_node is None:
                    self.head = node.next
                else:
                    previous_node.next = node.next
                if self.tail is node:
                    self.tail = previous_node
                return
            previous_node = node
            node = node.next

    def remove_all_duplicates(self) -> None:
        seen = set()
        previous_node: Optional[QueueNode] = None
        node = self.head
        while node is not None:
            if node.value in seen:
                previous_node.next = node.next
                if self.tail is node:
                    self.tail = previous_node
            else:
                seen.add(node.value)
                previous_node = node
            node = node.next


class Solution:
    def processLinkedQueue(self, operations: List[str],
                           values: List[int]) -> List[int]:
        queue = LinkedQueue()
        dequeued_values: List[int] = []
        for operation, value in zip(operations, values):
            if operation == "enqueue":
                queue.enqueue(value)
            elif operation == "dequeue":
                dequeued_values.append(queue.dequeue())
            elif operation == "delete":
                queue.delete(value)
            elif operation == "removeAllDuplicates":
                queue.remove_all_duplicates()
        return dequeued_values
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` total

`enqueue` and `dequeue` are `O(1)` each; `delete` walks at most the list length once, and `remove_all_duplicates` scans the list exactly once, so a batch of `n` operations costs `O(n)` in total.

##### Space Complexity: `O(n)`

One node per live element plus the `seen` set, which the statement permits only during `removeAllDuplicates` and which holds at most one entry per live element.

#### Key Insights

- The `tail` reference is what makes `enqueue` constant time; every tail-adjacent mutation (`delete` the last node, dedup dropping the last node) must repair it.
- `delete` needs the predecessor, not the match, because singly linked redirection happens in the node before the removed one; the head match is the no-predecessor special case.
- Deduplication is a single pass: the `seen` set classifies each node keep-or-skip in constant time, and the rewiring keeps first occurrences in order, as Example 1 shows.
- `dequeue` clearing `tail` on the last node keeps the empty-queue state consistent for the next `enqueue`.

## Comparison of Solutions

There is a single solution for this problem.

### Time Complexity

- **Simulate with Node References**: `O(n)` total - constant-time head and tail operations dominate, and each `delete` or dedup pass walks the list at most once.

### Space Complexity

- **Simulate with Node References**: `O(n)` - one node per live element, plus the dedup set that exists only while `removeAllDuplicates` runs.

### Trade-offs

- **Simulate with Node References**: faithful to the statement's requirement to build the list by hand, with every cost where the statement puts it; the price is pointer bookkeeping, chiefly the `tail` repair and the head-vs-middle cases in `delete`.

### When to Use Each

- **Simulate with Node References (Recommended)**: always, here: the statement mandates explicit nodes with `head` and `tail` references, so this is the one admissible design.

### Optimization Notes

- Wiring `delete` to stop at the first match matters twice: it matches the statement's semantics (Example 3) and it bounds the scan by the first occurrence.
- The `remove_all_duplicates` loop maintains `previous_node` as the last kept node, so each duplicate is spliced out with one assignment and `tail` is repaired inside the loop rather than in a second pass.
- A dictionary keyed by value counting live occurrences would let `delete` skip early, but adds bookkeeping the operation budget (`n <= 2000`) never amortizes.
