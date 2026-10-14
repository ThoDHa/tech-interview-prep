"""Time Based Key-Value Store: https://leetcode.com/problems/time-based-key-value-store/

Write-up & approaches: ../../docs/problems/time_based_key_value_store.md

Design a TimeMap that stores multiple values for the same key at different
timestamps; `get(key, t)` returns the value with the largest timestamp `<= t`
(or `""` if none). Timestamps passed to `set` are strictly increasing.

  uv run python time_based_key_value_store/solution.py     # debug one case (see CASE below)
  uv run pytest time_based_key_value_store/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class TimeMap:
    def __init__(self) -> None:
        # Init empty state here (e.g. key -> history of timestamped values).
        self.store: dict = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def get(self, key: str, timestamp: int) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a TimeMap method above, then run this
    # file. Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    try:
        got = run_operations(TimeMap, case["operations"], case["arguments"])
    except NotSolved:
        got = "implement TimeMap (set/get) first"
    print(f"case {case['id']}:")
    print(f"operations: {case['operations']}")
    print(f"arguments:  {case['arguments']}")
    print(f"expected:   {case['expected']}")
    print(f"got:        {got}")
