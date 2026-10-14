"""LRU Cache: https://leetcode.com/problems/lru-cache/

Write-up & approaches: ../../docs/problems/lru_cache.md

Design a data structure that follows the constraints of a Least Recently Used
(LRU) cache, with O(1) average time for both get and put.

  uv run python lru_cache/solution.py     # debug one case (see CASE below)
  uv run pytest lru_cache/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class LRUCache:
    def __init__(self, capacity: int) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def get(self, key: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def put(self, key: int, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


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
