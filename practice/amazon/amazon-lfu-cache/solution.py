"""LFU Cache — https://www.fastprep.io/problems/amazon-lfu-cache

Write-up & approaches: ../../../docs/amazon/amazon-lfu-cache.md

Process commands on an initially empty least-frequently-used cache with positive integer capacity.

  uv run python amazon/amazon-lfu-cache/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-lfu-cache/              # run the test sets
"""
from harness import NotSolved, pick_case, run_operations


class LFUCache:
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
    # Debug playground: set a breakpoint in an LFUCache method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(LFUCache, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement LFUCache's methods first")
