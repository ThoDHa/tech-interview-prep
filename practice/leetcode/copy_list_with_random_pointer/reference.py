"""Copy List With Random Pointer — https://leetcode.com/problems/copy-list-with-random-pointer/

Write-up & approaches: ../../docs/problems/copy_list_with_random_pointer.md

Canonical reference implementation: the write-up's Interleaving solution
(deep copy in O(1) auxiliary space). Your own attempt lives in solution.py.

You are given the head of a linked list of length `n`. Unlike a singly linked list, each node contains an additional pointer `random`, which may point to any node in the list, or `null`. Create a deep copy of the list and return its head.

  uv run python copy_list_with_random_pointer/reference.py   # debug one case (see below)
  uv run pytest copy_list_with_random_pointer/               # run the test sets
"""

from typing import List, Optional


class Node:
    """Linked list node with a `random` pointer, matching the LeetCode definition."""

    def __init__(self, val: int, next: "Optional[Node]" = None, random: "Optional[Node]" = None) -> None:
        self.val = val
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        """Deep-copy the list, splicing copies into the original to wire `random`.

        Pass 1 interleaves each fresh node after its original, so a node's
        copy is reachable as `node.next`. Pass 2 writes each copy's `random`
        as `current.random.next`, reaching the target's copy without a map.
        Pass 3 unzips the interleaving, restoring the original list and
        returning the copy list's head.

        Args:
            head: First node of the list to copy, or None.

        Returns:
            The head of a deep copy: fresh nodes whose `next` and `random`
            pointers mirror the original's structure and never reference it.

        Time:  O(n): three linear passes.
        Space: O(1): beyond the copied nodes themselves, pointer variables only.
        """
        if head is None:
            return None

        current = head
        while current is not None:
            copy = Node(current.val, current.next)
            current.next = copy
            current = copy.next

        current = head
        while current is not None:
            if current.random is not None:
                current.next.random = current.random.next
            current = current.next.next

        copy_head = head.next
        original = head
        while original is not None:
            copy = original.next
            original.next = copy.next
            if copy.next is not None:
                copy.next = copy.next.next
            original = original.next
        return copy_head


def build_list(pairs: List[List[Optional[int]]]) -> Optional[Node]:
    """Build the list from the LeetCode `[[val, random_index], ...]` form."""
    nodes = [Node(val) for val, _ in pairs]
    for i, (_, random_index) in enumerate(pairs):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[random_index] if random_index is not None else None
    return nodes[0] if nodes else None


def to_pairs(head: Optional[Node]) -> List[List[Optional[int]]]:
    """Serialize a list back to the `[[val, random_index], ...]` form."""
    nodes = []
    current = head
    while current is not None:
        nodes.append(current)
        current = current.next
    positions = {node: i for i, node in enumerate(nodes)}
    return [
        [node.val, positions[node.random] if node.random is not None else None]
        for node in nodes
    ]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in copyRandomList above, then run this
    # file. cases.json is empty (multi-method starter), so a literal example
    # stands in.
    pairs = [[3, None], [7, 3], [4, 0], [5, 1]]
    head = build_list(pairs)
    copied = Solution().copyRandomList(head)
    print(f"args = {pairs}")
    print(f"expected: {pairs}")
    print(f"got:      {to_pairs(copied)}")
    print(f"original untouched: {to_pairs(head) == pairs}")
