"""Latest-Timestamp Key-Value Store — https://www.fastprep.io/problems/amazon-latest-timestamp-key-value-store

Write-up & approaches: ../../../docs/amazon/amazon-latest-timestamp-key-value-store.md

Source note: The source reports set(timestamp,key,value) and get(key) returning the greatest-timestamp value. This exercise uses a finite operation sequence with authored tie handling, missing-key out

  uv run python amazon/amazon-latest-timestamp-key-value-store/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-latest-timestamp-key-value-store/              # run the test sets
"""
from harness import NotSolved, pick_case, run_operations


class LatestTimestampStore:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def set(self, timestamp: int, key: str, value: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def get(self, key: str) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a LatestTimestampStore method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(LatestTimestampStore, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement LatestTimestampStore's methods first")
