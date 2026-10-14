"""Implement Queue using Stacks: https://leetcode.com/problems/implement-queue-using-stacks/

Write-up & approaches: ../../docs/problems/implement_queue_using_stacks.md

Implement a first in first out (FIFO) queue using only two stacks. The queue
must support `push`, `pop`, `peek`, and `empty` using only standard stack
operations (push to top, peek/pop from top, size, is empty).

  uv run python implement_queue_using_stacks/solution.py     # debug one case (see CASE below)
  uv run pytest implement_queue_using_stacks/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class MyQueue:
    def __init__(self) -> None:
        # Init empty state here. Use only standard stack operations on lists
        # (append to push, pop()/[-1] for the top) when you implement below.
        self.data: list = []

    def push(self, x: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def pop(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def peek(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def empty(self) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a MyQueue method above, then run this
    # file. Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    try:
        got = run_operations(MyQueue, case["operations"], case["arguments"])
    except NotSolved:
        got = "implement MyQueue (push/pop/peek/empty) first"
    print(f"case {case['id']}:")
    print(f"operations: {case['operations']}")
    print(f"arguments:  {case['arguments']}")
    print(f"expected:   {case['expected']}")
    print(f"got:        {got}")
