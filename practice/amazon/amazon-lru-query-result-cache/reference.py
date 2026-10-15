"""LRU Cache for Query Results — https://www.fastprep.io/problems/amazon-lru-query-result-cache

Write-up & approaches: ../../../docs/amazon/amazon-lru-query-result-cache.md
Reference implementation of the write-up's recommended Hash Map + Doubly
Linked List solution, kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.
"""

from typing import Dict, Optional


class Node:
    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: "Optional[Node]" = None
        self.next: "Optional[Node]" = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        """Wire the two sentinels together and start an empty node map.

        Time:  O(1): two sentinel nodes and one empty dict.
        Space: O(capacity): the cache never holds more entries than the
            capacity allows.
        """
        self.capacity = capacity
        self.nodes: Dict[int, Node] = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: Node) -> None:
        """Splice `node` out of the list; constant pointer work.

        Time:  O(1): two pointer reassignments.
        Space: O(1).
        """
        previous_node, next_node = node.prev, node.next
        previous_node.next = next_node
        next_node.prev = previous_node

    def _append_to_back(self, node: Node) -> None:
        """Splice `node` in just before the tail sentinel, marking it
        most recently used.

        Time:  O(1): four pointer reassignments.
        Space: O(1).
        """
        last_node = self.tail.prev
        last_node.next = node
        node.prev = last_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        """Return the stored value for `key`, or -1 when absent; a hit
        moves the node to the most recently used end. Membership, not a
        sentinel comparison, decides hits because stored values may be
        -1.

        Time:  O(1) expected: one dict lookup plus two constant splices.
        Space: O(1).
        """
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self._unlink(node)
        self._append_to_back(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update `key`, renewing its recency either way (an
        update never changes the cache size), and evict exactly the
        least recently used entry when an insertion exceeds the
        capacity.

        Time:  O(1) expected: a dict membership test, node creation or
            update, and at most one eviction, all constant work.
        Space: O(1) amortized per call: the cache stays within capacity.
        """
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self._unlink(node)
            self._append_to_back(node)
            return
        node = Node(key, value)
        self.nodes[key] = node
        self._append_to_back(node)
        if len(self.nodes) > self.capacity:
            least_recent = self.head.next
            self._unlink(least_recent)
            del self.nodes[least_recent.key]


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    print(cache.get(1))
    cache.put(3, 30)
    print(cache.get(2))
    print(cache.get(3))
