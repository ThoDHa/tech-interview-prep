"""Linked-List Queue with Delete and Deduplication — https://www.fastprep.io/problems/amazon-linked-list-queue-operations

Write-up & approaches: ../../../docs/amazon/amazon-linked-list-queue-operations.md
Reference implementation of the write-up's Simulate with Node References
solution (the one admissible design per the statement), kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.
"""

from typing import List, Optional


class QueueNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Optional["QueueNode"] = None


class LinkedQueue:
    def __init__(self) -> None:
        """Start an empty queue with head and tail both unset.

        Time:  O(1): two references and no nodes.
        Space: O(1): nothing stored yet.
        """
        self.head: Optional[QueueNode] = None
        self.tail: Optional[QueueNode] = None

    def enqueue(self, value: int) -> None:
        """Append a node carrying `value` at the tail.

        Time:  O(1): the tail reference makes the append constant time.
        Space: O(1) per call: one node retained while it is queued.
        """
        node = QueueNode(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def dequeue(self) -> int:
        """Remove the head and return its value; clearing `tail` on the
        last node keeps the empty state consistent for the next enqueue.

        Time:  O(1): one reference advance plus the tail repair.
        Space: O(1): the removed node is released.
        """
        if self.head is None:
            raise ValueError("dequeue called on an empty queue")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        return node.value

    def delete(self, value: int) -> None:
        """Remove the first node, from the head, whose value equals
        `value`; a missing match leaves the queue unchanged, and removing
        the tail repairs the tail reference.

        Time:  O(n) for n queued nodes: the scan stops at the first
            match.
        Space: O(1): the predecessor reference is the only extra state.
        """
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

    def removeAllDuplicates(self) -> None:
        """Keep the first occurrence of every value, splice out later
        occurrences in one pass, and repair the tail when the last node
        is dropped. The camelCase name mirrors the statement's operation
        token, which the harness dispatches by attribute.

        Time:  O(n) for n queued nodes: one scan with constant-time set
            membership per node.
        Space: O(n) for the membership set, which the statement permits
            only during this operation.
        """
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


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    queue = LinkedQueue()
    for value in (3, 1, 3, 2, 1):
        queue.enqueue(value)
    queue.remove_all_duplicates()
    print(queue.dequeue())
    queue.delete(1)
    print(queue.dequeue())
