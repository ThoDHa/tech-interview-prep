"""Min Stack: https://leetcode.com/problems/min-stack/

Write-up & approaches: ../../docs/problems/min_stack.md

Design a stack that supports push, pop, top, and retrieving the minimum element
in constant time.

  uv run python min_stack/solution.py     # debug one case (see CASE below)
  uv run pytest min_stack/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class MinStack:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def push(self, val: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def pop(self) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def top(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def getMin(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a MinStack method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(MinStack, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement MinStack's methods first")
