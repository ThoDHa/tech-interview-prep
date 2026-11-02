"""LFU Cache — https://www.fastprep.io/problems/amazon-lfu-cache

Write-up & approaches: ../../../docs/amazon/amazon-lfu-cache.md

Reference implementation of the write-up's recommended Frequency Buckets
with Doubly Linked Lists solution, presented as the design class behind
the page's judged processLfuCache form. Your own attempt lives in
solution.py.

  uv run python amazon/amazon-lfu-cache/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-lfu-cache/              # run the test sets
"""

from typing import Dict, Optional


class Node:
    """One cached key: its value, its frequency, and its two neighbors
    inside the frequency bucket it currently sits in."""

    def __init__(self, key: int, value: int, frequency: int) -> None:
        self.key = key
        self.value = value
        self.frequency = frequency
        self.prev_node: Optional["Node"] = None
        self.next_node: Optional["Node"] = None


class Bucket:
    """A doubly linked list of nodes sharing one frequency, bracketed by
    sentinels: the least recently used node sits after the head, the most
    recently used before the tail."""

    def __init__(self) -> None:
        """Wire the two sentinels to each other.

        Time:  O(1): two nodes wired together.
        Space: O(1): the two sentinels.
        """
        self.head = Node(0, 0, 0)
        self.tail = Node(0, 0, 0)
        self.head.next_node = self.tail
        self.tail.prev_node = self.head

    def append(self, node: Node) -> None:
        """Insert the node just before the tail sentinel, making it the
        bucket's most recently used entry.

        Time:  O(1): four pointer writes.
        Space: O(1): no allocation beyond the caller's node.
        """
        last_node = self.tail.prev_node
        node.prev_node = last_node
        node.next_node = self.tail
        last_node.next_node = node
        self.tail.prev_node = node

    def unlink(self, node: Node) -> None:
        """Splice the node out of the bucket, leaving its neighbors
        connected to each other.

        Time:  O(1): two pointer writes.
        Space: O(1).
        """
        node.prev_node.next_node = node.next_node
        node.next_node.prev_node = node.prev_node

    def pop_lru(self) -> Node:
        """Remove and return the node just after the head sentinel, the
        bucket's least recently used entry.

        Time:  O(1): one splice.
        Space: O(1): the removed node is returned, not copied.
        """
        lru_node = self.head.next_node
        self.unlink(lru_node)
        return lru_node

    def is_empty(self) -> bool:
        """Report whether no real node sits between the sentinels.

        Time:  O(1): one pointer comparison.
        Space: O(1).
        """
        return self.head.next_node is self.tail


class LFUCache:
    """A least-frequently-used cache with O(1)-average get and put.

    Successful gets and updating puts raise the touched key's frequency
    and move it to the most-recently-used end of its new frequency
    bucket; a fresh key starts at frequency one. Inserting a new key
    into a full cache evicts the smallest-frequency key, least recently
    used within the tie.
    """

    def __init__(self, capacity: int) -> None:
        """Start empty, with both indexes empty and no frequency holding
        a key yet.

        Time:  O(1): three assignments.
        Space: O(1): the structures grow only as keys arrive.
        """
        self.capacity = capacity
        self.key_node: Dict[int, Node] = {}
        self.buckets: Dict[int, Bucket] = {}
        self.min_frequency = 0

    def get(self, key: int) -> int:
        """Return the cached value for the key, or -1 when absent, and
        promote the key to the next frequency bucket on a hit.

        Time:  O(1) average: one dict probe plus constant bucket work.
        Space: O(1): the key's node moves, nothing is allocated.
        """
        node = self.key_node.get(key)
        if node is None:
            return -1
        self._promote(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update the key, evicting the least-frequently-used
        key (least recently used within the tie) when a fresh insertion
        would exceed the capacity.

        Time:  O(1) average: one dict probe plus constant bucket work on
            both the update and the insert-evict path.
        Space: O(1) per call: at most one node allocated, and an eviction
            releases one.
        """
        node = self.key_node.get(key)
        if node is not None:
            node.value = value
            self._promote(node)
            return
        if len(self.key_node) == self.capacity:
            lru_node = self.buckets[self.min_frequency].pop_lru()
            del self.key_node[lru_node.key]
        node = Node(key, value, 1)
        self.key_node[key] = node
        self.buckets.setdefault(1, Bucket()).append(node)
        self.min_frequency = 1

    def _promote(self, node: Node) -> None:
        """Move the node to the most-recently-used end of the next
        frequency bucket, advancing min_frequency when its old bucket was
        the minimum and just emptied; the emptied bucket is released so
        both indexes stay proportional to the cached keys.

        Time:  O(1) average: one splice, one append, one dict write.
        Space: O(1): at most one bucket object allocated, and an emptied
            one released.
        """
        bucket = self.buckets[node.frequency]
        bucket.unlink(node)
        emptied_frequency = node.frequency
        if bucket.is_empty():
            if emptied_frequency == self.min_frequency:
                self.min_frequency += 1
            del self.buckets[emptied_frequency]
        node.frequency += 1
        self.buckets.setdefault(node.frequency, Bucket()).append(node)


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))
    cache.put(3, 3)
    print(cache.get(2))
    print(cache.get(3))
    cache.put(4, 4)
    print(cache.get(1))
    print(cache.get(3))
    print(cache.get(4))
