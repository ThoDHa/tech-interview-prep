"""Linked-List Queue with Delete and Deduplication — https://www.fastprep.io/problems/amazon-linked-list-queue-operations

Write-up & approaches: ../../../docs/amazon/amazon-linked-list-queue-operations.md

Source note: The source omits whether deletion removes one or all matches, which duplicate occurrence survives, and the callable batch format. The judged core task matches the visible report at about 

  uv run python amazon/amazon-linked-list-queue-operations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-linked-list-queue-operations/              # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class LinkedQueue:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def enqueue(self, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def dequeue(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def delete(self, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def removeAllDuplicates(self) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a LinkedQueue method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1_dedup_delete"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(LinkedQueue, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement LinkedQueue's methods first")
