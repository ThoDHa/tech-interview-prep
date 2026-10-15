"""Stack with Constant-Time Middle Queries — https://www.fastprep.io/problems/amazon-middle-stack-operations

Write-up & approaches: ../../../docs/amazon/amazon-middle-stack-operations.md
Reference implementation of the write-up's recommended Doubly Linked List
with Middle Pointer solution, kept next to the harness so authored cases
stay falsifiable. Your own attempt lives in solution.py.
"""

from typing import Optional


class Node:
    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.prev_node: Optional["Node"] = None
        self.next_node: Optional["Node"] = None


class MiddleStack:
    def __init__(self) -> None:
        """Bracket the empty list with sentinels; the middle pointer
        starts off the head sentinel and advances on the first push.

        Time:  O(1): two nodes wired together.
        Space: O(1): the two sentinels.
        """
        self.head = Node()
        self.tail = Node()
        self.head.next_node = self.tail
        self.tail.prev_node = self.head
        self.middle_node: Node = self.head
        self.count = 0

    def push(self, value: int) -> None:
        """Insert a node just before the tail sentinel and advance the
        middle pointer exactly when the new count is odd (the new node
        is the odd-size center).

        Time:  O(1) worst case: four pointer writes plus at most one
            middle hop.
        Space: O(1) per call: one node retained while it is stacked.
        """
        node = Node(value)
        last_node = self.tail.prev_node
        node.prev_node = last_node
        node.next_node = self.tail
        last_node.next_node = node
        self.tail.prev_node = node
        self.count += 1
        if self.count % 2 == 1:
            self.middle_node = self.middle_node.next_node

    def pop(self) -> Optional[int]:
        """Unlink the top node and retreat the middle pointer exactly
        when the new count is even; report None for an empty stack.

        Time:  O(1) worst case: two pointer writes plus at most one
            middle hop.
        Space: O(1): the removed node is released.
        """
        if self.count == 0:
            return None
        node = self.tail.prev_node
        last_node = node.prev_node
        last_node.next_node = self.tail
        self.tail.prev_node = last_node
        self.count -= 1
        if self.count % 2 == 0:
            self.middle_node = self.middle_node.prev_node
        return node.value

    def top(self) -> Optional[int]:
        """Return the top value, or None for an empty stack.

        Time:  O(1): one dereference through the tail sentinel.
        Space: O(1).
        """
        if self.count == 0:
            return None
        return self.tail.prev_node.value

    def middle(self) -> Optional[int]:
        """Return the lower-middle value (the one closer to the bottom),
        or None for an empty stack.

        Time:  O(1): one dereference.
        Space: O(1).
        """
        if self.count == 0:
            return None
        return self.middle_node.value


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    stack = MiddleStack()
    for value in (1, 2, 3):
        stack.push(value)
    print(stack.middle_value())
    print(stack.top())
    print(stack.pop())
    print(stack.middle_value())
