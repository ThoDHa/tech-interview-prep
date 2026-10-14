"""LRU Cache: https://leetcode.com/problems/lru-cache/

Write-up & approaches: ../../../docs/leetcode/lru_cache.md

Design a data structure that follows the constraints of a Least Recently Used
(LRU) cache, with O(1) average time for both get and put.

  uv run python lru_cache/solution.py     # debug one case (see CASE below)
  uv run pytest lru_cache/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class Node:
    def __init__(self, key = 0, value = 0) -> None:
        self.key = key
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        # Initialize empty state here; methods below raise until implemented.
        self.capacity = capacity
        self.cache: dict[int, Node] = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head


    def _remove(self, node: Node) -> None:
        prev, next = node.prev, node.next
        prev.next = next
        next.prev = prev

    def _add_to_back(self, node: Node) -> None:
        tail_prev = self.tail.prev
        tail_prev.next = node
        node.prev = tail_prev
        node.next = self.tail
        self.tail.prev = node



    def get(self, key: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_back(node)

        return node.value

    def put(self, key: int, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add_to_back(node)
        else:
            node = Node(key,value)
            self.cache[key] = node
            self._add_to_back(node)

            if len(self.cache) > self.capacity:
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]

if __name__ == "__main__":
    # Debug playground: set a breakpoint in a LRUCache method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(LRUCache, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement LRUCache's methods first")
